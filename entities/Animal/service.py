from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from db.models import Class, Order, Animal, Family
from entities.Animal.dto import AnimalDTO
from entities.Animal.model import Animal as AnimalModel
from entities.Class.dto import ClassDTO
from entities.Family.service import FamilyService
from entities.Family.model import Family as FamilyModel
from entities.Order.model import Order as OrderModel
from entities.Class.model import Class as ClassModel
from entities.service import Service


class AnimalService(Service[ClassModel, ClassDTO, int]):
    def __init__(self, family_service: FamilyService):
        self._family_service = family_service

        self._animals_subq = (
            select(
                Animal.id, Animal.name, Family.id, Family.name, Order.id, Order.name, Class.id, Class.name
            )
            .join_from(Animal, Family)
            .join_from(Family, Order)
            .join_from(Order, Class)
            .subquery()
        )

        self._animal_alias = aliased(Animal, self._animals_subq, name="animal")
        self._family_alias = aliased(Family, self._animals_subq, name="family")
        self._order_alias = aliased(Order, self._animals_subq, name="order")
        self._class_alias = aliased(Class, self._animals_subq, name="class_")

    async def get(self, session: AsyncSession) -> list[AnimalModel]:
        res = (await session.execute(
            select(self._animal_alias, self._family_alias, self._order_alias, self._class_alias)
        ))

        return [AnimalModel(
            id=row.animal.id,
            name=row.animal.name,
            family=FamilyModel(
                id=row.family.id,
                name=row.family.name,
                order=OrderModel(
                    id=row.order.id,
                    name=row.order.name,
                    class_=ClassModel(
                        id=row.class_.id,
                        name=row.class_.name
                    )
                )
            )
        ) for row in res]

    async def get_by_id(self, session: AsyncSession, id_: int) -> AnimalModel | None:
        row = (await session.execute(
            select(
                self._animal_alias, self._family_alias, self._order_alias, self._class_alias
            )
            .where(self._animal_alias.id == id_)
        )).first()

        if row is None:
            return None
        return AnimalModel(
            id=row.animal.id,
            name=row.animal.name,
            family=FamilyModel(
                id=row.family.id,
                name=row.family.name,
                order=OrderModel(
                    id=row.order.id,
                    name=row.order.name,
                    class_=ClassModel(
                        id=row.class_.id,
                        name=row.class_.name
                    )
                )
            )
        )

    async def insert(self, session: AsyncSession, item: AnimalDTO):
        try:
            id_ = (await session.execute(
                insert(Animal).values(name=item.name, orderId=item.family_id)
            )).lastrowid

            family = await AnimalService.check_insert(
                id_,
                self._family_service.get_by_id(session, item.family_id),
                session.commit()
            )

            return AnimalModel(id=id_, name=item.name, family=family)

        except IntegrityError as ex:
            await session.rollback()
            return None

    async def delete(self, session: AsyncSession, id_: int) -> None:
        (await session.execute(delete(Animal).where(Animal.id == id_)))
        await session.commit()
