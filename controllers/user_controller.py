from neo4j_connection import Neo4jConnection
import uuid  # Para generar IDs aleatorios

class UserController:
    @staticmethod
    def create_user(user_data):
        user_data['id'] = str(uuid.uuid4())  # Genera un UUID aleatorio
        query = """
        CREATE (u:User {
            id: $id,
            email: $email,
            name: $name,
            hashed_password: $password_hash,
            created_at: datetime()
        })
        RETURN u {.id, .email, .name, created_at: toString(datetime())}
        """
        with Neo4jConnection() as conn:
            return conn.query(query, user_data)[0]

    @staticmethod
    def get_user_by_id(user_id):
        query = "MATCH (u:User {id: $user_id}) RETURN u {.id, .email, .name, .hashed_password} AS user"
        with Neo4jConnection() as conn:
            result = conn.query(query, {"user_id": user_id})
            return result[0]['user'] if result else None

    @staticmethod
    def get_user_by_email(email):
        query = """
        MATCH (u:User {email: $email})
        RETURN u {.id, .email, .name, .hashed_password} AS user
        """
        with Neo4jConnection() as conn:
            result = conn.query(query, {"email": email})
            return result[0]['user'] if result else None
