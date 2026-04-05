from pydantic import BaseModel, Field


class CatBaseScheme(BaseModel):
    name: str = Field(max_length=100)
    description: str | None = Field(default=None)


class CategoryScheme(CatBaseScheme):
    pass


class SubcategoryScheme(CatBaseScheme):
    category_id: int = Field(default=1, alias="ID категории")


class SEServicesScheme(BaseModel):
    subcategory_id: int = Field(default=1)
    name: str = Field(max_length=100, alias='Имя услуги')
    description: str = Field(max_length=200, alias='Описание')
    price: float | None = Field(default=None)
    currency: str = Field(max_length=5, default='BYN')
    status: str = Field(max_length=20, default='active')
    views_count: int = Field(default=0)
    location: str = Field(max_length=200)
    experience_years: int | None = Field(default=None, alias='Опыт работы')
    portfolio_url: str | None = Field(max_length=500, default=None, alias='Ссылка на портфолио')
    availability: str | None = Field(max_length=100, default=None, alias='Доступность')
    min_duration_hours: int | None = Field(default=None, alias='Мин-я длительность выполнения')
    max_duration_hours: int | None = Field(default=None, alias='Макс-я длительность выполнения')
    has_guarantee: bool = Field(default=False, alias='Наличие гарантии')