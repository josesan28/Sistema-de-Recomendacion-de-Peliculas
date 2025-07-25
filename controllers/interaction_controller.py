from neo4j_connection import Neo4jConnection
from datetime import datetime

class InteractionController:

    @staticmethod
    def add_interaction(user_id, movie_id, interaction_type):
        if interaction_type not in ['like', 'dislike']:
            raise ValueError("El tipo de interacción debe ser 'like' o 'dislike'.")

        weight = 1.0 if interaction_type == 'like' else -1.0

        user_check_query = """
        MATCH (u:User {id: $user_id})
        RETURN u.id AS user_id, u.name AS user_name, u.email AS user_email
        """
        
        try:
            with Neo4jConnection() as conn:
                user_check = conn.query(user_check_query, {"user_id": user_id})
                
                if not user_check:
                    raise ValueError(f"Usuario {user_id} no existe. Debe iniciar sesión correctamente.")
                
                user_info = user_check[0]
                print(f"DEBUG >> Usuario encontrado: {user_info['user_name']} ({user_info['user_email']})")
                
                movie_check_query = """
                MATCH (m:Movie {id: $movie_id})
                RETURN m.id AS movie_id, m.title AS movie_title
                """
                
                movie_check = conn.query(movie_check_query, {"movie_id": movie_id})
                
                if not movie_check:
                    raise ValueError(f"La película {movie_id} no existe en la base de datos")
                
                movie_info = movie_check[0]
                print(f"DEBUG >> Película encontrada: {movie_info['movie_title']}")

                interaction_query = """
                // Registrar la interacción básica
                MATCH (u:User {id: $user_id}), (m:Movie {id: $movie_id})
                MERGE (u)-[r:INTERACTED]->(m)
                SET r.type = $interaction_type,
                    r.weight = $weight,
                    r.timestamp = datetime()

                WITH u, m, $weight AS weight

                // Procesar géneros (si existen)
                OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)
                WITH u, m, weight, COLLECT(DISTINCT g) AS genres
                FOREACH (genre IN genres |
                    MERGE (u)-[ug:USER_GENRE_PREFERENCE]->(genre)
                    SET ug.peso = coalesce(ug.peso, 0) + (weight * 0.15)
                )

                WITH u, m, weight

                // Procesar directores (si existen)
                OPTIONAL MATCH (m)-[:DIRECTED_BY]->(d:Director)
                WITH u, m, weight, COLLECT(DISTINCT d) AS directors
                FOREACH (director IN directors |
                    MERGE (u)-[ud:USER_DIRECTOR_PREFERENCE]->(director)
                    SET ud.peso = coalesce(ud.peso, 0) + (weight * 0.12)
                )

                WITH u, m, weight

                // Procesar actores (si existen)
                OPTIONAL MATCH (m)-[:HAS_ACTOR]->(a:Actor)
                WITH u, m, weight, COLLECT(DISTINCT a) AS actors
                FOREACH (actor IN actors |
                    MERGE (u)-[ua:USER_ACTOR_PREFERENCE]->(actor)
                    SET ua.peso = coalesce(ua.peso, 0) + (weight * 0.08)
                )

                WITH u, m, weight

                // Procesar temporadas/contextos (si existen)
                OPTIONAL MATCH (m)-[:APPROPIATE_FOR_SEASON]->(s)
                WHERE s:Season OR s:Contexto
                WITH u, m, weight, COLLECT(DISTINCT s) AS seasons
                FOREACH (season IN seasons |
                    MERGE (u)-[us:USER_SEASON_PREFERENCE]->(season)
                    SET us.peso = coalesce(us.peso, 0) + (weight * 0.05)
                )

                // Retornar información básica
                RETURN {
                    user: {id: u.id, name: u.name, email: u.email},
                    movie: {id: m.id, title: m.title},
                    interaction: {type: $interaction_type, weight: $weight},
                    status: 'success'
                } AS result
                """

                result = conn.query(interaction_query, {
                    "user_id": user_id,
                    "movie_id": movie_id,
                    "interaction_type": interaction_type,
                    "weight": weight
                })

                print(f"DEBUG >> Interacción procesada exitosamente para usuario real: {user_info['user_name']}")
                
                return {
                    "message": f"Interacción '{interaction_type}' registrada exitosamente",
                    "data": result[0] if result else None,
                    "user": user_info,
                    "movie": movie_info,
                    "status": "success"
                }
                
        except Exception as e:
            print(f"ERROR >> En add_interaction: {str(e)}")
            raise e

    @staticmethod
    def get_user_interactions(user_id, limit=10):
        query = """
        MATCH (u:User {id: $user_id})-[r:INTERACTED]->(m:Movie)
        RETURN {
            movie: {id: m.id, title: m.title},
            interaction: {type: r.type, weight: r.weight, timestamp: toString(r.timestamp)}
        } AS interaction
        ORDER BY r.timestamp DESC
        LIMIT $limit
        """
        
        with Neo4jConnection() as conn:
            return conn.query(query, {"user_id": user_id, "limit": limit})

    @staticmethod
    def get_user_preferences(user_id):
        query = """
        MATCH (u:User {id: $user_id})
        
        // Preferencias de géneros
        OPTIONAL MATCH (u)-[pg:USER_GENRE_PREFERENCE]->(g:Genre)
        WITH u, COLLECT({name: g.name, peso: pg.peso}) AS genre_prefs
        
        // Preferencias de directores
        OPTIONAL MATCH (u)-[pd:USER_DIRECTOR_PREFERENCE]->(d:Director)
        WITH u, genre_prefs, COLLECT({name: d.name, peso: pd.peso}) AS director_prefs
        
        // Preferencias de actores
        OPTIONAL MATCH (u)-[pa:USER_ACTOR_PREFERENCE]->(a:Actor)
        WITH u, genre_prefs, director_prefs, COLLECT({name: a.name, peso: pa.peso}) AS actor_prefs
        
        RETURN {
            user: {id: u.id, name: u.name, email: u.email},
            preferences: {
                genres: [x IN genre_prefs WHERE x.peso > 0.05 | x],
                directors: [x IN director_prefs WHERE x.peso > 0.05 | x],
                actors: [x IN actor_prefs WHERE x.peso > 0.05 | x]
            }
        } AS user_preferences
        """
        
        with Neo4jConnection() as conn:
            result = conn.query(query, {"user_id": user_id})
            return result[0] if result else None