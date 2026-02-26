import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("DB_HOST"))

def get_connection():
    print(os.getenv("DB_HOST"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_NAME"))

    print("Connecting to PostgreSQL")
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    return connection