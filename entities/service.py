from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Awaitable, Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from entities.dto import DTO
from entities.model import Model

T = TypeVar('T', Model, None, covariant=True)
D = TypeVar('D', DTO, None, covariant=True)


class Service(ABC, Generic[T, D]):
    @abstractmethod
    async def get(self, session: AsyncSession) -> list[T]:
        ...

    @abstractmethod
    async def get_by_id(self, session: AsyncSession, id_: int) -> T | None:
        ...

    @abstractmethod
    async def insert(self, session: AsyncSession, item: D) -> T | None:
        ...

    @abstractmethod
    async def delete(self, session: AsyncSession, id_: int) -> None:
        ...

    @staticmethod
    async def check_insert(insert_id: int, sub_query: Awaitable[Any], commit: Awaitable[None]) -> (int, Any):
        res = await sub_query

        if res is None:
            raise IntegrityError()

        await commit
        return res
