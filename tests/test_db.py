from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from models.users_budgets import User, Budget, users_budgets
from models.cash_flows import CashFlow, CashFlowCategory


async def test_user_adding(db: AsyncSession):
    """Test creation some user in DB"""
    name: str = 'Test_user'
    created_at: datetime = datetime.now()
    user = User(name=name, created_at=created_at)
    db.add(user)
    await db.commit()

    res = await db.execute(select(User))
    user = res.scalars().first()
    assert user.id == 1
    assert user.name == name
    assert user.created_at == created_at


async def test_budget_adding(db: AsyncSession):
    """Test creation some budget in DB"""
    name: str = 'family'
    created_at: datetime = datetime.now()
    budget: Budget = Budget(name=name, created_at=created_at)
    db.add(budget)
    await db.commit()

    res = await db.execute(select(Budget).options(selectinload(Budget.cash_flow_categories)))
    budget = res.scalars().first()
    assert budget.id == 1
    assert budget.name == name
    assert budget.created_at == created_at
    assert not budget.is_archived
    assert not budget.cash_flow_categories

async def test_adding_common_budget_on_different_users(db: AsyncSession):
    """Test creation two users and one common budget"""
    user1: User = User(name='Stive')
    user2: User = User(name='Jack')
    budget: Budget = Budget(name='common')
    budget.users.extend([user1, user2])
    db.add(budget)
    await db.commit()
    
    res = await db.execute(select(Budget).options(selectinload(Budget.users)))
    budget = res.scalars().first()
    users = budget.users
    assert users
    assert len(users) == 2
    assert users[0].name == 'Stive'
    assert users[1].name == 'Jack'

async def test_adding_common_user_on_different_budgets(db: AsyncSession):
    """Test creation two budgets and ine common user"""
    user: User = User(name='common')
    budget1: Budget = Budget(name='one')
    budget2: Budget = Budget(name='two')

    user.budgets.extend([budget1, budget2])
    db.add(user)
    await db.commit()
    
    res = await db.execute(select(User).options(selectinload(User.budgets)))
    user = res.scalars().first()
    budgets = user.budgets
    assert budgets
    assert len(budgets) == 2
    assert budgets[0].name == 'one'
    assert budgets[1].name == 'two'

async def test_incomes_category_adding(db: AsyncSession):
    """Test creation incomes category"""
    budget: Budget = Budget(name='some')

    category_name = 'Salary'
    incomes_category: CashFlowCategory = CashFlowCategory(
        name=category_name,
        is_expense=False,
    )
    incomes_category.budget = budget
    db.add(incomes_category)
    await db.commit()

    res = await db.execute(select(CashFlowCategory))
    incomes_category = res.scalars().first()
    assert incomes_category
    assert incomes_category.name == category_name

async def test_expenses_category_adding(db: AsyncSession):
    """Test creation expenses category"""
    budget: Budget = Budget(name='some')

    category_name = 'Shoping'
    expenses_category: CashFlowCategory = CashFlowCategory(
        name=category_name,
        is_expense=True,
    )
    expenses_category.budget = budget
    db.add(expenses_category)
    await db.commit()

    res = await db.execute(select(CashFlowCategory))
    expenses_category = res.scalars().first()
    assert expenses_category
    assert expenses_category.name == category_name

async def test_income_adding(db: AsyncSession):
    """Test creation income"""
    budget_name: str = 'some'
    budget: Budget = Budget(name=budget_name)

    category_name: str = 'Salary'
    incomes_category: CashFlowCategory = CashFlowCategory(
        name=category_name,
        is_expense=False,
    )
    incomes_category.budget = budget

    value = 100000
    description = 'Some description'
    income = CashFlow(
        value=value,
        description=description,
    )
    income.category = incomes_category
    db.add(income)
    await db.commit()

    res = await db.execute(select(CashFlow).options(
        joinedload(CashFlow.category),
        )
    )
    income = res.scalars().first()
    assert income
    assert (income.value, income.description) == (value, description)
    assert income.category.name == category_name

async def test_expense_adding(db: AsyncSession):
    """Test creation income"""
    budget_name: str = 'some'
    budget: Budget = Budget(name=budget_name)

    category_name: str = 'Shoping'
    expenses_category: CashFlowCategory = CashFlowCategory(
        name=category_name,
        is_expense=True,
    )
    expenses_category.budget = budget

    value = -10000
    description = 'Some description'
    expense = CashFlow(
        value=value,
        description=description,
    )
    expense.category = expenses_category
    db.add(expense)
    await db.commit()

    res = await db.execute(select(CashFlow).options(
        joinedload(CashFlow.category),
        )
    )
    expense = res.scalars().first()
    assert expense
    assert (expense.value, expense.description) == (value, description)
    assert expense.category.name == category_name
