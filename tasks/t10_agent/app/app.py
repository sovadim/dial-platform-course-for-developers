from typing import Union

import uvicorn

from aidial_sdk import DIALApp
from aidial_sdk.chat_completion import (
    ChatCompletion, Request, Response
)
from aidial_sdk.deployment.configuration import ConfigurationRequest, ConfigurationResponse

from tasks.t10_agent.app.agent import Agent
from tasks.t10_agent.app.tools.deployment.essay_generation_tool import EssayGenerationTool
from tasks.t10_agent.app.tools.deployment.image_generation_tool import ImageGenerationTool
from tasks.t10_agent.app.tools.deployment.microwave_rag_tool import MicrowaveRagTool

_DIAL_CORE_URL="http://localhost:8080"

class FinalTaskAgentApplication(ChatCompletion):

    async def chat_completion(self, request: Request, response: Response) -> None:
        # TODO 1: Open a single-choice response and start the agentic loop.
        #   - Use `with response.create_single_choice() as choice:`
        #   - Inside, create Agent(dial_core_url=_DIAL_CORE_URL, tools=[...]) with all three tools:
        #       ImageGenerationTool(_DIAL_CORE_URL)
        #       EssayGenerationTool(_DIAL_CORE_URL)
        #       MicrowaveRagTool(_DIAL_CORE_URL)
        #   - Call: await agent.handle_request(deployment_name="gpt-5.2", choice=choice, request=request)
        pass

    async def configuration(self, request: ConfigurationRequest) -> Union[ConfigurationResponse, dict]:
        return {
            "type": "object",
            "properties": {
                "conversation_starter_button": {
                    "description": "Conversation starters",
                    "type": "number",
                    "dial:widget": "buttons",
                    "oneOf": [
                        {
                            "const": 1,
                            "title": "Calculate 3943232/4902*323",
                            "dial:widgetOptions": {"populateText": "Calculate 3943232/4902*323"}
                        },
                        {
                            "const": 2,
                            "title": "Generate 3 red dots",
                            "dial:widgetOptions": {"populateText": "Generate picture with 3 small red dots on the white background"}
                        }
                    ]
                }
            }
        }


# TODO 2: Wire up the DIAL app.
#   1. Create a DIALApp instance and store it in `app`
#   2. Register FinalTaskAgentApplication() under deployment name "final-task-agent"
#      using app.add_chat_completion(...)
#   3. Add the if __name__ == "__main__": guard and run uvicorn on port 5032, host "0.0.0.0"
