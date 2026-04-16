import asyncio
import json
from typing import Any

from aidial_client import AsyncDial
from aidial_sdk.chat_completion import Choice, Message, Role, Request, Response, ToolCall

from tasks.t4_stage_and_state.t2_calculator_agent.utils import StageProcessor, unpack_messages


TOOL_CALL_HISTORY_KEY = "tool_call_history"

SYSTEM_PROMPT = """You are a helpful AI assistant. You can:
1. Answer general knowledge questions and have conversations.
2. Perform mathematical calculations.

When asked to compute a numeric value, always use the `calculate` tool rather than answering from memory.
For general questions and conversations, respond directly without using any tools.
"""

class CalculatorAgent:

    def __init__(self, dial_core_url: str, tools: list):
        self.dial_core_url = dial_core_url
        self.tools = tools
        self._tools_dict: dict[str, Any] = {tool.name: tool for tool in tools}
        self.state: dict = {TOOL_CALL_HISTORY_KEY: []}

    async def handle_request(
        self, deployment_name: str, choice: Choice, request: Request
    ) -> Message:
        client: AsyncDial = AsyncDial(
            base_url=self.dial_core_url,
            api_key=request.api_key,
            api_version="2025-01-01-preview"
        )

        chunks = await client.chat.completions.create(
            messages=self._prepare_messages(request.messages),
            tools=[tool.schema for tool in self.tools],
            stream=True,
            deployment_name=deployment_name,
        )

        tool_call_index_map: dict = {}
        content = ""

        async for chunk in chunks:
            if not (chunk.choices and len(chunk.choices) > 0):
                continue
            delta = chunk.choices[0].delta
            if not delta:
                continue

            if delta.content:
                choice.append_content(delta.content)
                content += delta.content

            if delta.tool_calls:
                for tc_delta in delta.tool_calls:
                    if tc_delta.id:
                        # First chunk for this tool call — store it keyed by index
                        tool_call_index_map[tc_delta.index] = tc_delta
                    else:
                        # Subsequent chunks — accumulate arguments
                        tc = tool_call_index_map[tc_delta.index]
                        if tc_delta.function:
                            tc.function.arguments += tc_delta.function.arguments or ""

        assistant_message = Message(
            role=Role.ASSISTANT,
            content=content,
            tool_calls=[ToolCall.validate(tc) for tc in tool_call_index_map.values()] or None,
        )

        if assistant_message.tool_calls:
            tasks = [
                self._process_tool_call(tool_call=tc, choice=choice)
                for tc in assistant_message.tool_calls
            ]
            tool_messages: list[dict] = await asyncio.gather(*tasks)

            # TODO 2a: Persist this turn's exchange to state before recursing.
            #   - Append assistant_message.dict(exclude_none=True) to self.state[TOOL_CALL_HISTORY_KEY]
            #   - Extend self.state[TOOL_CALL_HISTORY_KEY] with tool_messages
            #   Then recurse so the model can produce its final answer using the tool results:
            #   return await self.handle_request(deployment_name=..., choice=..., request=...)

        # TODO 2b: No tool calls — the model produced its final answer.
        #   - Call choice.set_state(self.state) to persist tool call history for the next turn
        #   - Return assistant_message

    def _prepare_messages(self, messages: list[Message]) -> list[dict]:
        unpacked_messages = unpack_messages(
            messages=messages,
            current_state_history=self.state[TOOL_CALL_HISTORY_KEY],
            tool_call_history_key=TOOL_CALL_HISTORY_KEY
        )
        unpacked_messages.insert(
            0,
            {
                "role": Role.SYSTEM.value,
                "content": SYSTEM_PROMPT,
            }
        )

        print("\nHistory:")
        for msg in unpacked_messages:
            print(f"     {json.dumps(msg)}")

        print(f"{'-' * 100}\n")

        return unpacked_messages

    async def _process_tool_call(self, tool_call: ToolCall, choice: Choice) -> dict:
        # TODO 1: Wrap tool execution in a stage.
        #   - Open the stage: stage = StageProcessor.open_stage(choice, tool_call.function.name)
        #   - In a try block:
        #       - Look up the tool: tool = self._tools_dict[tool_call.function.name]
        #       - Append the arguments as a formatted JSON markdown block to the stage:
        #         f"## Arguments:\n```json\n{json.dumps(json.loads(tool_call.function.arguments), indent=2)}\n```\n\n"
        #       - Call: tool_message = await tool.execute(tool_call, stage)
        #   - In an except block: build a fallback Message(role=Role.TOOL, content=f"Error: {e}", tool_call_id=tool_call.id)
        #   - In a finally block: StageProcessor.close_stage_safely(stage)
        #   - return `tool_message.dict(exclude_none=True)`
        raise NotImplementedError()

