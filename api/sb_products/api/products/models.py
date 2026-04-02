from sqlalchemy import ForeignKey, Integer, String, DECIMAL, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from decimal import Decimal

from database.base_models import Base


class Product(Base):
    """Товары"""
    __tablename__ = 'products'

    subcategory_id: Mapped[int] = mapped_column(Integer,
                                                ForeignKey('subcategories.id', ondelete='CASCADE'),
                                                nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10,2), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default='BYN')
    status: Mapped[str] = mapped_column(String(20), default='active')
    views_count: Mapped[int] = mapped_column(Integer, default=0)
    location: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    brand: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    model: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    condition: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    warranty_months: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    color: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    dimensions: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    weight: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    subcategory: Mapped['Subcategory'] = relationship(back_populates='products')
