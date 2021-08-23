from abc import ABC

from humps import camelize
from pydantic import BaseModel


class BaseDto(BaseModel, ABC):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True
