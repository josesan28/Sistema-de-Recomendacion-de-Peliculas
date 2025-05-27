from neo4j_connection import Neo4jConnection

class MovieController:
    @staticmethod
    def get_movie(movie_id):
        query = """
        MATCH (m:Movie {id: $movie_id})
        RETURN m {.id, .title, .year} AS movie
        """
        with Neo4jConnection() as conn:
            result = conn.query(query, {"movie_id": movie_id})
            return result[0] if result else None

    @staticmethod
    def get_latest_movies(limit=10):
        query = """
        MATCH (m:Movie)
        RETURN m {.id, .title, .year} AS movie
        ORDER BY m.year DESC
        LIMIT $limit
        """
        with Neo4jConnection() as conn:
            return conn.query(query, {"limit": limit})

    @staticmethod
    def get_movies_by_season(season_name):
        query = """
        MATCH (m:Movie)-[:APPROPIATE_FOR_SEASON]->(:Season {name: $season_name})
        RETURN m {.id, .title, .year} AS movie
        ORDER BY m.year DESC
        LIMIT 20
        """
        with Neo4jConnection() as conn:
            return conn.query(query, {"season_name": season_name})

    @staticmethod
    def search_movies(title_keyword):
        query = """
        MATCH (m:Movie)
        WHERE toLower(m.title) CONTAINS toLower($keyword)
        RETURN m {.id, .title, .year} AS movie
        LIMIT 20
        """
        with Neo4jConnection() as conn:
            return conn.query(query, {"keyword": title_keyword})
        
    @staticmethod
    def get_top_movies(limit=10):
        """Obtiene las películas más populares basadas en interacciones positivas"""
        query = """
        MATCH (m:Movie)
        OPTIONAL MATCH (m)<-[r:INTERACTED]-()
        WHERE r.weight > 0
        WITH m, COUNT(r) AS positive_interactions
        RETURN m {.id, .title, .year, popularity: positive_interactions} AS movie
        ORDER BY positive_interactions DESC, m.year DESC
        LIMIT $limit
        """
        with Neo4jConnection() as conn:
            return conn.query(query, {"limit": limit})