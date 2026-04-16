import json
from abc import ABC, abstractmethod
from typing import Any

from aidial_client import AsyncDial
from aidial_sdk.chat_completion import Message, Role, CustomContent
from pydantic import StrictStr

from tasks.t10_agent.app.tools.base import BaseTool
from tasks.t10_agent.app.tools.models import ToolCallParams


class DeploymentTool(BaseTool, ABC):

    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    @property
    @abstractmethod
    def deployment_name(self) -> str:
        pass

    @property
    def tool_parameters(self) -> dict[str, Any]:
        return {}

    async def _execute(self, tool_call_params: ToolCallParams) -> str | Message:
        # TODO: Call a DIAL deployment as a tool and collect the full streaming response.
        #
        #   1. Create an AsyncDial client:
        #      - base_url: self.endpoint
        #      - api_key: tool_call_params.api_key
        #      - api_version: "2025-01-01-preview"
        #
        #   2. Parse arguments from the tool call:
        #      - arguments = json.loads(tool_call_params.tool_call.function.arguments)
        #      - Extract "prompt" and delete it from arguments (remaining keys become configuration)
        #      - Update the stage header: tool_call_params.stage.append_name(f": {prompt}")
        #
        #   3. Stream from client.chat.completions.create():
        #      - messages: [{"role": "user", "content": prompt}]
        #      - stream: True
        #      - deployment_name: self.deployment_name
        #      - extra_body: {"custom_fields": {"configuration": {**arguments}}}
        #        (this forwards extra params like image `size` to the downstream deployment)
        #      - **self.tool_parameters  (unpack any extra call-level params from the subclass)
        #
        #   4. Iterate the stream; for each chunk:
        #      - Accumulate delta.content into a `content` string and append to stage
        #      - Collect delta.custom_content.attachments into a CustomContent object and
        #        mirror each attachment to the stage via stage.add_attachment(...)
        #
        #   5. Return:
        #      Message(role=Role.TOOL, content=StrictStr(content),
        #              custom_content=custom_content,
        #              tool_call_id=StrictStr(tool_call_params.tool_call.id))
        pass

