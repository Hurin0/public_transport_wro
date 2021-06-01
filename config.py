import os

user = os.getenv('POSTGRES_USER', 'postgres')
password = os.getenv('POSTGRES_PASSWORD', 'toor')
host = os.getenv('POSTGRES_HOST', 'localhost')
database = os.getenv('POSTGRES_DB', 'mpkweb')
port = os.getenv('POSTGRES_PORT', '9000')

DATABASE_CONNECTION_URI = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
