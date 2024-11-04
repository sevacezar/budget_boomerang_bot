from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.types import Numeric

from database import Base

class CashFlowCategory(Base):
    """Model of categories of expenses or incomes"""

    __tablename__ = 'cash_flow_categories'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    budget_id: Mapped[int] = mapped_column(ForeignKey('budgets.id'))
    name: Mapped[str] = mapped_column(nullable=False)
    is_expense: Mapped[bool] = mapped_column(default=True)
    # is_archived: Mapped[bool] = mapped_column(default=False)

    budget = relationship(
        'Budget',
        back_populates='cash_flow_categories',
    )
    cash_flows = relationship(
        'CashFlow',
        back_populates='category',
        cascade='delete',
    )

    def __repr__(self):
        """Representates cash-flow category"""
        return f'{self.__class__.__name__}(id={self.id}, name="{self.name}")'
    

class CashFlow(Base):
    """Model of incomes and expenses"""

    __tablename__ = 'cash_flows'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('cash_flow_categories.id'))
    value: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    # is_archived: Mapped[bool] = mapped_column(default=False)

    category = relationship(
        'CashFlowCategory',
        back_populates='cash_flows',
    )

    def __repr__(self):
        """Representates specific cash-flow"""
        return f'{self.__class__.__name__}(id={self.id}, value="{self.value}", desc="{self.description}")'

