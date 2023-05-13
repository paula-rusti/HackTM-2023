import asyncio
import json
import os
import time

import aio_pika
from influxdb_client import InfluxDBClient, Point
from persistance.data_formatter import format_data
from persistance.influx_client import write_api
from persistance.mongo_client import MongoClient


async def consume():
    # todo pass clients to constructor
    mongo_client_instance = MongoClient()
    await mongo_client_instance.create_collection()

    # Connect to the RabbitMQ server
    connection_string = os.getenv("RABBIT_MQ") or 'amqp://guest:guest@localhost/'
    connection = await aio_pika.connect_robust(connection_string)
    channel = await connection.channel()

    # Declare the queue and bind to it
    queue_name = 'bme680-data'
    queue = await channel.declare_queue(queue_name, passive=True)

    # influx db
    username = 'username'
    password = 'password'

    database = 'telegraf'
    retention_policy = 'autogen'

    bucket = f'{database}/{retention_policy}'

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                print("Received message:", message.body)
                data_for_influx = json.loads(message.body)
                formatted_data = format_data(data_for_influx)
                with InfluxDBClient(url='http://localhost:8086', token=f'{username}:{password}', org='-') as client:
                    with client.write_api() as write_api:
                        write_api.write(bucket="enviro", org="enviro", record=formatted_data['temperature'])
                        write_api.write(bucket="enviro", org="enviro", record=formatted_data['humidity'])
                        write_api.write(bucket="enviro", org="enviro", record=formatted_data['pressure'])
                        write_api.write(bucket="enviro", org="enviro", record=formatted_data['gas_resistance'])
                await mongo_client_instance.insert_one(json.loads(message.body))

async def main():
    # Start the consumer
    await consume()


if __name__ == '__main__':
    asyncio.run(main())
