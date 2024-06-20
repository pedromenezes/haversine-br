import logging
from fastapi import FastAPI, HTTPException, Query
import redis
from pydantic import BaseModel
from typing import List, Optional
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

redis_host = os.getenv('REDIS_HOST', 'redis')
redis_client = redis.StrictRedis(host=redis_host, port=6379, db=0)

class NearestCity(BaseModel):
    name: str
    distance: float

class NearestCitiesResponse(BaseModel):
    city: str
    nearest_cities: List[NearestCity]
    unit: str = "km"

@app.get("/nearest_cities/{city_name}", response_model=NearestCitiesResponse)
def get_nearest_cities(city_name: str, max_results: Optional[int] = Query(5, gt=0, le=10)):
    """
    Retorna as cidades mais próximas em quilômetros.
    
    - **city_name**: Nome da cidade para a qual encontrar as cidades mais próximas.
    - **max_results**: Número máximo de resultados a serem retornados (1-10, padrão: 5).
    """
    hash_key = f"distances:{city_name}"
    if not redis_client.exists(hash_key):
        raise HTTPException(status_code=404, detail="City not found")
    
    distances = redis_client.hgetall(hash_key)
    nearest_cities = [{"name": city.decode("utf-8"), "distance": float(distance)} for city, distance in distances.items()]
    nearest_cities.sort(key=lambda x: x["distance"])

    return {"city": city_name, "nearest_cities": nearest_cities[:max_results], "unit": "km"}

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Distância entre Cidades. Use /docs para ver os endpoints disponíveis."}
