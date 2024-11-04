from sqlalchemy.ext.asyncio import AsyncSession

from models.users_budgets import User, Budget, users_budgets
from models.cash_flows import CashFlow, CashFlowCategory
from services.create_transactions import EntitiesCreator

async def test_user_creating(db: AsyncSession):
    """Tests creation some user"""
    name: str = 'Test_user'
    user = await EntitiesCreator(session=db).create_user(
        username=name,
    )

    assert user
    assert user.id == 1
    assert user.name == name

async def test_budget_creating(
        db: AsyncSession,
        user: User,
    ):
    """Tests creation some budget"""
    
    budget_name: str = 'Some budget'
    budget: Budget = await EntitiesCreator(session=db).create_budget(
        username=user.name,
        budget_name=budget_name,
    )

    assert budget
    assert budget.id == 1
    assert budget.name == budget_name
    assert budget.users[0] == user 


async def test_income_category_creating(
        db: AsyncSession,
        budget: Budget,
):
    """Tests creation income category of budget"""
    category_name: str = 'Salary'
    income_category: CashFlowCategory = await EntitiesCreator(session=db).create_cash_flow_category(
        username=budget.users[0].name,
        budget_id=budget.id,
        category_name=category_name,
        is_income_category=True,
    )

    assert income_category
    assert income_category.id == 1
    assert income_category.name == category_name
    assert income_category.is_expense == False
    assert income_category.budget == budget

async def test_expense_category_creating(
        db: AsyncSession,
        budget: Budget,
):
    """Tests creation expense category of budget"""
    category_name: str = 'Shopping'
    expense_category: CashFlowCategory = await EntitiesCreator(session=db).create_cash_flow_category(
        username=budget.users[0].name,
        budget_id=budget.id,
        category_name=category_name,
        is_income_category=False,
    )

    assert expense_category
    assert expense_category.id == 1
    assert expense_category.name == category_name
    assert expense_category.is_expense == True
    assert expense_category.budget == budget

async def test_income_cash_flow_creating(
        db: AsyncSession,
        income_category: CashFlowCategory,
):
    """Tests creation income cash flow"""
    value: float = 1000.1234
    description: str = 'Work'
    income: CashFlow = await EntitiesCreator(session=db).create_cash_flow(
        username=income_category.budget.users[0].name,
        budget_id=income_category.budget.id,
        category_id=income_category.id,
        value=value,
        description=description,
    )

    assert income
    assert income.id == 1
    assert income.value == value
    assert income.description == description
    assert income.category == income_category

async def test_expense_cash_flow_creating(
        db: AsyncSession,
        expense_category: CashFlowCategory,
):
    """Tests creation expense cash flow"""
    value: float = 1000.1234
    description: str = 'Club'
    expense: CashFlow = await EntitiesCreator(session=db).create_cash_flow(
        username=expense_category.budget.users[0].name,
        budget_id=expense_category.budget.id,
        category_id=expense_category.id,
        value=value,
        description=description,
    )

    assert expense
    assert expense.id == 1
    assert expense.value == -value
    assert expense.description == description
    assert expense.category == expense_category
