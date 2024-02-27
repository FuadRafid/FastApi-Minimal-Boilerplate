from abc import ABC

from humps import camelize
from pydantic import BaseModel


class BaseDto(BaseModel, ABC):
    class Config:
        alias_generator = camelize
        populate_by_name = True
