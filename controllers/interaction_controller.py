from neo4j_connection import Neo4jConnection
from datetime import datetime

class InteractionController:
    
    @staticmethod
    def add_interaction(user_id, movie_id, interaction_type):
        if interaction_type == 'like':
            weight = 1.0
        else:
            weight = -1.0
        
        query = """
        MATCH (u:User {id: $user_id}), (m:Movie {id: $movie_id})
        MERGE (u)-[r:INTERACTED]->(m)
        SET r.type = $interaction_type,
            r.weight = $weight,
            r.timestamp = datetime()

        WITH m, $weight AS weight
        MATCH (m)-[rel:HAS_GENRE]->(g:Genre)
        SET rel.peso = rel.peso + (weight * 0.10)

        WITH m, weight
        MATCH (m)-[rel:DIRECTED_BY]->(d:Director)
        SET rel.peso = rel.peso + (weight * 0.10)

        WITH m, weight
        MATCH (m)-[rel:HAS_ACTOR]->(a:Actor)
        SET rel.peso = rel.peso + (weight * 0.07)

        WITH m, weight
        MATCH (m)-[rel:APPROPIATE_FOR_SEASON]->(s:Season)
        SET rel.peso = rel.peso + (weight * 0.05)

        WITH m {.id, .title} AS movie, COUNT(*) AS updated_relations
        RETURN { movie: movie, updated_relations: updated_relations } AS result
        """
        with Neo4jConnection() as conn:
            result = conn.query(query, {
                "user_id": user_id,
                "movie_id": movie_id,
                "interaction_type": interaction_type,
                "weight": weight
            })
            return result[0] if result else None