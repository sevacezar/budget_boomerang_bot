from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import DbException, TgException
from models.users_budgets import User, Budget
from models.cash_flows import CashFlow, CashFlowCategory
from services.get_transactions import EntitiesGetter
from services.utils import get_entity_from_list

class EntitiesUpdater:
    """Class with functions of updateing entities"""

    def __init__(self, session: AsyncSession):
        self.session = session

    
    async def update_budget_name(
            self,
            username: str,
            budget_id: str,
            new_budget_name: str,
    ) -> Budget:
        """Updates budget name"""
        user: User = await EntitiesGetter(session=self.session).get_user_by_name(
            name=username,
            get_related_budgets=True,
        )
        
        if not user:
            raise DbException(f'User {username} not found')

        budget: Budget | None = get_entity_from_list(
            entities=user.budgets,
            id=budget_id,
        )

        if not budget:
            raise TgException(f"User doesnt have budget with id {budget_id}")

        budget.name = new_budget_name
        await self.session.commit()
        return budget

    async def update_category_name(
            self,
            username: str,
            budget_id: str,
            category_id: str,
            new_category_name: str,
    ) -> CashFlowCategory:
        """Updates category name"""
        user: User = await EntitiesGetter(session=self.session).get_user_by_name(
            name=username,
            get_related_categories=True,
        )
        
        if not user:
            raise DbException(f'User {username} not found')

        budget: Budget | None = get_entity_from_list(
            entities=user.budgets,
            id=budget_id,
        )

        if not budget:
            raise TgException(f"User doesnt have budget with id {budget_id}")

        category: CashFlowCategory = get_entity_from_list(
            entities=budget.cash_flow_categories,
            id=category_id,
        )

        if not category:
            raise TgException(f"Budget doesnt have category with id {category_id}")
        
        category.name = new_category_name
        await self.session.commit()
        return category
    
    async def update_cash_flow(
            self,
            username: str,
            budget_id: int,
            category_id: int,
            cash_flow_id: int,
            params: dict,
    ) -> CashFlow:
        """Updates cash flow"""
        user: User = await EntitiesGetter(session=self.session).get_user_by_name(
            name=username,
            get_related_cash_flows=True,
        )
        
        if not user:
            raise DbException(f'User {username} not found')

        budget: Budget | None = get_entity_from_list(
            entities=user.budgets,
            id=budget_id,
        )

        if not budget:
            raise TgException(f"User doesnt have budget with id {budget_id}")

        category: CashFlowCategory = get_entity_from_list(
            entities=budget.cash_flow_categories,
            id=category_id,
        )

        if not category:
            raise TgException(f"Budget doesnt have category with id {category_id}")
        
        cash_flow: CashFlow = get_entity_from_list(
            entities=category.cash_flows,
            id=cash_flow_id,
        )
        
        if not cash_flow:
            raise TgException(f"Category doesnt have cash-flow with id {cash_flow_id}")

        for param_name, param_value in params.items():
            if hasattr(cash_flow, param_name):
                setattr(cash_flow, param_name, param_value)
        
        await self.session.commit()
        return cash_flow
