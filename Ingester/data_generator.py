import asyncio
import json
import random

import aio_pika


def create_message():
    message_data = {
        "sensor_type": "temperature_sensor_mock",
        "location_name": "HackTM2023 - Craft",
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
        await asyncio.sleep(0.01)

        # Close the connection
        # await connection.close()


# Run the coroutine
asyncio.run(publish_message())
