from typing import List

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column, Relationship

from db.base import Base
from entities.model import Model


class Class(Base):
    __tablename__ = 'classes'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    classId: Mapped[int] = mapped_column(ForeignKey('classes.id'))
    name: Mapped[str] = mapped_column(String(50), unique=True)

    class_: Mapped['Class'] = relationship('Class', lazy='joined')


class Family(Base):
    __tablename__ = 'families'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    orderId: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    name: Mapped[str] = mapped_column(String(50), unique=True)

    order: Mapped['Order'] = relationship('Order', lazy='joined')


class Parameter(Base):
    __tablename__ = 'parameters'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    animalId: Mapped[int] = mapped_column(ForeignKey('animals.id', ondelete='CASCADE'))
    key: Mapped[str] = mapped_column(String(50))
    value: Mapped[str] = mapped_column(String(50))


class Animal(Base):
    __tablename__ = 'animals'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    familyId: Mapped[int] = mapped_column(ForeignKey('families.id'))
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(String(1024), default='')
    environmentDescription: Mapped[str] = mapped_column(String(1024), default='')
    zooDescription: Mapped[str] = mapped_column(String(1024), default='')

    family: Mapped['Family'] = relationship('Family', lazy='joined')
    parameters: Mapped[List['Parameter']] = relationship(lazy='joined')

