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
