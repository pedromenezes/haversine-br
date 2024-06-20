import logging
from haversine import haversine
import httpx
import redis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

url = "https://raw.githubusercontent.com/kelvins/municipios-brasileiros/main/json/municipios.json"

logger.info("Baixando o arquivo JSON")
response = httpx.get(url)
logger.info("Arquivo JSON baixado com sucesso")
cities = response.json()

def calculate_distances(city, cities):
    city_name = city["nome"]
    city_lat_lon = (city["latitude"], city["longitude"])
    distances = []
    for other_city in cities:
        other_city_name = other_city["nome"]
        if city_name != other_city_name:
            other_city_lat_lon = (other_city["latitude"], other_city["longitude"])
            distance = haversine(city_lat_lon, other_city_lat_lon)  # Distâncias em quilômetros
            distances.append({"name": other_city_name, "distance": distance})
    distances.sort(key=lambda x: x["distance"])
    return city_name, distances[:5]

def save_results_to_redis(city_name, distances):
    hash_key = f"distances:{city_name}"
    for distance in distances:
        redis_client.hset(hash_key, distance["name"], distance["distance"])
    logger.info(f"Distâncias salvas no Redis para a cidade {city_name}")

def process_city(city, cities):
    city_name, distances = calculate_distances(city, cities)
    save_results_to_redis(city_name, distances)

logger.info("Calculando distâncias entre as cidades")
for i, city in enumerate(cities):
    if not redis_client.exists(f"distances:{city['nome']}"):
        process_city(city, cities)
    if (i + 1) % (len(cities) // 20) == 0 or (i + 1) == len(cities):  # Log a cada 5% ou ao final
        logger.info(f"Progresso: {i + 1}/{len(cities)} cidades processadas ({((i + 1) / len(cities)) * 100:.1f}%)")

logger.info("Distâncias calculadas com sucesso")
