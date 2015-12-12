import falcon
import yaml
import logging
import sys
log_format = '%(asctime)s %(name)s[%(process)d] %(levelname)s: %(message)s'
logging.basicConfig(stream=sys.stdout,
                    level=logging.DEBUG,
                    format=log_format)
logger = logging.getLogger('pubsub')


def max_body(limit):
    """Validate if a request size exceed 'limit'"""

    def hook(req, resp, resource, params):
        length = req.content_length
        if length is not None and length > limit:
            msg = ('The size of the request is too large. The body must not '
                   'exceed ' + str(limit) + ' bytes in length.')

            raise falcon.HTTPRequestEntityTooLarge(
                'Request body is too large', msg)

    return hook


def get_config(backend):
    """Open and read yaml file with all the backend information"""

    with open("pubsub/backend/config.yml") as config:
        return yaml.load(config).get(backend)
