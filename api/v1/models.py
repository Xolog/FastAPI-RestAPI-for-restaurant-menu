import uuid
from decimal import Decimal
from typing import Annotated

from sqlalchemy import ForeignKey, UUID, Numeric
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column

Base = declarative_base()

uuidpk = Annotated[UUID, mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )]


class Menu(Base):
    __tablename__ = 'menu'

    id: Mapped[uuidpk]

    title: Mapped[str]
    description: Mapped[str | None]
    submenu = relationship('Submenu',
                           back_populates='menu',
                           cascade='all, delete-orphan',
                           primaryjoin='Menu.id == Submenu.menu_id',
                           lazy='joined')

    @hybrid_property
    def submenus_count(self) -> int:
        return len(self.submenu)

    @hybrid_property
    def dishes_count(self) -> int:
        count = 0
        for item in self.submenu:
            count += len(item.dish)

        return count


class Submenu(Base):
    __tablename__ = 'submenu'

    id: Mapped[uuidpk]

    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]
    menu_id = mapped_column(UUID(as_uuid=True), ForeignKey('menu.id', ondelete='CASCADE'))
    menu = relationship('Menu', back_populates='submenu')
    dish = relationship("Dish",
                        back_populates="submenu",
                        primaryjoin='Submenu.id == Dish.submenu_id',
                        lazy='joined')

    @hybrid_property
    def dishes_count(self) -> int:
        return len(self.dish)


class Dish(Base):
    __tablename__ = 'dish'

    id: Mapped[uuidpk]

    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=True)
    submenu_id = mapped_column(UUID(as_uuid=True), ForeignKey('submenu.id', ondelete='CASCADE'))
    submenu = relationship('Submenu', back_populates='dish')
