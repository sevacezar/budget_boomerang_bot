from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users_budgets import User, Budget, users_budgets
from models.cash_flows import CashFlow, CashFlowCategory
from services.get_transactions import EntitiesGetter

async def test_get_user_by_name(
        db: AsyncSession,
        user: User,
):
    """Tests getting user by username"""
    test_user: User = await EntitiesGetter(session=db).get_user_by_name(
        name=user.name,
    )
    assert test_user
    assert test_user == user

async def test_get_user_by_name_with_budget(
        db: AsyncSession,
        budget: Budget,
):
    """Tests getting user with related budgets"""
    test_user: User = await EntitiesGetter(session=db).get_user_by_name(
        name=budget.users[0].name,
        get_related_budgets=True,
    )
    assert test_user
    assert test_user == budget.users[0]

    assert test_user.budgets
    assert test_user.budgets[0]
    assert test_user.budgets[0] == budget

async def test_get_user_by_name_with_category(
        db: AsyncSession,
        expense_category: CashFlowCategory,
):
    """Tests getting user with related budgets and categories"""
    test_user: User = await EntitiesGetter(session=db).get_user_by_name(
        name=expense_category.budget.users[0].name,
        get_related_categories=True,
    )
    assert test_user
    assert test_user == expense_category.budget.users[0]

    assert test_user.budgets
    assert test_user.budgets[0]
    assert test_user.budgets[0] == expense_category.budget

    assert test_user.budgets[0].cash_flow_categories
    assert test_user.budgets[0].cash_flow_categories[0]
    assert test_user.budgets[0].cash_flow_categories[0] == expense_category

async def test_get_user_by_name_with_cash_flows(
        db: AsyncSession,
        expense: CashFlow,
):
    """Tests getting user with related budgets, categories, expenses"""
    test_user: User = await EntitiesGetter(session=db).get_user_by_name(
        name=expense.category.budget.users[0].name,
        get_related_cash_flows=True,
    )
    assert test_user
    assert test_user == expense.category.budget.users[0]

    assert test_user.budgets
    assert test_user.budgets[0]
    assert test_user.budgets[0] == expense.category.budget

    assert test_user.budgets[0].cash_flow_categories
    assert test_user.budgets[0].cash_flow_categories[0]
    assert test_user.budgets[0].cash_flow_categories[0] == expense.category

    assert test_user.budgets[0].cash_flow_categories[0].cash_flows
    assert test_user.budgets[0].cash_flow_categories[0].cash_flows[0]
    assert test_user.budgets[0].cash_flow_categories[0].cash_flows[0] == expense


async def test_get_all_budgets_by_username(
        db: AsyncSession,
        budget: Budget,
):
    """Tests getting all budgets of user"""
    username: str = budget.users[0].name
    budgets: list[Budget] = await EntitiesGetter(session=db).get_all_budgets_by_username(
        username=username,
    )
    assert budgets
    assert isinstance(budgets, list)
    assert budgets[0] == budget

async def test_get_all_budgets_by_username_with_categories(
        db: AsyncSession,
        expense_category: CashFlowCategory,
):
    """Tests getting all budgets of user with related categories"""
    username: str = expense_category.budget.users[0].name
    budgets: list[Budget] = await EntitiesGetter(session=db).get_all_budgets_by_username(
        username=username,
        get_related_categories=True,
    )
    assert budgets
    assert isinstance(budgets, list)
    assert budgets[0] == expense_category.budget

    assert budgets[0].cash_flow_categories
    assert budgets[0].cash_flow_categories[0] == expense_category

