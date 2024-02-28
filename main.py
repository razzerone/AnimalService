import re

from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

import config
from auth.auth import Auth
from auth.bearer import JWTBearer
from auth.key_service.exceptions import InvalidToken
from entities.Animal.dto import AnimalDTO
from entities.Animal.model import Animal
from entities.Animal.service import AnimalService
from db.base import get_session, init_models
from entities.Class.dto import ClassDTO
from entities.Class.model import Class
from entities.Class.service import ClassService
from entities.Family.dto import FamilyDTO
from entities.Family.model import Family
from entities.Family.service import FamilyService
from entities.Image.dto import ImageDTO
from entities.Image.model import Image
from entities.Image.service import ImageService
from entities.Order.dto import OrderDTO
from entities.Order.model import Order
from entities.Order.service import OrderService
from entities.Parameter.dto import ParameterDTO
from entities.Parameter.model import Parameter
from entities.Parameter.service import ParameterService

app = FastAPI(debug=config.DEBUG)

classService = ClassService()
orderService = OrderService(classService)
familyService = FamilyService(orderService)
animalService = AnimalService(familyService)
parameterService = ParameterService()
imageService = ImageService()

if config.USE_OPEN_KEY_FILE:
    if config.DEBUG:
        print('use local key service')
    from auth.key_service.file.service import LocalKeyService

    keyService = LocalKeyService()
else:
    from auth.key_service.api.api import APIKeyService

    keyService = APIKeyService(config.KEY_SERVICE_URL)

auth = Auth(keyService)


def auth_post(path: str):
    return app.post(path, dependencies=[Depends(JWTBearer(auth))])


def auth_delete(path: str):
    return app.delete(path, dependencies=[Depends(JWTBearer(auth))])


@app.on_event('startup')
async def init_db():
    await init_models()


@app.get('/animals/parameters')
async def get_parameters(session: AsyncSession = Depends(get_session)) -> list[Parameter]:
    res = await parameterService.get(session)
    return res


@app.get('/animals/parameters/{parameter_id}')
async def get_parameter_by_id(parameter_id: int, session: AsyncSession = Depends(get_session)) -> Parameter:
    res = await parameterService.get_by_id(session, parameter_id)
    if res is None:
        raise HTTPException(404, f'parameter with id={parameter_id} not found')
    return res


@auth_post('/animals/parameters')
async def insert_parameter(parameter: ParameterDTO, session: AsyncSession = Depends(get_session)):
    res = await parameterService.insert(session, parameter)
    if res is None:
        raise HTTPException(409, f'parameter already exists')
    return res


@auth_delete('/animals/parameters/{parameter_id}')
async def delete_parameter(parameter_id: int, session: AsyncSession = Depends(get_session)):
    await parameterService.delete(session, parameter_id)
    return JSONResponse({})


@app.get('/animals/images')
async def get_images(session: AsyncSession = Depends(get_session)) -> list[Image]:
    res = await imageService.get(session)
    return res


@app.get('/animals/images/{image_id}')
async def get_image_by_id(image_id: int, session: AsyncSession = Depends(get_session)) -> Image:
    res = await imageService.get_by_id(session, image_id)
    if res is None:
        raise HTTPException(404, f'image with id={image_id} not found')
    return res


@auth_post('/animals/images')
async def insert_image(image: ImageDTO, session: AsyncSession = Depends(get_session)):
    res = await imageService.insert(session, image)
    if res is None:
        raise HTTPException(409, f'image already exists')
    return res


@auth_delete('/animals/images/{image_id}')
async def delete_image(image_id: int, session: AsyncSession = Depends(get_session)):
    await imageService.delete(session, image_id)
    return JSONResponse({})


@app.get('/animals')
async def get_animals(session: AsyncSession = Depends(get_session)) -> list[Animal]:
    res = await animalService.get(session)
    return res


@app.get('/animals/{animal_id}')
async def get_animal_by_id(animal_id: int, session: AsyncSession = Depends(get_session)) -> Animal:
    res = await animalService.get_by_id(session, animal_id)
    if res is None:
        raise HTTPException(404, f'animal with id={animal_id} not found')
    return res


@auth_post('/animals')
async def insert_animal(animal: AnimalDTO, session: AsyncSession = Depends(get_session)):
    res = await animalService.insert(session, animal)
    if res is None:
        raise HTTPException(409, f'animal already exists')
    return res


@auth_delete('/animals/{animal_id}')
async def delete_animal(animal_id: int, session: AsyncSession = Depends(get_session)):
    await animalService.delete(session, animal_id)
    return JSONResponse({})


@app.get('/families')
async def get_families(session: AsyncSession = Depends(get_session)) -> list[Family]:
    res = await familyService.get(session)
    return res


@app.get('/families/{family_id}')
async def get_family_by_id(family_id: int, session: AsyncSession = Depends(get_session)) -> Family:
    res = await familyService.get_by_id(session, family_id)
    if res is None:
        raise HTTPException(404, f'family with id={family_id} not found')
    return res


@auth_post('/families')
async def insert_family(family: FamilyDTO, session: AsyncSession = Depends(get_session)):
    res = await familyService.insert(session, family)
    if res is None:
        raise HTTPException(409, f'family already exists')
    return res


@auth_delete('/families/{family_id}')
async def delete_family(family_id: int, session: AsyncSession = Depends(get_session)):
    await familyService.delete(session, family_id)
    return JSONResponse({})


@app.get('/orders')
async def get_orders(session: AsyncSession = Depends(get_session)) -> list[Order]:
    res = await orderService.get(session)
    return res


@app.get('/orders/{order_id}')
async def get_order_by_id(order_id: int, session: AsyncSession = Depends(get_session)) -> Order:
    res = await orderService.get_by_id(session, order_id)
    if res is None:
        raise HTTPException(404, f'order with id={order_id} not found')
    return res


@auth_post('/orders')
async def insert_order(order: OrderDTO, session: AsyncSession = Depends(get_session)):
    res = await orderService.insert(session, order)
    if res is None:
        raise HTTPException(409, f'order already exists')
    return res


@auth_delete('/orders/{order_id}')
async def delete_order(order_id: int, session: AsyncSession = Depends(get_session)):
    await orderService.delete(session, order_id)
    return JSONResponse({})


@app.get('/classes')
async def get_classes(session: AsyncSession = Depends(get_session)) -> list[Class]:
    res = await classService.get(session)
    return res


@app.get('/classes/{class_id}')
async def get_class_by_id(class_id: int, session: AsyncSession = Depends(get_session)) -> Class:
    res = await classService.get_by_id(session, class_id)
    if res is None:
        raise HTTPException(404, f'class with id={class_id} not found')
    return res


@auth_post('/classes')
async def insert_class(class_: ClassDTO, session: AsyncSession = Depends(get_session)) -> Class:
    res = await classService.insert(session, class_)
    if res is None:
        raise HTTPException(409, f'class already exists')
    return res


@auth_delete('/classes/{class_id}')
async def delete_class(class_id: int, session: AsyncSession = Depends(get_session)):
    await classService.delete(session, class_id)
    return JSONResponse({})
