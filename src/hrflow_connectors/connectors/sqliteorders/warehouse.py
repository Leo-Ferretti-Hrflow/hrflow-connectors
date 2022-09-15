import sqlite3
import typing as t
from logging import LoggerAdapter

from pydantic import BaseModel, Field

from hrflow_connectors.core import DataType, ReadMode, Warehouse, WarehouseReadAction


class ReadOrderParameters(BaseModel):
    db_name: str = Field(..., repr=False)


def read(
    adapter: LoggerAdapter,
    parameters: ReadOrderParameters,
    read_mode: t.Optional[ReadMode] = None,
    read_from: t.Optional[str] = None,
) -> t.Iterable[t.Dict]:
    connection = sqlite3.connect(parameters.db_name)
    query = (
        "SELECT id, product, quantity, updated_at FROM orders ORDER BY updated_at ASC;"
    )
    if read_mode is ReadMode.incremental and read_from is not None:
        # Making use of the last updated_at that was read in order to only fetch new items not already written to the target Warehouse
        query = (
            "SELECT id, product, quantity, updated_at FROM orders WHERE updated_at > {}"
            " ORDER BY updated_at ASC;".format(read_from)
        )
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        for order in cursor:
            yield dict(
                id=order[0], product=order[1], quantity=order[2], updated_at=order[3]
            )
    finally:
        cursor.close()
        connection.close()


SQLiteOrdersWarehouse = Warehouse(
    name="SQLiteOrdersWarehouse",
    data_type=DataType.other,
    read=WarehouseReadAction(
        parameters=ReadOrderParameters,
        function=read,
        # Set the boolean flag to True
        supports_incremental=True,
        item_to_read_from=lambda order: order["updated_at"],
    ),
)
