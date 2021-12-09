import asyncio
import json
import os
from threading import Thread

import aioamqp
import redis
import requests
from random import randrange

tasks = ['сфоткайте трех уличных котов',
         'эстетика ебеней',
         'ночные посиделки на кухне',
         'фотография-иллюстрация к стихотворению Бродского']


def get_task():
    r = randrange(len(tasks))
    print(tasks[r])
    return tasks[r]


async def on_request(channel, body, envelope, properties):
    print(" [.] get_url_status(%s)" % body)
    response = get_task()

    await channel.basic_publish(
        payload=str(response),
        exchange_name='',
        routing_key=properties.reply_to,
        properties={
            'correlation_id': properties.correlation_id,
        },
    )

    await channel.basic_client_ack(delivery_tag=envelope.delivery_tag)


async def rpc_server():
    transport, protocol = await aioamqp.connect(host='rabbit',
                                                port=5672,
                                                login='guest',
                                                password='guest')

    channel = await protocol.channel()

    await channel.queue_declare(queue_name='rpc_queue')
    await channel.basic_qos(prefetch_count=1, prefetch_size=0, connection_global=False)
    await channel.basic_consume(on_request, queue_name='rpc_queue')
    print(" [x] Awaiting RPC requests")


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(rpc_server())
event_loop.run_forever()
