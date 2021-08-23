from pydantic import Field

from app.dto.base_dto import BaseDto


class CalculationRequestDto(BaseDto):
    first_number: int
    second_number: int = Field(gt=0)
