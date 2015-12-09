from gevent import monkey
monkey.patch_all()

import uuid

import kombu

from kombu.mixins import ConsumerMixin

from pubsub.backend.base import BaseSubscriber, BasePublisher
from pubsub.helpers import get_config


class RabbitMQPublisher(BasePublisher):
    def __init__(self):
        self.config = get_config('rabbitmq').get('publisher', None)
        self._connection = self._connect()

    def start(self):
        self._exchange = self._create_exchange()
        self._producer = self._create_producer()

    def publish(self, message):
        message_id = str(uuid.uuid4())
        message = {'payload': message,
                   'message_id': message_id,
                   'reply_to': None}

        self._producer.publish(
            message, exchange=self._exchange, **self.config.get('publish'))
        return message_id

    def _create_producer(self):
        return kombu.Producer(self._connection)

    def _create_exchange(self):
        exchange = kombu.Exchange(
            **self.config.get('exchange'))(self._connection)
        exchange.declare()
        return exchange

    def _connect(self):
        connection = kombu.Connection(**self.config.get('connection'))
        connection.ensure_connection()
        return connection


class RabbitMQSubscriber(ConsumerMixin, BaseSubscriber):
    def __init__(self):
        self.config = get_config('rabbitmq').get('subscriber', None)
        self.connection = self._connect()

    def start(self):
        self._exchange = self._create_exchange()
        self._queue = self._create_queue()

    def run_forever(self):
        self.run()

    def get_consumers(self, consumer, channel):
        return [consumer(
            queues=[self._queue],
            callbacks=[self.on_message],
            **self.config.get('consumer'))]

    def _connect(self):
        connection = kombu.Connection(**self.config.get('connection'))
        connection.ensure_connection()
        return connection

    def _create_exchange(self):
        exchange = kombu.Exchange(
            **self.config.get('exchange'))(self.connection)
        exchange.declare()
        return exchange

    def _create_queue(self):
        queue = kombu.Queue(
            exchange=self._exchange,
            **self.config.get('queue'))(self.connection)
        queue.declare()
        return queue

    def on_message(self, body, message):
        message.ack()
