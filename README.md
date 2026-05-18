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

> **[2026.5.10]** [v1.3.10](https://github.com/HKUDS/DeepTutor/releases/tag/v1.3.10) — Remote Docker CORS recovery, `DISABLE_SSL_VERIFY` across SDK providers, safer code-block citations, and optional Matrix E2EE add-on.

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

<details>
<summary><b>Past releases (more than 2 weeks ago)</b></summary>

> **[2026.4.25]** [v1.2.5](https://github.com/HKUDS/DeepTutor/releases/tag/v1.2.5) — Persistent chat attachments with file-preview drawer, attachment-aware capability pipelines, TutorBot Markdown export.

> **[2026.4.25]** [v1.2.4](https://github.com/HKUDS/DeepTutor/releases/tag/v1.2.4) — Text/code/SVG attachments, one-command Setup Tour, Markdown chat export, compact KB management UI.

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
<<<<<<< HEAD
- **Optional Authentication** — Disabled by default for local use. Flip two env vars to require login when hosting publicly. Multi-user support with bcrypt-hashed passwords, JWT sessions, a self-service registration page, and a built-in admin dashboard for managing accounts and roles. Optionally back auth and storage with **PocketBase** for OAuth-ready authentication and improved multi-user concurrency — drops in as an optional sidecar with no code changes required.
>>>>>>> 72bcdd7 (prepare v1.3.9 release)
=======
- **Optional Authentication** — Disabled by default for local use. Set `data/user/settings/auth.json` to require login when hosting publicly. Multi-user support with bcrypt-hashed passwords, JWT sessions, a self-service registration page, and a built-in admin dashboard for managing accounts and roles. Optionally back auth and storage with **PocketBase** for OAuth-ready authentication and improved multi-user concurrency — drops in as an optional sidecar with no code changes required.
>>>>>>> 85779c8 (refactor env settings and installation)

---

## 🚀 Get Started

<<<<<<< HEAD
<<<<<<< HEAD
The easiest way to evaluate the project is to run it using Docker Compose. This provides a one-command setup for the full stack (LiteRTLM API and FastAPI backend).
=======
### Prerequisites
=======
DeepTutor now has four parallel installation paths. All of them use the same runtime configuration layout:
>>>>>>> 85779c8 (refactor env settings and installation)

- Settings live in `data/user/settings/` under your current workspace, or under `DEEPTUTOR_HOME` / `deeptutor start --home` when you choose one explicitly.
- `model_catalog.json` stores model provider profiles, base URLs, API keys, active models, embedding settings, and search settings.
- `system.json` stores launch ports, public API base, CORS, TLS, and attachment options.
- `auth.json` stores the optional auth toggle and bootstrap credential hash.
- `integrations.json` stores optional sidecars such as PocketBase.
- Project-root `.env` is no longer used as an application configuration file.

For the full local app, the recommended order is **choose a workspace → install → `deeptutor init` → `deeptutor start`**. `deeptutor start` can backfill missing default files as a safety net, but normal first-run setup should go through `deeptutor init` so ports and model settings are explicit before the Web app starts.

### Option 1 — Install DeepTutor

Use this when you want the full local Web app and CLI without cloning the repository.

```bash
mkdir -p my-deeptutor
cd my-deeptutor
pip install -U deeptutor
deeptutor init
deeptutor start
```

`deeptutor init` writes configuration under `data/user/settings/` in the directory where you run it. It prompts for:

- Backend port, default `8001`
- Frontend port, default `3782`
- LLM provider binding, base URL, API key, and model name
- Optional embedding provider for Knowledge Base / RAG

After `deeptutor start`, open the frontend URL printed in the terminal. With default ports, that URL is [http://127.0.0.1:3782](http://127.0.0.1:3782). If you changed `frontend_port` during `deeptutor init` or later edited `data/user/settings/system.json`, use that configured port instead.

Keep the `deeptutor start` terminal open. Press `Ctrl+C` in that terminal to stop both backend and frontend.

Notes:

- `deeptutor start` starts the FastAPI backend and the packaged Next.js frontend together.
- The packaged Web app does not require `git clone` or `npm install`, but it still needs a local Node.js 20+ runtime to execute the bundled Next.js standalone server.
- If you deliberately skip `deeptutor init` for a quick trial, the app starts with safe default ports and empty model settings; configure models afterward in **Settings → Models**.

### Option 2 — Install From Source

Use this when you are developing DeepTutor or want to run directly from a checkout.

**1. Clone the repository**

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor
```

**2. Create a Python environment**

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

Conda / Miniconda:

```bash
conda create -n deeptutor python=3.11
conda activate deeptutor
python -m pip install --upgrade pip
```

**3. Install the local package and frontend dependencies**

```bash
pip install -e .
cd web
npm install
cd ..
```

**4. Configure and start**

```bash
deeptutor init
deeptutor start
```

Source installs use the local `web/` directory for the frontend. They are intentionally developer-friendly and do not write configuration to `.env`; edit `data/user/settings/*.json` or use the Web Settings page.

Useful developer extras:

```bash
pip install -e ".[dev]"             # tests/lint tools
pip install -e ".[tutorbot]"        # TutorBot engine + channel SDKs
pip install -e ".[matrix]"          # Matrix channel without E2EE/libolm
pip install -e ".[matrix-e2e]"      # Matrix E2EE; requires libolm
pip install -e ".[math-animator]"   # Manim addon; requires LaTeX/ffmpeg/system libs
```

### Option 3 — Docker

Use this when you want the full Web app in one container. Images are published to GitHub Container Registry:

- `ghcr.io/hkuds/deeptutor:latest` — stable release
- `ghcr.io/hkuds/deeptutor:pre` — pre-release, when available

```bash
docker pull ghcr.io/hkuds/deeptutor:latest
docker run -p 127.0.0.1:3782:3782 \
  -p 127.0.0.1:8001:8001 \
  -v deeptutor-data:/app/data \
  ghcr.io/hkuds/deeptutor:latest
```

Then open [http://127.0.0.1:3782](http://127.0.0.1:3782). Config, API keys, logs, workspace files, memory, and knowledge bases are stored in the `deeptutor-data` volume under `/app/data`.

The container creates `/app/data/user/settings/*.json` automatically on first boot. You can configure model providers directly in the Web Settings page without preparing local JSON files manually.

To use different host ports, change the left side of the `-p` mappings. For example, `-p 127.0.0.1:8088:3782` makes the Web UI available at `http://127.0.0.1:8088` while the container still listens on `3782`. If you change the container-side ports in `/app/data/user/settings/system.json`, restart the container and make the right side of each `-p host:container` mapping match the configured container port.

#### Connecting To Ollama Or Other Host Services

Inside a Docker container, `localhost` refers to the container itself, not your host machine. If you run Ollama, LM Studio, llama.cpp, vLLM, or another model service on the host, use one of these approaches.

Option A — host gateway, recommended for normal Docker runs:

```bash
docker run -p 127.0.0.1:3782:3782 \
  -p 127.0.0.1:8001:8001 \
  --add-host=host.docker.internal:host-gateway \
  -v deeptutor-data:/app/data \
  ghcr.io/hkuds/deeptutor:latest
```

Then in **DeepTutor Settings → Models**, set the provider Base URL to `host.docker.internal`:

- Ollama LLM endpoint: `http://host.docker.internal:11434/v1`
- Ollama embedding endpoint: `http://host.docker.internal:11434/api/embed`
- LM Studio: `http://host.docker.internal:1234/v1`
- llama.cpp: `http://host.docker.internal:8080/v1`

On Docker Desktop for macOS/Windows, `host.docker.internal` is usually available even without `--add-host`. On Linux, the `--add-host=host.docker.internal:host-gateway` flag is the portable way to create that hostname on modern Docker Engine.

Option B — host networking, Linux only:

```bash
docker run --network=host \
  -v deeptutor-data:/app/data \
  ghcr.io/hkuds/deeptutor:latest
```

No `-p` mapping is needed in host-network mode. The container shares the host network directly, so open [http://127.0.0.1:3782](http://127.0.0.1:3782) by default, or the `frontend_port` configured in `/app/data/user/settings/system.json`. In this mode, host services can usually be reached with normal localhost URLs such as `http://127.0.0.1:11434/v1`. Host networking exposes container ports directly on the host and may conflict with existing services.

To stop a foreground Docker run, press `Ctrl+C`. If you started it detached with `-d`, run `docker stop <container-name-or-id>`.

<<<<<<< HEAD
**2b. Build from source**
>>>>>>> b4cca8e (fix: add tutorbot nvidia nim provider)
=======
### Option 4 — CLI Only

Use this when you do not need the Web UI.
>>>>>>> 85779c8 (refactor env settings and installation)

```bash
pip install -U deeptutor-cli
deeptutor init --cli
deeptutor chat
```

<<<<<<< HEAD
Once the containers are running:
- The **Frontend (Voice UI)** will be accessible.
- The **Backend API** will serve requests using the local models.

<<<<<<< HEAD
*(Note: On first run, it may take a few minutes to download the models.)*
=======
**3. Verify & manage**
=======
`deeptutor init --cli` uses the same `data/user/settings/` layout as the full app, but changes the wizard behavior:

- It skips backend/frontend port prompts because CLI-only usage does not start the Web app.
- It still writes default `system.json`, `auth.json`, `integrations.json`, `model_catalog.json`, `main.yaml`, and `agents.yaml` so the runtime layout is complete.
- It still prompts for the active LLM provider and model.
- It asks whether to configure embeddings, but the default answer is `No`; choose `Yes` if you plan to use `deeptutor kb ...` or RAG tools.
>>>>>>> 85779c8 (refactor env settings and installation)

Common CLI commands:

```bash
deeptutor chat
deeptutor chat --capability deep_solve --tool rag --kb my-kb
deeptutor run chat "Explain Fourier transform"
deeptutor run deep_solve "Solve x^2 = 4" --tool rag --kb my-kb
deeptutor kb create my-kb --doc textbook.pdf
deeptutor kb list
deeptutor memory show
```

`deeptutor-cli` does not ship Web assets or server dependencies. If you later want the Web app, install the full package with `pip install -U deeptutor`, run `deeptutor init` if you want to add Web ports, and then run `deeptutor start` from the same workspace.

### Configuration Reference

The Web Settings page is the recommended editor, but the files are plain JSON/YAML and can be managed directly:

| File | Purpose |
|:---|:---|
| `data/user/settings/model_catalog.json` | LLM, embedding, and search provider profiles; API keys; active models |
| `data/user/settings/system.json` | Backend/frontend ports, public API base, CORS, SSL verification, attachment directory |
| `data/user/settings/auth.json` | Optional auth toggle, username, password hash, token/cookie settings |
| `data/user/settings/integrations.json` | Optional PocketBase and sidecar integration settings |
| `data/user/settings/interface.json` | UI language/theme/sidebar preferences |
| `data/user/settings/main.yaml` | Runtime behavior defaults and path injection |
| `data/user/settings/agents.yaml` | Capability/tool temperature and token settings |

<<<<<<< HEAD
</details>

<details>
<summary><b>Authentication (public deployments)</b></summary>

Authentication is **disabled by default** — no login is required on localhost. For multi-tenant deployments (per-user workspaces, admin-curated models / KBs / skills, audit log), see the dedicated [Multi-User](#-multi-user--shared-deployments-with-per-user-workspaces) section below for the full setup, env-var reference, and operational caveats.

**Headless single-user (no `/register` flow):** if you can't reach the browser to bootstrap the first admin (e.g. an unattended container), pre-seed the credential via env vars:

```bash
# Generate a bcrypt hash on any host with the project checked out:
python -c "from deeptutor.services.auth import hash_password; print(hash_password('yourpassword'))"
```

```dotenv
AUTH_ENABLED=true
AUTH_USERNAME=admin
AUTH_PASSWORD_HASH=<paste hash here>
# Optional. Auto-generated under multi-user/_system/auth/auth_secret if blank.
AUTH_SECRET=your-secret-here
```

This env-var path serves a single account and is treated as the admin. Once you run the browser registration flow, the on-disk store at `multi-user/_system/auth/users.json` takes priority and the env vars become a fallback.

</details>

<details>
<summary><b>PocketBase sidecar (optional auth + storage)</b></summary>

PocketBase is an optional lightweight backend that replaces the built-in SQLite/JSON auth and session storage. It adds OAuth-ready authentication, real-time subscriptions, and a visual admin panel — with zero changes required to switch back if you don't set `POCKETBASE_URL`.

> ⚠️ **PocketBase mode is currently single-user only.** The default schema has no `role` field on `users` (every login resolves to `role=user`, so no admin can be created), and the session/message/turn queries are not filtered by `user_id`. Multi-user deployments should keep `POCKETBASE_URL` blank and use the default JSON/SQLite backend.

**When to use it:** local single-user setups that want OAuth-ready auth and a visual admin panel without yet caring about per-user isolation.

**Quick start (Docker Compose):**

```bash
# PocketBase starts automatically alongside DeepTutor when using docker compose
docker compose up -d

# 1. Open the admin panel and create your admin account
open http://localhost:8090/_/

# 2. Bootstrap collections (run once)
pip install pocketbase
python scripts/pb_setup.py

# 3. Enable PocketBase in .env and restart
```

**Required `.env` additions:**

```dotenv
POCKETBASE_URL=http://localhost:8090          # or http://pocketbase:8090 inside Docker
POCKETBASE_ADMIN_EMAIL=admin@example.com
POCKETBASE_ADMIN_PASSWORD=your-admin-password
```

**devenv users:**

```bash
devenv up   # starts PocketBase on :8090 alongside backend and frontend
```

Leave `POCKETBASE_URL` unset (or remove it) to fall back to the built-in SQLite backend at any time — no data migration needed for new sessions.

</details>

<details>
<summary><b>Development mode (hot-reload)</b></summary>

Layer the dev override to mount source code and enable hot-reload for both services:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

Changes to `deeptutor/`, `deeptutor_cli/`, `scripts/`, and `web/` are reflected immediately.

</details>

<details>
<summary><b>Custom ports</b></summary>

Override the default ports in `.env`:

```dotenv
BACKEND_PORT=9001
FRONTEND_PORT=4000
```

Then restart:

```bash
docker compose up -d     # or docker compose -f docker-compose.ghcr.yml up -d
```

</details>

<details>
<summary><b>Data persistence</b></summary>

User data and knowledge bases are persisted via Docker volumes mapped to local directories:

| Container path | Host path | Content |
|:---|:---|:---|
| `/app/data/user` | `./data/user` | Settings, workspace, sessions, logs |
| `/app/data/memory` | `./data/memory` | Shared long-term memory (`SUMMARY.md`, `PROFILE.md`) |
| `/app/data/knowledge_bases` | `./data/knowledge_bases` | Uploaded documents & vector indices |

These directories survive `docker compose down` and are reused on the next `docker compose up`.

</details>

<details>
<summary><b>Environment variables reference</b></summary>

> See [`.env.example`](.env.example) for the canonical, fully-commented list. The table below covers the variables most users touch.

| Variable | Required | Description |
|:---|:---:|:---|
| `LLM_BINDING` | **Yes** | LLM provider (`openai`, `anthropic`, `deepseek`, etc.) |
| `LLM_MODEL` | **Yes** | Model name (e.g. `gpt-4o`) |
| `LLM_API_KEY` | **Yes** | Your LLM API key |
| `LLM_HOST` | **Yes** | Chat-completions base URL |
| `LLM_API_VERSION` | No | Required for Azure OpenAI; blank otherwise |
| `LLM_REASONING_EFFORT` | No | DeepSeek `high`/`max`/`minimal` or OpenAI o-series `low`/`medium`/`high` |
| `EMBEDDING_BINDING` | Knowledge Base only | Embedding provider |
| `EMBEDDING_MODEL` | Knowledge Base only | Embedding model name |
| `EMBEDDING_API_KEY` | Knowledge Base only | Embedding API key |
| `EMBEDDING_HOST` | Knowledge Base only | Full embedding endpoint URL (v1.3.0+ — called verbatim, no path appended) |
| `EMBEDDING_DIMENSION` | No | Vector dimension; leave empty for auto-detection |
| `EMBEDDING_SEND_DIMENSIONS` | No | Tri-state — `true`/`false`/blank (auto) |
| `SEARCH_PROVIDER` | No | `brave`, `tavily`, `serper`, `jina`, `perplexity`, `searxng`, `duckduckgo` |
| `SEARCH_API_KEY` | No | Search API key |
| `SEARCH_BASE_URL` | No | Required for self-hosted SearXNG |
| `SEARCH_PROXY` | No | Optional HTTP/HTTPS proxy for outbound search traffic |
| `BACKEND_PORT` | No | Backend port (default `8001`) |
| `FRONTEND_PORT` | No | Frontend port (default `3782`) |
| `POCKETBASE_PORT` | No | Docker port mapping for the optional PocketBase sidecar (default `8090`) |
| `NEXT_PUBLIC_API_BASE_EXTERNAL` | No | Public backend URL for cloud deployment |
| `NEXT_PUBLIC_API_BASE` | No | Direct backend URL override for the Next.js client |
| `CORS_ORIGIN` | No | Single extra origin appended to the FastAPI CORS allowlist |
| `CORS_ORIGINS` | No | Comma/newline-separated extra origins for authenticated remote deployments |
| `DISABLE_SSL_VERIFY` | No | Disable outbound TLS verification (default `false`) |
| `AUTH_ENABLED` | No | Require login when `true` (default `false`) |
| `NEXT_PUBLIC_AUTH_ENABLED` | No | Optional frontend override; blank derives from `AUTH_ENABLED` |
| `AUTH_SECRET` | No | JWT signing secret; generated under `multi-user/_system/auth/auth_secret` if blank |
| `AUTH_TOKEN_EXPIRE_HOURS` | No | Session duration in hours (default `24`) |
| `AUTH_COOKIE_SECURE` | No | Mark the auth cookie `Secure` when serving over HTTPS (default `false`) |
| `AUTH_USERNAME` | No | Single-user mode: admin username |
| `AUTH_PASSWORD_HASH` | No | Single-user mode: bcrypt hash of admin password |
| `POCKETBASE_URL` | No | Enable the PocketBase sidecar by setting it (single-user only — see warning above) |
| `POCKETBASE_ADMIN_EMAIL` / `POCKETBASE_ADMIN_PASSWORD` | No | Admin credentials for the Python backend to manage PocketBase collections |
| `POCKETBASE_EXTERNAL_URL` | No | Public PocketBase URL for OAuth redirects (remote deployments only) |
| `CHAT_ATTACHMENT_DIR` | No | Override for the chat attachment storage root |

</details>

### Option D — CLI Only

If you just want the CLI without the web frontend:

```bash
# Includes RAG, document parsing, and all built-in LLM provider SDKs.
# Same set as Option B minus FastAPI/uvicorn.
python -m pip install -e ".[cli]"
```

You still need to configure your LLM provider. The quickest way:

```bash
cp .env.example .env   # then edit .env to fill in your API keys
```

Once configured, you're ready to go:

```bash
deeptutor chat                                   # Interactive REPL
deeptutor run chat "Explain Fourier transform"   # One-shot capability
deeptutor run deep_solve "Solve x^2 = 4"         # Multi-agent problem solving
deeptutor kb create my-kb --doc textbook.pdf     # Build a knowledge base
```

> See [DeepTutor CLI](#%EF%B8%8F-deeptutor-cli--agent-native-interface) for the full feature guide and command reference.
>>>>>>> ac8f00b (prepare v1.3.10 release)

---
=======
Minimal model setup can be done in the browser: open **Settings → Models**, add an LLM profile, set Base URL / API key / model name, and save. Add an embedding profile only if you plan to use Knowledge Base / RAG features.
>>>>>>> 85779c8 (refactor env settings and installation)

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

<<<<<<< HEAD
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
=======
**Quick start (5 steps):**

```bash
# 1. Enable auth in data/user/settings/auth.json:
#    {"enabled": true, "token_expire_hours": 24, "cookie_secure": false}

# 2. Restart the web stack.
deeptutor start

# 3. Open http://localhost:3782/register and create the first account.
#    The first registration is the only public one; that user becomes admin
#    and the /register endpoint is closed automatically afterward.

# 4. As admin, navigate to /admin/users → "Add user" to provision teammates.

# 5. For each user, click the slider icon → assign LLM profiles, knowledge
#    bases, and skills. Save. The user can now sign in and start working.
```

**What the admin sees:**

- **Full Settings page** at `/settings` — manage LLM / embedding / search providers, API keys, model catalogs, and runtime "Apply".
- **User management** at `/admin/users` — create, promote, demote, and delete accounts. The public `/register` endpoint is automatically closed once the first admin exists; further accounts go through `POST /api/v1/auth/users` (admin-only).
- **Grant editor** — for each non-admin user, pick the model profiles, knowledge bases, and skills they may use. Grants carry **logical IDs only**; API keys never cross the grant boundary.
- **Audit trail** — every grant change and assigned-resource access is appended to `multi-user/_system/audit/usage.jsonl`.

**What ordinary users get:**

- **Isolated workspace** under `multi-user/<uid>/` — their own chat history (`chat_history.db`), memory (`SUMMARY.md` / `PROFILE.md`), notebooks, and personal knowledge bases. Nothing is shared by default.
- **Read-only access** to admin-assigned knowledge bases and skills, surfaced inline next to their own resources with an "Assigned by admin" badge.
- **Redacted Settings page** — only theme, language, and a summary of granted models. API keys, base URLs, and provider endpoints are never returned for non-admin requests.
- **Scoped LLM** — chat turns are routed through the admin-assigned model. If no LLM is granted, the turn is rejected up-front (no silent fallback to the admin's keys).

**Workspace layout:**

```
multi-user/
├── _system/
│   ├── auth/users.json          # Hashed credentials, roles
│   ├── auth/auth_secret         # JWT signing secret (auto-generated)
│   ├── grants/<uid>.json        # Per-user resource grants (admin-managed)
│   └── audit/usage.jsonl        # Audit trail
└── <uid>/
    ├── user/
    │   ├── chat_history.db
    │   ├── settings/interface.json
    │   └── workspace/{chat,co-writer,book,...}
    ├── memory/{SUMMARY.md,PROFILE.md}
    └── knowledge_bases/...
```

**Configuration reference:**

| Setting | Required | Description |
|:---|:---|:---|
| `data/user/settings/auth.json: enabled` | Yes | Set to `true` to enable multi-user auth. Default `false` (single-user mode — admin paths everywhere). |
| `multi-user/_system/auth/auth_secret` | Recommended | JWT signing secret. Auto-generated on first authenticated boot if missing. |
| `data/user/settings/auth.json: token_expire_hours` | No | JWT lifetime; defaults to `24`. |
| `data/user/settings/auth.json: username/password_hash` | No | Optional headless single-user bootstrap credential. Leave blank when using browser registration. |
| `data/user/settings/system.json` | No | `deeptutor start` derives frontend auth flags and API base from runtime settings. |

> ⚠️ **PocketBase mode (`integrations.pocketbase_url` set) is single-user only.** The default PocketBase schema has no `role` field on `users` (every login resolves to `role=user`, no admin can be created), and `sessions` / `messages` / `turns` queries are not filtered by `user_id`. Multi-user deployments must keep `integrations.pocketbase_url` blank and use the default JSON/SQLite backend.

> ⚠️ **Single-process recommendation.** The first-user-becomes-admin promotion is protected by an in-process `threading.Lock`. Multi-worker deployments should provision the first admin offline (start with `auth.json.enabled=false`, register the admin via the bootstrap flow, then set `auth.json.enabled=true`) or back the user store with an external system.

## 🗺️ Roadmap

| Status | Milestone |
|:---:|:---|
| 🎯 | **Authentication & Login** — Optional login page for public deployments with multi-user support |
| 🎯 | **Themes & Appearance** — Diverse theme options and customizable UI appearance |
| 🎯 | **Interaction Improvement** — optimize icon design and interaction details |
| 🔜 | **Better Memories** — integrating better memory management |
| 🔜 | **LightRAG Integration** — Integrate [LightRAG](https://github.com/HKUDS/LightRAG) as an advanced knowledge base engine |
| 🔜 | **Documentation Site** — Comprehensive docs page with guides, API reference, and tutorials |

> If you find DeepTutor useful, [give us a star](https://github.com/HKUDS/DeepTutor/stargazers) — it helps us keep going!
>>>>>>> 85779c8 (refactor env settings and installation)

---

## 📖 Story & Impact

*María is 9 years old. She lives in a rural community where her school has one teacher for 42 students. A storm knocks out the internet.*

*But María's tablet still works. Edu — a patient, cheerful voice — asks her how many mangos she'd give to each friend if she had 12 and three friends. She gets it wrong, but Edu never says "wrong." It just tries again, differently.*

*The internet is down. EducaT isn't.*

By providing an adaptive, voice-first, infinitely patient tutor that works entirely offline, EducaT aims to close the educational equity gap and build community resilience.
