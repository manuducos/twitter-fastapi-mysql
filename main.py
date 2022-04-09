# FastAPI
from fastapi import FastAPI

# Routes
from routes import user, tweet

app = FastAPI()

app.include_router(user.user)
app.include_router(tweet.tweet)