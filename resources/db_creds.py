import os
from dotenv import load_dotenv
import psycopg2
load_dotenv()

class DBCreds:
    DB_MOVIES_HOST = os.getenv('DB_MOVIES_HOST')
    DB_MOVIES_PORT = os.getenv('DB_MOVIES_PORT')
    DB_MOVIES_NAME = os.getenv('DB_MOVIES_NAME')
    USERNAME = os.getenv('DB_MOVIES_USERNAME')
    PASSWORD = os.getenv('DB_MOVIES_PASSWORD')