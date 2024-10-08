import pytest
from fastapi.testclient import TestClient
from app.main import app
import redis
import os

client = TestClient(app)

redis_host = os.getenv('REDIS_HOST', 'redis-test')
redis_client = redis.StrictRedis(host=redis_host, port=6379, db=0)

test_city = "TestCity"
test_nearest_cities = [
    {"name": "City1", "distance": 10.0},
    {"name": "City2", "distance": 20.0},
    {"name": "City3", "distance": 30.0},
    {"name": "City4", "distance": 40.0},
    {"name": "City5", "distance": 50.0}
]


@pytest.fixture(autouse=True)
def setup_and_teardown():
    redis_client.flushdb()
    hash_key = f"distances:{test_city}"
    for city in test_nearest_cities:
        redis_client.hset(hash_key, city["name"], city["distance"])
    yield
    redis_client.flushdb()


def test_get_nearest_cities():
    response = client.get(f"/nearest_cities/{test_city}?max_results=5")
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == test_city
    assert len(data["nearest_cities"]) == 5
    assert data["unit"] == "km"
    for i, city in enumerate(test_nearest_cities):
        assert data["nearest_cities"][i]["name"] == city["name"]
        assert data["nearest_cities"][i]["distance"] == city["distance"]


def test_get_nearest_cities_not_found():
    response = client.get("/nearest_cities/NonExistentCity")
    assert response.status_code == 404
    assert response.json()["detail"] == "City not found"


def test_get_nearest_cities_with_different_max_results():
    response = client.get(f"/nearest_cities/{test_city}?max_results=3")
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == test_city
    assert len(data["nearest_cities"]) == 3
    assert data["unit"] == "km"
    for i, city in enumerate(test_nearest_cities[:3]):
        assert data["nearest_cities"][i]["name"] == city["name"]
        assert data["nearest_cities"][i]["distance"] == city["distance"]


def test_list_cities():
    # Adiciona algumas cidades ao Redis
    cities = ["CityA", "CityB", "CityC"]
    for city in cities:
        redis_client.hset(f"distances:{city}", "DummyCity", 100.0)

    response = client.get("/cities")
    assert response.status_code == 200
    data = response.json()

    # Verifica se todas as cidades adicionadas estão na resposta
    assert set(data) == set(cities + [test_city])
    assert len(data) == len(cities) + 1  # +1 para incluir test_city
    assert all(isinstance(city, str) for city in data)
