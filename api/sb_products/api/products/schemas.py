from pydantic import BaseModel, Field
from typing import List
from decimal import Decimal


class ProductScheme(BaseModel):
    subcategory_id: int = Field(default=1)
    name: str = Field(max_length=100, alias='Имя товара')
    description: str = Field(max_length=200, alias='Описание')
    price: float | None = Field(default=None)
    currency: str = Field(max_length=5, default='BYN')
    status: str = Field(max_length=20, default='active')
    views_count: int = Field(default=0)
    location: str = Field(max_length=200)
    brand: str | None = Field(max_length=100, default=None, alias='Бренд')
    model: str | None = Field(max_length=100, default=None, alias='Модель')
    condition: str | None = Field(max_length=50, default=None, alias='Состояние')
    quantity: int | None = Field(default=1, alias='Количество')
    warranty_months: int | None = Field(default=None, alias='Срок гарантии')
    color: str | None = Field(max_length=50, default=None, alias='Цвет')
    dimensions: str | None = Field(max_length=100, default=None, alias='Размеры')
    weight: str | None = Field(max_length=50, default=None, alias='Вес')


class ProductsQuery(BaseModel):
    subcategories: List[str] | None = Field(default=None, alias='Подкатегории')
    brands: List[str] | None = Field(default=None, alias='Бренды')
    min_price: int | None = Field(default=None, gt=0, alias='Минимальная цена')
    max_price: int | None = Field(default=None, gt=0, alias='Максимальная цена')
    color: str | None = Field(default=None, alias='Цвет')