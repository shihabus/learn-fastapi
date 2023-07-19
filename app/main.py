from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body


# for schema validation
from pydantic import BaseModel

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
    return {"message": "Hello Shana"}


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


# Create a post route
# pass default status code
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(
    post: Post,
):
    print(post)
    # convert to dict
    print(post.dict())

    post_dict = post.dict()
    post_dict["id"] = randrange(0, 100000)

    my_posts.append(post_dict)
    return {"data": post_dict}


# id is path parameter
@app.get("/posts/{id}")
# we can validate the path params
def get_post(id: int, response: Response):
    print(id)
    post = find_post(id)
    if not post:
        # Response.status = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with {id} was not found"}

        # throw an exception
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"post with {id} was not found")
    return {"data": post}


# delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post_idx = find_post_index(id)
    if post_idx == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"post with {id} was not found")
    deleted_post = my_posts.pop(post_idx)
    return {"data": deleted_post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    post_idx = find_post_index(id)
    if post_idx == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"post with {id} was not found")

    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[post_idx] = post

    return {"data": my_posts}
