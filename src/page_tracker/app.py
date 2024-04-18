import os
from functools import cache

from flask import Flask
from redis import Redis, RedisError

app = Flask(__name__)


@app.get("/")
def index():
    try:
        page_views = redis().incr("page_views")
    except RedisError:
        app.logger.exception("Redis error")
        return "Простите, что то не так \N{pensive face}", 500
    else:
        return f"Эту страницу просматривали {page_views} раз."


@cache
def redis():
    """Кешируем экземпляр клиента для гарантии
    единичного экземпляра в памяти Синглтон"""
    return Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
