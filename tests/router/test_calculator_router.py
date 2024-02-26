import asyncio
from asyncio import AbstractEventLoop
from http import HTTPStatus
from unittest import TestCase
from unittest.mock import patch

from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ErrorWrapper, ValidationError

from app.dto.request.calculation_request_dto import CalculationRequestDto
from app.exception.application_exception import ApplicationException
from app.router import calculator_router


def get_mocked_request_validation_error(first_number: int, second_number: int):
    validation_errors = [ErrorWrapper(exc=Exception(), loc=("firstNumber",))]
    raise RequestValidationError(errors=[
        ErrorWrapper(exc=ValidationError(model=CalculationRequestDto, errors=validation_errors),
                     loc=('body',), )], body={'', })


def get_mocked_service_exception(first_number: int, second_number: int):
    raise ApplicationException()


class MockCalculatorService:

    def add_numbers(self, first_number: str, second_number: str) -> str:
        return str(int(first_number) + int(second_number))

    def subtract_numbers(self, first_number: str, second_number: str) -> str:
        return str(int(first_number) - int(second_number))

    def multiply_numbers(self, first_number: str, second_number: str) -> str:
        return str(int(first_number) * int(second_number))

    def divide_numbers(self, first_number: str, second_number: str) -> str:
        return str(int(int(first_number) / int(second_number)))


class TestCalculatorRouter(TestCase):
    __loop: AbstractEventLoop
    __wrong_number_format_message = "Wrong number format, inputs must be integers"

    @classmethod
    def setUpClass(cls):
        cls.__loop = asyncio.new_event_loop()

    @classmethod
    def tearDownClass(cls):
        cls.__loop.close()

    @patch.object(calculator_router, "__calculator_service", MockCalculatorService())
    def test_calculator_message__should_return_correct_output(self):
        response = self.__loop.run_until_complete(calculator_router.calculator_message())
        assert response["text"] == "This is a calculator"

    @patch.object(calculator_router, "__calculator_service", MockCalculatorService())
    def test_add_numbers__given_correct_input__should_return_correct_output(self):
        response = self.__loop.run_until_complete(calculator_router.add_numbers(3, 4))
        assert response.answer == 7

    @patch.object(calculator_router, "__calculator_service", MockCalculatorService())
    def test_subtract_numbers__given_correct_input__should_return_correct_output(self):
        response = self.__loop.run_until_complete(calculator_router.subtract_numbers(10, 4))
        assert response.answer == 6

    @patch.object(calculator_router, "__calculator_service", MockCalculatorService())
    def test_multiply_numbers__given_correct_input__should_return_correct_output(self):
        response = self.__loop.run_until_complete(calculator_router.multiply_numbers(3, 4))
        assert response.answer == 12

    @patch.object(calculator_router, "__calculator_service", MockCalculatorService())
    def test_divide_numbers__given_correct_input__should_return_correct_output(self):
        response = self.__loop.run_until_complete(
            calculator_router.divide_numbers(CalculationRequestDto(first_number=10, second_number=5)))
        assert response.answer == 2

    @patch("app.router.calculator_router.__calculator_service.divide_numbers", get_mocked_request_validation_error)
    def test_calculator_router_when_throws_request_validation_error_should_return_correct_output(self):
        dto = CalculationRequestDto(first_number=10, second_number=2)
        with self.assertRaises(RequestValidationError) as raisedException:
            self.__loop.run_until_complete(calculator_router.divide_numbers(dto))
        assert len(raisedException.exception.errors()) == 1
        assert raisedException.exception.errors()[0].exc.errors() == [
            {'loc': ('firstNumber',), 'msg': '', 'type': 'value_error.exception'}
        ]

    @patch("app.router.calculator_router.__calculator_service.subtract_numbers", get_mocked_service_exception)
    def test_calculator_router_when_throws_service_exception_should_return_correct_output(self):
        with self.assertRaises(ApplicationException) as raisedException:
            self.__loop.run_until_complete(calculator_router.subtract_numbers(3,2))
        assert raisedException.exception.status == HTTPStatus.INTERNAL_SERVER_ERROR
        assert raisedException.exception.message == "Internal Server Error"
