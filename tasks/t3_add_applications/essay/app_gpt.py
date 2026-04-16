import uvicorn

from aidial_sdk import DIALApp

from tasks.t3_add_applications.essay.essay_assistant import EssayAssistantApplication

# TODO: Wire up the DIAL application.
#   1. Create a DIALApp instance and store it in `app`
#   2. Register EssayAssistantApplication("gpt-5.2") under deployment name "essay-assistant-gpt"
#      using app.add_chat_completion(deployment_name=..., impl=...)

app: DIALApp = None


if __name__ == "__main__":
    uvicorn.run(app, port=5025, host="0.0.0.0")