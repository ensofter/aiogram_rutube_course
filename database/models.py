from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, DateTime, func


class Base(DeclarativeBase):
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(length=150), nullable=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    gender: Mapped[int] = mapped_column(Integer, nullable=True)
    photo: Mapped[str] = mapped_column(String(150), nullable=True)
    education: Mapped[int] = mapped_column(String(150), nullable=True)
    wish_news: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_hold: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
