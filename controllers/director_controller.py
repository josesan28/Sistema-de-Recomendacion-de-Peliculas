from neo4j_connection import Neo4jConnection

class DirectorController:
    @staticmethod
    def get_director(director_id):
        query = """
        MATCH (d:Director {id: $director_id})
        RETURN d {.id, .name} AS director
        """
        with Neo4jConnection() as conn:
            result = conn.query(query, {"director_id": director_id})
            return result[0] if result else None

    @staticmethod
    def get_all_directors():
        query = """
        MATCH (d:Director)
        RETURN d {.id, .name} AS director
        ORDER BY d.name
        """
        with Neo4jConnection() as conn:
            return conn.query(query)

    @staticmethod
    def get_movies_by_director(director_name, min_weight=0.5):
        query = """
        MATCH (d:Director {name: $director_name})<-[r:DIRECTED_BY]-(m:Movie)
        WHERE r.peso >= $min_weight
        RETURN m {.id, .title, .year, director_weight: r.peso} AS movie
        ORDER BY r.peso DESC
        LIMIT 20
        """
        with Neo4jConnection() as conn:
            return conn.query(query, {"director_name": director_name, "min_weight": min_weight})