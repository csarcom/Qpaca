class BasePublisher(object):
    def start(self):
        raise NotImplementedError

    def publish(self):
        raise NotImplementedError


class BaseSubscriber(object):
    def start(self):
        raise NotImplementedError

    def on_message(self):
        raise NotImplementedError
