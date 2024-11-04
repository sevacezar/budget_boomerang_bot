from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users_budgets import User, Budget, users_budgets
from models.cash_flows import CashFlow, CashFlowCategory
from services.update_transactions import EntitiesUpdater

async def test_budget_update_name(
        db: AsyncSession,
        budget: Budget,
):
    """Tests name updating of budget"""
    new_budget_name: str = 'New Budget'
    budget: Budget = await EntitiesUpdater(session=db).update_budget_name(
        username=budget.users[0].name,
        budget_id=budget.id,
        new_budget_name=new_budget_name,
    )

    budget = await db.execute(select(Budget).limit(1))
    budget: Budget | None = budget.scalars().one_or_none()
    assert budget

    assert budget.name == new_budget_name


async def test_category_update_name(
        db: AsyncSession,
        expense_category: CashFlowCategory,
):
    """Tests name updating of category"""
    new_category_name: str = 'Mega shopping'
    category: CashFlowCategory = await EntitiesUpdater(session=db).update_category_name(
        username=expense_category.budget.users[0].name,
        budget_id=expense_category.budget.id,
        category_id=expense_category.id,
        new_category_name=new_category_name,
    )

    category = await db.execute(select(CashFlowCategory).limit(1))
    category: CashFlowCategory | None = category.scalars().one_or_none()
    assert category

    assert category.name == new_category_name

async def test_cash_flow_update_value(
        db: AsyncSession,
        expense: CashFlow,
):
    """Tests value updating of cash-flow"""
    update_params: dict = {'value': 1234567.12}
    cash_flow: CashFlow = await EntitiesUpdater(session=db).update_cash_flow(
        username=expense.category.budget.users[0].name,
        budget_id=expense.category.budget_id,
        category_id=expense.category_id,
        cash_flow_id=expense.id,
        params=update_params,
    )
    assert cash_flow
    assert cash_flow.value == update_params.get('value')

async def test_cash_flow_update_description(
        db: AsyncSession,
        expense: CashFlow,
):
    """Tests description updating of cash-flow"""
    update_params: dict = {'description': 'New description'}
    cash_flow: CashFlow = await EntitiesUpdater(session=db).update_cash_flow(
        username=expense.category.budget.users[0].name,
        budget_id=expense.category.budget_id,
        category_id=expense.category_id,
        cash_flow_id=expense.id,
        params=update_params,
    )
    assert cash_flow
    assert cash_flow.description == update_params.get('description')

async def test_cash_flow_update_value_and_description(
        db: AsyncSession,
        expense: CashFlow,
):
    """Tests value and description updating of cash-flow"""
    update_params: dict = {'value': 1234567.12, 'description': 'New description'}
    cash_flow: CashFlow = await EntitiesUpdater(session=db).update_cash_flow(
        username=expense.category.budget.users[0].name,
        budget_id=expense.category.budget_id,
        category_id=expense.category_id,
        cash_flow_id=expense.id,
        params=update_params,
    )
    assert cash_flow
    assert cash_flow.value == update_params.get('value')
    assert cash_flow.description == update_params.get('description')