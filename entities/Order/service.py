from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from db.models import Class, Order
from entities.Class.model import Class as ClassModel
from entities.Class.service import ClassService
from entities.Order.dto import OrderDTO
from entities.Order.model import Order as OrderModel
from entities.service import Service


class OrderService(Service[OrderModel, OrderDTO, int]):
    def __init__(self, class_service: ClassService):
        self._class_service = class_service

        self._orders_subq = (
            select(Order.id, Order.name, Class.id, Class.name)
            .join_from(Order, Class)
            .subquery()
        )

        self._order_alias = aliased(Order, self._orders_subq, name="order")
        self._class_alias = aliased(Class, self._orders_subq, name="class_")

    async def get(self, session: AsyncSession) -> list[OrderModel]:
        orders = (await session.execute(
            select(Order)
        )).scalars().all()

        return [OrderModel(
            id=order.id,
            name=order.name,
            class_=ClassModel(
                id=order.class_.id,
                name=order.class_.name
            )
        ) for order in orders]

    async def get_by_id(self, session: AsyncSession, id_: int) -> OrderModel | None:
        order = (await session.execute(
            select(Order).where(Order.id == id_)
        )).scalar_one_or_none()

        if order is None:
            return None
        return OrderModel(
            id=order.id,
            name=order.name,
            class_=ClassModel(
                id=order.class_.id,
                name=order.class_.name
            )
        )

    async def insert(self, session: AsyncSession, item: OrderDTO):
        try:
            id_ = (await session.execute(
                insert(Order).values(name=item.name, classId=item.class_id)
            )).lastrowid

            class_ = await OrderService.check_insert(
                id_,
                self._class_service.get_by_id(session, item.class_id),
                session.commit()
            )

            return OrderModel(id=id_, name=item.name, class_=class_)

        except IntegrityError as ex:
            await session.rollback()
            return None

    async def delete(self, session: AsyncSession, id_: int):
        (await session.execute(delete(Order).where(Order.id == id_)))
        await session.commit()
