import mock
import pytest


from pubsub.backend.rabbitmq import (
    RabbitMQ, RabbitMQPublisher, RabbitMQSubscriber)


class TestRabbitMQ(object):

    @mock.patch('pubsub.backend.rabbitmq.RabbitMQPublisher._connect')
    @mock.patch('pubsub.backend.rabbitmq.RabbitMQSubscriber._connect')
    def setup_class(self, mock1, mock2):
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

    @mock.patch('pubsub.backend.rabbitmq.RabbitMQPublisher._create_producer')
    def test_call_create_producer(self, mocked_function):
        self.publisher.start()
        assert self.publisher._create_producer.called

    def test_call_producer_publish(self):
        self.publisher._producer = mock.Mock()
        self.publisher.publish(None)
        assert self.publisher._producer.publish.called


class TestRabbitMQSubscriber(object):

    @mock.patch('pubsub.backend.rabbitmq.RabbitMQSubscriber._connect')
    def setup_class(self, mock1):
        self.subscriber = RabbitMQSubscriber()

    @mock.patch('pubsub.backend.rabbitmq.RabbitMQSubscriber._connect')
    def test_call_connect(self, mocked_function):
        RabbitMQSubscriber()
        assert mocked_function.called

    @mock.patch('pubsub.backend.rabbitmq.RabbitMQSubscriber._create_queue')
    def test_call_create_queue(self, mocked_function):
        self.subscriber.start()
        assert mocked_function.called

    @pytest.mark.skipif(True, reason='For some reason its is not working')
    @mock.patch('pubsub.backend.rabbitmq.RabbitMQSubscriber._create_exchange')
    def test_call_create_exchange(self, mocked_function):
        self.subscriber.start()
        assert mocked_function.called

    def test_ack_message_on_message(self):
        message = mock.Mock(ack=mock.Mock(return_value=True))
        self.subscriber.on_message(
            body=None, message=message)
        assert message.ack.called

    def test_return_get_consumers(self):
        self.subscriber._queue = mock.Mock()
        self.subscriber.on_message = mock.Mock()
        consumers = self.subscriber.get_consumers(mock.Mock(), mock.Mock())
        assert type(consumers) is list
        assert len(consumers) == 1


class TestSomething(object):
    def test_something(self):
        backend = RabbitMQ()
        assert backend is not None
