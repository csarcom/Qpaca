"""
It is just a example using HTTP falcon library. You can create and expose
a Publisher API using RPC or anything else. You can also create your own
falcon Resource.

You can run it using:
    gunicorn -b 0.0.0.0:8000 example.publisher:app

If you want to start more publishers using different routing_keys,
you can just create different routes like:

    app.add_route('/publish/routing_key1', PublishResource(backend=RabbitMQPublisher(config1)))
    app.add_route('/publish/routing_key2', PublishResource(backend=RabbitMQPublisher(config2)))
""" # NOQA

import falcon

from qpaca.middleware import JSONTranslator, RequireJSON
from qpaca.resource import PublishResource
from qpaca.backend.rabbitmq import RabbitMQPublisher

app = falcon.API(middleware=[
    RequireJSON(),
    JSONTranslator(),
])

# Routes
app.add_route('/publish/', PublishResource(publisher=RabbitMQPublisher()))
