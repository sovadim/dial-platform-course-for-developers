import os

import uvicorn
from aidial_sdk import DIALApp
from aidial_sdk.chat_completion import ChatCompletion, Request, Response, Choice, Stage
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.vectorstores import VectorStore
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import SecretStr

SYSTEM_PROMPT = """You are a RAG-powered assistant that assists users with their questions about microwave usage.
            
## Structure of User message:
`Context` - Retrieved documents relevant to the query.
`Query` - The user's actual question.

## Instructions:
- Use information from `RAG CONTEXT` as context when answering the `Query`.
- Cite specific sources when using information from the context.
- Answer ONLY based on conversation history and RAG context.
- If no relevant information exists in `Context` or conversation history, state that you cannot answer the question.
"""


class _StageProcessor:
    @staticmethod
    def open_stage(choice: Choice, name: str) -> Stage:
        stage = choice.create_stage(name)
        stage.open()
        return stage

    @staticmethod
    def close_stage_safely(stage: Stage) -> None:
        try:
            stage.close()
        except Exception:
            pass


class MicrowaveRagApp(ChatCompletion):

    def __init__(self, embeddings: AzureOpenAIEmbeddings, llm_client: AzureChatOpenAI):
        self.llm_client = llm_client
        self.embeddings = embeddings
        self.vectorstore = self._setup_vectorstore()

    def _setup_vectorstore(self) -> VectorStore:
        """Initialize the RAG system"""
        print("🔄 Initializing Microwave Manual RAG System...")

        if os.path.exists('microwave_faiss_index'):
            vectorstore = FAISS.load_local(
                folder_path='microwave_faiss_index',
                embeddings=self.embeddings,
                allow_dangerous_deserialization=True,
            )
            print("✅ Loaded existing FAISS index")
        else:
            vectorstore = self._create_new_index()
            print("✅ RAG system initialized successfully!")

        return vectorstore

    def _create_new_index(self) -> VectorStore:
        print("📖 Loading text document...")
        loader = TextLoader('microwave_manual.txt', encoding='utf-8')
        documents = loader.load()

        print("✂️ Splitting document into chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=50,
            separators=["\n\n", "\n", "."]
        )
        chunks = text_splitter.split_documents(documents)
        print(f"✅ Created {len(chunks)} chunks")

        print("🔍 Creating embeddings and FAISS index...")
        vectorstore = FAISS.from_documents(chunks, self.embeddings)
        vectorstore.save_local("microwave_faiss_index")
        print("💾 Index saved for future use")

        return vectorstore

    def retrieve_context(self, query: str, choice: Choice, k: int = 4, score=0.3):
        stage = _StageProcessor.open_stage(choice, f"RAG Search: {query}")
        stage.append_content(f"## Query:\n```\n{query}\n```\n\n")

        # TODO 3: Perform the similarity search and build the context string.
        #   - Call self.vectorstore.similarity_search_with_relevance_scores(query, k=k, score_threshold=score)
        #   - Iterate the result — each item is a (doc, score) tuple; collect doc.page_content into a list
        #   - Join with "\n\n" to form the result string
        #   - Append the result to the stage: stage.append_content(f"## Result:\n```\n{result}\n```\n\n")
        #   - Close the stage safely: _StageProcessor.close_stage_safely(stage)
        #   - Return result

    async def chat_completion(self, request: Request, response: Response) -> None:
        with response.create_single_choice() as choice:
            message_content = request.messages[-1].content
            retrieved_context = self.retrieve_context(message_content, choice)

            # TODO 4: Build the RAG prompt and stream the LLM response.
            #   - Construct a messages list:
            #       [SystemMessage(content=SYSTEM_PROMPT),
            #        HumanMessage(content=f"## Context:\n {retrieved_context}\n\n## Query: \n{message_content}")]
            #   - Stream via: chunks = self.llm_client.astream(messages)
            #   - async for chunk in chunks: if chunk.content is truthy, call choice.append_content(chunk.content)


_DIAL_URL = "http://localhost:8080"
_API_KEY = "dial_api_key"

# TODO 1: Create the embeddings client and assign it to `embeddings_client`.
#   Use AzureOpenAIEmbeddings with:
#   - deployment: "text-embedding-3-small"
#   - dimensions: 784  ← must match the pre-built FAISS index; changing it forces a full rebuild
#   - azure_endpoint: _DIAL_URL
#   - api_key: SecretStr(_API_KEY)
embeddings_client = None  # replace with AzureOpenAIEmbeddings(...)

# TODO 2: Create the LLM client and assign it to `llm_client`.
#   Use AzureChatOpenAI with:
#   - azure_deployment: "gpt-5.2"
#   - azure_endpoint: _DIAL_URL
#   - api_key: SecretStr(_API_KEY)
#   - api_version: "2025-01-01-preview"
llm_client = None  # replace with AzureChatOpenAI(...)

rag_app = MicrowaveRagApp(embeddings=embeddings_client, llm_client=llm_client)

app: DIALApp = DIALApp()

app.add_chat_completion(deployment_name="microwave-rag", impl=rag_app)

if __name__ == "__main__":
    uvicorn.run(app, port=5030, host="0.0.0.0")
