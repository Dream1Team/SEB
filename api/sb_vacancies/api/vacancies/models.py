from sqlalchemy import ForeignKey, Integer, String, DECIMAL, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List

from database.base_models import Base
# from api.subcategories.models import Subcategory


class Vacancy(Base):
    __tablename__ = 'vacancies'

    subcategory_id: Mapped[int] = mapped_column(Integer, ForeignKey('subcategories.id', ondelete='CASCADE'), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    employment_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    experience_required: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    schedule: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    salary_from: Mapped[Optional[float]] = mapped_column(DECIMAL(10, 2), nullable=True)
    salary_to: Mapped[Optional[float]] = mapped_column(DECIMAL(10, 2), nullable=True)
    salary_period: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    company_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    requirements: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    responsibilities: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    benefits: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    views_count: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    subcategory: Mapped["Subcategory"] = relationship(back_populates="vacancies")

    def __repr__(self):
        return f"<Vacancy: {self.title}>"
