import kombu
import socket
import requests
import json

from pubsub.helpers import logger


class RabbitMQHandler(object):
    def _create_producer(self):
        """Create a RabbitMQ producer"""

        return kombu.Producer(self.connection)

    def _create_exchange(self):
        """Create a RabbitMQ exchange"""

        logger.debug('Creating RabbitMQ Exchange')
        exchange = kombu.Exchange(
            **self.config.get('exchange'))(self.connection)
        exchange.declare()
        return exchange

    def _connect(self):
        """Create a RabbitMQ connection"""

        logger.debug('Connecting with RabbitMQ')

        # TODO: Isolate this requests.get
        #       Look for a better way instead using host ip(if any)
        req = requests.get(
            'http://192.168.99.100:8500/v1/catalog/service/rabbitmq-5672')
        hosts = ['{0}:{1}'.format(i['Address'], i['ServicePort'])
                 for i in json.loads(req.text)]

        # TODO: Make it connect using all hosts, for now we are always
        # using one
        connection = kombu.Connection(
            hostname='amqp://guest:guest@{0}//'.format(hosts[0]),
            **self.config.get('connection'))
        connection.ensure_connection()
        return connection

    def _create_queue(self):
        """Create a RabbitMQ queue"""

        queue_name = socket.gethostname()
        logger.debug('Creating RabbitMQ Queue')
        queue = kombu.Queue(
            exchange=self._exchange, name=queue_name,
            auto_delete=True, **self.config.get('queue'))(self.connection)
        queue.declare()
        return queue
