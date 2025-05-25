from neo4j_connection import Neo4jConnection
from datetime import datetime

class InteractionController:

    @staticmethod
    def add_interaction(user_id, movie_id, interaction_type):
        if interaction_type not in ['like', 'dislike']:
            raise ValueError("El tipo de interacción debe ser 'like' o 'dislike'.")

        weight = 1.0 if interaction_type == 'like' else -1.0

        # Verificar existencia de nodos
        check_query = """
        MATCH (u:User {id: $user_id})
        OPTIONAL MATCH (m:Movie {id: $movie_id})
        RETURN u IS NOT NULL AS user_exists, m IS NOT NULL AS movie_exists
        """
        with Neo4jConnection() as conn:
            check = conn.query(check_query, {
                "user_id": user_id,
                "movie_id": movie_id
            })[0]

            print("DEBUG >> Existencia de nodos:")
            print("  Usuario:", check['user_exists'])
            print("  Película:", check['movie_exists'])

            if not check['user_exists']:
                raise ValueError("El usuario no existe")
            if not check['movie_exists']:
                raise ValueError("La película no existe")

        # Registrar interacción y actualizar preferencias
        interaction_query = """
        MATCH (u:User {id: $user_id}), (m:Movie {id: $movie_id})
        MERGE (u)-[r:INTERACTED]->(m)
        SET r.type = $interaction_type,
            r.weight = $weight,
            r.timestamp = datetime()

        WITH u, m, $weight AS weight

        // Actualizar y obtener pesos de Géneros
        OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)
        MERGE (u)-[ug:USER_GENRE_PREFERENCE]->(g)
        SET ug.peso = coalesce(ug.peso, 0) + (weight * 0.10)
        WITH u, m, weight, COLLECT({name: g.name, peso: ug.peso}) AS genres

        // Actualizar y obtener pesos de Directores
        OPTIONAL MATCH (m)-[:DIRECTED_BY]->(d:Director)
        MERGE (u)-[ud:USER_DIRECTOR_PREFERENCE]->(d)
        SET ud.peso = coalesce(ud.peso, 0) + (weight * 0.10)
        WITH u, m, weight, genres, COLLECT({name: d.name, peso: ud.peso}) AS directors

        // Actualizar y obtener pesos de Actores
        OPTIONAL MATCH (m)-[:HAS_ACTOR]->(a:Actor)
        MERGE (u)-[ua:USER_ACTOR_PREFERENCE]->(a)
        SET ua.peso = coalesce(ua.peso, 0) + (weight * 0.07)
        WITH u, m, weight, genres, directors, COLLECT({name: a.name, peso: ua.peso}) AS actors

        // Actualizar y obtener pesos de Temporadas
        OPTIONAL MATCH (m)-[:APPROPIATE_FOR_SEASON]->(s:Season)
        MERGE (u)-[us:USER_SEASON_PREFERENCE]->(s)
        SET us.peso = coalesce(us.peso, 0) + (weight * 0.05)
        WITH m, genres, directors, actors, COLLECT({name: s.name, peso: us.peso}) AS seasons

        RETURN {
            movie: {id: m.id, title: m.title},
            updated: {
                genres: genres,
                directors: directors,
                actors: actors,
                seasons: seasons
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

            return result[0] if result else None
