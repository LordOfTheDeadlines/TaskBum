import asyncio
from random import randrange

import aioamqp
from app_redis import r
from config import Configuration
from .views import add_task_description

tasks = ['сфоткайте трех уличных котов',
         'эстетика заброшек',
         'ночные посиделки на кухне',
         'фотография-иллюстрация к стихотворению Бродского']


def get_task():
    if r.exists('last_task'):
        print('[x] Use redis')
        task = r.get('last_task').decode('utf-8')
    else:
        print('[x] Use algorithm')
        rnd = randrange(len(tasks))
        task = tasks[rnd]
        r.set('last_task', task, ex=10)
    return task


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
    transport, protocol = await aioamqp.connect(host=Configuration.RABBITMQ_HOST,
                                                port=5672,
                                                login=Configuration.RABBITMQ_LOGIN,
                                                password=Configuration.RABBITMQ_PASSWORD)

    channel = await protocol.channel()

    await channel.queue_declare(queue_name='rpc_queue')
    await channel.basic_qos(prefetch_count=1, prefetch_size=0, connection_global=False)
    await channel.basic_consume(on_request, queue_name='rpc_queue')
    print(" [x] Awaiting RPC requests")


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(rpc_server())
event_loop.run_forever()
