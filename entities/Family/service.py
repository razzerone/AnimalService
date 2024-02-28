from sqlalchemy import select, insert, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from db.models import Family, Order, Class
from entities.Family.dto import FamilyDTO
from entities.Family.model import Family as FamilyModel
from entities.Order.model import Order as OrderModel
from entities.Class.model import Class as ClassModel
from entities.Order.service import OrderService
from entities.service import Service


class FamilyService(Service[FamilyModel, FamilyDTO, int]):
    def __init__(self, order_service: OrderService):
        self._order_service = order_service

        self._families_subq = (
            select(Family.id, Family.name, Order.id, Order.name, Class.id, Class.name)
            .join_from(Family, Order)
            .join_from(Order, Class)
            .subquery()
        )

        self._family_alias = aliased(Family, self._families_subq, name="family")
        self._order_alias = aliased(Order, self._families_subq, name="order")
        self._class_alias = aliased(Class, self._families_subq, name="class_")

    async def delete(self, session: AsyncSession, id_: int) -> None:
        (await session.execute(delete(Family).where(Family.id == id_)))
        await session.commit()

    async def insert(self, session: AsyncSession, item: FamilyDTO) -> FamilyModel | None:
        try:
            id_ = (await session.execute(
                insert(Family).values(name=item.name, orderId=item.order_id)
            )).lastrowid

            order = await FamilyService.check_insert(
                id_,
                self._order_service.get_by_id(session, item.order_id),
                session.commit()
            )

            return FamilyModel(id=id_, name=item.name, order=order)

        except IntegrityError as ex:
            await session.rollback()
            return None

    async def get_by_id(self, session: AsyncSession, id_: int) -> FamilyModel | None:
        family = (await session.execute(
            select(Family).where(Family.id == id_)
        )).scalar_one_or_none()

        if family is None:
            return None
        return FamilyModel(
            id=family.id,
            name=family.name,
            order=OrderModel(
                id=family.order.id,
                name=family.order.name,
                class_=ClassModel(
                    id=family.order.class_.id,
                    name=family.order.class_.name
                )
            )
        )

    async def get(self, session: AsyncSession) -> list[FamilyModel]:
        families = (await session.execute(
            select(Family)
        )).scalars().all()

        return [FamilyModel(
            id=family.id,
            name=family.name,
            order=OrderModel(
                id=family.order.id,
                name=family.order.name,
                class_=ClassModel(
                    id=family.order.class_.id,
                    name=family.order.class_.name
                )
            )
        ) for family in families]
