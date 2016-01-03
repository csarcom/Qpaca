import mock
import pytest

import falcon

from qpaca.middleware import JSONTranslator, RequireJSON


class TestJSONTranslator(object):
    def setup_class(self):
        self.middleware = JSONTranslator()

    def test_request_content_lenght_none(self):
        result = self.middleware.process_request(
            req=mock.Mock(content_length=None), resp=mock.Mock())
        assert result is None

    def test_request_no_body(self):
        with pytest.raises(falcon.HTTPBadRequest):
            # TODO: Search for a better way to mock this
            self.middleware.process_request(
                req=mock.Mock(stream=mock.Mock(
                    read=mock.Mock(return_value=None))),
                resp=mock.Mock())

    def test_response_no_result(self):
        result = self.middleware.process_response(
            req=mock.Mock(context={}), resp=mock.Mock(), resource=mock.Mock())
        assert result is None

    def test_response_success(self):
        resp = mock.Mock()
        self.middleware.process_response(
            req=mock.Mock(context={'result': 'mocked_resp'}), resp=resp,
            resource=mock.Mock())

        assert resp.body == '"mocked_resp"'


class TestRequireJSON(object):
    def setup_class(self):
        self.middleware = RequireJSON()

    def test_client_accepts_json(self):
        with pytest.raises(falcon.HTTPNotAcceptable):
            self.middleware.process_request(
                req=mock.Mock(client_accepts_json=False), resp=mock.Mock)

    def test_support_json_only(self):
        with pytest.raises(falcon.HTTPUnsupportedMediaType):
            self.middleware.process_request(
                req=mock.Mock(method='POST', content_type='application/xml'),
                resp=mock.Mock)
