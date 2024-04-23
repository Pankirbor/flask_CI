import pytest

from flask.testing import FlaskClient
from redis import Redis
from werkzeug import Response


@pytest.mark.timeout(1.5)
def test_should_update_redis(redis_client: Redis, http_client: FlaskClient):
    redis_client.set("page_views", 4)
    response: Response = http_client.get("/")

    assert response.status_code == 200
    assert response.text == "Эту страницу просматривали 5 раз."
    assert redis_client.get("page_views") == b"5"
