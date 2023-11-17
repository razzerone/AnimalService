from sqlalchemy import select, delete, insert, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Class
from entities.Class.dto import ClassDTO
from entities.Class.model import Class as ClassModel
from entities.service import Service


class ClassService(Service[ClassModel, ClassDTO]):
    async def get(self, session: AsyncSession) -> list[ClassModel]:
        res = (await session.scalars(select(Class))).all()
        return [ClassModel(id=e.id, name=e.name) for e in res]

    async def get_by_id(self, session: AsyncSession, id_: int) -> ClassModel | None:
        res = (await session.scalars(select(Class).filter(Class.id == id_))).first()

        if res is None:
            return None
        return ClassModel(id=res.id, name=res.name)

    async def insert(self, session: AsyncSession, item: ClassDTO) -> Class | None:
        try:
            id_ = (await session.execute(insert(Class).values(name=item.name))).lastrowid
            await session.commit()
            return ClassModel(id=id_, name=item.name)
        except IntegrityError as ex:
            await session.rollback()
            return None

    async def delete(self, session: AsyncSession, id_: int) -> None:
        (await session.execute(delete(Class).where(Class.id == id_)))
        await session.commit()
