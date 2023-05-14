import functools
import openai

from fastapi import FastAPI, Depends, Header
from motor.motor_asyncio import AsyncIOMotorClient


app = FastAPI()


async def mongo_collection():
    client = AsyncIOMotorClient("mongodb://root:0l8MwKdttH@mongodb:27017")
    database = client["sensor_data_db"]
    collection = database["sensor_data"]
    return collection


@app.get("/latest")
async def status_latest_values(x_api_key:str = Header(...)):
    if x_api_key != "hacktm-2023-ai":
        return {"ok": False, "error": "Invalid API key"}
    collection = await mongo_collection()
    cursor = collection.find().sort("timestamp", -1).limit(1)
    document = await cursor.to_list(length=1)
    if not document:
        return {"response": "Service not available try again later"}
    document = document[0]
    # document = {
    #     "sensor_type": "Bme680Bosh",
    #     "location_name": "HackTM2023 - Craft",
    #     "timestamp": 1683977102438,   # discard this
    #     "temperature": 52.68,
    #     "humidity": 84.114,
    #     "pressure": 1011.23,
    #     "gas_resistance": 274224.4536061566
    # }
    # query openai with sensor daa and get response
    query = f"I have the following data for you:\n temperature {document['temperature']}°C, humidity {document['humidity']}%.\n Is it nice here for humans? What data values did I give you, please respond with the numbers. \n Please respond short and don't include the fact that you're an AI model. "
    open_ai_token = "sk-"
    openai.api_key = open_ai_token
    openai.organization = "org-nyQ7qUk1cEqkIC6hVucb6iBv"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": query
            }
        ],

    )
    try:
        data = response["choices"][0]["message"]["content"]
        return {"response": data}
    except Exception as e:
        return {"response": "Service not available try again later"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)