from hrflow_connectors.connectors.localjson.warehouse import LocalJSONWarehouse
from hrflow_connectors.connectors.sqliteorders.warehouse import SQLiteOrdersWarehouse
from hrflow_connectors.core import (
    BaseActionParameters,
    Connector,
    ConnectorAction,
    WorkflowType,
)

SQLiteOrders = Connector(
    name="SQLiteOrders",
    description="Read from SQLite, Write to JSON",
    url="https://sqliteorder.ai",
    actions=[
        ConnectorAction(
            name="pull_orders",
            trigger_type=WorkflowType.pull,
            description="Send orders from SQLite to JSON file.",
            parameters=BaseActionParameters,
            origin=SQLiteOrdersWarehouse,
            target=LocalJSONWarehouse,
        ),
    ],
)