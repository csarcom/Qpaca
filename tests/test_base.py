import pytest

from pubsub.backend.base import BasePublisher, BaseSubscriber


class TestBasePublisher(object):
    def setup_class(self):
        self.publisher = BasePublisher()

    def test_base_publisher_start(self):
        with pytest.raises(NotImplementedError):
            self.publisher.start()

    def test_base_publisher_publish(self):
        with pytest.raises(NotImplementedError):
            self.publisher.publish()


class TestBaseSubscriber(object):
    def setup_class(self):
        self.subscriber = BaseSubscriber()

    def test_base_subscriber_start(self):
        with pytest.raises(NotImplementedError):
            self.subscriber.start()

    def test_base_subscriber_on_message(self):
        with pytest.raises(NotImplementedError):
            self.subscriber.on_message()
