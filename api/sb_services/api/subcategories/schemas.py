from pydantic import BaseModel, Field
from typing import Optional

from api.categories.schemas import CatBaseScheme


class SubcategoryScheme(CatBaseScheme):
    category_id: int = Field(default=1, alias="ID категории")
