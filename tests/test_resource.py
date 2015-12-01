import mock
import pytest

import falcon

from pubsub.resource import ServerResource, PublishResource


class TestServerResource(object):
    def setup_class(self):
        self.resource = ServerResource()

    def test_on_post(self):
        with pytest.raises(NotImplementedError):
            self.resource.on_post()

    def test_dispatch(self):
        with pytest.raises(NotImplementedError):
            self.resource._dispatch()


class TestPublishResource(object):
    def setup_class(self):
        self.resource = PublishResource(backend=mock.Mock())

    def test_on_post_req_key_error(self):
        with pytest.raises(falcon.errors.HTTPBadRequest):
            self.resource.on_post(req=mock.Mock(
                content_length=1, context={'mock': 'mock'}), resp=mock.Mock())

    def test_on_post_success(self):
        response = mock.Mock()
        self.resource.on_post(req=mock.Mock(
            content_length=1, context={'payload': 'mock'}), resp=response)

        assert response.status == '201 Created'
        assert "/result/" in response.location
