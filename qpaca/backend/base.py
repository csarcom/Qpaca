class BasePublisher(object):
    """Implement a base publisher"""

    def start(self):
        """Handle all backend dependencies"""

        raise NotImplementedError

    def publish(self):
        """Take care of delivery a message to the backend"""

        raise NotImplementedError


class BaseSubscriber(object):
    """Implement a base publisher"""

    def start(self):
        """Handle all backend dependencies"""

        raise NotImplementedError

    def on_message(self):
        """Handle received messages"""

        raise NotImplementedError
