from sqlalchemy import ForeignKey, Integer, String, DECIMAL, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List

from database.base_models import Base
# from api.categories.models import Category
# from api.vacancies.models import Vacancy


class Subcategory(Base):
    __tablename__ = 'subcategories'

    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    category: Mapped["Category"] = relationship(back_populates="subcategories")
    vacancies: Mapped[List["Vacancy"]] = relationship(back_populates="subcategory")

    def __repr__(self):
        return f"<Subcategory {self.name} (Category: {self.category_id})>"



