from abc import ABC, abstractmethod
from typing import Any

from aidial_client.types.chat import ToolParam, FunctionParam
from aidial_client.types.chat.legacy.chat_completion import Role
from aidial_sdk.chat_completion import Message
from pydantic import StrictStr

from tasks.t10_agent.app.tools.models import ToolCallParams


class BaseTool(ABC):

    async def execute(self, tool_call_params: ToolCallParams) -> Message:
        # TODO: Implement the error-handling execute wrapper.
        #   1. Construct a base Message:
        #      msg = Message(role=Role.TOOL,
        #                    name=StrictStr(tool_call_params.tool_call.function.name),
        #                    tool_call_id=StrictStr(tool_call_params.tool_call.id))
        #   2. In a try block:
        #      - Call result = await self._execute(tool_call_params)
        #      - If result is already a Message instance: assign it directly to msg
        #      - Otherwise: set msg.content = StrictStr(result)
        #   3. In an except block (catch Exception as e):
        #      - Set msg.content to a descriptive error string
        #      - Append the error to the stage as a markdown code block:
        #        tool_call_params.stage.append_content(f"## Error:\n```markdown\n{e}\n```\n\n")
        #   4. Return msg
        pass

    @abstractmethod
    async def _execute(self, tool_call_params: ToolCallParams) -> str | Message:
        pass

    @property
    def show_in_stage(self) -> bool:
        return True

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def parameters(self) -> dict[str, Any]:
        pass

    @property
    def schema(self) -> ToolParam:
        return ToolParam(
            type="function",
            function=FunctionParam(
                name=self.name,
                description=self.description,
                parameters=self.parameters
            )
        )
