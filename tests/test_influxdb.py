import socket
import datetime

import mock

from pubsub.monitoring.influxdb import InfluxDB


class TestInfluxDB(object):

    @mock.patch('pubsub.monitoring.influxdb.InfluxDBClient')
    def test_init(self, mocked_class):
        client = InfluxDB(name='something', config={'client': {}})
        assert mocked_class.called
        assert client.name == 'something'

    @mock.patch('pubsub.monitoring.influxdb.InfluxDB.write')
    def test_write_parameters(self, mocked_function):
        client = InfluxDB(name='something', config={'client': {}})
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f'")
        client.write(1, date)
        mocked_function.assert_called_with(1, date)

    @mock.patch('pubsub.monitoring.influxdb.InfluxDBClient.write_points')
    def test_write_influx(self, mocked_function):
        client = InfluxDB(name='something', config={'client': {}})
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f'")
        client.write(1, date)
        mocked_function.assert_called_with(
            [{
                "measurement": 'something',
                "tags": {
                    "host": 'something-' + socket.gethostname(),
                },
                "time": date,
                "fields": {
                    "value": 1}}])
