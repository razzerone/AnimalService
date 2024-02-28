from sqlalchemy import select, insert, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from db.models import Parameter
from entities.Parameter.dto import ParameterDTO
from entities.Parameter.model import Parameter as ParameterModel
from entities.service import Service


class ParameterService(Service[ParameterModel, ParameterDTO, int]):
    def __init__(self):
        self._parameters_subq = (
            select(
                Parameter.id, Parameter.key, Parameter.value
            )
            .subquery()
        )

        self._parameter_alias = aliased(Parameter, self._parameters_subq, name="parameter")

    async def delete(self, session: AsyncSession, id_: int) -> None:
        (await session.execute(delete(Parameter).where(Parameter.id == id_)))
        await session.commit()

    async def insert(self, session: AsyncSession, item: ParameterDTO) -> ParameterModel | None:
        try:
            id_ = (await session.execute(
                insert(Parameter)
                .values(
                    animalId=item.animal_id,
                    key=item.key,
                    value=item.value
                ))).lastrowid
            await session.commit()
            return ParameterModel(
                id=id_,
                key=item.key,
                value=item.value
            )
        except IntegrityError as ex:
            await session.rollback()
            return None

    async def get_by_id(self, session: AsyncSession, id_: int) -> ParameterModel | None:
        row = (await session.execute(
            select(Parameter)
            .where(Parameter.id == id_)
        )).first()

        return Parameter(
            id=row.id,
            key=row.key,
            value=row.value
        )

    async def get(self, session: AsyncSession) -> list[ParameterModel]:
        res = (await session.execute(
            select(Parameter)
        )).scalars().all()

        return [
            Parameter(
                id=row.id,
                key=row.key,
                value=row.value
            )
            for row in res]
