import time
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users_budgets import User, Budget, users_budgets
from models.cash_flows import CashFlow, CashFlowCategory
from services.delete_transactions import EntitiesDeleter


async def test_budget_deleting_with_income_category(
        db: AsyncSession,
        income_category: CashFlowCategory,
):
    """Tests deleting budget with income category"""
    is_deleted: bool = await EntitiesDeleter(session=db).delete_budget(
        username=income_category.budget.users[0].name,
        budget_id=income_category.budget.id,
    )
    assert is_deleted is True
    
    budget = await db.execute(select(Budget).limit(1))
    budget: Budget | None = budget.scalars().one_or_none()
    assert not budget

    category = await db.execute(select(CashFlowCategory).limit(1))
    category: CashFlowCategory | None = category.scalars().one_or_none()
    assert not category

async def test_budget_deleting_with_income_cash_flow(
        db: AsyncSession,
        income: CashFlow,
):
    """Tests deleting budget with income cash-flow"""
    is_deleted: bool = await EntitiesDeleter(session=db).delete_budget(
        username=income.category.budget.users[0].name,
        budget_id=income.category.budget.id,
    )
    assert is_deleted is True
    
    budget = await db.execute(select(Budget).limit(1))
    budget: Budget | None = budget.scalars().one_or_none()
    assert not budget

    category = await db.execute(select(CashFlowCategory).limit(1))
    category: CashFlowCategory | None = category.scalars().one_or_none()
    assert not category

    income = await db.execute(select(CashFlow).limit(1))
    income: CashFlow | None = income.scalar_one_or_none()
    assert not income

async def test_category_deleting_with_income_cash_flow(
        db: AsyncSession,
        income: CashFlow,
):
    """Tests deleting category with income cash-flows"""
    is_deleted: bool = await EntitiesDeleter(session=db).delete_category(
        username=income.category.budget.users[0].name,
        budget_id=income.category.budget.id,
        category_id=income.category.id,
    )
    assert is_deleted is True

    category = await db.execute(select(CashFlowCategory).limit(1))
    category: CashFlowCategory | None = category.scalars().one_or_none()
    assert not category

    income = await db.execute(select(CashFlow).limit(1))
    income: CashFlow | None = income.scalar_one_or_none()
    assert not income

async def test_cash_flow_deleting(
        db: AsyncSession,
        expense: CashFlow,
):
    """Tests deleting cash flow"""
    is_deleted: bool = await EntitiesDeleter(session=db).delete_cash_flow(
        username=expense.category.budget.users[0].name,
        budget_id=expense.category.budget.id,
        category_id=expense.category.id,
        cash_flow_id=expense.id,
    )
    assert is_deleted is True

    cash_flow = await db.execute(select(CashFlow).limit(1))
    cash_flow: CashFlow | None = cash_flow.scalar_one_or_none()
    assert not cash_flow

