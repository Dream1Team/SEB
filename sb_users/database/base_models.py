from datetime import datetime

from sqlalchemy import func, ForeignKey, String, DateTime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class UserModel(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(unique=True, index=True, nullable=True)
    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=True)
    password: Mapped[str] = mapped_column(nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    google_id: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String, nullable=True)
    phone: Mapped[str] = mapped_column(nullable=True)
    birthday: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    last_login: Mapped[datetime] = mapped_column(server_default=func.now())

    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_premium: Mapped[bool] = mapped_column(default=False)

    se_profile: Mapped['SEProfileModel'] = relationship(back_populates='users')
    employer: Mapped['EmployerProfile'] = relationship(back_populates='users')
    vacancy_searcher: Mapped['VacancySearcherModel'] = relationship(back_populates='users')
    seller: Mapped['SellerModel'] = relationship(back_populates='users')


class SEProfileModel(Base):
    __tablename__ = 'self_employed_data'

    se_number: Mapped[str] = mapped_column()
    user: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

    users: Mapped['UserModel'] = relationship(back_populates='se_profile')


class EmployerProfile(Base):
    __tablename__ = 'employer_data'

    company_name: Mapped[str] = mapped_column()
    # vacancies
    user: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

    users: Mapped['UserModel'] = relationship(back_populates='employer')


class VacancySearcherModel(Base):
    __tablename__ = 'vacancy_searcher_data'

    # portfolio:
    # resume:
    needed_salary: Mapped[int] = mapped_column()
    salary_currency: Mapped[str] = mapped_column()
    user: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

    users: Mapped['UserModel'] = relationship(back_populates='vacancy_searcher')


class SellerModel(Base):
    __tablename__ = 'seller_data'

    country: Mapped[str] = mapped_column()
    city: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column()
    user: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

    users: Mapped['UserModel'] = relationship(back_populates='seller')

