import os
import sys
from typing import Any, AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from  sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from database import Base
from models.users_budgets import User, Budget
from models.cash_flows import CashFlow, CashFlowCategory

DATABASE_URL_TESTS = 'postgresql+asyncpg://postgres:postgres@localhost:5433/test'

engine = create_async_engine(
    url=DATABASE_URL_TESTS,
    poolclass=NullPool,
    )

async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    )

@pytest.fixture(scope='function', autouse=True)
async def setup_database():
    """Setup database every test"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope='function')
async def db() -> AsyncGenerator[AsyncSession, Any]:
    """Generate DB-session"""
    async with async_session() as session:
        yield session

@pytest.fixture(scope='function')
async def user(db: AsyncSession) -> User:
    """Creates user for tests"""
    user = User(name='Test user')
    db.add(user)
    await db.commit()
    return user

@pytest.fixture(scope='function')
async def budget(
    db: AsyncSession,
    user: User,
) -> Budget:
    """Creates budget for tests"""
    budget: Budget = Budget(name='Family budget')
    budget.users.append(user)
    db.add(budget)
    await db.commit()
    return budget

@pytest.fixture(scope='function')
async def income_category(
    db: AsyncSession,
    budget: Budget,
) -> CashFlowCategory:
    """Creates income category for tests"""
    category_name: str = 'Salary'
    income_category: CashFlowCategory = CashFlowCategory(
        name=category_name,
        is_expense=False,
    )
    income_category.budget = budget
    db.add(income_category)
    await db.commit()
    return income_category

@pytest.fixture(scope='function')
async def expense_category(
    db: AsyncSession,
    budget: Budget,
) -> CashFlowCategory:
    """Creates expense category for tests"""
    category_name: str = 'Shopping'
    expense_category: CashFlowCategory = CashFlowCategory(
        name=category_name,
        is_expense=True,
    )
    expense_category.budget = budget
    db.add(expense_category)
    await db.commit()
    return expense_category


@pytest.fixture(scope='function')
async def income(
    db: AsyncSession,
    income_category: CashFlowCategory,
) -> CashFlow:
    """Creates income for tests"""
    income: CashFlow = CashFlow(
        value=1000.12,
    )
    income.category = income_category
    db.add(income)
    await db.commit()
    return income


@pytest.fixture(scope='function')
async def expense(
    db: AsyncSession,
    expense_category: CashFlowCategory,
) -> CashFlow:
    """Creates expense for tests"""
    expense: CashFlow = CashFlow(
        value=999.10,
    )
    expense.category = expense_category
    db.add(expense)
    await db.commit()
    return expense
