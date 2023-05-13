import asyncio
import json

import aio_pika

from persistance.data_formatter import format_data
from persistance.influx_client import write_api
from persistance.mongo_client import MongoClient


async def consume():
    # todo pass clients to constructor
    # mongo_client_instance = MongoClient()
    # await mongo_client_instance.create_collection()

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
                data_for_influx = json.loads(message.body)
                formatted_data = format_data(data_for_influx)
                write_api.write(bucket="initial_bucket", org="Home", record=formatted_data['temperature'])
                write_api.write(bucket="initial_bucket", org="Home", record=formatted_data['humidity'])
                write_api.write(bucket="initial_bucket", org="Home", record=formatted_data['pressure'])
                write_api.write(bucket="initial_bucket", org="Home", record=formatted_data['gas_resistance'])
                # await mongo_client_instance.insert_one(json.loads(message.body))


async def main():
    # Start the consumer
    await consume()


if __name__ == '__main__':
    asyncio.run(main())
