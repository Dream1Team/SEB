from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal


class VacancyScheme(BaseModel):
    """Базовая схема вакансии"""
    subcategory_id: int = Field(..., description="ID подкатегории")
    title: str = Field(..., min_length=1, max_length=200, description="Название вакансии")
    description: str = Field(..., min_length=1, description="Описание вакансии")
    employment_type: Optional[str] = Field(None, max_length=50, description="Тип занятости")
    experience_required: Optional[str] = Field(None, max_length=50, description="Требуемый опыт")
    schedule: Optional[str] = Field(None, max_length=100, description="График работы")
    salary_from: Optional[Decimal] = Field(None, ge=0, description="Зарплата от")
    salary_to: Optional[Decimal] = Field(None, ge=0, description="Зарплата до")
    salary_period: Optional[str] = Field(None, max_length=20, description="Период зарплаты")
    company_name: Optional[str] = Field(None, max_length=200, description="Название компании")
    requirements: Optional[str] = Field(None, description="Требования")
    responsibilities: Optional[str] = Field(None, description="Обязанности")
    benefits: Optional[str] = Field(None, description="Условия и бонусы")
    views_count: Optional[str] = Field(None, max_length=200, description="Количество просмотров")


class VacanciesQuery(BaseModel):
    subcategories: List[str] | None = Field(default=None, alias='Подкатегории')
    min_salary: int | None = Field(default=None, gt=0, alias='Минимальная зарплата')
    location: str | None = Field(default=None, alias='Локация')