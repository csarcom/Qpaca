import kombu


class RabbitMQHandler(object):
    def _create_producer(self):
        return kombu.Producer(self.connection)

    def _create_exchange(self):
        exchange = kombu.Exchange(
            **self.config.get('exchange'))(self.connection)
        exchange.declare()
        return exchange

    def _connect(self):
        connection = kombu.Connection(**self.config.get('connection'))
        connection.ensure_connection()
        return connection

    def _create_queue(self):
        queue = kombu.Queue(
            exchange=self._exchange,
            **self.config.get('queue'))(self.connection)
        queue.declare()
        return queue
