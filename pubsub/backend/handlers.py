import kombu


class RabbitMQHandler(object):
    def _create_producer(self):
        """Create a RabbitMQ producer"""

        return kombu.Producer(self.connection)

    def _create_exchange(self):
        """Create a RabbitMQ exchange"""

        exchange = kombu.Exchange(
            **self.config.get('exchange'))(self.connection)
        exchange.declare()
        return exchange

    def _connect(self):
        """Create a RabbitMQ connection"""

        connection = kombu.Connection(**self.config.get('connection'))
        connection.ensure_connection()
        return connection

    def _create_queue(self):
        """Create a RabbitMQ queue"""

        queue = kombu.Queue(
            exchange=self._exchange,
            **self.config.get('queue'))(self.connection)
        queue.declare()
        return queue
