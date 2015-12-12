from gevent import monkey
monkey.patch_all()

import uuid

from kombu.mixins import ConsumerMixin

from pubsub.backend.base import BaseSubscriber, BasePublisher
from pubsub.helpers import get_config
from pubsub.backend.handlers import RabbitMQHandler


class RabbitMQPublisher(BasePublisher, RabbitMQHandler):
    def __init__(self, config=None):
        self.config = config or get_config('rabbitmq').get('publisher', None)
        self.connection = self._connect()

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


class RabbitMQSubscriber(ConsumerMixin, BaseSubscriber, RabbitMQHandler):
    def __init__(self, config=None):
        self.config = config or get_config('rabbitmq').get('subscriber', None)
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

    def on_message(self, body, message):
        message.ack()
