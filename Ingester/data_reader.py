import asyncio
import json

import aio_pika

from persistance.mongo_client import MongoClient


async def consume():
    mongo_client_instance = MongoClient()
    await mongo_client_instance.create_collection()

    # Connect to the RabbitMQ server
    connection = await aio_pika.connect_robust('amqp://guest:guest@localhost/')
    channel = await connection.channel()

    # Declare the queue and bind to it
    queue_name = 'sensor_data_queue'
    queue = await channel.declare_queue(queue_name)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                print("Received message:", message.body)
                await mongo_client_instance.insert_one(json.loads(message.body))


async def main():
    # Start the consumer
    await consume()


if __name__ == '__main__':
    asyncio.run(main())
