from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# connect to DB
# SQLALCHEMY_DATABASE_URL='postgresql://user:password@postgresserver/db'
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# NOT USED
# connect to db using psycopg2
# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             dbname="fastapi",
#             user="postgres",
#             password="1234",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("DB connection was successful!")
#         break
#     except Exception as error:
#         print("Connecting to db failed")
#         print("Error: ", error)
#         time.sleep(2)
