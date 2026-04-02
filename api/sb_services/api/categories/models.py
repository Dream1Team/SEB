from sqlalchemy import ForeignKey, String, Text, DateTime, Boolean, DECIMAL, Integer, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from datetime import datetime

from database.base_models import Base


class Category(Base):
    __tablename__ = 'categories'

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(100), nullable=False, unique=False)

    subcategories: Mapped[List["Subcategory"]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    def __repr__(self):
        return f"<Category {self.name}>"

#
# class Image(Base):
#     """Изображения для объявлений"""
#     __tablename__ = 'images'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     listing_id: Mapped[int] = mapped_column(
#         Integer,
#         ForeignKey('listings.id', ondelete='CASCADE'),
#         nullable=False
#     )
#     url: Mapped[str] = mapped_column(String(500), nullable=False)
#     thumbnail_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
#     alt_text: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
#     order_index: Mapped[int] = mapped_column(Integer, default=0)
#     is_main: Mapped[bool] = mapped_column(Boolean, default=False)
#     created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
#
#     # Связи
#     listing: Mapped["Listing"] = relationship(back_populates="images")
#
#     def __repr__(self):
#         return f'<Image {self.id}>'