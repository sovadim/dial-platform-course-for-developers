<h1 align="center">DIAL Platform Course for Developers</h1>
<p align="center">
    <p align="center">
    <a href="https://dialx.ai/">
      <img src="https://dialx.ai/logo/dialx_logo.svg" alt="About DIALX">
    </a>
</p>
<h4 align="center">
    <a href="https://discord.gg/ukzj9U9tEe">
        <img src="https://img.shields.io/static/v1?label=DIALX%20Community%20on&message=Discord&color=blue&logo=Discord&style=flat-square" alt="Discord">
    </a>
</h4>

---

## About

This is a fork of the DIAL Platform Course with my walk-through.

## Platform Components

| Component               | Purpose                                                                         |
|-------------------------|---------------------------------------------------------------------------------|
| DIAL Core               | Central gateway — routes requests to model adapters; OpenAI-compatible REST API |
| DIAL Chat               | End-user chat UI                                                                |
| Themes                  | Icons and theme assets served to Chat                                           |
| Model adapters          | Thin proxies for OpenAI, AWS Bedrock (Anthropic), VertexAI (Gemini)             |
| DIAL SDK (`aidial-sdk`) | Python SDK for building custom AI applications behind the gateway               |

## Course Outline

| #                                                      | Topic                     | What you will do                                                       |
|--------------------------------------------------------|---------------------------|------------------------------------------------------------------------|
| [t1](tasks/t1_start_platform/README.md)                | Start the Platform        | Spin up the full Docker Compose stack                                  |
| [t2](tasks/t2_add_models/README.md)                    | Add Models                | Connect OpenAI, Anthropic, and Gemini models via config and adapters   |
| [t3](tasks/t3_add_applications/README.md)              | Add Applications          | Build your first DIAL SDK apps (Echo and Essay Assistant)              |
| [t4](tasks/t4_stage_and_state/README.md)               | Stage & State             | Use Stages and State primitives for richer UX and conversation memory  |
| [t5](tasks/t5_files/README.md)                         | Files                     | Handle image uploads, multimodal LLMs, and TTS audio attachments       |
| [t6](tasks/t6_embeddings_and_frameworks/README.md)     | Embeddings & Frameworks   | Build a RAG app with LangChain against DIAL's embedding endpoint       |
| [t7](tasks/t7_buttons/README.md)                       | Buttons                   | Expose a configuration endpoint and render interactive buttons in Chat |
| [t8](tasks/t8_agent/README.md)                         | Agent — Capstone          | Build a multi-tool streaming agent combining all platform capabilities |
| [Extra task 1](tasks/t_extra_1_themes/README.md) | Themes *(optional)*       | Customize Chat's color palette and branding                            |
| [Extra task 2](tasks/t_extra_2_chat_overlay/README.md) | Chat Overlay *(optional)* | Embed DIAL Chat into an external web page via the overlay library      |

---

## How to run

With Docker:
```bash
docker compose up -d --build
```

With podman:
```bash
podman machine start
podman-compose up -d --build
```

## How to run applications from tasks

Task 3:
```bash
uv run -m tasks.t3_add_applications.echo.echo_app
uv run -m tasks.t3_add_applications.essay.app_gpt
uv run -m tasks.t3_add_applications.essay.app_sonnet
```

Task 4:
```bash
uv run -m tasks.t4_stage_and_state.t1_simple.poem_assistant
uv run -m tasks.t4_stage_and_state.t2_calculator_agent.app
```
