import gevent
import sys
sys.path.insert(0, '.')

from pubsub.backend.rabbitmq import RabbitMQSubscriber


if __name__ == '__main__':
    subscriber = RabbitMQSubscriber()
    subscriber.start()
    g = gevent.spawn(subscriber.run_forever)
    g.join()
