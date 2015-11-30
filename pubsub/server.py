import falcon

from pubsub.middleware import JSONTranslator, RequireJSON
from pubsub.resource import PublishResource
from pubsub.backend import RabbitMQ


app = falcon.API(middleware=[
    RequireJSON(),
    JSONTranslator(),
])

# Routes
app.add_route('/publish/', PublishResource(backend=RabbitMQ))
