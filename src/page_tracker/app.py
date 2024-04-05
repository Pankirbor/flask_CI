from flask import Flask
from redis import Redis

app = Flask(__name__)
redis = Redis()


@app.get("/")
def index():
    page_views = redis.incr("page_views")
    return f"Эту страницу просматривали {page_views} раз."
