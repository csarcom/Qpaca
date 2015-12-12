import gevent
import sys
sys.path.insert(0, '.')

from pubsub.backend.rabbitmq import RabbitMQSubscriber


if __name__ == '__main__':
    """
    Create and start a Subscriber. Use gevent to spawn a subscriber greenlet,
    You can start more than one subscriber if you wish.
    """

    subscriber = RabbitMQSubscriber()
    subscriber.start()
    g = gevent.spawn(subscriber.run_forever)
    g.join()
