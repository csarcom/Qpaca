from gevent import monkey
monkey.patch_all()

import uuid

import kombu
import gevent

from kombu.mixins import ConsumerMixin

from pubsub.backend.base import BaseBackend


class RabbitMQ(BaseBackend):
    def __init__(self, *args, **kwargs):
        self.publisher = RabbitMQPublisher()
        self.subscriber = RabbitMQSubscriber()

    def start(self):
        self.publisher.start()
        self.subscriber.start()
        gevent.spawn(self.subscriber.run_forever)

    def publish(self, message):
        return self.publisher.publish(message)


class RabbitMQPublisher(object):
    def __init__(self, *args, **kwargs):
        self.exchange_name = 'python-pubsub'
        self.amqp_address = 'amqp://guest:guest@my_rabbitmq:5672//'
        self.routing_key = 'pubsub'
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
            message, exchange=self._exchange, routing_key=self.routing_key,
            serializer='json', compression='zlib', retry=True)
        print ('Message sent')
        return message_id

    def _create_producer(self):
        return kombu.Producer(self._connection)

    def _create_exchange(self):
        exchange = kombu.Exchange(
            self.exchange_name,
            type='direct',
            durable=True, auto_delete=False)(self._connection)
        exchange.declare()
        return exchange

    def _connect(self):
        connection = kombu.Connection(
            self.amqp_address,
            transport_options={'confirm_publish': True},
            failover_strategy='round-robin')
        connection.ensure_connection()
        return connection


class RabbitMQSubscriber(ConsumerMixin):
    def __init__(self, *args, **kwargs):
        self.exchange_name = 'python-pubsub'
        self.amqp_address = 'amqp://guest:guest@my_rabbitmq:5672//'
        self.routing_key = 'pubsub'
        self.queue_name = 'store'
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
            accept={'application/json'},)]

    def _connect(self):
        connection = kombu.Connection(self.amqp_address,
                                      failover_strategy='round-robin')
        connection.ensure_connection()
        return connection

    def _create_exchange(self):
        exchange = kombu.Exchange(
            self.exchange_name,
            type='direct',
            durable=True, auto_delete=False)(self.connection)
        exchange.declare()
        return exchange

    def _create_queue(self):
        queue = kombu.Queue(
            self.queue_name, self._exchange,
            routing_key=self.routing_key, auto_delete=True)(self.connection)
        queue.declare()
        return queue

    def on_message(self, body, message):
        print ('Got message: {0}'.format(body))
        message.ack()
