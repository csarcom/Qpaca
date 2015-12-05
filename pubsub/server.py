import time

import falcon

from pubsub.middleware import JSONTranslator, RequireJSON
from pubsub.resource import PublishResource
from pubsub.backend.rabbitmq import RabbitMQ

time.sleep(5)
app = falcon.API(middleware=[
    RequireJSON(),
    JSONTranslator(),
])

# Routes

app.add_route('/publish/', PublishResource(backend=RabbitMQ))
