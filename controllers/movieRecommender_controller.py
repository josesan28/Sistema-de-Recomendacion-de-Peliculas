from neo4j_connection import Neo4jConnection
import random

class MovieRecommenderController:
    @staticmethod
    def get_recommendations_for_user(user_id, limit=10):

        query = """
        MATCH (u:User {id: $user_id})
        
        // 1. PREFERENCIAS DE GÉNERO (50% peso)
        OPTIONAL MATCH (u)-[pg:USER_GENRE_PREFERENCE]->(g:Genre)
        WITH u, COLLECT({genre: g, weight: pg.peso}) AS genre_prefs
        
        // 2. PREFERENCIAS DE ACTORES (20% peso)
        OPTIONAL MATCH (u)-[pa:USER_ACTOR_PREFERENCE]->(a:Actor)
        WITH u, genre_prefs, COLLECT({actor: a, weight: pa.peso}) AS actor_prefs
        
        // 3. PREFERENCIAS DE DIRECTORES (30% peso)
        OPTIONAL MATCH (u)-[pd:USER_DIRECTOR_PREFERENCE]->(d:Director)
        WITH u, genre_prefs, actor_prefs, COLLECT({director: d, weight: pd.peso}) AS director_prefs
        
        // 4. PREFERENCIAS DE TEMPORADA (opcional)
        OPTIONAL MATCH (u)-[ps:USER_SEASON_PREFERENCE]->(s)
        WITH u, genre_prefs, actor_prefs, director_prefs, COLLECT({season: s, weight: ps.peso}) AS season_prefs
        
        CALL {
            WITH u, genre_prefs, actor_prefs, director_prefs, season_prefs
            
            MATCH (m:Movie)
            WHERE NOT EXISTS((u)-[:INTERACTED]->(m))
            
            // 1. Puntaje por géneros
            OPTIONAL MATCH (m)-[:HAS_GENRE]->(mg:Genre)
            WITH m, genre_prefs, actor_prefs, director_prefs, season_prefs,
                 REDUCE(s = 0, gp IN genre_prefs | 
                   CASE WHEN mg = gp.genre THEN s + gp.weight * 0.5 ELSE s END) AS genre_score
                 
            // 2. Puntaje por actores
            OPTIONAL MATCH (m)-[:HAS_ACTOR]->(ma:Actor)
            WITH m, genre_score, actor_prefs, director_prefs, season_prefs,
                 genre_score + REDUCE(s = 0, ap IN actor_prefs | 
                   CASE WHEN ma = ap.actor THEN s + ap.weight * 0.2 ELSE s END) AS actor_score
                 
            // 3. Puntaje por directores
            OPTIONAL MATCH (m)-[:DIRECTED_BY]->(md:Director)
            WITH m, genre_score, actor_score, director_prefs, season_prefs,
                 actor_score + REDUCE(s = 0, dp IN director_prefs | 
                   CASE WHEN md = dp.director THEN s + dp.weight * 0.3 ELSE s END) AS director_score
                 
            // 4. Puntaje por temporada (opcional)
            OPTIONAL MATCH (m)-[:APPROPIATE_FOR_SEASON]->(ms)
            WITH m, genre_score, actor_score, director_score, season_prefs,
                 director_score + REDUCE(s = 0, sp IN season_prefs | 
                   CASE WHEN ms = sp.season THEN s + sp.weight * 0.1 ELSE s END) AS final_score
                 
            // Obtener información completa de la película
            OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)
            OPTIONAL MATCH (m)-[:HAS_ACTOR]->(a:Actor)
            OPTIONAL MATCH (m)-[:DIRECTED_BY]->(d:Director)
            
            RETURN m, 
                   final_score AS score,
                   COLLECT(DISTINCT g.name)[0..3] AS genres,
                   COLLECT(DISTINCT a.name)[0..2] AS actors,
                   COLLECT(DISTINCT d.name)[0] AS director
            ORDER BY score DESC
            LIMIT $limit
        }
        
        RETURN {
            id: m.id,
            title: m.title,
            year: m.year,
            score: round(score * 100) / 100,
            genres: genres,
            actors: actors,
            director: director,
            recommendation_type: 'content_based'
        } AS movie
        ORDER BY score DESC
        LIMIT $limit
        """
        
        try:
            with Neo4jConnection() as conn:
                print(f"DEBUG >> Buscando recomendaciones para usuario: {user_id}")
                result = conn.query(query, {"user_id": user_id, "limit": limit})
                print(f"DEBUG >> Recomendaciones encontradas: {len(result)}")
                
                if len(result) < limit:
                    fallback = MovieRecommenderController._get_popular_movies(
                        user_id, limit - len(result))
                    result.extend(fallback)
                
                # Extraer solo la parte 'movie' de cada resultado para mantener compatibilidad
                movies = [item['movie'] for item in result if 'movie' in item]
                return movies
                
        except Exception as e:
            print(f"ERROR >> En get_recommendations_for_user: {str(e)}")
            return MovieRecommenderController._get_popular_movies(user_id, limit)

    @staticmethod
    def _get_popular_movies(user_id, limit):
        """Fallback: películas populares que no ha visto (versión original mejorada)"""
        query = """
        MATCH (u:User {id: $user_id})
        MATCH (m:Movie)
        WHERE NOT EXISTS((u)-[:INTERACTED]->(m))
        
        OPTIONAL MATCH (m)<-[int:INTERACTED]-() WHERE int.weight > 0
        WITH m, COUNT(int) AS popularity
        
        // Obtener información de la película
        OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)
        OPTIONAL MATCH (m)-[:HAS_ACTOR]->(a:Actor)
        OPTIONAL MATCH (m)-[:DIRECTED_BY]->(d:Director)
        
        WITH m, popularity,
             COLLECT(DISTINCT g.name)[0..3] AS genres,
             COLLECT(DISTINCT a.name)[0..2] AS actors,
             COLLECT(DISTINCT d.name)[0] AS director
        
        WITH m, genres, actors, director,
             CASE 
                WHEN popularity > 50 THEN 0.9
                WHEN popularity > 30 THEN 0.7
                WHEN popularity > 10 THEN 0.5
                ELSE 0.3
             END AS score
        
        RETURN {
            id: m.id,
            title: m.title,
            year: m.year,
            score: score,
            genres: genres,
            actors: actors,
            director: director,
            recommendation_type: 'popular'
        } AS movie
        
        ORDER BY score DESC, m.title
        LIMIT $limit
        """
        
        try:
            with Neo4jConnection() as conn:
                print(f"DEBUG >> Buscando películas populares para usuario: {user_id}")
                result = conn.query(query, {"user_id": user_id, "limit": limit})
                print(f"DEBUG >> Películas populares encontradas: {len(result)}")
                if result:
                    # Extraer solo la parte 'movie' de cada resultado
                    movies = [item['movie'] for item in result if 'movie' in item]
                    return movies
                return []
        except Exception as e:
            print(f"ERROR >> En _get_popular_movies: {str(e)}")
            return []

    @staticmethod
    def get_explanation_for_recommendation(user_id, movie_id):
        """Explicación de por qué se recomendó (versión original)"""
        query = """
        MATCH (u:User {id: $user_id}), (m:Movie {id: $movie_id})
        
        OPTIONAL MATCH (u)-[pg:USER_GENRE_PREFERENCE]->(g:Genre)<-[:HAS_GENRE]-(m)
        WITH u, m, COLLECT({genre: g.name, weight: pg.peso}) AS genre_matches
        
        OPTIONAL MATCH (u)-[pa:USER_ACTOR_PREFERENCE]->(a:Actor)<-[:HAS_ACTOR]-(m)
        WITH u, m, genre_matches, COLLECT({actor: a.name, weight: pa.peso}) AS actor_matches
        
        OPTIONAL MATCH (u)-[pd:USER_DIRECTOR_PREFERENCE]->(d:Director)<-[:DIRECTED_BY]-(m)
        WITH u, m, genre_matches, actor_matches, COLLECT({director: d.name, weight: pd.peso}) AS director_matches
        
        OPTIONAL MATCH (m)<-[int:INTERACTED]-() WHERE int.weight > 0
        WITH u, m, genre_matches, actor_matches, director_matches,
             COUNT(int) AS popularity_count
        
        RETURN {
            movie: {id: m.id, title: m.title},
            reasons: {
                matched_genres: [x IN genre_matches WHERE x.weight > 0.1 | {
                    genre: x.genre, 
                    user_preference: x.weight
                }],
                matched_actors: [x IN actor_matches WHERE x.weight > 0.1 | {
                    actor: x.actor, 
                    user_preference: x.weight
                }],
                matched_directors: [x IN director_matches WHERE x.weight > 0.1 | {
                    director: x.director, 
                    user_preference: x.weight
                }],
                is_popular: popularity_count > 5
            }
        } AS explanation
        """
        
        with Neo4jConnection() as conn:
            result = conn.query(query, {"user_id": user_id, "movie_id": movie_id})
            return result[0] if result else None