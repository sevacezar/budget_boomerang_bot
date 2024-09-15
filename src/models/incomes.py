from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Table, func
from sqlalchemy.orm import Mapped, relationship, mapped_column

from database import Base

class IncomesCategory(Base):
    """Модель категорий доходов"""

    __tablename__ = 'incomes_categories'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    budget_id: Mapped[int] = mapped_column(ForeignKey('budgets.id'))
    name: Mapped[str] = mapped_column(nullable=False)

    budget = relationship('Budget', back_populates='incomes_categories')
    incomes = relationship('Income', back_populates='category')

    def __repr__(self):
        """Формально предсатвляет категорию дохода"""
        return f'{self.__class__.__name__}(id={self.id}, name="{self.name}")'
    

class Income(Base):
    """Модель конкретных доходов"""

    __tablename__ = 'incomes'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('incomes_categories.id'))
    value: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    category = relationship('IncomesCategory', back_populates='incomes')

    def __repr__(self):
        """Формально предсатвляет конкретный доход"""
        return f'{self.__class__.__name__}(id={self.id}, value="{self.value}", desc="{self.description}")'
