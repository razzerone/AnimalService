from sqlalchemy import Column, ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from db.base import Base


class Class(Base):
    __tablename__ = 'classes'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), unique=True)


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, autoincrement=True, primary_key=True)
    classId = Column(Integer, ForeignKey('classes.id'))
    name = Column(String(50), unique=True)


class Animal(Base):
    __tablename__ = 'animals'

    id = Column(Integer, autoincrement=True, primary_key=True)
    orderId = Column(Integer, ForeignKey('orders.id'))
    name = Column(String(50), unique=True)
