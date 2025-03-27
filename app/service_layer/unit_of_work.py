import abc
from typing import Self

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from app import config
from app.adapters import repository


class AbstractUnitOfWork(abc.ABC):
    messages: repository.AbstractRepository

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    async def commit(self) -> None:
        await self._commit()

    @abc.abstractmethod
    async def _commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError


DEFAULT_SESSION_FACTORY = async_sessionmaker(
    bind=create_async_engine(
        config.get_postgres_creds(),
    )
)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession] = DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    async def __aenter__(self) -> Self:
        self.session = self.session_factory()
        self.messages = repository.SqlAlchemyRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, *args) -> None:
        await super().__aexit__(*args)
        await self.session.close()

    async def _commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
