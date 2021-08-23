import logging

from app.exception.application_exception import ApplicationException
from app.service.calculator_service import CalculatorService


class CalculatorServiceImpl(CalculatorService):
    __logger = logging.getLogger(__name__)

    def add_numbers(self, first_number: int, second_number: int) -> int:
        if first_number < 0 or second_number < 0:
            raise ApplicationException("Numbers must be positive")
        self.__create_log(first_number, second_number, "add")
        answer: int = first_number + second_number
        return answer

    def subtract_numbers(self, first_number: int, second_number: int) -> int:
        self.__create_log(first_number, second_number, "subtract")
        answer: int = first_number - second_number
        return answer

    def multiply_numbers(self, first_number: int, second_number: int) -> int:
        self.__create_log(first_number, second_number, "multiply")
        answer: int = first_number * second_number
        return answer

    def divide_numbers(self, first_number: int, second_number: int) -> int:
        if first_number < second_number:
            raise ApplicationException("firstNumber must be greater than secondNumber")
        self.__create_log(first_number, second_number, "divide")
        answer: int = int(first_number / second_number)
        return answer

    def __create_log(self, first_number: int, second_number: int, operation: str):
        self.__logger.debug(
            "Doing operation: " + operation + ". " + "First number is: " + str(first_number) + ", " + "Second number "
                                                                                                      "is: " + str(
                second_number))
