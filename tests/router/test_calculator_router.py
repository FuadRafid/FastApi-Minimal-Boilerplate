import asyncio
from asyncio import AbstractEventLoop
from http import HTTPStatus
from unittest import TestCase
from unittest.mock import patch

from pydantic import ValidationError
from pydantic_core import InitErrorDetails

from app.dto.request.calculation_request_dto import CalculationRequestDto
from app.exception.application_exception import ApplicationException
from app.router import calculator_router


def get_mocked_request_validation_error(first_number: int, second_number: int):
    error: InitErrorDetails = {
        'type': 'greater_than',
        'loc': ("secondNumber",),
        'input': -1,
        'ctx': {'gt': 0},
    }
    raise ValidationError.from_exception_data(CalculationRequestDto.__name__, [error])


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
        with self.assertRaises(ValidationError) as raisedException:
            self.__loop.run_until_complete(calculator_router.divide_numbers(dto))
        assert len(raisedException.exception.errors()) == 1
        assert raisedException.exception.errors() == [
            {'ctx': {'gt': 0}, 'input': -1, 'loc': ('secondNumber',), 'msg': 'Input should be greater than 0',
             'type': 'greater_than', 'url': 'https://errors.pydantic.dev/2.6/v/greater_than'}]

    @patch("app.router.calculator_router.__calculator_service.subtract_numbers", get_mocked_service_exception)
    def test_calculator_router_when_throws_service_exception_should_return_correct_output(self):
        with self.assertRaises(ApplicationException) as raisedException:
            self.__loop.run_until_complete(calculator_router.subtract_numbers(3, 2))
        assert raisedException.exception.status == HTTPStatus.INTERNAL_SERVER_ERROR
        assert raisedException.exception.message == "Internal Server Error"
