from neo4j_connection import Neo4jConnection
from datetime import datetime

class InteractionController:

    @staticmethod
    def add_interaction(user_id, movie_id, interaction_type):
        if interaction_type not in ['like', 'dislike']:
            raise ValueError("El tipo de interacción debe ser 'like' o 'dislike'.")

        weight = 1.0 if interaction_type == 'like' else -1.0

        # Verificar existencia de nodos básicos
        check_query = """
        MATCH (u:User {id: $user_id})
        OPTIONAL MATCH (m:Movie {id: $movie_id})
        RETURN u IS NOT NULL AS user_exists, m IS NOT NULL AS movie_exists
        """
        
        try:
            with Neo4jConnection() as conn:
                check = conn.query(check_query, {
                    "user_id": user_id,
                    "movie_id": movie_id
                })
                
                if not check:
                    raise ValueError("Error al verificar la existencia de nodos")
                
                check_result = check[0]
                print("DEBUG >> Existencia de nodos:")
                print("  Usuario:", check_result['user_exists'])
                print("  Película:", check_result['movie_exists'])

                if not check_result['user_exists']:
                    raise ValueError("El usuario no existe")
                if not check_result['movie_exists']:
                    raise ValueError("La película no existe")

            # Query simplificado que maneja conexiones faltantes
            interaction_query = """
            // Primero registrar la interacción básica
            MATCH (u:User {id: $user_id}), (m:Movie {id: $movie_id})
            MERGE (u)-[r:INTERACTED]->(m)
            SET r.type = $interaction_type,
                r.weight = $weight,
                r.timestamp = datetime()

            // Procesar géneros (si existen)
            WITH u, m, $weight AS weight
            CALL {
                WITH u, m, weight
                OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)
                WITH u, g, weight WHERE g IS NOT NULL
                MERGE (u)-[ug:USER_GENRE_PREFERENCE]->(g)
                SET ug.peso = coalesce(ug.peso, 0) + (weight * 0.10)
                RETURN COLLECT({name: g.name, peso: ug.peso}) AS genres
            }

            // Procesar directores (si existen)
            CALL {
                WITH u, m, weight
                OPTIONAL MATCH (m)-[:DIRECTED_BY]->(d:Director)
                WITH u, d, weight WHERE d IS NOT NULL
                MERGE (u)-[ud:USER_DIRECTOR_PREFERENCE]->(d)
                SET ud.peso = coalesce(ud.peso, 0) + (weight * 0.10)
                RETURN COLLECT({name: d.name, peso: ud.peso}) AS directors
            }

            // Procesar actores (si existen)
            CALL {
                WITH u, m, weight
                OPTIONAL MATCH (m)-[:HAS_ACTOR]->(a:Actor)
                WITH u, a, weight WHERE a IS NOT NULL
                MERGE (u)-[ua:USER_ACTOR_PREFERENCE]->(a)
                SET ua.peso = coalesce(ua.peso, 0) + (weight * 0.07)
                RETURN COLLECT({name: a.name, peso: ua.peso}) AS actors
            }

            // Procesar temporadas/contextos (si existen) - flexible para diferentes modelos
            CALL {
                WITH u, m, weight
                OPTIONAL MATCH (m)-[:APPROPIATE_FOR_SEASON]->(s)
                WHERE s:Season OR s:Contexto
                WITH u, s, weight WHERE s IS NOT NULL
                MERGE (u)-[us:USER_SEASON_PREFERENCE]->(s)
                SET us.peso = coalesce(us.peso, 0) + (weight * 0.05)
                RETURN COLLECT({
                    name: coalesce(s.name, s.nombre, "Unknown"), 
                    peso: us.peso
                }) AS seasons
            }

            RETURN {
                movie: {id: m.id, title: m.title},
                interaction: {type: $interaction_type, weight: $weight},
                updated: {
                    genres: coalesce(genres, []),
                    directors: coalesce(directors, []),
                    actors: coalesce(actors, []),
                    seasons: coalesce(seasons, [])
                }
            } AS result
            """

            with Neo4jConnection() as conn:
                result = conn.query(interaction_query, {
                    "user_id": user_id,
                    "movie_id": movie_id,
                    "interaction_type": interaction_type,
                    "weight": weight
                })

                print("DEBUG >> Resultado del query:", result)
                return result[0] if result else {"message": "Interacción registrada exitosamente"}
                
        except Exception as e:
            print(f"ERROR >> En add_interaction: {str(e)}")
            raise e