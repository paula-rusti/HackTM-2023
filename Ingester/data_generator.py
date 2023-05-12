import asyncio
import time

import aio_pika
import json


async def publish_message():
    # Define the message data
    message_data = {
        "sensor_type": "temperature_sensor_mock",
        "timestamp": 1620805817,
        "temperature": 25.3,
        "humidity": 60.5,
        "pressure": 1013.25,
        "gas_resistance": 1200.0
    }

    # Convert the message data to a JSON string
    message_json = json.dumps(message_data)

    # Connect to RabbitMQ
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")

    # Create a channel
    channel = await connection.channel()

    # Declare the exchange and queue
    exchange = await channel.declare_exchange('sensor_data', aio_pika.ExchangeType.FANOUT)
    queue = await channel.declare_queue('sensor_data_queue')
    await queue.bind(exchange)

    # Publish the message to RabbitMQ
    while True:
        await exchange.publish(aio_pika.Message(body=message_json.encode()), routing_key='sensor_data')
        await asyncio.sleep(1)

         # Close the connection
        # await connection.close()


# Run the coroutine
asyncio.run(publish_message())
