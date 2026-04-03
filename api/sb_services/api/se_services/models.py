from sqlalchemy import ForeignKey, Integer, String, DECIMAL, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from decimal import Decimal

from database.base_models import Base


class SEServices(Base):
    __tablename__ = 'se_services'

    subcategory_id: Mapped[int] = mapped_column(Integer,
                                                ForeignKey('subcategories.id', ondelete='CASCADE'),
                                                nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default='BYN')
    status: Mapped[str] = mapped_column(String(20), default='active')
    views_count: Mapped[int] = mapped_column(Integer, default=0)
    location: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    experience_years: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    portfolio_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    availability: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    min_duration_hours: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    max_duration_hours: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    has_guarantee: Mapped[bool] = mapped_column(Boolean, default=False)

    subcategory: Mapped['Subcategory'] = relationship(back_populates="se_services")

    def __repr__(self):
        return f"<SEService {self.name}>"