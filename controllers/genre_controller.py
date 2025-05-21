from neo4j_connection import Neo4jConnection

class GenreController:
    @staticmethod
    def get_genre(genre_name):
        query = """
        MATCH (g:Genre {name: $genre_name})
        RETURN g
        """
        return Neo4jConnection().query(query, {"genre_name": genre_name})

    @staticmethod
    def get_all_genres():
        query = "MATCH (g:Genre) RETURN g"
        return Neo4jConnection().query(query)
