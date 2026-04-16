import json

import uvicorn
from aidial_client import AsyncDial
from aidial_sdk import DIALApp
from aidial_sdk.chat_completion import ChatCompletion, Request, Response

SYSTEM_PROMPT = """You are a poetry-focused assistant. Respond to every request by writing a **short poem** of up to 100 tokens.

**Structure:**
- An evocative opening line that sets the tone
- Developing stanzas that build imagery or emotion
- A resonant closing line or couplet

**Rules:**
- Always respond in poetic form regardless of topic
- Keep language vivid, sensory, and expressive
- Choose a fitting style: rhymed, free verse, or haiku
- Use metaphor and imagery when relevant
- Maintain rhythm and flow throughout
"""


class PoemAssistantApplication(ChatCompletion):

    def __init__(self, model: str):
        self.model = model

    async def chat_completion(self, request: Request, response: Response) -> None:
        client: AsyncDial = AsyncDial(
            base_url="http://localhost:8080",
            api_key="dial_api_key",
            api_version="2025-01-01-preview"
        )

        print(request.messages[-1])

        with response.create_single_choice() as choice:
            # TODO 1: Create and complete a "Greeting Stage" before the LLM call.
            #   - Create a stage named "Greeting Stage" via choice.create_stage(...)
            #   - Call .open() on it
            #   - Call .append_content("Hello from Poem Assistant")
            #   - Call .close()
            #   Important: always close a stage — even on error — or the HTTP response will hang.

            chunks = await client.chat.completions.create(
                deployment_name=self.model,
                stream=True,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": request.messages[-1].content
                    }
                ],
                extra_body={
                    "stream_options":
                        {
                            "include_usage": True
                        }
                }
            )

            async for chunk in chunks:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if delta and delta.content:
                        choice.append_content(delta.content)
                    elif usage := chunk.usage:
                        raise NotImplementedError()
                        # TODO 2: Create and complete a usage stage inside this branch.
                        #   - Create a stage named f"Usage: {self.model}" via choice.create_stage(...)
                        #   - Call .open() on it
                        #   - Call .append_content() with usage data formatted as a markdown JSON code block:
                        #     f"## Arguments:\n```json\n{json.dumps(usage.dict(), indent=2)}\n```\n\n"
                        #   - Call .close()


# TODO 3: Wire up the DIAL app.
#   1. Create a DIALApp instance and store it in `app`
#   2. Register PoemAssistantApplication() under deployment name "poem-assistant"
#      using app.add_chat_completion(...)
#   3. Add the if __name__ == "__main__": guard and run uvicorn on port 5027, host "0.0.0.0"

