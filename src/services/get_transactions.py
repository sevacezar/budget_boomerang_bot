from typing import Literal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.users_budgets import User, Budget
from models.cash_flows import CashFlow, CashFlowCategory


class EntitiesGetter:
    """Class with functions of getting entities"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_name(
        self,
        name: str,
        get_related_budgets: bool = False,
        get_related_categories: bool = False,
        get_related_cash_flows: bool = False,
    ) -> User | None:
        """Get user by name with loading related entities"""

        if get_related_cash_flows:
            get_related_categories = True
        
        if get_related_categories:
            get_related_budgets = True

        options = None
        if get_related_budgets:
            options = selectinload(User.budgets)
            if get_related_categories:
                options = options.selectinload(Budget.cash_flow_categories)
                if get_related_cash_flows:
                    options = options.selectinload(CashFlowCategory.cash_flows)

        query = select(User)
        
        if options:
            query = query.options(options)

        query = query.where(User.name == name)

        res = await self.session.execute(query)
        user: User | None = res.scalars().one_or_none()
        return user

    async def get_all_budgets_by_username(
        self,
        username: str,
        get_related_categories: bool = False,
        get_related_cash_flows: bool = False,
    ) -> User | None:
        """Get budget by username with loading related entities"""

        if get_related_cash_flows:
            get_related_categories = True

        options = None
        if get_related_categories:
            options = selectinload(Budget.cash_flow_categories)
            if get_related_cash_flows:
                options = options.selectinload(CashFlowCategory.cash_flows)

        query = select(Budget)
        
        if options:
            query = query.options(options)

        query = query.join(Budget.users).where(User.name == username)

        res = await self.session.execute(query)
        budgets: list[Budget] = res.scalars().all()
        return budgets
    
    async def get_budget_by_id(
        self,
        id: int,
        get_related_categories: bool = False,
        get_related_cash_flows: bool = False,
    ) -> User | None:
        """Get budget by id with loading related entities"""

        if get_related_cash_flows:
            get_related_categories = True

        options = None
        if get_related_categories:
            options = selectinload(Budget.cash_flow_categories)
            if get_related_cash_flows:
                options = options.selectinload(CashFlowCategory.cash_flows)

        query = select(Budget)
        
        if options:
            query = query.options(options)

        query = query.where(Budget.id == id)

        res = await self.session.execute(query)
        budget: list[Budget] = res.scalars().one_or_none()
        return budget
    
    async def get_categories_by_budget_id(
            self,
            id: int,
            category_type: Literal['income', 'expense'],
            get_related_cash_flows: bool = False,
    ) -> list[CashFlowCategory]:
        """Gets categories of specific budget by budget id"""

        options = None
        if get_related_cash_flows:
            options = selectinload(CashFlowCategory.cash_flows)
        
        query = select(CashFlowCategory)
        
        if options:
            query = query.options(options)

        is_expense = category_type == 'expense'
        query = query.where(CashFlowCategory.budget_id == id and CashFlowCategory.is_expense == is_expense)

        res = await self.session.execute(query)
        categories: list[CashFlowCategory] = res.scalars().all()
        return categories
    
    async def get_category_by_id(
            self,
            id: int,
            get_related_cash_flows: bool = False,
    ) -> CashFlowCategory:
        """Gets cash-flow category by category id"""
        options = None
        if get_related_cash_flows:
            options = selectinload(CashFlowCategory.cash_flows)
        
        query = select(CashFlowCategory)
        
        if options:
            query = query.options(options)

        query = query.where(CashFlowCategory.id == id)

        res = await self.session.execute(query)
        category: CashFlowCategory = res.scalar_one_or_none()
        return category
    
    async def get_cash_flows_by_category_id(
            self,
            id: int,
    ) -> list[CashFlow]:
        """Gets cash flows of specific category by category id"""

        query = select(CashFlow).where(CashFlow.category_id == id)
        res = await self.session.execute(query)
        cash_flows: list[CashFlow] = res.scalars().all()
        return cash_flows