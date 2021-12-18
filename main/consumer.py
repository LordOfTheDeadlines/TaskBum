import asyncio
from random import randrange
import aioamqp

from app import app
from modules.database import db
from modules.app_redis import r
db.app = app
from config.config import Configuration
from views import add_task_description

tasks = ['сфоткайте трех уличных котов',
         'эстетика заброшек',
         'ночные посиделки на кухне',
         'фотография-иллюстрация к стихотворению Бродского']


async def callback(channel, body, envelope, properties):
    try:
        task = r.get('last_task').decode('utf-8')
        print('[x] Use redis')
    except:
        print('[x] Use algorithm')
        rnd = randrange(len(tasks))
        task = tasks[rnd]
        r.set('last_task', task, ex=10)
    finally:
        print('[x] Callback end')
        add_task_description(task, body)


async def receive():
    transport, protocol = await aioamqp.connect(host=Configuration.RABBITMQ_HOST,
                                                port=int(Configuration.RABBITMQ_PORT),
                                                login=Configuration.RABBITMQ_LOGIN,
                                                password=Configuration.RABBITMQ_PASSWORD)
    channel = await protocol.channel()

    await channel.queue_declare(queue_name='hello')

    await channel.basic_consume(callback, queue_name='hello')


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(receive())
event_loop.run_forever()

