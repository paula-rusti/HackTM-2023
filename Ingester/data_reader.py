import asyncio
import aio_pika


async def consume():
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


async def main():
    # Start the consumer
    await consume()


if __name__ == '__main__':
    asyncio.run(main())
