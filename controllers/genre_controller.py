from neo4j_connection import Neo4jConnection

class GenreController:
    @staticmethod
    def get_genre(genre_name):
        query = """
        MATCH (g:Genre {name: $genre_name})
        RETURN g {.name} AS genre
        """
        with Neo4jConnection() as conn:
            result = conn.query(query, {"genre_name": genre_name})
            return result[0] if result else None

    @staticmethod
    def get_all_genres():
        query = """
        MATCH (g:Genre)
        RETURN g {.name} AS genre
        ORDER BY g.name
        """
        with Neo4jConnection() as conn:
            return conn.query(query)
    
    @staticmethod
    def get_movies_by_genre(genre_name, min_weight=0.5):
        query = """
        MATCH (g:Genre {name: $genre_name})<-[r:HAS_GENRE]-(m:Movie)
        WHERE r.peso >= $min_weight
        RETURN m {.id, .title, .year, genre_weight: r.peso} AS movie
        ORDER BY r.peso DESC
        LIMIT 20
        """
        with Neo4jConnection() as conn:
            return conn.query(query, {"genre_name": genre_name, "min_weight": min_weight})