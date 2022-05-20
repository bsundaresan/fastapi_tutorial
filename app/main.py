from fastapi import FastAPI

#Import engine and get_db from database file
from .database import *
from . import models

from .routers import posts, users, auth, votes

from .config import settings

#For cross-origin resource sharing
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#Change when the app is deployed publicly
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This creates the table (not needed as we are using Alembic)
# models.Base.metadata.create_all(bind=engine)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
def home():
    
    return {
        "message": "Welcome to my API!"
        }
