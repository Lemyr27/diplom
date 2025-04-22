import abc
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain import model


class AbstractRepository(abc.ABC):
    async def add(self, message: model.Message) -> None:
        await self._add(message)

    async def list(self) -> List[model.Message]:
        result = await self._list()
        return result

    @abc.abstractmethod
    async def _add(self, message: model.Message) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def _list(self) -> List[model.Message]:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    async def _add(self, message: model.Message) -> None:
        self.session.add(message)

    async def _list(self) -> List[model.Message]:
        stmt = select(model.Message).order_by(model.Message.created_at)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
