import functools
import openai

from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorClient


app = FastAPI()


async def mongo_collection():
    # client = AsyncIOMotorClient("mongodb://root:0l8MwKdttH@mongodb:27017")
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    database = client["sensor_data_db"]
    collection = database["sensor_data"]
    return collection


@app.get("/latest")
async def status_latest_values():
    collection = await mongo_collection()
    cursor = collection.find().sort("timestamp", -1).limit(1)
    document = await cursor.to_list(length=1)
    if not document:
        return {"response": "Service not available try again later"}

    document = document[0]
    document = {
        "sensor_type": "Bme680Bosh",
        "location_name": "HackTM2023 - Craft",
        "timestamp": 1683977102438,   # discard this
        "temperature": 22.68,
        "humidity": 54.114,
        "pressure": 1011.23,
        "gas_resistance": 274224.4536061566
    }
    # query openai with sensor daa and get response
    query = f"You're an environmentalist and I have the following data for you:\n temperature {document['temperature']}°C, humidity {document['humidity']}%, pressure {document['pressure']}hPa, gas resistance {document['gas_resistance']}Ohm.\n What should I do?"
    open_ai_token = "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"
    openai.api_key = open_ai_token
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=query,
        temperature=0.9,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )
    return {"response": "Service not available try again later"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)