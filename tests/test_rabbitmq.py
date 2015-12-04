import mock


from pubsub.backend.rabbitmq import RabbitMQ, RabbitMQPublisher


class TestRabbitMQ(object):
    def setup_class(self):
        self.backend = RabbitMQ()

    @mock.patch('pubsub.backend.rabbitmq.RabbitMQPublisher.start')
    def test_call_start_publisher(self, mocked_function):
        self.backend.start()
        assert mocked_function.called

    @mock.patch('pubsub.backend.rabbitmq.RabbitMQSubscriber.start')
    def test_call_start_subscriber(self, mocked_function):
        self.backend.start()
        assert mocked_function.called

    @mock.patch('pubsub.backend.rabbitmq.RabbitMQPublisher.publish')
    def test_call_publish(self, mocked_function):
        self.backend.publish(None)
        assert mocked_function.called

    @mock.patch('pubsub.backend.rabbitmq.RabbitMQPublisher.publish')
    def test_publisher_publish_args(self, mocked_function):
        self.backend.publish('message')
        mocked_function.assert_called_with('message')


class TestRabbitMQPublisher(object):
    def setup_class(self):
        self.publisher = RabbitMQPublisher()

    @mock.patch('pubsub.backend.rabbitmq.RabbitMQPublisher._connect')
    def test_call_connect(self, mocked_function):
        RabbitMQPublisher()
        assert mocked_function.called

    @mock.patch('pubsub.backend.rabbitmq.RabbitMQPublisher._create_exchange')
    def test_call_create_exchange(self, mocked_function):
        self.publisher.start()
        assert mocked_function.called

    @mock.patch('pubsub.backend.rabbitmq.RabbitMQPublisher._create_producer')
    def test_call_create_producer(self, mocked_function):
        self.publisher.start()
        assert self.publisher._create_producer.called

    def test_call_producer_publish(self):
        self.publisher._producer = mock.Mock()
        self.publisher.publish(None)
        assert self.publisher._producer.publish.called
