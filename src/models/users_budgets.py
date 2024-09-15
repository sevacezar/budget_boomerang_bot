from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Table, func
from sqlalchemy.orm import Mapped, relationship, mapped_column

from database import Base

class User(Base):
    """Модель пользователей ORM"""

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

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

    incomes_categories = relationship('IncomesCategory', back_populates='budget')
    expenses_categories = relationship('ExpensesCategory', back_populates='budget')
    
    def __repr__(self):
        """Формально предсатвляет бюджет"""
        return f'{self.__class__.__name__}(id={self.id}, name="{self.name}")'

# Таблица-связь многие-ко-многим
users_budgets = Table(
    'user_budgets',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('budget_id', Integer, ForeignKey('budgets.id'))
)