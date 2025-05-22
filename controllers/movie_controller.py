from neo4j_connection import Neo4jConnection

class MovieController:
    @staticmethod
    def get_movie(movie_id):
        query = """
        MATCH (m:Movie {id: $movie_id})
        OPTIONAL MATCH (m)-[hg:HAS_GENRE]->(g:Genre)
        OPTIONAL MATCH (m)-[db:DIRECTED_BY]->(d:Director)
        OPTIONAL MATCH (m)-[ha:HAS_ACTOR]->(a:Actor)
        OPTIONAL MATCH (m)-[afs:APPROPIATE_FOR_SEASON]->(s:Season)
        RETURN m {.*, 
                 genres: COLLECT(DISTINCT {name: g.name, weight: hg.peso}),
                 directors: COLLECT(DISTINCT {name: d.name, weight: db.peso}),
                 actors: COLLECT(DISTINCT {name: a.name, weight: ha.peso}),
                 seasons: COLLECT(DISTINCT {name: s.name, weight: afs.peso})
                } AS movie
        """
        result = Neo4jConnection().query(query, {"movie_id": movie_id})
        return result[0] if result else None

    @staticmethod
    def get_top_movies(limit=10):
        query = """
        MATCH (m:Movie)
        WHERE m.rating IS NOT NULL
        RETURN m {.id, .title, .year, .rating} AS movie
        ORDER BY m.rating DESC
        LIMIT $limit
        """
        return Neo4jConnection().query(query, {"limit": limit})


    @staticmethod
    def get_movies_by_season(season_name, min_weight=0.5):
        query = """
        MATCH (m:Movie)-[r:APPROPIATE_FOR_SEASON]->(s:Season {name: $season_name})
        WHERE r.peso >= $min_weight
        RETURN m {.id, .title, .year, season_weight: r.peso} AS movie
        ORDER BY r.peso DESC
        LIMIT 20
        """
        return Neo4jConnection().query(query, {"season_name": season_name, "min_weight": min_weight})

    @staticmethod
    def search_movies(title_keyword):
        query = """
        MATCH (m:Movie)
        WHERE toLower(m.title) CONTAINS toLower($keyword)
        RETURN m {.id, .title, .year} AS movie
        LIMIT 20
        """
        return Neo4jConnection().query(query, {"keyword": title_keyword})