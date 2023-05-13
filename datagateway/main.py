import functools
import json
from typing import Union

from aio_pika import connect, Message, ExchangeType
from fastapi import FastAPI, APIRouter, Depends, Header
from pydantic import BaseModel

router = APIRouter()


class Bme680Values(BaseModel):
    sensor_type: str
    location_name: str
    timestamp: int
    temperature: float
    humidity: float
    pressure: float
    gas_resistance: float


@functools.lru_cache()
async def rabbitmq():
    connection = await connect("amqp://gateway:gateway@rabbitmq-headless/")
    channel = await connection.channel()
    sensors_exchange = await channel.declare_exchange(
        "sensor-data", ExchangeType.TOPIC, passive=True
    )
    return sensors_exchange


@router.post("/bme680/ingest")
async def ingest(data: Bme680Values, x_api_key:str = Header(...)):
    if x_api_key != "hacktm-2023":
        return {"ok": False, "error": "Invalid API key"}
    dict_data = data.dict()
    sensors_exchange = await rabbitmq()
    await sensors_exchange.publish(Message(json.dumps(dict_data).encode()), routing_key=data.sensor_type)
    return {"ok": True}


def create_app():
    app = FastAPI()
    app.include_router(router)
    return app


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(create_app(), host="0.0.0.0")
