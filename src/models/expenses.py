# from datetime import datetime

# from sqlalchemy import Column, ForeignKey, Integer, Table, func
# from sqlalchemy.orm import Mapped, relationship, mapped_column

# from database import Base

# class ExpensesCategory(Base):
#     """Модель категорий расходов"""

#     __tablename__ = 'expenses_categories'

#     id: Mapped[int] = mapped_column(primary_key=True, index=True)
#     budget_id: Mapped[int] = mapped_column(ForeignKey('budgets.id'))
#     name: Mapped[str] = mapped_column(nullable=False)

#     budget = relationship('Budget', back_populates='expenses_categories')
#     expenses = relationship('Expense', back_populates='category')

#     def __repr__(self):
#         """Формально предсатвляет категорию расхода"""
#         return f'{self.__class__.__name__}(id={self.id}, name="{self.name}")'
    

# class Expense(Base):
#     """Модель конкретных расходов"""

#     __tablename__ = 'expenses'

#     id: Mapped[int] = mapped_column(primary_key=True, index=True)
#     category_id: Mapped[int] = mapped_column(ForeignKey('expenses_categories.id'))
#     value: Mapped[float] = mapped_column(nullable=False)
#     description: Mapped[str]
#     created_at: Mapped[datetime] = mapped_column(server_default=func.now())

#     category = relationship('ExpensesCategory', back_populates='expenses')

#     def __repr__(self):
#         """Формально предсатвляет конкретный расход"""
#         return f'{self.__class__.__name__}(id={self.id}, value="{self.value}", desc="{self.description}")'

