import pytest
import requests


@pytest.mark.timeout(1.5)
def test_should_update_redis(redis_client, flask_url):
    print(redis_client.get("page_views"))
    redis_client.set("page_views", 4)
    print(redis_client.get("page_views"))
    response: requests.Response = requests.get(flask_url)

    assert response.status_code == 200
    assert response.text == "Эту страницу просматривали 5 раз."
    assert redis_client.get("page_views") == b"5"
