import uvicorn

from aidial_sdk import DIALApp
from aidial_sdk.chat_completion import (
    ChatCompletion, Request, Response
)

from tasks.t4_stage_and_state.t2_calculator_agent.agent import CalculatorAgent
from tasks.t4_stage_and_state.t2_calculator_agent.calculator_tool import CalculateTool


class CalculatorAgentApplication(ChatCompletion):

    async def chat_completion(self, request: Request, response: Response) -> None:
        with response.create_single_choice() as choice:
            # TODO: Instantiate CalculatorAgent and run the agentic loop.
            #   - Create CalculatorAgent(dial_core_url="http://localhost:8080", tools=[CalculateTool()])
            #   - Call await agent.handle_request(deployment_name="gpt-5.2", choice=choice, request=request)
            raise NotImplementedError()


# TODO: Wire up the DIAL app.
#   1. Create a DIALApp instance and store it in `app`
#   2. Register CalculatorAgentApplication() under deployment name "calculator-agent"
#      using app.add_chat_completion(...)
#   3. Add the if __name__ == "__main__": guard and run uvicorn on port 5028, host "0.0.0.0"