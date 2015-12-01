import uuid

import kombu

from pubsub.backend.base import BaseBackend


class RabbitMQ(BaseBackend):
    def __init__(self, *args, **kwargs):
        self.publisher = RabbitMQPublisher()
        self.subscriber = RabbitMQSubscriber()

    def start(self):
        self.publisher.start()
        self.subscriber.start()

    def publish(self, message):
        return self.publisher.publish(message)


class RabbitMQPublisher(object):
    def __init__(self, *args, **kwargs):
        self.exchange_name = 'python-pubsub'
        self.amqp_address = 'amqp://guest:guest@my_rabbitmq:5672//'
        self.routing_key = 'pubsub'

    def start(self):
        self._connection = self._connect()
        self._exchange = self._create_exchange()
        self._producer = self._create_producer()

    def publish(self, message):
        message_id = str(uuid.uuid4())
        message = {'payload': message,
                   'uuid': message_id}

        self._producer.publish(
            message, exchange=self._exchange, routing_key=self.routing_key,
            serializer='json', compression='zlib', retry=True)
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
        return connection.ensure_connection()


class RabbitMQSubscriber(object):
    def __init__(self, *args, **kwargs):
        pass

    def start(self):
        pass
