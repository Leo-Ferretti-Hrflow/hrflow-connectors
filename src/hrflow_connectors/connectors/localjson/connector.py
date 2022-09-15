from hrflow_connectors.connectors.hrflow.warehouse import (
    HrFlowJobWarehouse,
    HrFlowProfileWarehouse,
)
from hrflow_connectors.connectors.localjson.warehouse import LocalJSONWarehouse
from hrflow_connectors.core import (
    BaseActionParameters,
    Connector,
    ConnectorAction,
    WorkflowType,
)

LocalJSON = Connector(
    name="LocalJSON",
    description="Read from JSON, Write to JSON",
    url="https://localjson.ai",
    actions=[
        ConnectorAction(
            name="pull_jobs",
            trigger_type=WorkflowType.pull,
            description="Send jobs from local JSON file to a ***Hrflow.ai Board***.",
            parameters=BaseActionParameters,
            origin=LocalJSONWarehouse,
            target=HrFlowJobWarehouse,
        ),
        ConnectorAction(
            name="push_profile",
            trigger_type=WorkflowType.catch,
            description="Push a profile from a Hrflow.ai Source to a local JSON file",
            parameters=BaseActionParameters,
            origin=HrFlowProfileWarehouse,
            target=LocalJSONWarehouse,
        ),
    ],
)

