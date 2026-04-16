from typing import Any

from aidial_sdk.chat_completion import Message
from pydantic import StrictStr

from tasks.t10_agent.app.tools.deployment.base import DeploymentTool
from tasks.t10_agent.app.tools.models import ToolCallParams


class ImageGenerationTool(DeploymentTool):

    async def _execute(self, tool_call_params: ToolCallParams) -> str | Message:
        # TODO: Call the parent implementation, then render the generated image inline in Chat.
        #   1. Call msg = await super()._execute(tool_call_params) to get the base message with attachments
        #   2. If msg.custom_content and msg.custom_content.attachments is not empty:
        #      - For each attachment whose type is "image/png" or "image/jpeg":
        #          tool_call_params.choice.append_content(f"\n\r![image]({attachment.url})\n\r")
        #          This renders the image inline in the assistant message in Chat.
        #      - If msg.content is empty after the parent call, set a fixed content string telling the LLM
        #        that the image has already been shown and it should not attempt to display it again.
        #   3. Return msg
        pass

    @property
    def deployment_name(self) -> str:
        # TODO: Return the DIAL deployment name for the image generation model.
        #   Note: this is a model (not a custom application), showing that DeploymentTool
        #   works identically for both models and applications registered in DIAL Core.
        pass

    @property
    def name(self) -> str:
        # TODO: Return the tool identifier the LLM will use when calling this tool.
        pass

    @property
    def description(self) -> str:
        # TODO: Return a description of this tool for the LLM.
        #   Be precise: mention the available image sizes (enum), when to use this tool,
        #   and what kinds of requests are out of scope (e.g. data/chart visualizations).
        pass

    @property
    def parameters(self) -> dict[str, Any]:
        # TODO: Return a JSON Schema dict describing the tool's inputs.
        #   Include:
        #   - "prompt" (required string): extensive description of the image to generate
        #   - "size" (optional string): an enum of supported resolutions,
        #     e.g. ["1024x1024", "1024x1792", "1792x1024"], with a default value
        pass