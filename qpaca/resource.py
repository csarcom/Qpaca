import falcon

from qpaca.helpers import max_body


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.

class ServerResource(object):
    """Implement a default ServerResource.

    Its just a model to how create your own resource
    """

    def _dispatch(self):
        raise NotImplementedError

    def on_post(self):
        raise NotImplementedError


class PublishResource(ServerResource):
    """Simple Publisher Resource.
    It create and start a RabbitMQPublisher and take care of dispatch
    new messages.
    """

    def __init__(self, publisher, *args, **kwargs):
        self.publisher = publisher
        self.publisher.start()

    def _dispatch(self, message):
        return self.publisher.publish(message)

    @falcon.before(max_body(64 * 1024))
    def on_post(self, req, resp):
        """
        Verify if the request has a payload key with the message
        and dispatch it.

        Return the location of a future result
        """

        try:
            message = req.context['payload']
        except KeyError:
            raise falcon.HTTPBadRequest(

                'Missing payload',
                'A payload must be submitted in the request body.')

        message_id = self._dispatch(message)

        resp.status = falcon.HTTP_201
        resp.location = "/result/{0}".format(message_id)
