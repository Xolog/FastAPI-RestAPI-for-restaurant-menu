import uuid

from sqlalchemy import String, ForeignKey, Column, UUID, Numeric, MetaData
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# metadata = MetaData()


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    title = Column(String)
    description = Column(String)
    submenu = relationship('Submenu', back_populates='menu', cascade='all, delete-orphan')


class Submenu(Base):
    __tablename__ = 'submenu'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    title = Column(String)
    description = Column(String)
    menu_id = Column(UUID(as_uuid=True), ForeignKey('menu.id', ondelete='CASCADE'))
    menu = relationship('Menu', back_populates='submenu')
    dish = relationship("Dish", back_populates="submenu")


class Dish(Base):
    __tablename__ = 'dish'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    title = Column(String, unique=True)
    description = Column(String)
    price = Column(Numeric(10, 2), nullable=False)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenu.id', ondelete='CASCADE'))
    submenu = relationship('Submenu', back_populates='dish')

