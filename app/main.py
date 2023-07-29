import time
from fastapi import FastAPI


import psycopg2
from psycopg2.extras import RealDictCursor

# start using sqlalchemy
from . import models
from .database import engine

# routes
from .routers import posts, users


# connect to DB
models.Base.metadata.create_all(bind=engine)


# connect to db using psycopg2
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname="fastapi",
            user="postgres",
            password="1234",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("DB connection was successful!")
        break
    except Exception as error:
        print("Connecting to db failed")
        print("Error: ", error)
        time.sleep(2)

app = FastAPI()


# temp, store posts in memory
my_posts = [{"id": 1, "title": "Title of post 1", "content": "Content of post 1"}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


# Path operation or route
@app.get("/")
# function name can be anything, need not be root
async def root():
    return {"message": "FASTAPI is running"}


app.include_router(posts.router)
app.include_router(users.router)

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return posts
