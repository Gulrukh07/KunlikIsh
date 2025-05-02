from contextlib import asynccontextmanager

from sqlalchemy import Text, ForeignKey, VARCHAR, BIGINT, String, Enum, DECIMAL, TIMESTAMP, func
from enum import Enum as PyEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.future import select
from db import db
from db.utils import CreatedModel

class GenderType(PyEnum):
    MAN = 'man'
    WOMAN = 'woman'


class User():
    __tablename__ = "users"
    chat_id: Mapped[str] =  mapped_column(VARCHAR, primary_key=True, unique=True)
    tg_first_name : Mapped[str]
    created_at : Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())




class Employee():
    __tablename__ = "employees"
    chat_id :Mapped[str] = mapped_column(VARCHAR, ForeignKey("users.chat_id", ondelete='Cascade'),primary_key=True, unique=True)
    first_name : Mapped[str]
    last_name : Mapped[str]
    phone_number : Mapped[str]
    username : Mapped[str] = mapped_column(VARCHAR, nullable=True)
    gender : Mapped[str] = mapped_column(Enum(GenderType))
    work_type:Mapped[str] = mapped_column(VARCHAR(100))
    work_description:Mapped[str] = mapped_column(Text)

    @classmethod
    async def get_by_chat_id(cls, chat_id):
        query = select(cls).where(cls.chat_id == chat_id)
        objects = await db.execute(query)
        object_ = objects.first()
        if object_:
            return object_[0]
        else:
            return []


class Employer():
    __tablename__ = "employers"
    chat_id :Mapped[str] = mapped_column(VARCHAR, ForeignKey("users.chat_id", ondelete='Cascade'),primary_key=True, unique=True)
    first_name : Mapped[str]
    last_name : Mapped[str]
    phone_number : Mapped[str]
    username : Mapped[str] = mapped_column(VARCHAR, nullable=True)

    @classmethod
    async def get_by_chat_id(cls, chat_id):
        query = select(cls).where(cls.chat_id == chat_id)
        objects = await db.execute(query)
        object_ = objects.first()
        if object_:
            return object_[0]
        else:
            return []

class Category(CreatedModel):
    __tablename__ = 'categories'
    title : Mapped[str]

    @classmethod
    async def get_by_title(cls, title_):
        query = select(cls).where(cls.title == title_)
        objects = await db.execute(query)
        object_ = objects.first()
        if object_:
            return object_[0]
        else:
            return []


class Work(CreatedModel):
    __tablename__ = 'works'
    title : Mapped[str]
    category_id : Mapped[list[Category]] = mapped_column(BIGINT, ForeignKey(Category.id, ondelete='Cascade'))
    description : Mapped[str] = mapped_column(Text)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    photo_id :  Mapped[str] = mapped_column(String, nullable=False)
    worker_gender : Mapped[str] = mapped_column(Enum(GenderType), nullable=True)
    num_of_workers : Mapped[int] = mapped_column(nullable=True)
    price : Mapped[float] = mapped_column(DECIMAL(10,2), nullable=False)
    employee_id : Mapped[str] = mapped_column(VARCHAR, ForeignKey("employees.chat_id", ondelete='Cascade'),nullable=True, unique=True)
    employer_id : Mapped[str] = mapped_column(VARCHAR, ForeignKey("employers.chat_id", ondelete='Cascade'), unique=True)

