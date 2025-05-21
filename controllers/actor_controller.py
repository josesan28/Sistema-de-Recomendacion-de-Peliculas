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
