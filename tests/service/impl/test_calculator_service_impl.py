from unittest import TestCase

from app.exception.application_exception import ApplicationException
from app.service.impl.calculator_service_impl import CalculatorServiceImpl


class TestCalculatorServiceImpl(TestCase):
    service: CalculatorServiceImpl = CalculatorServiceImpl()

    def test_add_numbers__given_correct_input__should_return_correct_output(self):
        assert self.service.add_numbers(3, 5) == 8

    def test_add_numbers__given_negative_inputs__should_raise_error(self):
        with self.assertRaises(ApplicationException) as ex:
            self.service.add_numbers(-3, 5)
        assert str(ex.exception) == "Numbers must be positive"

        with self.assertRaises(ApplicationException) as ex:
            self.service.add_numbers(3, -5)
        assert str(ex.exception) == "Numbers must be positive"

        with self.assertRaises(ApplicationException) as ex:
            self.service.add_numbers(-3, -5)
        assert str(ex.exception) == "Numbers must be positive"

    def test_subtract_numbers__given_correct_input__should_return_correct_output(self):
        assert self.service.subtract_numbers(3, 5) == -2

    def test_multiply_numbers__given_correct_input__should_return_correct_output(self):
        assert self.service.multiply_numbers(3, 5) == 15

    def test_divide_numbers__given_correct_input__should_return_correct_output(self):
        assert self.service.divide_numbers(10, 2) == 5

    def test_divide_numbers__given_first_number_smaller__should_raise_error(self):
        with self.assertRaises(ApplicationException) as exception:
            self.service.divide_numbers(3, 5)
        assert str(exception.exception) == "firstNumber must be greater than secondNumber"
