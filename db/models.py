from enum import Enum as PyEnum

from sqlalchemy import Text, ForeignKey, VARCHAR, BIGINT, Enum, DECIMAL, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.utils import TimeBasedModel, Base


class GenderType(PyEnum):
    MAN = 'man'
    WOMAN = 'woman'


class WorkStatus(PyEnum):
    Done = 'done'
    PENDING = 'pending'


class PaymentStatus(PyEnum):
    Paid = 'paid'
    PENDING = 'pending'


class User(TimeBasedModel):
    chat_id: Mapped[int] = mapped_column(BIGINT, unique=True)
    tg_first_name: Mapped[str]


class Employee(TimeBasedModel):
    chat_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.chat_id", ondelete='CASCADE'))
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone_number: Mapped[str]
    username: Mapped[str] = mapped_column(VARCHAR, nullable=True)
    gender: Mapped[str] = mapped_column(Enum(GenderType))
    work_type: Mapped[str] = mapped_column(VARCHAR(100))
    work_description: Mapped[str] = mapped_column(Text)
    balance: Mapped[float] = mapped_column(DECIMAL, default=0)


class Employer(TimeBasedModel):
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone_number: Mapped[str]
    username: Mapped[str] = mapped_column(VARCHAR, nullable=True)
    chat_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.chat_id", ondelete='CASCADE'))

    works: Mapped[list["Work"]] = relationship("Work", back_populates="employer", cascade="all, delete-orphan")
    balance: Mapped[float] = mapped_column(DECIMAL, default=0)


class Category(TimeBasedModel):
    __tablename__ = "categories"
    title: Mapped[str]


class Photo(TimeBasedModel):
    photo_id: Mapped[str]
    work_id: Mapped[int] = mapped_column(ForeignKey("works.id", ondelete="CASCADE"), nullable=True)
    work: Mapped["Work"] = relationship("Work", back_populates="photos")


class Work(TimeBasedModel):
    title: Mapped[str]
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id", ondelete='Cascade'))
    description: Mapped[str] = mapped_column(Text)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    worker_gender: Mapped[str] = mapped_column(Enum(GenderType), nullable=True)
    num_of_workers: Mapped[int] = mapped_column(nullable=True)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(15, 2), nullable=False)
    employee_id: Mapped[int] = mapped_column(Integer, ForeignKey("employees.id", ondelete='Cascade'), nullable=True)
    employer_id: Mapped[int] = mapped_column(Integer, ForeignKey("employers.id", ondelete='Cascade'))
    status: Mapped[str] = mapped_column(Enum(WorkStatus), default=WorkStatus.PENDING, nullable=True)

    photos: Mapped[list["Photo"]] = relationship("Photo", back_populates="work", cascade="all, delete-orphan")
    employer: Mapped["Employer"] = relationship("Employer", back_populates="works")
    rating: Mapped["Rating"] = relationship("Rating", back_populates="works", uselist=False,
                                            cascade="all, delete-orphan")
    payment_status: Mapped[str] = mapped_column(Enum(WorkStatus), default=WorkStatus.PENDING)

    # @classmethod
    # async def get_employer_id(cls, employer_id_):
    #     query = select(cls).where(cls.employer_id == employer_id_)
    #     result = await db.execute(query)
    #     return result.scalars().first()


class Rating(TimeBasedModel):
    rating: Mapped[int] = mapped_column(Integer, default=5)
    feedback: Mapped[str] = mapped_column(Text)
    work_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("works.id", ondelete="Cascade"))

    works: Mapped["Work"] = relationship("Work", back_populates="rating")


class PaymentPhotos(TimeBasedModel):
    photo_id: Mapped[str]
    employer_id: Mapped[int] = mapped_column(Integer, ForeignKey('employers.id', ondelete='Cascade'), nullable=True)
    employee_id: Mapped[int] = mapped_column(Integer, ForeignKey('employees.id', ondelete='Cascade'), nullable=True)


metadata = Base.metadata
