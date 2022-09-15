
# Pull orders
`SQLiteOrdersWarehouse` :arrow_right: `LocalJSONWarehouse`

Send orders from SQLite to JSON file.



## Action Parameters

| Field | Type | Default | Description |
| ----- | ---- | ------- | ----------- |
| `logics`  | `typing.List[typing.Callable[[typing.Dict], typing.Optional[typing.Dict]]]` | [] | List of logic functions |
| `format`  | `typing.Callable[[typing.Dict], typing.Dict]` | [`<lambda>`](../../../core/connector.py#L180) | Formatting function |
| `read_mode`  | `str` | ReadMode.sync | If 'incremental' then `read_from` of the last run is given to Origin Warehouse during read. **The actual behavior depends on implementation of read**. In 'sync' mode `read_from` is neither fetched nor given to Origin Warehouse during read. |

## Source Parameters

| Field | Type | Default | Description |
| ----- | ---- | ------- | ----------- |
| `db_name` :red_circle: | `str` | None |  |

## Destination Parameters

| Field | Type | Default | Description |
| ----- | ---- | ------- | ----------- |
| `path` :red_circle: | `Path` | None | Path where to save JSON file |
| `mode`  | `Literal` | erase |  |

:red_circle: : *required*

## Example

```python
import logging
from hrflow_connectors import SQLiteOrders
from hrflow_connectors.core import ReadMode


logging.basicConfig(level=logging.INFO)


SQLiteOrders.pull_orders(
    workflow_id="some_string_identifier",
    action_parameters=dict(
        logics=[],
        format=lambda *args, **kwargs: None # Put your code logic here,
        read_mode=ReadMode.sync,
    ),
    origin_parameters=dict(
        db_name="your_db_name",
    ),
    target_parameters=dict(
        path=***,
        mode=erase,
    )
)
```