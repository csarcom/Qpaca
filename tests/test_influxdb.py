import socket
import datetime

import mock

from pubsub.monitoring.influx import InfluxDB


class TestInfluxDB(object):

    @mock.patch('pubsub.monitoring.influx.InfluxDBClient')
    def test_init(self, mocked_class):
        client = InfluxDB(name='something', config={'client': {}})
        assert mocked_class.called
        assert client.name == 'something'

    @mock.patch('pubsub.monitoring.influx.InfluxDB.write')
    def test_write_parameters(self, mocked_function):
        client = InfluxDB(name='something', config={'client': {}})
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f'")
        client.write((date, 1))
        mocked_function.assert_called_with((date, 1))

    @mock.patch('pubsub.monitoring.influx.InfluxDBClient.write_points')
    def test_write_influx(self, mocked_function):
        client = InfluxDB(name='something', config={'client': {}})
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f'")
        client.write(point=(date, 1))
        mocked_function.assert_called_with(
            [{
                "measurement": 'something',
                "tags": {
                    "host": 'something-' + socket.gethostname(),
                },
                "time": date,
                "fields": {
                    "value": 1}}])
