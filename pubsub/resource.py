import falcon

from pubsub.helpers import max_body


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.

class ServerResource(object):
    def _dispatch(self):
        raise NotImplementedError

    def on_post(self):
        raise NotImplementedError


class PublishResource(ServerResource):
    def __init__(self, backend, *args, **kwargs):
        self.publisher = backend()
        self.publisher.start()

    def _dispatch(self, message):
        return self.publisher.publish(message)

    @falcon.before(max_body(64 * 1024))
    def on_post(self, req, resp):
        try:
            message = req.context['payload']
        except KeyError:
            raise falcon.HTTPBadRequest(

                'Missing payload',
                'A payload must be submitted in the request body.')

        message_id = self._dispatch(message)

        resp.status = falcon.HTTP_201
        resp.location = "/result/{0}".format(message_id)
