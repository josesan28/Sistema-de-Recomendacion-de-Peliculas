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
    
    @staticmethod
    def get_movies_by_genre(genre_name, min_weight=0.5):
        query = """
        MATCH (g:Genre {name: $genre_name})<-[r:HAS_GENRE]-(m:Movie)
        WHERE r.peso >= $min_weight
        RETURN m {.id, .title, .year, genre_weight: r.peso} AS movie
        ORDER BY r.peso DESC
        LIMIT 20
        """
        return Neo4jConnection().query(query, {"genre_name": genre_name, "min_weight": min_weight})
