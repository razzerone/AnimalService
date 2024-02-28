from functools import reduce

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, joinedload

from db.models import Class, Order, Animal, Family, Parameter
from entities.Animal.dto import AnimalDTO
from entities.Animal.model import Animal as AnimalModel
from entities.Class.dto import ClassDTO
from entities.Family.service import FamilyService
from entities.Family.model import Family as FamilyModel
from entities.Order.model import Order as OrderModel
from entities.Class.model import Class as ClassModel
from entities.Parameter.model import Parameter as ParameterModel
from entities.service import Service


class AnimalService(Service[ClassModel, ClassDTO, int]):
    def __init__(self, family_service: FamilyService):
        self._family_service = family_service

        self._animals_subq = (
            select(
                Animal.id, Animal.name, Animal.description, Animal.environmentDescription, Animal.zooDescription,
                Family.id, Family.name, Order.id, Order.name, Class.id, Class.name,
                Parameter.id, Parameter.key, Parameter.value
            )
            .join_from(Animal, Family)
            .join_from(Family, Order)
            .join_from(Order, Class)
            .outerjoin_from(Animal, Parameter)
            .subquery()
        )

        self._animal_alias = aliased(Animal, self._animals_subq, name="animal")
        self._family_alias = aliased(Family, self._animals_subq, name="family")
        self._order_alias = aliased(Order, self._animals_subq, name="order")
        self._class_alias = aliased(Class, self._animals_subq, name="class_")
        self._parameter_alias = aliased(Parameter, self._animals_subq, name="parameter")

    async def get(self, session: AsyncSession) -> list[AnimalModel]:
        animals = (await session.execute(
            select(Animal).options(joinedload(Animal.parameters))
        )).scalars().unique().all()

        # return fold_animal_list_parameters(res)

        # res = (await session.execute(
        #     select(self._animal_alias, self._family_alias, self._order_alias, self._class_alias, self._parameter_alias)
        # )).all()
        #
        # return fold_animal_list_parameters(res)

        return [AnimalModel(
            id=animal.id,
            name=animal.name,
            description=animal.description,
            environment_description=animal.environmentDescription,
            zoo_description=animal.zooDescription,
            parameters=[ParameterModel(id=p.id, key=p.key, value=p.value) for p in animal.parameters],
            geolocation=(animal.latitude, animal.longitude),
            family=FamilyModel(
                id=animal.family.id,
                name=animal.family.name,
                order=OrderModel(
                    id=animal.family.order.id,
                    name=animal.family.order.name,
                    class_=ClassModel(
                        id=animal.family.order.class_.id,
                        name=animal.family.order.class_.name
                    )
                )
            )
        ) for animal in animals]

    async def get_by_id(self, session: AsyncSession, id_: int) -> AnimalModel | None:
        animal = (await session.execute(
            select(Animal).options(joinedload(Animal.parameters)).where(Animal.id == id_)
        )).unique().scalar_one_or_none()

        if animal is None:
            return None

        return AnimalModel(
            id=animal.id,
            name=animal.name,
            description=animal.description,
            environment_description=animal.environmentDescription,
            zoo_description=animal.zooDescription,
            parameters=[ParameterModel(id=p.id, key=p.key, value=p.value) for p in animal.parameters],
            geolocation=(animal.latitude, animal.longitude),
            family=FamilyModel(
                id=animal.family.id,
                name=animal.family.name,
                order=OrderModel(
                    id=animal.family.order.id,
                    name=animal.family.order.name,
                    class_=ClassModel(
                        id=animal.family.order.class_.id,
                        name=animal.family.order.class_.name
                    )
                )
            )
        )

        # return fold_animal_parameters(res)

    # if row is None:
    #     return None
    # return AnimalModel(
    #     id=row.animal.id,
    #     name=row.animal.name,
    #     family=FamilyModel(
    #         id=row.family.id,
    #         name=row.family.name,
    #         order=OrderModel(
    #             id=row.order.id,
    #             name=row.order.name,
    #             class_=ClassModel(
    #                 id=row.class_.id,
    #                 name=row.class_.name
    #             )
    #         )
    #     )
    # )

    async def insert(self, session: AsyncSession, item: AnimalDTO):
        try:
            id_ = (await session.execute(
                insert(Animal).values(
                    name=item.name,
                    familyId=item.family_id,
                    description="" if item.description is None else item.description,
                    environmentDescription="" if item.environment_description is None else item.environment_description,
                    zooDescription="" if item.zoo_description is None else item.zoo_description,
                    latitude=item.geolocation[0],
                    longitude=item.geolocation[0]
                )
            )).lastrowid

            family = await AnimalService.check_insert(
                id_,
                self._family_service.get_by_id(session, item.family_id),
                session.commit()
            )

            return AnimalModel(
                id=id_,
                name=item.name,
                family=family,
                parameters=[],
                description=item.description,
                environment_description=item.environment_description,
                zoo_description=item.zoo_description,
                geolocation=item.geolocation
            )

        except IntegrityError as ex:
            await session.rollback()
            return None

    async def delete(self, session: AsyncSession, id_: int) -> None:
        (await session.execute(delete(Animal).where(Animal.id == id_)))
        await session.commit()


def fold_animal_parameters(rows) -> AnimalModel:
    animal = _animal_from_row(rows[0])
    for row in rows[1:]:
        animal.parameters.append(_parameter_from_row(row))

    return animal


def fold_animal_list_parameters(rows) -> list[AnimalModel]:
    return list(reduce(_product_animal_list, rows, {}).values())


def _product_animal_list(acc: dict[int, AnimalModel], row) -> dict[int, AnimalModel]:
    if row.animal.id in acc:
        acc[row.animal.id].parameters.append(_parameter_from_row(row))
        return acc
    acc[row.animal.id] = _animal_from_row(row)
    return acc


def _animal_from_row(row) -> AnimalModel:
    return AnimalModel(
        id=row.animal.id,
        name=row.animal.name,
        parameters=[] if row.parameter is None else [_parameter_from_row(row)],
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
        ),
        description=row.animal.description,
        environment_description=row.animal.environmentDescription,
        zoo_description=row.animal.zooDescription

    )


def _parameter_from_row(row) -> Parameter:
    return ParameterModel(
        id=row.parameter.id,
        key=row.parameter.key,
        value=row.parameter.value
    )
