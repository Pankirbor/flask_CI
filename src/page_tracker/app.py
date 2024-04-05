from functools import cache

from flask import Flask
from redis import Redis

app = Flask(__name__)


@app.get("/")
def index():
    page_views = redis().incr("page_views")
    return f"Эту страницу просматривали {page_views} раз."


@cache
def redis():
    """Кешируем экземпляр клиента для гарантии
    единичного экземпляра в памяти Синглтон"""
    return Redis()
