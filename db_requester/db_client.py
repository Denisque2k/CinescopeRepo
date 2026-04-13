from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from resources.db_creds import DBCreds

USERNAME = DBCreds.USERNAME
PASSWORD = DBCreds.PASSWORD
HOST = DBCreds.DB_MOVIES_HOST
PORT = DBCreds.DB_MOVIES_PORT
DATABASE_NAME = DBCreds.DB_MOVIES_NAME

# Двидок для подключения к БД
engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}",
    echo=False # Установить True для отладки SQL запросов
)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """Создает новую сессию БД"""
    return SessionLocal()