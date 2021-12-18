import asyncio
import aioamqp
from flask import current_app


async def send(body):
    transport, protocol = await aioamqp.connect(host=current_app.config['RABBITMQ_HOST'],
                                                port=int(current_app.config['RABBITMQ_PORT']),
                                                login=current_app.config['RABBITMQ_LOGIN'],
                                                password=current_app.config['RABBITMQ_PASSWORD'])
    channel = await protocol.channel()

    await channel.queue_declare(queue_name='hello')

    await channel.basic_publish(
        payload=str(body),
        exchange_name='',
        routing_key='hello'
    )

    print(" [x] Sent")
    await protocol.close()
    transport.close()


loop = asyncio.get_event_loop()
