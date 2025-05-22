from neo4j_connection import Neo4jConnection

class ActorController:
    @staticmethod
    def get_actor(actor_id):
        query = """
        MATCH (a:Actor {id: $actor_id})
        RETURN a
        """
        return Neo4jConnection().query(query, {"actor_id": actor_id})

    @staticmethod
    def get_all_actors():
        query = "MATCH (a:Actor) RETURN a"
        return Neo4jConnection().query(query)
    
    @staticmethod
    def search_actors(keyword):
        query = """
        MATCH (a:Actor)
        WHERE toLower(a.name) CONTAINS toLower($keyword)
        RETURN a
        LIMIT 20
        """
        return Neo4jConnection().query(query, {"keyword": keyword})
    
    @staticmethod
    def get_movies_by_actor(actor_name, min_weight=0.5):
        query = """
        MATCH (a:Actor {name: $actor_name})<-[r:HAS_ACTOR]-(m:Movie)
        WHERE r.peso >= $min_weight
        RETURN m {.id, .title, .year, actor_weight: r.peso} AS movie
        ORDER BY r.peso DESC
        LIMIT 20
        """
        return Neo4jConnection().query(query, {"actor_name": actor_name, "min_weight": min_weight})