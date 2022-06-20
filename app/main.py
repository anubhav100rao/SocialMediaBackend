from typing import List
from fastapi import FastAPI, Request
from .database import Base, engine
from . import models
from .routers import post, user, auth, vote
import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(post.router, tags=["posts"])
app.include_router(user.router, tags=["users"])
app.include_router(auth.router, tags=["auth"])
app.include_router(vote.router, tags=["votes"])


# default route
@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
def root(request: Request, path_name: str):
    return {
        "message": "Welcome to Social Network API",
        "version": "1.0.0",
        "server": "FastAPI",
        "server time": str(datetime.datetime.now()),
        "available routes": [
            {
                "post": "http://localhost:8000/posts",
            },
            {
                "user": "http://localhost:8000/users"
            },
            {
                "documentation": "http://localhost:8000/docs",
            }
        ],
        "request_method": request.method,
        "path_name": path_name
    }


