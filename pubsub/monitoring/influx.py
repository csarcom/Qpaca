import socket
import datetime

from influxdb import InfluxDBClient

from pubsub.helpers import logger


class InfluxDB(object):
    """Implements a InfluxDB client handler"""

    def __init__(self, name, config, *args, **kwargs):

        logger.debug('Starting InfluxDB client')
        self.client = InfluxDBClient(**config.get('client'))
        self.name = name

    def write(self, data, date=datetime.datetime.now().strftime(
              "%Y-%m-%d %H:%M:%S.%f'")):
        """Write to InfluxDB"""

        host = "{0}-{1}".format(self.name, socket.gethostname())
        json_body = [{
            "measurement": self.name,
            "tags": {
                "host": host,
            },
            "time": date,
            "fields": {
                "value": data
            }}]

        logger.debug('Write on InfluxDB: {0}. value={1}'.format(host, data))
        self.client.write_points(json_body)
