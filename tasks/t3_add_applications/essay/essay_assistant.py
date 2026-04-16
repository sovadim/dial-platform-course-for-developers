from aidial_client import AsyncDial

from aidial_sdk.chat_completion import ChatCompletion, Request, Response

SYSTEM_PROMPT = """You are an essay-focused assistant. Respond to every request by writing a **short essay** of up to 100 tokens.

**Structure:**
- Clear introduction with thesis
- Body paragraphs with supporting points
- Concise conclusion

**Rules:**
- Always write in essay format regardless of topic
- Keep responses analytical and structured
- Use formal, academic tone
- Include specific examples when relevant
- Maintain logical flow between paragraphs
"""


class EssayAssistantApplication(ChatCompletion):

    def __init__(self, model: str):
        self.model = model

    async def chat_completion(self, request: Request, response: Response) -> None:
        print(request.messages[-1])

        # TODO 1: Create an AsyncDial client and store it in `client`.
        #   - base_url: "http://localhost:8080"  (DIAL Core; use localhost since this app runs outside Docker)
        #   - api_key: "dial_api_key"
        #   - api_version: "2025-01-01-preview"

        # TODO 2: Open a single-choice response using response.create_single_choice() as a context manager.
        #   Use `with response.create_single_choice() as choice:` and put TODOs 3-4 inside the block.

            # TODO 3: Create a streaming chat completion request via client.chat.completions.create().
            #   Pass:
            #   - deployment_name: self.model
            #   - stream: True
            #   - messages: a list with two entries —
            #       {"role": "system", "content": SYSTEM_PROMPT}
            #       {"role": "user",   "content": request.messages[-1].content}
            #   Store the result in `chunks`.

            # TODO 4: Iterate the async stream: `async for chunk in chunks`.
            #   For each chunk:
            #   - Check that chunk.choices is non-empty
            #   - Extract delta = chunk.choices[0].delta
            #   - Only call choice.append_content(delta.content) if both delta and delta.content are not None
            #   Hint: some chunks carry no content (e.g. the final usage chunk) — always guard before appending.

    # Task 7: add configuration() here👇