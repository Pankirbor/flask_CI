import unittest.mock

from redis import ConnectionError
from werkzeug import Response


@unittest.mock.patch("page_tracker.app.redis")
def test_should_call_redis_incr(mock_redis, http_client):
    mock_redis.return_value.incr.return_value = 5
    response = http_client.get("/")

    assert response.status_code == 200
    assert response.text == "Эту страницу просматривали 5 раз."
    mock_redis.return_value.incr.assert_called_once_with("page_views")


@unittest.mock.patch("page_tracker.app.redis")
def test_should_handle_redis_connection_error(mock_redis, http_client):
    mock_redis.return_value.incr.side_effect = ConnectionError
    response: Response = http_client.get("/")

    assert response.status_code == 500
    assert response.text == "Простите, что то не так \N{pensive face}"
