import mock


from pubsub.backend.rabbitmq import RabbitMQPublisher, RabbitMQSubscriber


class TestRabbitMQPublisher(object):

    @mock.patch('pubsub.backend.rabbitmq.RabbitMQPublisher._connect')
    def setup_class(self, mock1):
        self.publisher = RabbitMQPublisher()

    @mock.patch('pubsub.backend.rabbitmq.RabbitMQPublisher._connect')
    def test_call_connect(self, mocked_function):
        RabbitMQPublisher()
        assert mocked_function.called

    @mock.patch('pubsub.backend.rabbitmq.RabbitMQPublisher._create_exchange')
    def test_call_create_exchange(self, mocked_function):
        self.publisher.start()
        assert mocked_function.called

    @mock.patch('pubsub.backend.rabbitmq.RabbitMQPublisher._create_exchange')
    @mock.patch('pubsub.backend.rabbitmq.RabbitMQPublisher._create_producer')
    def test_call_create_producer(self, mocked_exchange, mocked_producer):
        self.publisher.start()
        assert self.publisher._create_producer.called

    def test_call_producer_publish(self):
        self.publisher.config = {'publish': {}}
        self.publisher._producer = mock.Mock()
        self.publisher.publish(None)
        assert self.publisher._producer.publish.called

    @mock.patch('kombu.Exchange')
    def test_create_exchange(self, mocked_exchange):
        self.publisher.config = {'exchange': {}}
        exchange = self.publisher._create_exchange()
        assert exchange is not None

    @mock.patch('kombu.Connection')
    def test_connect(self, mocked_connection):
        self.publisher.config = {'connection': {}}
        connection = self.publisher._connect()
        assert connection is not None


class TestRabbitMQSubscriber(object):

    @mock.patch('pubsub.backend.rabbitmq.RabbitMQSubscriber._connect')
    def setup_class(self, mock1):
        self.subscriber = RabbitMQSubscriber()

    @mock.patch('pubsub.backend.rabbitmq.RabbitMQSubscriber._connect')
    def test_call_connect(self, mocked_function):
        RabbitMQSubscriber()
        assert mocked_function.called

    @mock.patch('pubsub.backend.rabbitmq.RabbitMQSubscriber._create_exchange')
    @mock.patch('pubsub.backend.rabbitmq.RabbitMQSubscriber._create_queue')
    def test_call_create_queue(self, mocked_exchange, mocked_queue):
        self.subscriber.start()
        assert mocked_queue.called

    @mock.patch('pubsub.backend.rabbitmq.RabbitMQSubscriber._create_exchange')
    @mock.patch('pubsub.backend.rabbitmq.RabbitMQSubscriber._create_queue')
    def test_call_create_exchange(self, mocked_exchange, mocked_queue):
        self.subscriber.start()
        assert mocked_exchange.called

    def test_ack_message_on_message(self):
        message = mock.Mock(ack=mock.Mock(return_value=True))
        self.subscriber.on_message(
            body=None, message=message)
        assert message.ack.called

    def test_return_get_consumers(self):
        self.subscriber.config = {'consumer': {}}
        self.subscriber._queue = mock.Mock()
        self.subscriber.on_message = mock.Mock()
        consumers = self.subscriber.get_consumers(mock.Mock(), mock.Mock())
        assert type(consumers) is list
        assert len(consumers) == 1

    @mock.patch('kombu.Exchange')
    def test_create_exchange(self, mocked_exchange):
        self.subscriber.config = {'exchange': {}}
        exchange = self.subscriber._create_exchange()
        assert exchange is not None

    @mock.patch('kombu.Queue')
    def test_create_queue(self, mocked_queue):
        self.subscriber.config = {'queue': {}}
        connection = self.subscriber._create_queue()
        assert connection is not None

    @mock.patch('kombu.Connection')
    def test_connect(self, mocked_connection):
        self.subscriber.config = {'connection': {}}
        connection = self.subscriber._connect()
        assert connection is not None

    @mock.patch('pubsub.backend.rabbitmq.RabbitMQSubscriber.run')
    def test_call_consumer_run(self, mocked_function):
        self.subscriber.run_forever()
        assert mocked_function.called
