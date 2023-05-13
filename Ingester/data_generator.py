import asyncio
import random
import time
from datetime import datetime, timedelta

import aio_pika
import json

def create_message():
    # Define the message data
    # start_date = datetime(2022, 1, 1)
    # end_date = datetime(2022, 12, 31)
    # random_timestamp = (
    #         start_date
    #         + timedelta(
    #             seconds=random.randint(0, int((end_date - start_date).total_seconds()))
    #         )
    #     ).isoformat,

    message_data = {
        "sensor_type": "temperature_sensor_mock",
        "timestamp": 121234324234532,
        "temperature": random.uniform(-30.0, 100.0),
        "humidity": random.uniform(0.0, 1.0),
        "pressure": random.uniform(0.0, 1.0),
        "gas_resistance": random.uniform(0, 2000),
    }
    return message_data


async def publish_message():
    # Convert the message data to a JSON string

    # Connect to RabbitMQ
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")

    # Create a channel
    channel = await connection.channel()

    # Declare the exchange and queue
    exchange = await channel.declare_exchange(
        "sensor_data", aio_pika.ExchangeType.FANOUT
    )
    queue = await channel.declare_queue("sensor_data_queue")
    await queue.bind(exchange)

    # Publish the message to RabbitMQ
    while True:
        message_json = create_message()
        await exchange.publish(
            aio_pika.Message(body=json.dumps(message_json).encode()), routing_key="sensor_data"
        )
        await asyncio.sleep(1)

        # Close the connection
        # await connection.close()


# Run the coroutine
asyncio.run(publish_message())
