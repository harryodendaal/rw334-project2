import os

user = "test"
password = "password"
host = "0.0.0.0"
database = "database"
port = "5432"

DATABASE_CONNECTION_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "neo"
NEO4J_URL = "bolt://8.tcp.ngrok.io:13593"