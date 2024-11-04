from models.users_budgets import User, Budget
from models.cash_flows import CashFlow, CashFlowCategory


def get_entity_from_list(
        entities: list[Budget | CashFlow | CashFlowCategory],
        name: str | None = None,
        id: int | None = None,
) -> Budget | CashFlow | CashFlowCategory | None:
    """Get entity by entity name among list of entities"""

    if not entities:
        return None

    if id:
        entities_filtered: list = list(
            filter(
                lambda x: x.id == id,
                entities,
            )
        )
    elif name:
        entities_filtered: list = list(
            filter(
                lambda x: x.name == name,
                entities,
            )
        )
    else:
        return None

    if entities_filtered:
        return entities_filtered[0]
    else:
        return None
