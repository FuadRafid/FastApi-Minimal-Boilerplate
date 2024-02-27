import logging
from datetime import datetime
from http import HTTPStatus

from fastapi.responses import Response

from app.exception.error_response import ErrorResponse


def get_datetime_now():
    return datetime.now()


class ErrorResponseFactory:
    __logger = logging.getLogger(__name__)

    @staticmethod
    def get_error_response(status_code: HTTPStatus, client_message: str) -> Response:
        ErrorResponseFactory.__logger.error("An error occurred", exc_info=True)
        error_response = ErrorResponse(
            timestamp=str(get_datetime_now()),
            error=status_code.phrase,
            message=client_message)
        return Response(error_response.model_dump_json(), media_type="application/json", status_code=status_code.value)
