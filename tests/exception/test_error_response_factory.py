from datetime import datetime
from http import HTTPStatus
from unittest import TestCase
from unittest.mock import patch

from fastapi.responses import Response

from app.exception.error_response_factory import ErrorResponseFactory


class TestErrorResponseFactory(TestCase):
    @patch('app.exception.error_response_factory.ErrorResponseFactory._ErrorResponseFactory__logger')
    @patch('app.exception.error_response_factory.get_datetime_now')
    def test_get_error_response_factory_should_return_correct_response(self, mocked_datetime_now, mocked_logger):
        mocked_datetime_now.return_value = datetime(year=2020, month=6, day=30)
        response: Response = ErrorResponseFactory.get_error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "client_message")
        self.assertTrue(mocked_logger.error.called)
        assert response.status_code == 500
        assert response.body == b'{"timestamp":"2020-06-30 00:00:00","message":"client_message","error":"Internal Server Error"}'
