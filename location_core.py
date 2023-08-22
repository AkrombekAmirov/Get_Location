from fastapi import APIRouter, HTTPException
from geopy.distance import great_circle
from pydantic import BaseModel
from redis import Redis
import json

redis_client = Redis(host='localhost', port=6379, db=0)
router = APIRouter()


class LocationData(BaseModel):
    latitude: float
    longitude: float
    type: str
    name: str


@router.post("/compare_locations/")
def compare_locations(location_data: LocationData):
    redis_client.hset(f"locations:{location_data.type}", location_data.name,
                      json.dumps({"latitude": location_data.latitude, "longitude": location_data.longitude}))
    result = []
    if location_data.type == "hodim":
        result.append({"hodim_name": location_data.name,
                       "yaqin_poyezd": find_nearest_location(location_data.latitude, location_data.longitude,
                                                             {field.decode(): json.loads(value) for field, value in
                                                              redis_client.hgetall(f"locations:poyezd").items()})})
    return True


def find_nearest_location(latitude, longitude, locations):
    for location_name, location in locations.items():
        distance = round(great_circle((latitude, longitude), (location['latitude'], location['longitude'])).kilometers,
                         1)
        if distance < float('3.0'):
            raise HTTPException(status_code=400, detail={"name": location_name, "latitude": location['latitude'],
                                "longitude": location['longitude'], "distance": distance})

    return False
