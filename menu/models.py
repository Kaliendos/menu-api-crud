import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from config.database.db import Base
from sqlalchemy.orm import relationship


class Menu(Base):
    __tablename__ = "Menu"

    id = sa.Column(
        UUID(as_uuid=True), primary_key=True,
        default=uuid.uuid4, index=True
    )
    title = sa.Column(sa.String)
    description = sa.Column(sa.Text)
    sub_menu = relationship("SubMenu", cascade="all, delete")


class SubMenu(Base):
    __tablename__ = "SubMenu"

    id = sa.Column(
        UUID(as_uuid=True), primary_key=True,
        default=uuid.uuid4, index=True
    )
    title = sa.Column(sa.String)
    description = sa.Column(sa.Text)
    menu_id = sa.Column(UUID, sa.ForeignKey("Menu.id"))
    Menu = relationship("Menu")
    Dish = relationship("Dish", cascade="all, delete")


class Dish(Base):
    __tablename__ = "Dish"
    id = sa.Column(
        UUID(as_uuid=True), primary_key=True,
        default=uuid.uuid4, index=True
    )
    title = sa.Column(sa.String)
    description = sa.Column(sa.Text)
    price = sa.Column(sa.Numeric(precision=10, scale=2), nullable=False)
    sub_menu_id = sa.Column(UUID, sa.ForeignKey("SubMenu.id"))
    SubMenu = relationship("SubMenu")

