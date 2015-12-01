class BaseBackend(object):
    def start(self):
        raise NotImplementedError

    def publish(self):
        raise NotImplementedError
