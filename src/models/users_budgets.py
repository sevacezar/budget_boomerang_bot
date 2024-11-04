from datetime import datetime
from typing import List

from sqlalchemy import Column, ForeignKey, Integer, Table, func, Index
from sqlalchemy.orm import Mapped, relationship, mapped_column

from database import Base


# Таблица-связь многие-ко-многим
users_budgets = Table(
    'user_budgets',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('budget_id', Integer, ForeignKey('budgets.id'))
)

class User(Base):
    """Модель пользователей ORM"""

    __tablename__ = 'users'
    __tableargs__ = (
        Index('ix_userx_name', 'name'),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # Relatioship
    budgets: Mapped[List['Budget']] = relationship(
        secondary=users_budgets,
        back_populates='users'
    )  # Many-to-many

    def __repr__(self):
        """Формально предсатвляет пользователя"""
        return f'{self.__class__.__name__}(id={self.id}, name="{self.name}")'

class Budget(Base):
    """Модель бюджетов"""

    __tablename__ = 'budgets'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default = func.now())
    is_archived: Mapped[bool] = mapped_column(default=False)

    users: Mapped[List[User]] = relationship(
        secondary=users_budgets,
        back_populates='budgets'
        )  # Many-to-many
    cash_flow_categories = relationship(
        'CashFlowCategory',
        back_populates='budget',
        cascade='delete',
    )
    
    def __repr__(self):
        """Формально предсатвляет бюджет"""
        return f'{self.__class__.__name__}(id={self.id}, name="{self.name}")'

# RECREATE DB!!!