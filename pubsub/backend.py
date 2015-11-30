import uuid


class Backend(object):
    def publish(self):
        raise NotImplementedError


class RabbitMQ(Backend):
    def __init__(self, *args, **kwargs):
        pass

    def publish(self, payload):
        print (payload)
        return uuid.uuid4()
