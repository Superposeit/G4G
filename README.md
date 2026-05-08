# EducaT — Adaptive Offline AI Tutor with P2P Knowledge Mesh

> **One-Liner**
> EducaT is a **100% offline-first adaptive tutoring system** (built as a fork of the open-source **DeepTutor** project) powered by quantized Gemma 4, democratizing personalized education in disconnected, crisis-prone communities.

<<<<<<< HEAD
**Hackathon:** [Gemma 4 Good — Kaggle × Google DeepMind](https://www.kaggle.com/competitions/gemma-4-good-hackathon)  
**Tracks:** `Future of Education` · `Global Resilience`  
**Model:** Gemma 4 E2B (INT4 quantized) + Gemma 4 E4B (fallback)  
**License:** Apache 2.0  
=======
# DeepTutor: Agent-Native Personalized Tutoring

<a href="https://trendshift.io/repositories/17099" target="_blank"><img src="https://trendshift.io/api/badge/repositories/17099" alt="HKUDS%2FDeepTutor | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Next.js 16](https://img.shields.io/badge/Next.js-16-000000?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue?style=flat-square)](LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/HKUDS/DeepTutor?style=flat-square&color=brightgreen)](https://github.com/HKUDS/DeepTutor/releases)
[![arXiv](https://img.shields.io/badge/arXiv-2604.26962-b31b1b?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2604.26962)

[![Discord](https://img.shields.io/badge/Discord-Community-5865F2?style=flat-square&logo=discord&logoColor=white)](https://discord.gg/eRsjPgMU4t)
[![Feishu](https://img.shields.io/badge/Feishu-Group-00D4AA?style=flat-square&logo=feishu&logoColor=white)](./Communication.md)
[![WeChat](https://img.shields.io/badge/WeChat-Group-07C160?style=flat-square&logo=wechat&logoColor=white)](https://github.com/HKUDS/DeepTutor/issues/78)

[Features](#-key-features) · [Get Started](#-get-started) · [Explore](#-explore-deeptutor) · [TutorBot](#-tutorbot--persistent-autonomous-ai-tutors) · [CLI](#%EF%B8%8F-deeptutor-cli--agent-native-interface) · [Multi-User](#-multi-user--shared-deployments-with-per-user-workspaces) · [Roadmap](#%EF%B8%8F-roadmap) · [Community](#-community--ecosystem)

[🇨🇳 中文](assets/README/README_CN.md) · [🇯🇵 日本語](assets/README/README_JA.md) · [🇪🇸 Español](assets/README/README_ES.md) · [🇫🇷 Français](assets/README/README_FR.md) · [🇸🇦 العربية](assets/README/README_AR.md) · [🇷🇺 Русский](assets/README/README_RU.md) · [🇮🇳 हिन्दी](assets/README/README_HI.md) · [🇵🇹 Português](assets/README/README_PT.md) · [🇹🇭 ภาษาไทย](assets/README/README_TH.md)  · 🇵🇱 [Polski](assets/README/README_PL.md)

</div>

---

> 🤝 **We welcome any kinds of contributing!** See our [Contributing Guide](CONTRIBUTING.md) for branching strategy, coding standards, and how to get started.

### 📦 Releases

> **[2026.5.9]** [v1.3.9](https://github.com/HKUDS/DeepTutor/releases/tag/v1.3.9) — TutorBot Zulip and NVIDIA NIM support, safer thinking-model routing, `deeptutor start`, sidebar tooltips, and session-store parity.

> **[2026.5.8]** [v1.3.8](https://github.com/HKUDS/DeepTutor/releases/tag/v1.3.8) — Optional multi-user deployments with isolated user workspaces, admin grants, auth routes, and scoped runtime access.

> **[2026.5.4]** [v1.3.7](https://github.com/HKUDS/DeepTutor/releases/tag/v1.3.7) — Thinking-model/provider fixes, visible Knowledge index history, and safer Co-Writer clear/template editing.

> **[2026.5.3]** [v1.3.6](https://github.com/HKUDS/DeepTutor/releases/tag/v1.3.6) — Catalog-based model selection for chat and TutorBot, safer RAG re-indexing, OpenAI Responses token-limit fixes, and Skills editor validation.

> **[2026.5.2]** [v1.3.5](https://github.com/HKUDS/DeepTutor/releases/tag/v1.3.5) — Smoother local launch settings, safer RAG queries, cleaner local embedding auth, and Settings dark-mode polish.

> **[2026.5.1]** [v1.3.4](https://github.com/HKUDS/DeepTutor/releases/tag/v1.3.4) — Book page chat persistence and rebuild flows, chat-to-book references, stronger language/reasoning handling, RAG document extraction hardening.

> **[2026.4.30]** [v1.3.3](https://github.com/HKUDS/DeepTutor/releases/tag/v1.3.3) — NVIDIA NIM + Gemini embedding support, unified Space context for chat history/skills/memory, session snapshots, RAG re-index resilience.

> **[2026.4.29]** [v1.3.2](https://github.com/HKUDS/DeepTutor/releases/tag/v1.3.2) — Transparent embedding endpoint URLs, RAG re-index resilience for invalid persisted vectors, memory cleanup for thinking-model output, Deep Solve runtime fix.

> **[2026.4.28]** [v1.3.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.3.1) — Stability: safer RAG routing & embedding validation, Docker persistence, IME-safe input, Windows/GBK robustness.

> **[2026.4.27]** [v1.3.0](https://github.com/HKUDS/DeepTutor/releases/tag/v1.3.0) — Versioned KB indexes with re-index workflow, rebuilt Knowledge workspace, embedding auto-discovery with new adapters, Space hub.

> **[2026.4.25]** [v1.2.5](https://github.com/HKUDS/DeepTutor/releases/tag/v1.2.5) — Persistent chat attachments with file-preview drawer, attachment-aware capability pipelines, TutorBot Markdown export.

> **[2026.4.25]** [v1.2.4](https://github.com/HKUDS/DeepTutor/releases/tag/v1.2.4) — Text/code/SVG attachments, one-command Setup Tour, Markdown chat export, compact KB management UI.

<details>
<summary><b>Past releases (more than 2 weeks ago)</b></summary>

> **[2026.4.24]** [v1.2.3](https://github.com/HKUDS/DeepTutor/releases/tag/v1.2.3) — Document attachments (PDF/DOCX/XLSX/PPTX), reasoning thinking-block display, Soul template editor, Co-Writer save-to-notebook.

> **[2026.4.22]** [v1.2.2](https://github.com/HKUDS/DeepTutor/releases/tag/v1.2.2) — User-authored Skills system, chat input performance overhaul, TutorBot auto-start, Book Library UI, visualization fullscreen.

> **[2026.4.21]** [v1.2.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.2.1) — Per-stage token limits, Regenerate response across all entry points, RAG & Gemma compatibility fixes.

> **[2026.4.20]** [v1.2.0](https://github.com/HKUDS/DeepTutor/releases/tag/v1.2.0) — Book Engine "living book" compiler, multi-document Co-Writer, interactive HTML visualizations, Question Bank @-mention.

> **[2026.4.18]** [v1.1.2](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.2) — Schema-driven Channels tab, RAG single-pipeline consolidation, externalized chat prompts.

> **[2026.4.17]** [v1.1.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.1) — Universal "Answer now", Co-Writer scroll sync, unified settings panel, streaming Stop button.

> **[2026.4.15]** [v1.1.0](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.0) — LaTeX block math overhaul, LLM diagnostic probe, Docker + local LLM guidance.

> **[2026.4.14]** [v1.1.0-beta](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.0-beta) — Bookmarkable sessions, Snow theme, WebSocket heartbeat & auto-reconnect, embedding registry overhaul.

> **[2026.4.13]** [v1.0.3](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.3) — Question Notebook with bookmarks & categories, Mermaid in Visualize, embedding mismatch detection, Qwen/vLLM compatibility, LM Studio & llama.cpp support, and Glass theme.

> **[2026.4.11]** [v1.0.2](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.2) — Search consolidation with SearXNG fallback, provider switch fix, and frontend resource leak fixes.

> **[2026.4.10]** [v1.0.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.1) — Visualize capability (Chart.js/SVG), quiz duplicate prevention, and o4-mini model support.

> **[2026.4.10]** [v1.0.0-beta.4](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.4) — Embedding progress tracking with rate-limit retry, cross-platform dependency fixes, and MIME validation fix.

> **[2026.4.8]** [v1.0.0-beta.3](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.3) — Native OpenAI/Anthropic SDK (drop litellm), Windows Math Animator support, robust JSON parsing, and full Chinese i18n.

> **[2026.4.7]** [v1.0.0-beta.2](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.2) — Hot settings reload, MinerU nested output, WebSocket fix, and Python 3.11+ minimum.

> **[2026.4.4]** [v1.0.0-beta.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.1) — Agent-native architecture rewrite (~200k lines): Tools + Capabilities plugin model, CLI & SDK, TutorBot, Co-Writer, Guided Learning, and persistent memory.

> **[2026.1.23]** [v0.6.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.6.0) — Session persistence, incremental document upload, flexible RAG pipeline import, and full Chinese localization.

> **[2026.1.18]** [v0.5.2](https://github.com/HKUDS/DeepTutor/releases/tag/v0.5.2) — Docling support for RAG-Anything, logging system optimization, and bug fixes.

> **[2026.1.15]** [v0.5.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.5.0) — Unified service configuration, RAG pipeline selection per knowledge base, question generation overhaul, and sidebar customization.

> **[2026.1.9]** [v0.4.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.4.0) — Multi-provider LLM & embedding support, new home page, RAG module decoupling, and environment variable refactor.

> **[2026.1.5]** [v0.3.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.3.0) — Unified PromptManager architecture, GitHub Actions CI/CD, and pre-built Docker images on GHCR.

> **[2026.1.2]** [v0.2.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.2.0) — Docker deployment, Next.js 16 & React 19 upgrade, WebSocket security hardening, and critical vulnerability fixes.

</details>

### 📰 News

> **[2026.4.19]** 🎉 We've reached 20k stars after 111 days! Thank you for the incredible support — we're committed to continuous iteration toward truly personalized, intelligent tutoring for everyone.

> **[2026.4.10]** 📄 Our paper is now live on arXiv! Read the [preprint](https://arxiv.org/abs/2604.26962) to learn more about the design and ideas behind DeepTutor.

> **[2026.4.4]** Long time no see! ✨ DeepTutor v1.0.0 is finally here — an agent-native evolution featuring a ground-up architecture rewrite, TutorBot, and flexible mode switching under the Apache-2.0 license. A new chapter begins, and our story continues!

> **[2026.2.6]** 🚀 We've reached 10k stars in just 39 days! A huge thank you to our incredible community for the support!

> **[2026.1.1]** Happy New Year! Join our [Discord](https://discord.gg/eRsjPgMU4t), [WeChat](https://github.com/HKUDS/DeepTutor/issues/78), or [Discussions](https://github.com/HKUDS/DeepTutor/discussions) — let's shape the future of DeepTutor together!

> **[2025.12.29]** DeepTutor is officially released!


## ✨ Key Features

- **Unified Chat Workspace** — Six modes, one thread. Chat, Deep Solve, Quiz Generation, Deep Research, Math Animator, and Visualize share the same context — start a conversation, escalate to multi-agent problem solving, generate quizzes, visualize concepts, then deep-dive into research, all without losing a single message.
- **AI Co-Writer** — A multi-document Markdown workspace where AI is a first-class collaborator. Select text, rewrite, expand, or summarize — drawing from your knowledge base and the web. Every piece feeds back into your learning ecosystem.
- **Book Engine** — Turn your materials into structured, interactive "living books". A multi-agent pipeline designs outlines, retrieves relevant sources, and compiles rich pages with 13 block types — quizzes, flash cards, timelines, concept graphs, interactive demos, and more.
- **Knowledge Hub** — Upload PDFs, Markdown, and text files to build RAG-ready knowledge bases. Organize insights in color-coded notebooks, revisit quiz questions in the Question Bank, and create custom Skills that shape how DeepTutor teaches you. Your documents don't just sit there — they actively power every conversation.
- **Persistent Memory** — DeepTutor builds a living profile of you: what you've studied, how you learn, and where you're heading. Shared across all features and TutorBots, it gets sharper with every interaction.
- **Personal TutorBots** — Not chatbots — autonomous tutors. Each TutorBot lives in its own workspace with its own memory, personality, and skill set. They set reminders, learn new abilities, and evolve as you grow. Powered by [nanobot](https://github.com/HKUDS/nanobot).
- **Agent-Native CLI** — Every capability, knowledge base, session, and TutorBot is one command away. Rich terminal output for humans, structured JSON for AI agents and pipelines. Hand DeepTutor a [`SKILL.md`](SKILL.md) and your agents can operate it autonomously.
- **Optional Authentication** — Disabled by default for local use. Flip two env vars to require login when hosting publicly. Multi-user support with bcrypt-hashed passwords, JWT sessions, a self-service registration page, and a built-in admin dashboard for managing accounts and roles. Optionally back auth and storage with **PocketBase** for OAuth-ready authentication and improved multi-user concurrency — drops in as an optional sidecar with no code changes required.
>>>>>>> 72bcdd7 (prepare v1.3.9 release)

---

## 🚀 Get Started

<<<<<<< HEAD
The easiest way to evaluate the project is to run it using Docker Compose. This provides a one-command setup for the full stack (LiteRTLM API and FastAPI backend).
=======
### Prerequisites

Before you begin, make sure the following are installed on your system:

| Requirement | Version | Check | Notes |
|:---|:---|:---|:---|
| [Git](https://git-scm.com/) | Any | `git --version` | For cloning the repository |
| [Python](https://www.python.org/downloads/) | 3.11+ | `python --version` | Backend runtime |
| [Node.js](https://nodejs.org/) | 20.9+ | `node --version` | Frontend runtime for local Web installs |
| [npm](https://www.npmjs.com/) | Bundled with Node.js | `npm --version` | Installed with Node.js |

> **Windows only (missing compiler fix):** If you do not have Visual Studio, install [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) and ensure the **Desktop development with C++** workload is selected.

You'll also need an **API key** from at least one LLM provider (e.g. [OpenAI](https://platform.openai.com/api-keys), [DeepSeek](https://platform.deepseek.com/), [Anthropic](https://console.anthropic.com/)). The Setup Tour will walk you through entering it.

### Option A — Setup Tour (Recommended)

A guided CLI wizard for first-time local Web setup. It checks your environment, installs Python and Node.js dependencies, writes `.env`, and lets you choose optional add-ons such as TutorBot, Matrix, and Math Animator.

**1. Clone the repository**

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor
```

**2. Create and activate a Python environment**

Pick **one** of the following based on your system.

macOS / Linux with `venv`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Windows PowerShell with `venv`:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Anaconda / Miniconda:

```bash
conda create -n deeptutor python=3.11
conda activate deeptutor
python -m pip install --upgrade pip
```

**3. Launch the guided tour**

```bash
python scripts/start_tour.py
```

During the install step, the tour asks which dependency profile you want:

| Choice | What it installs | When to choose it |
|:---|:---|:---|
| Web app (recommended) | CLI + API server + RAG/document parsing | Most first-time users |
| Web + TutorBot | Adds TutorBot engine and common channel SDKs | If you want autonomous tutor bots or channel integrations |
| Web + TutorBot + Matrix | Adds Matrix / Element channel support | Only if you already have `libolm` installed or are ready to install it |
| Math Animator add-on | Installs Manim separately | Only if you need animation generation and have LaTeX/ffmpeg/system build tools ready |

Once the wizard finishes:

```bash
python scripts/start_web.py
```

> **Daily launch** — The tour is only needed once. From now on, keep that Python environment activated and run `python scripts/start_web.py` to boot both the backend and frontend. The frontend URL is printed in the terminal. Re-run `start_tour.py` only if you want to reconfigure providers, change ports, or install optional add-ons.

> **Updating a local install** — If you installed with Option A or Option B from a git clone, run `python scripts/update.py`. The updater fetches the remote for your current branch, shows the local-vs-remote commit gap, asks you to confirm the detected branch mapping, then performs a safe fast-forward pull.

### Option B — Manual Local Install

Use this path if you prefer to run each setup command yourself.

**1. Clone the repository**

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor
```

**2. Create and activate a Python environment**

Pick **one** of the following.

macOS / Linux with `venv`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Windows PowerShell with `venv`:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Anaconda / Miniconda:

```bash
conda create -n deeptutor python=3.11
conda activate deeptutor
python -m pip install --upgrade pip
```

**3. Install dependencies**

```bash
# Backend + Web server dependencies. Includes CLI, RAG, document parsing,
# and built-in LLM provider SDKs.
python -m pip install -e ".[server]"

# Optional add-ons — install only the ones you need:
#   python -m pip install -e ".[tutorbot]"       # TutorBot engine + channel SDKs
#   python -m pip install -e ".[tutorbot,matrix]" # TutorBot + Matrix channel; requires libolm
#   python -m pip install -e ".[math-animator]"  # Manim; also requires LaTeX/ffmpeg/system build tools
#   python -m pip install -e ".[all]"            # Everything above + dev tools

# Frontend dependencies. Requires Node.js 20.9+.
cd web
npm install
cd ..
```

**4. Configure environment**

```bash
cp .env.example .env
```

Edit `.env` and fill in at least the LLM fields. Embedding fields are needed for Knowledge Base features and can be left for later if you only want to try chat first.

```dotenv
# LLM (required for chat)
LLM_BINDING=openai
LLM_MODEL=gpt-4o-mini
LLM_API_KEY=sk-xxx
LLM_HOST=https://api.openai.com/v1

# Embedding (required for Knowledge Base / RAG)
EMBEDDING_BINDING=openai
EMBEDDING_MODEL=text-embedding-3-large
EMBEDDING_API_KEY=sk-xxx
# v1.3.0+: use the full endpoint URL, not just https://api.openai.com/v1
EMBEDDING_HOST=https://api.openai.com/v1/embeddings
# Leave empty unless you need to force a specific dimension.
EMBEDDING_DIMENSION=
```

<details>
<summary><b>Supported LLM Providers</b></summary>

| Provider | Binding | Default Base URL |
|:--|:--|:--|
| AiHubMix | `aihubmix` | `https://aihubmix.com/v1` |
| Anthropic | `anthropic` | `https://api.anthropic.com/v1` |
| Azure OpenAI | `azure_openai` | — |
| BytePlus | `byteplus` | `https://ark.ap-southeast.bytepluses.com/api/v3` |
| BytePlus Coding Plan | `byteplus_coding_plan` | `https://ark.ap-southeast.bytepluses.com/api/coding/v3` |
| Custom | `custom` | — |
| Custom (Anthropic API) | `custom_anthropic` | — |
| DashScope | `dashscope` | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| DeepSeek | `deepseek` | `https://api.deepseek.com` |
| Gemini | `gemini` | `https://generativelanguage.googleapis.com/v1beta/openai/` |
| GitHub Copilot | `github_copilot` | `https://api.githubcopilot.com` |
| Groq | `groq` | `https://api.groq.com/openai/v1` |
| llama.cpp | `llama_cpp` | `http://localhost:8080/v1` |
| LM Studio | `lm_studio` | `http://localhost:1234/v1` |
| MiniMax | `minimax` | `https://api.minimaxi.com/v1` |
| MiniMax (Anthropic) | `minimax_anthropic` | `https://api.minimaxi.com/anthropic` |
| Mistral | `mistral` | `https://api.mistral.ai/v1` |
| Moonshot | `moonshot` | `https://api.moonshot.cn/v1` |
| NVIDIA NIM | `nvidia_nim` | `https://integrate.api.nvidia.com/v1` |
| Ollama | `ollama` | `http://localhost:11434/v1` |
| OpenAI | `openai` | `https://api.openai.com/v1` |
| OpenAI Codex | `openai_codex` | `https://chatgpt.com/backend-api` |
| OpenRouter | `openrouter` | `https://openrouter.ai/api/v1` |
| OpenVINO Model Server | `ovms` | `http://localhost:8000/v3` |
| Qianfan | `qianfan` | `https://qianfan.baidubce.com/v2` |
| SiliconFlow | `siliconflow` | `https://api.siliconflow.cn/v1` |
| Step Fun | `stepfun` | `https://api.stepfun.com/v1` |
| vLLM/Local | `vllm` | — |
| VolcEngine | `volcengine` | `https://ark.cn-beijing.volces.com/api/v3` |
| VolcEngine Coding Plan | `volcengine_coding_plan` | `https://ark.cn-beijing.volces.com/api/coding/v3` |
| Xiaomi MIMO | `xiaomi_mimo` | `https://api.xiaomimimo.com/v1` |
| Zhipu AI | `zhipu` | `https://open.bigmodel.cn/api/paas/v4` |

</details>

<details>
<summary><b>Supported Embedding Providers</b></summary>

| Provider | Binding | Model Example | Default Dim |
|:--|:--|:--|:--|
| OpenAI | `openai` | `text-embedding-3-large` | 3072 |
| Azure OpenAI | `azure_openai` | deployment name | — |
| Cohere | `cohere` | `embed-v4.0` | 1024 |
| Jina | `jina` | `jina-embeddings-v3` | 1024 |
| Ollama | `ollama` | `nomic-embed-text` | 768 |
| vLLM / LM Studio | `vllm` | Any embedding model | — |
| Any OpenAI-compatible | `custom` | — | — |

OpenAI-compatible providers (DashScope, SiliconFlow, etc.) work via the `custom` or `openai` binding.

</details>

<details>
<summary><b>Supported Web Search Providers</b></summary>

| Provider | Env Key | Notes |
|:--|:--|:--|
| Brave | `BRAVE_API_KEY` | Recommended, free tier available |
| Tavily | `TAVILY_API_KEY` | |
| Serper | `SERPER_API_KEY` | Google Search results via Serper |
| Jina | `JINA_API_KEY` | |
| SearXNG | — | Self-hosted, no API key needed |
| DuckDuckGo | — | No API key needed |
| Perplexity | `PERPLEXITY_API_KEY` | Requires API key |

</details>

**5. Start services**

The quickest way to launch everything:

```bash
python scripts/start_web.py
```

This starts both the backend and frontend. Keep the terminal open, then open the frontend URL printed in the terminal.

Alternatively, start each service manually in separate terminals:

```bash
# Backend (FastAPI)
python -m deeptutor.api.run_server

# Frontend (Next.js) — in a separate terminal
cd web && npm run dev -- -p 3782
```

| Service | Default Port |
|:---:|:---:|
| Backend | `8001` |
| Frontend | `3782` |

Open [http://localhost:3782](http://localhost:3782) and you're ready to go.

### Option C — Docker Deployment

Docker wraps the backend and frontend into a single container — no local Python or Node.js required. You only need [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or Docker Engine + Compose on Linux).

**1. Configure environment variables** (required for both options below)

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor
cp .env.example .env
```

Edit `.env` and fill in at least the required fields (same as [Option B](#option-b--manual-local-install) above).

**2a. Pull official image (recommended)**

Official images are published to [GitHub Container Registry](https://github.com/HKUDS/DeepTutor/pkgs/container/deeptutor) on every release, built for `linux/amd64` and `linux/arm64`.

```bash
docker compose -f docker-compose.ghcr.yml up -d
```

To pin a specific version, edit the image tag in `docker-compose.ghcr.yml`:

```yaml
image: ghcr.io/hkuds/deeptutor:1.3.4  # or :latest
```

**2b. Build from source**
>>>>>>> b4cca8e (fix: add tutorbot nvidia nim provider)

```bash
docker compose up -d
```

Once the containers are running:
- The **Frontend (Voice UI)** will be accessible.
- The **Backend API** will serve requests using the local models.

*(Note: On first run, it may take a few minutes to download the models.)*

---

## 🌍 The Problem

**Frontier AI tutoring exists — but only where infrastructure does.**

Across Latin America, Sub-Saharan Africa, and rural Asia, over **1.1 billion school-age children** face a compounding crisis:
- **Connectivity:** 40–60% of rural schools have no stable internet.
- **Teacher Shortage:** Massive deficits in educators (e.g., 20,000+ in the Dominican Republic).
- **Class Size:** 35–50 students per teacher makes personalization impossible.
- **Infrastructure Fragility:** Blackouts, hurricanes, and civil disruptions regularly sever cloud access.
- **Hardware Reality:** The only devices available are low-end Android phones and school tablets (2–4 GB RAM).

EducaT targets chronic educational inequality directly by making world-class AI available without internet.

---

## 💡 The Solution

EducaT gives every student the second explanation — the patient, adaptive re-teaching that overcrowded classrooms structurally cannot provide. It deploys adaptive AI tutoring directly onto devices already in students' hands.

### Core Objectives
- **100% Offline-First:** Fully functional adaptive math tutor running on devices with ≥ 2 GB RAM.
- **Low Latency on Edge Hardware:** Sub-3-second first-token latency on Gemma 4 E2B INT4 on a Snapdragon 680-class CPU.
- **Socratic Scaffolding:** Gemma 4's Thinking Mode is used to guide discovery step by step without just giving the answer.
- **DeepTutor Foundation:** Built on top of DeepTutor's powerful tool integration.
- **Specialized Educational Prompts:** Runs carefully crafted, specialized prompts with Gemma 4 to act as an effective learning companion.
- **Model Gallery:** Includes a built-in gallery where users and teachers can easily browse, add, and manage new models and capabilities directly from the interface.

---

## 🧠 Why Gemma 4?

Gemma 4 is uniquely positioned for this problem:
- **E2B Edge Model:** At 2.3B effective parameters, it runs on ~1.4 GB RAM post-quantization (fitting entry-level tablets).
- **Native Audio Encoder:** Enables voice input without an external ASR server for true offline interaction.
- **Thinking Mode:** Pedagogical reasoning stays internal, keeping the student-facing output clean and simple.
- **DeepTutor Tool Integration:** Natively interfaces with DeepTutor's powerful suite of tools to provide accurate and context-aware responses.
- **Apache 2.0 License:** No legal barriers for deployment by NGOs, ministries, or open source forks.

---



## 🛠️ Tech Stack

| Layer | Technology | Rationale |
|---|---|---|
| **Base Architecture**| DeepTutor (Fork) | Accelerated development leveraging a proven multi-agent tutoring framework |
| **AI Model** | Gemma 4 E2B IT (LiteRTLM models) | Edge-optimized; 2.3B eff. params; audio-native |
| **Local Inference** | LiteRTLM API | Lightweight, high-performance API for local edge model serving |
| **Audio In** | Gemma 4 native audio encoder | True offline audio; handles noisy classrooms |
| **Audio Out** | Coqui TTS `tts_models/es/css10/vits` | Local Spanish TTS; Caribbean accent tunable |
| **Mobile UI** | React Native (bare workflow) | Single codebase iOS/Android; ADHD-optimized minimal layout |
| **JS Runtime** | Bun | Faster startup + lower memory vs Node.js |
| **Local DB** | SQLite (expo-sqlite) | Zero-config; per-student isolation; works offline |
| **Vector Index** | FAISS (local) | Sub-second retrieval for RAG-augmented responses |

---

## 📖 Story & Impact

*María is 9 years old. She lives in a rural community where her school has one teacher for 42 students. A storm knocks out the internet.*

*But María's tablet still works. Edu — a patient, cheerful voice — asks her how many mangos she'd give to each friend if she had 12 and three friends. She gets it wrong, but Edu never says "wrong." It just tries again, differently.*

*The internet is down. EducaT isn't.*

By providing an adaptive, voice-first, infinitely patient tutor that works entirely offline, EducaT aims to close the educational equity gap and build community resilience.
