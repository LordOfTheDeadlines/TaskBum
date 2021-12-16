import asyncio
import uuid

import aioamqp
from flask import current_app
from models import PhotoTask

# RABBITMQ_HOST = 'rabbit'
# RABBITMQ_LOGIN = 'guest'
# RABBITMQ_PASSWORD = 'guest'


class TaskBumRpcClient(object):
    def __init__(self):
        self.transport = None
        self.protocol = None
        self.channel = None
        self.callback_queue = None
        self.waiter = asyncio.Event()

    async def connect(self):
        """ an `__init__` method can't be a coroutine"""
        self.transport, self.protocol = await aioamqp.connect(host=current_app.config['RABBITMQ_HOST'],
                                                              port=5672,
                                                              login=current_app.config['RABBITMQ_LOGIN'],
                                                              password=current_app.config['RABBITMQ_PASSWORD'])
        self.channel = await self.protocol.channel()

        result = await self.channel.queue_declare(queue_name='', exclusive=True)
        self.callback_queue = result['queue']

        await self.channel.basic_consume(
            self.on_response,
            no_ack=True,
            queue_name=self.callback_queue,
        )

    async def on_response(self, channel, body, envelope, properties):
        if self.corr_id == properties.correlation_id:
            self.response = body

        self.waiter.set()

    async def call(self):
        if not self.protocol:
            await self.connect()
        self.response = None
        self.corr_id = str(uuid.uuid4())
        await self.channel.basic_publish(
            payload='',
            exchange_name='',
            routing_key='rpc_queue',
            properties={
                'reply_to': self.callback_queue,
                'correlation_id': self.corr_id,
            },
        )
        await self.waiter.wait()

        await self.protocol.close()
        return self.response


async def rpc_client(current_user_id):
    taskbum_rpc = TaskBumRpcClient()
    print(" [x] Requesting get_url_status")
    response = await taskbum_rpc.call()
    print(" [.] Got %r" % response.decode('utf-8'))
    task = PhotoTask(response.decode('utf-8'), current_user_id)
    PhotoTask.create(task)


loop = asyncio.get_event_loop()
