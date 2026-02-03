from fastapi_pagination import Page
from pydantic import Field
from typing import TypeVar, Sequence

T = TypeVar("T")

class CustomPage(Page[T]):
    items: Sequence[T] = Field(serialization_alias="data")
