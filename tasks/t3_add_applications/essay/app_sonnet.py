import uvicorn

from aidial_sdk import DIALApp

from tasks.t3_add_applications.essay.essay_assistant import EssayAssistantApplication

# TODO: Wire up the DIAL application.
#   1. Create a DIALApp instance and store it in `app`
#   2. Register EssayAssistantApplication("claude-sonnet-4-6") under deployment name "essay-assistant-sonnet"
#      using app.add_chat_completion(deployment_name=..., impl=...)
#   3. Add the if __name__ == "__main__": guard and run uvicorn on port 5026, host "0.0.0.0"