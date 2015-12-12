import uuid

from kombu.mixins import ConsumerMixin

from pubsub.backend.base import BaseSubscriber, BasePublisher
from pubsub.helpers import get_config, logger
from pubsub.backend.handlers import RabbitMQHandler


class RabbitMQPublisher(BasePublisher, RabbitMQHandler):
    """Implements a RabbitMQ Publisher"""

    def __init__(self, config=None):
        self.config = config or get_config('rabbitmq').get('publisher', None)
        self.connection = self._connect()

    def start(self):
        """Create everything necessary to send a message"""

        logger.debug('Starting RabbitMQ Publisher')
        self._exchange = self._create_exchange()
        self._producer = self._create_producer()

    def publish(self, message):
        """
        Send a message to RabbitMQ exchange

        return a unique id for future result query
        """

        message_id = str(uuid.uuid4())
        message = {'payload': message,
                   'message_id': message_id,
                   'reply_to': None}

        self._producer.publish(
            message, exchange=self._exchange, **self.config.get('publish'))
        logger.info('Message sent: {0}'.format(message))
        return message_id


class RabbitMQSubscriber(ConsumerMixin, BaseSubscriber, RabbitMQHandler):
    def __init__(self, config=None):
        self.config = config or get_config('rabbitmq').get('subscriber', None)
        self.connection = self._connect()

    def start(self):
        """Create everything necessary to receive a message"""

        logger.debug('Starting RabbitMQ Subscriber')
        self._exchange = self._create_exchange()
        self._queue = self._create_queue()

    def run_forever(self):
        """Call kombu.ConsumerMixin run function
        It will start consume new messages
        """

        self.run()

    def get_consumers(self, consumer, channel):
        """Return a list with consumers"""

        return [consumer(
            queues=[self._queue],
            callbacks=[self.on_message],
            **self.config.get('consumer'))]

    def on_message(self, body, message):
        """it is called every time a new message is received"""

        logger.info('Message received: {0}'.format(body))
        message.ack()
