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


class Family(Base):
    __tablename__ = 'families'

    id = Column(Integer, autoincrement=True, primary_key=True)
    orderId = Column(Integer, ForeignKey('orders.id'))
    name = Column(String(50), unique=True)


class Animal(Base):
    __tablename__ = 'animals'

    id = Column(Integer, autoincrement=True, primary_key=True)
    familyId = Column(Integer, ForeignKey('families.id'))
    name = Column(String(50), unique=True)
    description = Column(String(512), default="")
    environmentDescription = Column(String(512), default="")
    zooDescription = Column(String(512), default="")


class Parameter(Base):
    __tablename__ = 'parameters'

    id = Column(Integer, autoincrement=True, primary_key=True)
    animalId = Column(Integer, ForeignKey('animals.id', ondelete="CASCADE"))
    key = Column(String(50))
    value = Column(String(50))
