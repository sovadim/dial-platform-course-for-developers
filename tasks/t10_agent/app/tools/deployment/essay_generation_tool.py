from typing import Any

from tasks.t10_agent.app.tools.deployment.base import DeploymentTool


class EssayGenerationTool(DeploymentTool):

    @property
    def deployment_name(self) -> str:
        # TODO: Return the DIAL deployment name for the essay assistant.
        #   This must match the key registered in core/applications.json (e.g. "essay-assistant-gpt").
        pass

    @property
    def name(self) -> str:
        # TODO: Return the tool identifier the LLM will reference when calling this tool.
        #   Use a descriptive snake_case string (e.g. "essay_generation_tool").
        pass

    @property
    def description(self) -> str:
        # TODO: Return a plain-English description of what this tool does.
        #   The LLM reads this at inference time to decide when to invoke it — be specific.
        pass

    @property
    def parameters(self) -> dict[str, Any]:
        # TODO: Return a JSON Schema dict describing the tool's inputs.
        #   At minimum include a required "prompt" string property that describes the essay to generate.
        #   Schema structure:
        #     {"type": "object", "properties": {"prompt": {"type": "string", "description": "..."}}, "required": ["prompt"]}
        pass