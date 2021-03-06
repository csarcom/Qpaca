import gevent
import sys
sys.path.insert(0, '.')

from qpaca.backend.rabbitmq import RabbitMQSubscriber


def custom_callback(body, message):
    """
    Do something with received messages
    """
    pass


if __name__ == '__main__':
    """
    Create and start a Subscriber. Use gevent to spawn a subscriber greenlet,
    You can start more than one subscriber if you wish.
    """

    subscriber = RabbitMQSubscriber()
    subscriber.start(callback=custom_callback)
    g = gevent.spawn(subscriber.run_forever)
    g.join()
