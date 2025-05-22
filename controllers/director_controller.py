from neo4j_connection import Neo4jConnection

class DirectorController:
    @staticmethod
    def get_director(director_id):
        query = """
        MATCH (d:Director {id: $director_id})
        RETURN d
        """
        return Neo4jConnection().query(query, {"director_id": director_id})

    @staticmethod
    def get_all_directors():
        query = "MATCH (d:Director) RETURN d"
        return Neo4jConnection().query(query)

    @staticmethod
    def get_movies_by_director(director_name, min_weight=0.5):
        query = """
        MATCH (d:Director {name: $director_name})<-[r:DIRECTED_BY]-(m:Movie)
        WHERE r.peso >= $min_weight
        RETURN m {.id, .title, .year, director_weight: r.peso} AS movie
        ORDER BY r.peso DESC
        LIMIT 20
        """
        return Neo4jConnection().query(query, {"director_name": director_name, "min_weight": min_weight})
