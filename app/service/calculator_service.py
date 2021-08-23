from abc import ABC


class CalculatorService(ABC):

    def add_numbers(self, first_number: int, second_number: int) -> int:
        raise NotImplementedError()

    def subtract_numbers(self, first_number: int, second_number: int) -> int:
        raise NotImplementedError()

    def multiply_numbers(self, first_number: int, second_number: int) -> int:
        raise NotImplementedError()

    def divide_numbers(self, first_number: int, second_number: int) -> int:
        raise NotImplementedError()
