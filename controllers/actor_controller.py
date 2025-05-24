from neo4j_connection import Neo4jConnection

class ActorController:
    @staticmethod
    def get_actor(actor_id):
        query = """
        MATCH (a:Actor {id: $actor_id})
        RETURN a {.id, .name} AS actor
        """
        with Neo4jConnection() as conn:
            result = conn.query(query, {"actor_id": actor_id})
            return result[0] if result else None

    @staticmethod
    def get_all_actors():
        query = """
        MATCH (a:Actor)
        RETURN a {.id, .name} AS actor
        ORDER BY a.name
        """
        with Neo4jConnection() as conn:
            return conn.query(query)
    
    @staticmethod
    def search_actors(keyword):
        query = """
        MATCH (a:Actor)
        WHERE toLower(a.name) CONTAINS toLower($keyword)
        RETURN a {.id, .name} AS actor
        LIMIT 20
        """
        with Neo4jConnection() as conn:
            return conn.query(query, {"keyword": keyword})
    
    @staticmethod
    def get_movies_by_actor(actor_name):
        query = """
        MATCH (m:Movie)-[:HAS_ACTOR]->(a:Actor {name: $actor_name})
        RETURN m {.id, .title, .year} AS movie
        ORDER BY m.year DESC
        LIMIT 20
        """
        with Neo4jConnection() as conn:
            return conn.query(query, {"actor_name": actor_name})