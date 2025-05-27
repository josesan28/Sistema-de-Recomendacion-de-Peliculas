from neo4j_connection import Neo4jConnection
import random

class MovieRecommenderController:
    @staticmethod
    def get_recommendations_for_user(user_id, limit=10):
        """
        Algoritmo híbrido de recomendación que combina:
        1. Filtrado colaborativo (usuarios similares)
        2. Filtrado basado en contenido (preferencias personales)
        3. Popularidad contextual (temporadas/festividades)
        """
        
        # Query principal que combina múltiples estrategias
        query = """
        // 1. FILTRADO BASADO EN CONTENIDO - Preferencias del usuario
        CALL {
            WITH $user_id AS uid
            OPTIONAL MATCH (u:User {id: uid})-[pref_g:USER_GENRE_PREFERENCE]->(g:Genre)<-[:HAS_GENRE]-(m:Movie)
            WHERE NOT EXISTS((u)-[:INTERACTED]->(m)) AND NOT EXISTS((u)-[:RATED]->(m))
            WITH m, SUM(pref_g.peso * 0.4) AS content_score_genres
            
            OPTIONAL MATCH (m)-[:HAS_ACTOR]->(a:Actor)<-[pref_a:USER_ACTOR_PREFERENCE]-(u)
            WITH m, content_score_genres, SUM(pref_a.peso * 0.3) AS content_score_actors
            
            OPTIONAL MATCH (m)-[:DIRECTED_BY]->(d:Director)<-[pref_d:USER_DIRECTOR_PREFERENCE]-(u)
            WITH m, content_score_genres, content_score_actors, SUM(pref_d.peso * 0.3) AS content_score_directors
            
            RETURN m, 
                   (coalesce(content_score_genres, 0) + 
                    coalesce(content_score_actors, 0) + 
                    coalesce(content_score_directors, 0)) AS content_score
            ORDER BY content_score DESC
            LIMIT 15
        }
        
        // 2. FILTRADO COLABORATIVO - Usuarios con gustos similares
        CALL {
            WITH $user_id AS uid
            MATCH (u:User {id: uid})-[r1:INTERACTED]->(m1:Movie)
            WHERE r1.weight > 0  // Solo likes
            MATCH (other:User)-[r2:INTERACTED]->(m1)
            WHERE other.id <> uid AND r2.weight > 0
            WITH other, COUNT(m1) AS common_likes, u
            WHERE common_likes >= 2  // Al menos 2 películas en común
            
            MATCH (other)-[r3:INTERACTED]->(rec_movie:Movie)
            WHERE r3.weight > 0 
              AND NOT EXISTS((u)-[:INTERACTED]->(rec_movie))
              AND NOT EXISTS((u)-[:RATED]->(rec_movie))
            
            RETURN rec_movie AS m, 
                   SUM(r3.weight * common_likes * 0.1) AS collaborative_score
            ORDER BY collaborative_score DESC
            LIMIT 10
        }
        
        // 3. CONTEXTO TEMPORAL/ESTACIONAL
        CALL {
            WITH $user_id AS uid
            OPTIONAL MATCH (u:User {id: uid})-[pref_s:USER_SEASON_PREFERENCE]->(s)<-[:APPROPIATE_FOR_SEASON]-(m:Movie)
            WHERE NOT EXISTS((u)-[:INTERACTED]->(m)) AND NOT EXISTS((u)-[:RATED]->(m))
            RETURN m, SUM(pref_s.peso * 0.2) AS seasonal_score
            ORDER BY seasonal_score DESC
            LIMIT 8
        }
        
        // 4. PELÍCULAS POPULARES (fallback)
        CALL {
            WITH $user_id AS uid
            MATCH (u:User {id: uid})
            MATCH (pop_movie:Movie)
            WHERE NOT EXISTS((u)-[:INTERACTED]->(pop_movie)) 
              AND NOT EXISTS((u)-[:RATED]->(pop_movie))
            OPTIONAL MATCH (pop_movie)<-[int:INTERACTED]-()
            WHERE int.weight > 0
            RETURN pop_movie AS m, COUNT(int) * 0.05 AS popularity_score
            ORDER BY popularity_score DESC
            LIMIT 5
        }
        
        // COMBINAR TODAS LAS ESTRATEGIAS
        WITH m, 
             coalesce(content_score, 0) AS content,
             coalesce(collaborative_score, 0) AS collaborative,
             coalesce(seasonal_score, 0) AS seasonal,
             coalesce(popularity_score, 0) AS popularity
        
        WITH m, (content + collaborative + seasonal + popularity) AS final_score
        WHERE final_score > 0
        
        // Obtener información completa de la película
        OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)
        OPTIONAL MATCH (m)-[:HAS_ACTOR]->(a:Actor)
        OPTIONAL MATCH (m)-[:DIRECTED_BY]->(d:Director)
        
        RETURN {
            id: m.id,
            title: m.title,
            year: m.year,
            score: round(final_score * 100) / 100,
            genres: COLLECT(DISTINCT g.name)[0..3],
            actors: COLLECT(DISTINCT a.name)[0..2],
            director: COLLECT(DISTINCT d.name)[0]
        } AS recommendation
        
        ORDER BY final_score DESC
        LIMIT $limit
        """
        
        try:
            with Neo4jConnection() as conn:
                result = conn.query(query, {"user_id": user_id, "limit": limit})
                
                # Si no hay suficientes recomendaciones, agregar películas aleatorias
                if len(result) < limit // 2:
                    fallback_movies = MovieRecommenderController._get_fallback_movies(
                        user_id, limit - len(result)
                    )
                    result.extend(fallback_movies)
                
                return result
                
        except Exception as e:
            print(f"Error en recomendaciones: {str(e)}")
            # Fallback a recomendaciones básicas
            return MovieRecommenderController._get_fallback_movies(user_id, limit)

    @staticmethod
    def _get_fallback_movies(user_id, limit):
        """Recomendaciones básicas cuando falla el algoritmo principal"""
        query = """
        MATCH (u:User {id: $user_id})
        MATCH (m:Movie)
        WHERE NOT EXISTS((u)-[:INTERACTED]->(m)) 
          AND NOT EXISTS((u)-[:RATED]->(m))
        
        OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)
        OPTIONAL MATCH (m)-[:HAS_ACTOR]->(a:Actor)
        OPTIONAL MATCH (m)-[:DIRECTED_BY]->(d:Director)
        
        RETURN {
            id: m.id,
            title: m.title,
            year: m.year,
            score: 0.1,
            genres: COLLECT(DISTINCT g.name)[0..3],
            actors: COLLECT(DISTINCT a.name)[0..2],
            director: COLLECT(DISTINCT d.name)[0]
        } AS recommendation
        
        ORDER BY m.title
        LIMIT $limit
        """
        
        with Neo4jConnection() as conn:
            result = conn.query(query, {"user_id": user_id, "limit": limit})
            # Mezclar aleatoriamente para variedad
            random.shuffle(result)
            return result

    @staticmethod
    def get_explanation_for_recommendation(user_id, movie_id):
        """Explica por qué se recomendó una película específica"""
        query = """
        MATCH (u:User {id: $user_id}), (m:Movie {id: $movie_id})
        
        // Verificar preferencias de género
        OPTIONAL MATCH (u)-[pg:USER_GENRE_PREFERENCE]->(g:Genre)<-[:HAS_GENRE]-(m)
        WITH u, m, COLLECT({genre: g.name, weight: pg.peso}) AS genre_matches
        
        // Verificar preferencias de actores
        OPTIONAL MATCH (u)-[pa:USER_ACTOR_PREFERENCE]->(a:Actor)<-[:HAS_ACTOR]-(m)
        WITH u, m, genre_matches, COLLECT({actor: a.name, weight: pa.peso}) AS actor_matches
        
        // Verificar preferencias de directores
        OPTIONAL MATCH (u)-[pd:USER_DIRECTOR_PREFERENCE]->(d:Director)<-[:DIRECTED_BY]-(m)
        WITH u, m, genre_matches, actor_matches, COLLECT({director: d.name, weight: pd.peso}) AS director_matches
        
        // Verificar usuarios similares
        OPTIONAL MATCH (u)-[:INTERACTED]->(shared:Movie)<-[:INTERACTED]-(similar:User)-[:INTERACTED]->(m)
        WITH u, m, genre_matches, actor_matches, director_matches, 
             COLLECT(DISTINCT similar.name) AS similar_users
        
        RETURN {
            movie: {id: m.id, title: m.title},
            reasons: {
                preferred_genres: [x IN genre_matches WHERE x.weight > 0.1 | x.genre],
                preferred_actors: [x IN actor_matches WHERE x.weight > 0.1 | x.actor],
                preferred_directors: [x IN director_matches WHERE x.weight > 0.1 | x.director],
                similar_users_liked: similar_users[0..3]
            }
        } AS explanation
        """
        
        with Neo4jConnection() as conn:
            result = conn.query(query, {"user_id": user_id, "movie_id": movie_id})
            return result[0] if result else None