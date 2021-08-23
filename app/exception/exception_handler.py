from fastapi import FastAPI
from fastapi.requests import Request

from app.exception.error_response_factory import ErrorResponseFactory
from app.exception.application_exception import ApplicationException


class ExceptionHandler:


    @staticmethod
    async def __application_exception_handler(request: Request, exception: ApplicationException):
        return ErrorResponseFactory.get_error_response(exception.status, exception.message)


    @classmethod
    def initiate_exception_handlers(cls, app: FastAPI):
        app.add_exception_handler(exc_class_or_status_code=ApplicationException,
                                  handler=cls.__application_exception_handler)

