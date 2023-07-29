from random import randrange
import time
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body


# for schema validation
from pydantic import BaseModel

import psycopg2
from psycopg2.extras import RealDictCursor

# start using sqlalchemy
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session


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


@app.get("/posts", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()
    return posts


# Create a post route
# pass default status code
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # # don't do this as it is vulnerable to SQL injection
    # # cursor.execute(f"INSERT INTO posts (title,content,published) VALUES ({post.title}, {post.content}, {post.published})")

    # # the SQL query is sanitized to prevent SQL injection
    # cursor.execute(
    #     """INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # # commit the changes to save it to the actual DB
    # conn.commit()

    # new_post = models.Post(
    #     title=post.title, content=post.content, published=post.published
    # )

    # spread operator
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    # similar to RETURNING in SQL
    db.refresh(new_post)

    return new_post


# id is path parameter
@app.get("/posts/{id}", response_model=schemas.Post)
# we can validate the path params
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id=%s""", str(id))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        # Response.status = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with {id} was not found"}

        # throw an exception
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"post with {id} was not found")
    return post


# delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", str(id))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"post with {id} was not found")
    post.delete(synchronize_session=False)
    db.commit()
    return {"message": "post was deleted"}


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(
    id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)
):
    # cursor.execute(
    #     """UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",
    #     (post.title, post.content, post.published, str(id)),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"post with {id} was not found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash password
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(
    id: int,
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist",
        )

    return user


# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return posts
