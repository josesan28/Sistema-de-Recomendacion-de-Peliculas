from neo4j_connection import Neo4jConnection

class MovieController:
    @staticmethod
    def get_movie(movie_id):
        query = """
        MATCH (m:Movie {id: $movie_id})
        OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)
        OPTIONAL MATCH (m)-[:HAS_ACTOR]->(a:Actor)
        OPTIONAL MATCH (m)-[:DIRECTED_BY]->(d:Director)
        OPTIONAL MATCH (m)-[:APPROPIATE_FOR_SEASON]->(s)
        RETURN m {
            .id, 
            .title, 
            .year,
            .description
        } AS movie,
        COLLECT(DISTINCT g.name) AS genres,
        COLLECT(DISTINCT a.name) AS actors,
        COLLECT(DISTINCT d.name) AS directors,
        COLLECT(DISTINCT coalesce(s.name, s.nombre)) AS seasons
        """
        with Neo4jConnection() as conn:
            result = conn.query(query, {"movie_id": movie_id})
            if result:
                movie_data = result[0]
                movie_data['movie']['genres'] = movie_data['genres']
                movie_data['movie']['actors'] = movie_data['actors']
                movie_data['movie']['directors'] = movie_data['directors']
                movie_data['movie']['seasons'] = movie_data['seasons']
                return movie_data['movie']
            return None

    @staticmethod
    def get_all_movies(limit=150):
        query = """
        MATCH (m:Movie)
        OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)
        OPTIONAL MATCH (m)-[:HAS_ACTOR]->(a:Actor)
        OPTIONAL MATCH (m)-[:DIRECTED_BY]->(d:Director)
        OPTIONAL MATCH (m)-[:APPROPIATE_FOR_SEASON]->(s)
        WITH m, g, a, d, s
        ORDER BY rand()
        WITH m, 
            COLLECT(DISTINCT g.name) AS genres,
            COLLECT(DISTINCT a.name)[0..3] AS actors,
            COLLECT(DISTINCT d.name) AS directors,
            COLLECT(DISTINCT coalesce(s.name, s.nombre)) AS seasons
        RETURN m {
            .id, 
            .title, 
            .year,
            .description
        } AS movie,
        genres,
        actors,
        directors,
        seasons
        LIMIT $limit
        """
        with Neo4jConnection() as conn:
            results = conn.query(query, {"limit": limit})
            movies = []
            for result in results:
                movie = result['movie']
                movie['genres'] = result['genres']
                movie['actors'] = result['actors']
                movie['directors'] = result['directors']
                movie['seasons'] = result['seasons']
                movies.append(movie)
            return movies

    @staticmethod
    def get_latest_movies(limit=10):
        query = """
        MATCH (m:Movie)
        WITH m
        ORDER BY m.year DESC
        LIMIT $limit
        OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)
        OPTIONAL MATCH (m)-[:HAS_ACTOR]->(a:Actor)
        OPTIONAL MATCH (m)-[:DIRECTED_BY]->(d:Director)
        OPTIONAL MATCH (m)-[:APPROPIATE_FOR_SEASON]->(s)
        RETURN m {
            .id, 
            .title, 
            .year,
            .description
        } AS movie,
        COLLECT(DISTINCT g.name) AS genres,
        COLLECT(DISTINCT a.name)[0..3] AS actors,
        COLLECT(DISTINCT d.name) AS directors,
        COLLECT(DISTINCT coalesce(s.name, s.nombre)) AS seasons
        """
        with Neo4jConnection() as conn:
            results = conn.query(query, {"limit": limit})
            movies = []
            for result in results:
                movie = result['movie']
                movie['genres'] = result['genres']
                movie['actors'] = result['actors']
                movie['directors'] = result['directors']
                movie['seasons'] = result['seasons']
                movies.append(movie)
            return movies

    @staticmethod
    def get_movies_by_season(season_name):
        query = """
        MATCH (m:Movie)-[:APPROPIATE_FOR_SEASON]->(s)
        WHERE toLower(coalesce(s.name, s.nombre)) CONTAINS toLower($season_name)
        WITH m, s
        ORDER BY m.year DESC
        LIMIT 20
        OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)
        OPTIONAL MATCH (m)-[:HAS_ACTOR]->(a:Actor)
        OPTIONAL MATCH (m)-[:DIRECTED_BY]->(d:Director)
        RETURN m {
            .id, 
            .title, 
            .year,
            .description
        } AS movie,
        COLLECT(DISTINCT g.name) AS genres,
        COLLECT(DISTINCT a.name)[0..3] AS actors,
        COLLECT(DISTINCT d.name) AS directors,
        [coalesce(s.name, s.nombre)] AS seasons
        """
        with Neo4jConnection() as conn:
            results = conn.query(query, {"season_name": season_name})
            movies = []
            for result in results:
                movie = result['movie']
                movie['genres'] = result['genres']
                movie['actors'] = result['actors']
                movie['directors'] = result['directors']
                movie['seasons'] = result['seasons']
                movies.append(movie)
            return movies

    @staticmethod
    def search_movies(title_keyword):
        query = """
        MATCH (m:Movie)
        WHERE toLower(m.title) CONTAINS toLower($keyword)
        OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)
        OPTIONAL MATCH (m)-[:HAS_ACTOR]->(a:Actor)
        OPTIONAL MATCH (m)-[:DIRECTED_BY]->(d:Director)
        OPTIONAL MATCH (m)-[:APPROPIATE_FOR_SEASON]->(s)
        RETURN m {
            .id, 
            .title, 
            .year,
            .description
        } AS movie,
        COLLECT(DISTINCT g.name) AS genres,
        COLLECT(DISTINCT a.name)[0..3] AS actors,
        COLLECT(DISTINCT d.name) AS directors,
        COLLECT(DISTINCT coalesce(s.name, s.nombre)) AS seasons
        LIMIT 20
        """
        with Neo4jConnection() as conn:
            results = conn.query(query, {"keyword": title_keyword})
            movies = []
            for result in results:
                movie = result['movie']
                movie['genres'] = result['genres']
                movie['actors'] = result['actors']
                movie['directors'] = result['directors']
                movie['seasons'] = result['seasons']
                movies.append(movie)
            return movies

    @staticmethod
    def advanced_search(query_params):
        conditions = []
        params = {}
        
        base_query = """
        MATCH (m:Movie)
        """
        
        if query_params.get('genre'):
            base_query += """
            MATCH (m)-[:HAS_GENRE]->(search_g:Genre)
            WHERE toLower(search_g.name) CONTAINS toLower($genre)
            """
            params['genre'] = query_params['genre']
        
        if query_params.get('actor'):
            base_query += """
            MATCH (m)-[:HAS_ACTOR]->(search_a:Actor)
            WHERE toLower(search_a.name) CONTAINS toLower($actor)
            """
            params['actor'] = query_params['actor']
        
        if query_params.get('director'):
            base_query += """
            MATCH (m)-[:DIRECTED_BY]->(search_d:Director)
            WHERE toLower(search_d.name) CONTAINS toLower($director)
            """
            params['director'] = query_params['director']
        
        if query_params.get('season'):
            base_query += """
            MATCH (m)-[:APPROPIATE_FOR_SEASON]->(search_s)
            WHERE toLower(coalesce(search_s.name, search_s.nombre)) CONTAINS toLower($season)
            """
            params['season'] = query_params['season']
        
        if query_params.get('title'):
            base_query += """
            WHERE toLower(m.title) CONTAINS toLower($title)
            """
            params['title'] = query_params['title']
        
        base_query += """
        WITH m
        ORDER BY m.title
        LIMIT 50
        OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)
        OPTIONAL MATCH (m)-[:HAS_ACTOR]->(a:Actor)
        OPTIONAL MATCH (m)-[:DIRECTED_BY]->(d:Director)
        OPTIONAL MATCH (m)-[:APPROPIATE_FOR_SEASON]->(s)
        RETURN m {
            .id, 
            .title, 
            .year,
            .description
        } AS movie,
        COLLECT(DISTINCT g.name) AS genres,
        COLLECT(DISTINCT a.name)[0..3] AS actors,
        COLLECT(DISTINCT d.name) AS directors,
        COLLECT(DISTINCT coalesce(s.name, s.nombre)) AS seasons
        """
        
        with Neo4jConnection() as conn:
            results = conn.query(base_query, params)
            movies = []
            for result in results:
                movie = result['movie']
                movie['genres'] = result['genres']
                movie['actors'] = result['actors']
                movie['directors'] = result['directors']
                movie['seasons'] = result['seasons']
                movies.append(movie)
            return movies
        
    @staticmethod
    def get_top_movies(limit=10):
        """Obtiene las películas más populares basadas en interacciones positivas"""
        query = """
        MATCH (m:Movie)
        OPTIONAL MATCH (m)<-[r:INTERACTED]-()
        WHERE r.weight > 0
        WITH m, COUNT(r) AS positive_interactions
        ORDER BY positive_interactions DESC, m.year DESC
        LIMIT $limit
        OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)
        OPTIONAL MATCH (m)-[:HAS_ACTOR]->(a:Actor)
        OPTIONAL MATCH (m)-[:DIRECTED_BY]->(d:Director)
        OPTIONAL MATCH (m)-[:APPROPIATE_FOR_SEASON]->(s)
        RETURN m {
            .id, 
            .title, 
            .year,
            .description,
            popularity: positive_interactions
        } AS movie,
        COLLECT(DISTINCT g.name) AS genres,
        COLLECT(DISTINCT a.name)[0..3] AS actors,
        COLLECT(DISTINCT d.name) AS directors,
        COLLECT(DISTINCT coalesce(s.name, s.nombre)) AS seasons
        """
        with Neo4jConnection() as conn:
            results = conn.query(query, {"limit": limit})
            movies = []
            for result in results:
                movie = result['movie']
                movie['genres'] = result['genres']
                movie['actors'] = result['actors']
                movie['directors'] = result['directors']
                movie['seasons'] = result['seasons']
                movies.append(movie)
            return movies