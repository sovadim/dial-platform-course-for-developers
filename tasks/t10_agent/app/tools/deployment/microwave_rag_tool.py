from typing import Any

from tasks.t10_agent.app.tools.deployment.base import DeploymentTool


class MicrowaveRagTool(DeploymentTool):

    @property
    def deployment_name(self) -> str:
        # TODO: Return the DIAL deployment name for the microwave RAG application.
        #   This must match the key registered in core/applications.json (built in task t6).
        pass

    @property
    def name(self) -> str:
        # TODO: Return the tool identifier the LLM will use when calling this tool.
        pass

    @property
    def description(self) -> str:
        # TODO: Return a description so the LLM knows when to call this tool.
        #   Describe that it searches through the microwave oven manual for relevant information.
        pass

    @property
    def parameters(self) -> dict[str, Any]:
        # TODO: Return a JSON Schema dict describing the tool's inputs.
        #   A single required "prompt" string is sufficient — it's what to search for in the manual.
        pass