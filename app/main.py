from fastapi import FastAPI

# start using sqlalchemy
# from . import models
# from .database import engine

# routes
from .routers import posts, users, auth, vote

# connect to DB
# now Alembic can take care of DB and table creation
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


# Path operation or route
@app.get("/")
# function name can be anything, need not be root
async def root():
    return {"message": "FASTAPI is running"}
