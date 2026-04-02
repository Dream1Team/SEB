from datetime import datetime

from sqlalchemy import func, DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
#
#
# try:
#     # from api.sb_services import *
#     # from api.sb_products import *
#     from api.se_services.models import *
#     from api.categories.models import *
#     from api.subcategories.models import *
# except ImportError:
#     pass