async def test_get_all_budgets_by_username_with_cash_flows(
        db: AsyncSession,
        expense: CashFlow,
):
    """Tests getting all budgets of user with related categories and cash_flows"""
    username: str = expense.category.budget.users[0].name
    budgets: list[Budget] = await EntitiesGetter(session=db).get_all_budgets_by_username(
        username=username,
        get_related_cash_flows=True,
    )
    assert budgets
    assert isinstance(budgets, list)
    assert budgets[0] == expense.category.budget

    assert budgets[0].cash_flow_categories
    assert budgets[0].cash_flow_categories[0] == expense.category

    assert budgets[0].cash_flow_categories[0].cash_flows
    assert budgets[0].cash_flow_categories[0].cash_flows[0] == expense

async def test_get_budget_by_id(
        db: AsyncSession,
        expense: CashFlow,
):
    """Tests getting budget by id with related categories and cash-flows"""
    id: int = expense.category.budget.id
    budget: Budget = await EntitiesGetter(session=db).get_budget_by_id(
        id=id,
        get_related_cash_flows=True,
    )
    assert budget
    assert budget == expense.category.budget

    assert budget.cash_flow_categories
    assert budget.cash_flow_categories[0] == expense.category

    assert budget.cash_flow_categories[0].cash_flows
    assert budget.cash_flow_categories[0].cash_flows[0] == expense

async def test_get_income_categories_by_budget_id(
        db: AsyncSession,
        income: CashFlow,
):
    """Tests getting all income categories of soecific budget by budget id"""
    id: int = income.category.budget.id
    categories: list[CashFlowCategory] = await EntitiesGetter(session=db).get_categories_by_budget_id(
        id=id,
        category_type='income',
        get_related_cash_flows=True,
    )

    assert categories
    assert isinstance(categories, list)

    assert all(map(lambda x: not x.is_expense, categories))

    assert categories[0].cash_flows
    assert categories[0].cash_flows[0] == income


async def test_get_expense_categories_by_budget_id(
        db: AsyncSession,
        expense: CashFlow,
):
    """Tests getting all expense categories of specific budget by budget id"""
    id: int = expense.category.budget.id
    categories: list[CashFlowCategory] = await EntitiesGetter(session=db).get_categories_by_budget_id(
        id=id,
        category_type='expense',
        get_related_cash_flows=True,
    )

    assert categories
    assert isinstance(categories, list)

    assert all(map(lambda x: x.is_expense, categories))

    assert categories[0].cash_flows
    assert categories[0].cash_flows[0] == expense

async def test_get_category_by_id(
        db: AsyncSession,
        expense: CashFlow,
):
    """Tests getting category by id with related cash-flows"""
    id: int = expense.category_id
    category: CashFlowCategory = await EntitiesGetter(session=db).get_category_by_id(
        id=id,
        get_related_cash_flows=True,
    )
    assert category
    assert category == expense.category
    assert category.cash_flows
    assert category.cash_flows[0] == expense

async def test_get_cash_flows_by_category_id(
        db: AsyncSession,
        expense: CashFlow,
):
    """Tests getting all cash-flows in category"""
    id: int = expense.category.id
    expenses: list[CashFlow] = await EntitiesGetter(session=db).get_cash_flows_by_category_id(
        id=id,
    )
    assert expenses
    assert isinstance(expenses, list)
    assert expenses[0] == expense

# async def test_get_all_expenses_summ_for_period(
#         db: AsyncSession,
#         expense_category: CashFlowCategory,
# ):
#     """Tests getting summ of all expenses in budget in specific period"""
#     value_1, value_2 = 1000.12, 2000.99
#     created_at_1, created_at_2 = datetime(2024, 9, 13, 12), datetime(2024, 9, 16, 10)
#     expense_1: CashFlow = CashFlow(
#         value=value_1,
#         created_at=created_at_1,
#     )
#     expense_2: CashFlow = CashFlow(
#         value=value_2,
#         created_at=created_at_2,
#     )
#     expense_category.cash_flows.extend([expense_1, expense_2])
#     db.add_all([expense_1, expense_2])
#     await db.commit()

    # expenses_summ: float = await EntitiesGetter(session=db).get_all_cash_flows_summ_for_period(
    #     budget_id=expense_category.budget_id,


    # )