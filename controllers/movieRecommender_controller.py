from neo4j_connection import Neo4jConnection

class MovieRecommenderController:
    @staticmethod
    def recommend_movies_for_user(user_id, top_n=10):
        query = """
        CALL {
            MATCH (u:User {id: $user_id})-[r:RATED]->(m:Movie)
            WHERE r.rating >= 3
            WITH COLLECT(m) AS liked_movies
            UNWIND liked_movies AS movie
            MATCH (movie)-[:HAS_GENRE]->(g:Genre)
            MATCH (movie)-[:HAS_ACTOR]->(a:Actor)
            MATCH (movie)-[:DIRECTED_BY]->(d:Director)
            RETURN COLLECT(DISTINCT g) + COLLECT(DISTINCT a) + COLLECT(DISTINCT d) AS seeds
        }
        CALL gds.graph.project.cypher(
            'userSubgraph',
            'MATCH (m:Movie) RETURN id(m) AS id',
            'MATCH (m1:Movie)-[r]-(m2) RETURN id(m1) AS source, id(m2) AS target, type(r) AS type'
        )
        YIELD graphName
        WITH seeds, graphName
        CALL gds.pageRank.stream(graphName, {
            maxIterations: 20,
            dampingFactor: 0.85,
            personalization: {nodeIds: [n IN seeds | id(n)]}
        })
        YIELD nodeId, score
        WITH gds.util.asNode(nodeId) AS movie, score
        WHERE movie:Movie
          AND NOT EXISTS((:User {id: $user_id})-[:RATED]->(movie))
        RETURN movie {.*, score: score}
        ORDER BY score DESC
        LIMIT $top_n
        """
        return Neo4jConnection().query(query, {"user_id": user_id, "top_n": top_n})
