from app.dto.base_dto import BaseDto


class ErrorResponse(BaseDto):
    timestamp: str
    message: str
    error: str
