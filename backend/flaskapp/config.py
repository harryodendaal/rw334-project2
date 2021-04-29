import os

user = "test"
password = "password"
host = "0.0.0.0"
database = "database"
port = "5432"

DATABASE_CONNECTION_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
