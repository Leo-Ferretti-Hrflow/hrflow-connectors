import json
import typing as t
from json import JSONDecodeError
from logging import LoggerAdapter
from pathlib import Path

from pydantic import BaseModel, Field, FilePath

from hrflow_connectors.core import (
    DataType,
    ReadMode,
    Warehouse,
    WarehouseReadAction,
    WarehouseWriteAction,
)


class ReadJsonParameters(BaseModel):
    path: FilePath = Field(..., description="Path to JSON file to read")


def read(
    adapter: LoggerAdapter,
    parameters: ReadJsonParameters,
    read_mode: t.Optional[ReadMode] = None,
    read_from: t.Optional[str] = None,
) -> t.Iterable[t.Dict]:
    # Because of validation happening in ReadJsonParameters
    # no need to handle FileNotFoundError
    try:
        with open(parameters.path, "r") as f:
            data = json.load(f)
    except JSONDecodeError as e:
        message = "Invalid JSON file. Failed to decode with error {}".format(repr(e))
        adapter.error(message)
        raise Exception(message)

    if isinstance(data, list):
        for item in data:
            yield item
    else:
        yield data


class WriteJsonParameters(BaseModel):
    path: Path = Field(..., description="Path where to save JSON file")
    mode: t.Optional[t.Literal["append", "erase"]] = "erase"


def write(
    adapter: LoggerAdapter, parameters: WriteJsonParameters, items: t.Iterable[t.Dict]
) -> t.List[t.Dict]:
    failed_items = []
    items = list(items)
    try:
        if parameters.mode == "erase":
            with open(parameters.path, "w") as f:
                json.dump(items, f)
        else:
            try:
                with open(parameters.path, "r") as f:
                    old_items = json.load(f)
            except FileNotFoundError:
                old_items = []
            old_items.extend(items)
            with open(parameters.path, "w") as f:
                json.dump(old_items, f)
    # More error handling can be added to cope with file permissions for example
    except TypeError as e:
        message = "Failed to JSON encode provided items with error {}".format(repr(e))
        adapter.error(message)
        failed_items = items

    return failed_items


LocalJSONWarehouse = Warehouse(
    name="LocalJSONWarehouse",
    data_type=DataType.other,
    read=WarehouseReadAction(
        parameters=ReadJsonParameters,
        function=read,
    ),
    write=WarehouseWriteAction(
        parameters=WriteJsonParameters,
        function=write,
    ),
)
