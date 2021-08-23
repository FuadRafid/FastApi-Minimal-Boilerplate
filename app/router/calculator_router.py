from fastapi import APIRouter
from fastapi.params import Path, Query

from app.dto.request.calculation_request_dto import CalculationRequestDto
from app.dto.response.calculation_response_dto import CalculationResponseDto
from app.service.calculator_service import CalculatorService
from app.service.impl.calculator_service_impl import CalculatorServiceImpl

router = APIRouter()
prefix = "/calculator"
__calculator_service: CalculatorService = CalculatorServiceImpl()


@router.get("/")
async def calculator_message() -> dict:
    return {"text": "This is a calculator"}


@router.get(path="/add/{firstNumber}/{secondNumber}", response_model=CalculationResponseDto)
async def add_numbers(first_number: int = Path(..., alias='firstNumber'),
                      second_number: int = Path(..., alias='secondNumber')) -> CalculationResponseDto:
    result: int = __calculator_service.add_numbers(first_number, second_number)
    return CalculationResponseDto(answer=result)


@router.post(path="/divide", response_model=CalculationResponseDto)
async def divide_numbers(calculation_request: CalculationRequestDto) -> CalculationResponseDto:
    result: int = __calculator_service.divide_numbers(calculation_request.first_number,
                                                      calculation_request.second_number)
    return CalculationResponseDto(answer=result)


@router.get(path="/subtract", response_model=CalculationResponseDto)
async def subtract_numbers(first_number: int = Query(..., alias='firstNumber'),
                           second_number: int = Query(..., alias='secondNumber')) -> CalculationResponseDto:
    result: int = __calculator_service.subtract_numbers(first_number, second_number)
    return CalculationResponseDto(answer=result)


@router.post(path="/multiply", response_model=CalculationResponseDto)
async def multiply_numbers(first_number: int = Query(..., alias='firstNumber'),
                           second_number: int = Query(..., alias='secondNumber')) -> CalculationResponseDto:
    result: int = __calculator_service.multiply_numbers(first_number, second_number)
    return CalculationResponseDto(answer=result)
