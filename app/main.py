from random import randrange
import time
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body


# for schema validation
from pydantic import BaseModel

import psycopg2
from psycopg2.extras import RealDictCursor


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


# schema modal
class Post(BaseModel):
    title: str
    content: str
    # optional and defaulted to True
    published: bool = True
    rating: Optional[int] = None


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


@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


# Create a post route
# pass default status code
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(
    post: Post,
):
    # don't do this as it is vulnerable to SQL injection
    # cursor.execute(f"INSERT INTO posts (title,content,published) VALUES ({post.title}, {post.content}, {post.published})")

    # the SQL query is sanitized to prevent SQL injection
    cursor.execute(
        """INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    # commit the changes to save it to the actual DB
    conn.commit()
    return {"data": new_post}


# id is path parameter
@app.get("/posts/{id}")
# we can validate the path params
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id=%s""", str(id))
    post = cursor.fetchone()
    if not post:
        # Response.status = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with {id} was not found"}

        # throw an exception
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"post with {id} was not found")
    return {"data": post}


# delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", str(id))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"post with {id} was not found")
    return {"data": deleted_post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",
        (post.title, post.content, post.published, str(id)),
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"post with {id} was not found")
    return {"data": updated_post}
