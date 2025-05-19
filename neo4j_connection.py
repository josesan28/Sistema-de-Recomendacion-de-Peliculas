import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Cargar variables de entorno
load_dotenv()

class Neo4jConnection:
    # Función para inicializar la clase obteniendo las credenciales
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI")
        self.user = os.getenv("NEO4J_USERNAME")
        self.password = os.getenv("NEO4J_PASSWORD")
        self.driver = None
    
    # Función para establecer la conexión con Neo4j
    def connect(self):
        if not self.driver:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        return self

    # Función para cerrar la conexión con Neo4j
    def close(self):
        if self.driver:
            self.driver.close()

    # Función especial para usar la conexión como un contexto
    def __enter__(self):
        return self.connect()

    # Función especial para cerrar la conexión al salir del contexto
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # Función para ejecutar una consulta Cypher
    def query(self, cypher_query, parameters=None):
        with self.driver.session() as session:
            result = session.run(cypher_query, parameters or {})
            return [record.data() for record in result]