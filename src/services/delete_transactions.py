from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import DbException, TgException
from models.users_budgets import User, Budget
from models.cash_flows import CashFlow, CashFlowCategory
from services.get_transactions import EntitiesGetter
from services.utils import get_entity_from_list

class EntitiesDeleter:
    """Class with functions of deleting entities"""

    def __init__(self, session: AsyncSession):
        self.session = session

    
    async def delete_budget(
            self,
            username: str,
            budget_id: int,
    ) -> bool:
        """Deletes budget with related categories and cash-flows"""
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

        await self.session.delete(budget)
        await self.session.commit()
        return True

    async def delete_category(
            self,
            username: str,
            budget_id: str,
            category_id: str,
    ) -> bool:
        """Deletes category with related cash-flows"""
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
        
        await self.session.delete(category)
        await self.session.commit()
        return True
    
    async def delete_cash_flow(
            self,
            username: str,
            budget_id: str,
            category_id: str,
            cash_flow_id: int,
    ) -> bool:
        """Deletes cash-flow"""
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
        
        await self.session.delete(cash_flow)
        await self.session.commit()
        return True