from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from entities.Animal.dto import AnimalDTO
from entities.Animal.model import Animal
from entities.Animal.service import AnimalService
from db.base import get_session, init_models
from entities.Class.dto import ClassDTO
from entities.Class.model import Class
from entities.Class.service import ClassService
from entities.Order.dto import OrderDTO
from entities.Order.model import Order
from entities.Order.service import OrderService

app = FastAPI()

classService = ClassService()
orderService = OrderService(classService)
animalService = AnimalService(orderService)


@app.on_event('startup')
async def init_db():
    await init_models()


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


@app.post('/animals')
async def insert_animal(animal: AnimalDTO, session: AsyncSession = Depends(get_session)):
    res = await animalService.insert(session, animal)
    if res is None:
        raise HTTPException(409, f'animal already exists')
    return res


@app.delete('/animals/{animal_id}')
async def delete_animal(animal_id: int, session: AsyncSession = Depends(get_session)):
    await animalService.delete(session, animal_id)
    JSONResponse({})


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


@app.post('/orders')
async def insert_order(order: OrderDTO, session: AsyncSession = Depends(get_session)):
    res = await orderService.insert(session, order)
    if res is None:
        raise HTTPException(409, f'order already exists')
    return res


@app.delete('/orders/{order_id}')
async def delete_order(order_id: int, session: AsyncSession = Depends(get_session)):
    await orderService.delete(session, order_id)
    JSONResponse({})


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


@app.post('/classes')
async def insert_class(class_: ClassDTO, session: AsyncSession = Depends(get_session)) -> Class:
    res = await classService.insert(session, class_)
    if res is None:
        raise HTTPException(409, f'class already exists')
    return res


@app.delete('/classes/{class_id}')
async def delete_class(class_id: int, session: AsyncSession = Depends(get_session)):
    await classService.delete(session, class_id)
    return JSONResponse({})

