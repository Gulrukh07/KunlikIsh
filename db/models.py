from sqlalchemy import Text, ForeignKey, VARCHAR, BIGINT, Enum, DECIMAL, Integer
from enum import Enum as PyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload
from sqlalchemy.future import select
from db import db, Base
from db.utils import CreatedModel


class GenderType(PyEnum):
    MAN = 'man'
    WOMAN = 'woman'


class User(CreatedModel):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, unique=True)
    tg_first_name: Mapped[str]


class Employee(CreatedModel):
    chat_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.id", ondelete='Cascade'), unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone_number: Mapped[str]
    username: Mapped[str] = mapped_column(VARCHAR, nullable=True)
    gender: Mapped[str] = mapped_column(Enum(GenderType))
    work_type: Mapped[str] = mapped_column(VARCHAR(100))
    work_description: Mapped[str] = mapped_column(Text)

    @classmethod
    async def get_by_chat_id(cls, chat_id):
        query = select(cls).where(cls.chat_id == chat_id)
        objects = await db.execute(query)
        object_ = objects.first()
        if object_:
            return object_[0]
        else:
            return []


class Employer(CreatedModel):
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone_number: Mapped[str]
    username: Mapped[str] = mapped_column(VARCHAR, nullable=True)
    chat_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.id", ondelete='Cascade'), unique=True)

    works : Mapped[list["Work"]] = relationship("Work", back_populates="employer", cascade="all, delete-orphan")

    @classmethod
    async def get_by_chat_id(cls, chat_id):
        query = (select(cls).
                 options(selectinload(cls.works)).
                 where(cls.chat_id == chat_id))
        objects = await db.execute(query)
        object_ = objects.first()
        if object_:
            return object_[0]
        else:
            return []


class Category(CreatedModel):
    __tablename__ = "categories"
    title: Mapped[str]

    @classmethod
    async def get_by_title(cls, title_):
        query = select(cls).where(cls.title == title_)
        objects = await db.execute(query)
        object_ = objects.first()
        if object_:
            return object_[0]
        else:
            return []


class Photo(CreatedModel):
    photo_id: Mapped[str]
    work_id: Mapped[int] = mapped_column(ForeignKey("works.id", ondelete="CASCADE"), nullable=True)
    work: Mapped["Work"] = relationship("Work", back_populates="photos")

    @classmethod
    async def get_by_photo_id(cls, photo_id):
        query = select(cls).where(cls.photo_id == photo_id)
        objects = await db.execute(query)
        object_ = objects.first()
        if object_:
            return object_[0]
        else:
            return []

class Work(CreatedModel):
    title: Mapped[str]
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id", ondelete='Cascade'), unique=True)
    description: Mapped[str] = mapped_column(Text)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    worker_gender: Mapped[str] = mapped_column(Enum(GenderType), nullable=True)
    num_of_workers: Mapped[int] = mapped_column(nullable=True)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(15,2), nullable=False)
    employee_id: Mapped[int] = mapped_column(Integer, ForeignKey("employees.id", ondelete='Cascade'), nullable=True)
    employer_id: Mapped[int] = mapped_column(Integer, ForeignKey("employers.id", ondelete='Cascade'))

    photos: Mapped[list["Photo"]] = relationship("Photo", back_populates="work", cascade="all, delete-orphan")
    employer :Mapped["Employer"] = relationship("Employer", back_populates="works")



metadata = Base.metadata
