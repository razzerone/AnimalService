from sqlalchemy import select, insert, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Image
from entities.Image.dto import ImageDTO
from entities.Image.model import Image as ImageModel
from entities.service import Service


class ImageService(Service[ImageModel, ImageDTO, int]):
    async def delete(self, session: AsyncSession, id_: int) -> None:
        await session.execute(delete(Image).where(Image.id == id_))
        await session.commit()

    async def insert(self, session: AsyncSession, item: ImageDTO) -> ImageModel | None:
        try:
            id_ = (await session.execute(
                insert(Image)
                .values(
                    animalId=item.animal_id,
                    url=item.url
                ))).lastrowid
            await session.commit()
            return ImageModel(
                id=id_,
                url=item.url
            )
        except IntegrityError as ex:
            await session.rollback()
            return None

    async def get_by_id(self, session: AsyncSession, id_: int) -> ImageModel | None:
        image = (await session.execute(
            select(Image).where(Image.id == id_)
        )).scalar_one_or_none()

        if image is None:
            return None

        return ImageModel(
                id=image.id,
                url=image.url
            )

    async def get(self, session: AsyncSession) -> list[ImageModel]:
        images = (await session.execute(
            select(Image)
        )).scalars().all()

        return [
            ImageModel(
                id=image.id,
                url=image.url
            )
            for image in images]
