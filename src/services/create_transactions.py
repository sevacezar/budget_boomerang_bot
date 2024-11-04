from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import DbException, TgException
from models.users_budgets import User, Budget
from models.cash_flows import CashFlow, CashFlowCategory
from services.get_transactions import EntitiesGetter
from services.utils import get_entity_from_list


class EntitiesCreator:
    """Class with functions of creating entities"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(
        self,
        username: str,
    ) -> User:
        """Creates new user"""

        user: User | None = await EntitiesGetter(session=self.session).get_user_by_name(
            name=username,
        )

        if user:
            raise DbException(f'User {username} already exists in DB')
        
        user = User(name=username)
        self.session.add(user)
        await self.session.commit()

        return user

    async def create_budget(
            self,
            username: str,
            budget_name: str,
    ) -> Budget:
        """Create new budget"""

        user: User | None = await EntitiesGetter(session=self.session).get_user_by_name(
            name=username,
            get_related_budgets=True,
        )
        
        if not user:
            raise DbException(f'User {username} not found')
        
        existing_budget: Budget | None = get_entity_from_list(
            entities=user.budgets,
            name=budget_name,
        )

        if existing_budget:
            raise TgException("User already has budget with same name")
        else:
            budget: Budget = Budget(name=budget_name)
            budget.users.append(user)
            self.session.add(budget)
            await self.session.commit()
            return budget

    async def create_cash_flow_category(
        self,
        username: str,
        budget_id: int,
        category_name: str,
        is_income_category: bool = False,
    ):
        """Create new cash-flow category"""

        user: User | None = await EntitiesGetter(session=self.session).get_user_by_name(
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
            raise DbException(f'Budget with id {budget_id} not found')

        existing_category: CashFlowCategory | None = get_entity_from_list(
            entities=budget.cash_flow_categories,
            name=category_name,
        )

        if existing_category:
            raise TgException("Budget already has category with same name")
        else:
            category: CashFlowCategory = CashFlowCategory(name=category_name)
            
            if is_income_category:
                category.is_expense = False
            else:
                category.is_expense = True

            category.budget = budget
            self.session.add(category)
            await self.session.commit()
            return category
        

    async def create_cash_flow(
        self,
        username: str,
        budget_id: int,
        category_id: int,
        value: Decimal,
        description: str,
    ):
        """Create new cash-flow"""

        user: User | None = await EntitiesGetter(session=self.session).get_user_by_name(
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
            raise DbException(f'Budget with id {budget_id} not found')

        category: CashFlowCategory | None = get_entity_from_list(
            entities=budget.cash_flow_categories,
            id=category_id,
        )

        if not category:
            raise DbException(f'Category with id {category_id} not found')
        
        if not isinstance(value, (Decimal, float, int)):
            raise TgException('Value of value-param is invalid')
        
        value = abs(value)
        if category.is_expense:
            value = -value
        
        cash_flow: CashFlow = CashFlow(
            value=value,
            description=description,
        )
        cash_flow.category = category

        self.session.add(cash_flow)
        await self.session.commit()
        return cash_flow

# TODO: add tests with adding existing entities and addind other behavior