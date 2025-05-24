import logging
from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, DateTime, select, delete as sqlalchemy_delete, \
    update as sqlalchemy_update, inspect, and_, func
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, AsyncSession
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, declared_attr, sessionmaker, selectinload

from config import conf


class Base(AsyncAttrs, DeclarativeBase):
    @declared_attr
    def __tablename__(cls) -> str:
        __name = cls.__name__[:1]
        for i in cls.__name__[1:]:
            if i.isupper():
                __name += '_'
            __name += i
        __name = __name.lower()

        if __name.endswith('y'):
            __name = __name[:-1] + 'ie'
        return __name + 's'

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}  # noqa

    def __repr__(self):
        return str(self.to_dict())


class AsyncDatabaseSession:
    def __init__(self) -> None:
        self._session = None
        self._engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    def init(self):
        self._engine = create_async_engine(conf.db.db_url)  # , echo=True)
        self._session = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)()  # noqa

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


db = AsyncDatabaseSession()
db.init()


class AbstractClass:

    @staticmethod
    async def commit():
        try:
            await db.commit()
        except Exception as e:
            await db.rollback()
            logging.info(f'postgres commit error: {e}')

    @classmethod
    async def get_all(cls):
        return (await db.execute(select(cls))).scalars().all()

    @classmethod
    async def get(cls, _id=None, telegram_id_=None):
        if _id:
            return (await db.execute(select(cls).where(cls.id == _id))).scalar()
        return (await db.execute(select(cls).where(cls.chat_id == telegram_id_))).scalar()

    @classmethod
    async def get_by_title(cls, title_):
        query = select(cls).where(cls.title == title_)
        result = await db.execute(query)
        return result.scalars().first()

    @classmethod
    async def get_by_employer_id(cls, employer_id_):
        query = select(cls).where(cls.employer_id == employer_id_)
        result = await db.execute(query)
        return result.scalars().first()


    @classmethod
    async def get_by_photo_id(cls, photo_id):
        query = select(cls).where(cls.photo_id == photo_id)
        objects = await db.execute(query)
        object_ = objects.first()
        if object_:
            return object_[0]
        else:
            return []

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

    @classmethod
    async def get_work_photos(cls, employer_id_):
        query = (select(cls).
                 options(selectinload(cls.photos)).
                 order_by(cls.created_at.desc()).
                 where(cls.employer_id == employer_id_))
        objects = await db.execute(query)
        object_ = objects.first()
        if object_:
            return object_[0]
        else:
            return []

    @classmethod
    async def create(cls, **kwargs):
        obj = cls(**kwargs)
        db.add(obj)
        await cls.commit()
        return obj

    @classmethod
    async def update(cls, _id: Optional[int], **kwargs):
        query = sqlalchemy_update(cls).where(cls.id == _id).values(**kwargs).execution_options(
            synchronize_session='fetch')
        await db.execute(query)
        await cls.commit()


    @classmethod
    async def delete(cls, _id: Optional[int]):
        query = sqlalchemy_delete(cls).where(cls.id == _id)
        await db.execute(query)
        await cls.commit()
        return (await db.execute(select(cls))).scalars()

    @classmethod
    async def filter(cls, **kwargs):
        conditions = [getattr(cls, key) == value for key, value in kwargs.items()]
        query = (select(cls).where(and_(*conditions)))
        return (await db.execute(query)).scalars().all()

    async def save_model(self):
        db.add(self)
        await self.commit()
        return self


class BaseModel(AbstractClass, Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)


class TimeBasedModel(BaseModel):
    __abstract__ = True
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=datetime.now())
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
