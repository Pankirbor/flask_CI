import unittest.mock

import pytest

from page_tracker.app import app


@pytest.fixture
def http_client():
    return app.test_client()


@unittest.mock.patch("page_tracker.app.redis")
def test_should_call_redis_incr(mock_redis, http_client):
    mock_redis.return_value.incr.return_value = 5
    response = http_client.get("/")

    assert response.status_code == 200
    assert response.text == "Эту страницу просматривали 5 раз."
    mock_redis.return_value.incr.assert_called_once_with("page_views")
