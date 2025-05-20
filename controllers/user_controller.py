from neo4j_connection import Neo4jConnection

class UserController:
    @staticmethod
    def create_user(user_data):
        query = """
        CREATE (u:User {id: $id, name: $name, email: $email})
        RETURN u
        """
        with Neo4jConnection() as conn:
            return conn.query(query, user_data)

    @staticmethod
    def get_user_by_id(user_id):
        query = "MATCH (u:User {id: $user_id}) RETURN u"
        with Neo4jConnection() as conn:
            return conn.query(query, {"user_id": user_id})