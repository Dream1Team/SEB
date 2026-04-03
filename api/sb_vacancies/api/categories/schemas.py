from pydantic import BaseModel, Field


class CatBaseScheme(BaseModel):
    name: str = Field(max_length=100)
    description: str | None = Field(default=None)


class CategoryScheme(CatBaseScheme):
    pass
