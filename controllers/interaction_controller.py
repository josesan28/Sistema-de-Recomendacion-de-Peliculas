from neo4j_connection import Neo4jConnection
from datetime import datetime

class InteractionController:

    @staticmethod
    def add_interaction(user_id, movie_id, interaction_type):
        if interaction_type == 'like':
            weight = 1.0
        else:
            weight = -1.0

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

        interaction_query = """
        MATCH (u:User {id: $user_id}), (m:Movie {id: $movie_id})
        MERGE (u)-[r:INTERACTED]->(m)
        SET r.type = $interaction_type,
            r.weight = $weight,
            r.timestamp = datetime()

       WITH m, $weight AS weight

        OPTIONAL MATCH (m)-[grel:HAS_GENRE]->(:Genre)
        SET grel.peso = coalesce(grel.peso, 0) + (weight * 0.10)
        WITH m, weight, COUNT(grel) AS genre_updated

        OPTIONAL MATCH (m)-[drel:DIRECTED_BY]->(:Director)
        SET drel.peso = coalesce(drel.peso, 0) + (weight * 0.10)
        WITH m, weight, genre_updated, COUNT(drel) AS director_updated

        OPTIONAL MATCH (m)-[arel:HAS_ACTOR]->(:Actor)
        SET arel.peso = coalesce(arel.peso, 0) + (weight * 0.07)
        WITH m, weight, genre_updated, director_updated, COUNT(arel) AS actor_updated

        OPTIONAL MATCH (m)-[srel:APPROPIATE_FOR_SEASON]->(:Season)
        SET srel.peso = coalesce(srel.peso, 0) + (weight * 0.05)
        WITH m {.id, .title} AS movie, genre_updated, director_updated, actor_updated, COUNT(srel) AS season_updated

        RETURN {
        movie: movie,
        updated: {
            genre: genre_updated,
            director: director_updated,
            actor: actor_updated,
            season: season_updated
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
