import dotenv
from dotenv import load_dotenv

load_dotenv(verbose=True)

def fetch(key):
    return dotenv.get_key(".env", key)

class EnvConstants:
    secret_key = fetch("SECRET_KEY")
    environment = fetch("ENVIRONMENT")
    class Database:
        name = fetch("POSTGRES_DB")
        username = fetch("POSTGRES_USER")
        password = fetch("POSTGRES_PASSWORD")
        host = fetch("DB_HOST")
        port = fetch("DB_PORT")


env = EnvConstants()