from decimal import Decimal
from typing import List, Optional

from sqlalchemy import Column, ForeignKey, DECIMAL
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column, Relationship

from db.base import Base
from entities.model import Model


class Class(Base):
    __tablename__ = 'classes'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    classId: Mapped[int] = mapped_column(ForeignKey('classes.id'))
    name: Mapped[str] = mapped_column(String(100), unique=True)

    class_: Mapped['Class'] = relationship('Class', lazy='joined')


class Family(Base):
    __tablename__ = 'families'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    orderId: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    name: Mapped[str] = mapped_column(String(100), unique=True)

    order: Mapped['Order'] = relationship('Order', lazy='joined')


class Parameter(Base):
    __tablename__ = 'parameters'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    animalId: Mapped[int] = mapped_column(ForeignKey('animals.id', ondelete='CASCADE'))
    key: Mapped[str] = mapped_column(String(100))
    value: Mapped[str] = mapped_column(String(100))


class Image(Base):
    __tablename__ = 'images'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    animalId: Mapped[int] = mapped_column(ForeignKey('animals.id', ondelete='CASCADE'))
    url: Mapped[str] = mapped_column(String(2083), default='')


class Animal(Base):
    __tablename__ = 'animals'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    familyId: Mapped[int] = mapped_column(ForeignKey('families.id'))
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(String(1024), default='')
    environmentDescription: Mapped[str] = mapped_column(String(1024), default='')
    zooDescription: Mapped[str] = mapped_column(String(1024), default='')
    latitude: Mapped[Decimal] = mapped_column(DECIMAL(precision=20, scale=10))
    longitude: Mapped[Decimal] = mapped_column(DECIMAL(precision=20, scale=10))
    qr_url: Mapped[str] = mapped_column(String(2083), default='')
    map_icon_url: Mapped[str] = mapped_column(String(2083), default='')
    list_icon_url: Mapped[str] = mapped_column(String(2083), default='')
    audio_url: Mapped[str] = mapped_column(String(2083), default='')

    family: Mapped['Family'] = relationship('Family', lazy='joined')
    parameters: Mapped[List['Parameter']] = relationship(lazy='joined')
    images: Mapped[List['Image']] = relationship(lazy='joined')

