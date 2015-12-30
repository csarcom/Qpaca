import socket

from influxdb import InfluxDBClient

from pubsub.helpers import logger


class InfluxDB(object):
    """Implements a InfluxDB client handler"""

    def __init__(self, name, config, *args, **kwargs):

        logger.debug('Starting InfluxDB client')
        self.client = InfluxDBClient(**config.get('client'))
        self.name = name

    def write(self, point):
        """Write to InfluxDB
        point is a tuple that contain (DATE, VALUE)
        """

        host = "{0}-{1}".format(self.name, socket.gethostname())
        json_body = [{
            "measurement": self.name,
            "tags": {
                "host": host,
            },
            "time": point[0],
            "fields": {
                "value": point[1]
            }}]

        logger.debug('Write on InfluxDB: {0}. point: {1}'.format(
            host, point))
        self.client.write_points(json_body)
