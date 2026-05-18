---
title: CHANGELOG
date: 2026-04-17
tags:
  - meta
  - versioning
---

# CHANGELOG

All notable changes to EducaT documentation are recorded here.
Format: [Semantic Versioning](https://semver.org) — `MAJOR.MINOR.PATCH`

- **MAJOR** — complete concept pivot or track change
- **MINOR** — new section, new document, significant content addition
- **PATCH** — corrections, rewording, formatting fixes

---

## [0.3.0] — 2026-04-25

### Added
- `docs/07_training-pipeline.md` — Full pipeline: dataset generation, QLoRA fine-tuning via Unsloth, Wanda pruning, GGUF conversion, INT4 quantization, LiteRT-LM conversion. Includes skip conditions and artifact summary.
- `docs/08_benchmarking.md` — Device matrix (MINERD fleet: SD662, Unisoc T618, Alcatel MT8768), latency/memory/quality/throughput benchmarks, min-spec determination protocol, regression test suite, benchmark recording template.
- `docs/09_deployment-stack.md` — Full deployment documentation: WSL2 dev stack (LiteRT-LM + DeepTutor + Windows bridge), Dokploy-managed cloud deployment (Docker Compose, 4 GB and 8 GB memory budgets), request sequence diagram, Android LiteRT-LM integration, image support roadmap (Path A: transformers multimodal; Path B: client-side moondream2 description).

### Changed
- Hardware target updated: SD662 (Samsung Galaxy Tab A7 2020, 3 GB RAM) confirmed as absolute minimum — harder than SD680 previously assumed. Latency expectations adjusted accordingly.
- LiteRT-LM confirmed as primary Android runtime (not llama.cpp) — llama.cpp too slow on SD662 for real-time tutoring.

### Decisions
- Dokploy chosen as PaaS layer for cloud demo (self-hosted, free, Docker Compose native, Traefik SSL included)
- Image support deferred: Path B (client-side moondream2 description) targeted for Week 4 as hackathon-viable option
- n8n included in stack but flagged as first service to disable if 4 GB server hits OOM
- DeepTutor RAG layer confirmed in stack with multilingual embeddings (paraphrase-multilingual-MiniLM-L12-v2)

## [Unreleased]

- Research index with Lottery Ticket Hypothesis integration
- P2P network design detailed spec
- MINERD curriculum YAML schema definition
- Resolve grade range: 1–6 vs 3–9
- Resolve reading comprehension scope: in vs out

## [0.4.0] — 2026-05-10

### Added
- `docs/10_litertlm-bridge.md` — Comprehensive documentation for the LiteRT-LM Bridge including architecture, API endpoints, configuration, Docker deployment, troubleshooting, and development guide.
- `docs/README.md` — Quick start guide for Docker setup with all services.

### Changed
- `docs/09_deployment-stack.md` — Updated LiteRT-LM setup section to reflect actual implementation using custom FastAPI bridge instead of non-existent `litert-lm serve` CLI command. Added environment variable configuration table and lazy loading documentation.
- `docs/09_deployment-stack.md` — Updated system prompt section to reflect OpenAI format message passing instead of file-based configuration.
- `docs/09_deployment-stack.md` — Updated DeepTutor integration to use correct port (8000 instead of 8080).
- `docs/09_deployment-stack.md` — Updated Open Questions section to remove resolved question about `litert-lm serve` and add new question about single-session limitation handling.

### Fixed
- `litertlm/bridge.py` — Improved error handling with detailed logging and proper exception handling for model loading and generation errors.
- `litertlm/bridge.py` — Added lazy loading for the LiteRT-LM engine to reduce memory usage when idle.
- `litertlm/bridge.py` — Made configuration flexible with environment variables for all settings (host, port, model ID, log level).
- `litertlm/bridge.py` — Added comprehensive docstrings and type hints for better code documentation.
- `litertlm/bridge.py` — Fixed Python version requirement from 3.12 to 3.11+ for better compatibility.
- `docker-compose.yml` — Streamlined setup to run all services by default without requiring `--profile litertlm`. Added automatic model download on first startup with Docker volume persistence.
- `docker-compose.yml` — Updated LiteRT-LM service to use new environment variables and improved health check endpoint.
- `docker-compose.yml` — Added dependency on litertlm service health for deeptutor service.
- `docker-compose.yml` — Added `litertlm-models` volume for model persistence.
- `.env.example` — Added LiteRT-LM configuration section with all supported environment variables. Changed default LLM binding to `litertlm` for out-of-the-box local model support.
- `docs/litertlm-integration.md` — Updated startup section to reflect Docker-first approach with automatic model download.
- `docs/litertlm-model-download.md` — Updated to prioritize Docker Compose workflow with automatic model download.
- `docs/docker-optimization.md` — Added quick start section with streamlined setup instructions.

### Decisions
- Confirmed that official `litert-lm` Python package does not include a built-in HTTP server, making the custom FastAPI bridge necessary.
- Lazy loading implemented to reduce memory footprint on low-end devices.
- Single-session limitation documented with threading lock implementation; future improvements noted for request queue and session pooling.
- Docker-first approach adopted for Windows compatibility (LiteRT-LM lacks Windows wheels).
- Automatic model download in Docker container eliminates manual setup steps.

---

## [0.2.0] — 2026-04-18

### Added
- `main.md §0 Brand Identity` — EducaT name etymology (Taíno layer), TutorRD public alias, mission statement, core values table, primary audience
- `main.md §10 Expected Outcomes & Impact` — formalized three measurable outcomes (learning gains, teacher time reclaimed, scalability blueprint)
- Tech stack: Bun runtime row + FAISS local vector index row

### Changed
- `main.md` version bump 0.1.0 → 0.2.0
- `main.md` alias list updated: added `TutorRD`
- `main.md §11` References renumbered (was §10)

### Decisions Needed (Open)
- Grade range: original scope grades 1–6 vs `EducaT_Project_Draft.md` grades 3–9
- Reading comprehension: currently out-of-scope; draft proposes it as in-scope module

### Source
- `EducaT_Project_Draft.md` — new brand/mission/outcomes content merged

---

## [0.1.0] — 2026-04-17

### Added
- `main.md` — Master EducaT technical draft (10 sections)
  - Problem Statement with RD education crisis statistics
  - Objectives (primary + stretch)
  - Scope with hackathon boundary + fine-tuning expert ruling
  - Justification: Gemma 4 capability table + P2P resilience argument
  - Tech Stack: full table, Mermaid architecture, data schemas
  - Branding & storytelling (María narrative)
  - 5-week development roadmap
  - Risk matrix (6 risks)
  - Scalability path: RD → Caribbean → Africa → Global
- `README.md` — Repo navigation hub
- `CHANGELOG.md` — This file
- `CONTRIBUTING.md` — Working conventions
- `.rules/doc-rules.md` — Documentation + versioning rules
- `docs/` — Modular spec stubs (01–06)
- `research/papers/LTH_lottery-ticket-hypothesis.md` — Frankle & Carlin 2019 note
- `research/index.md` — Research reading list
- `versions/v0.1.0/snapshot-notes.md` — Initial version snapshot record

### Decisions
- Merged two hackathon ideas (Edu-Paciencia + Guardian Local) into unified EducaT
- Chose prompt engineering over QLoRA fine-tuning for MVP (time-risk tradeoff)
- Selected Gemma 4 E2B INT4 Q4_K_M as primary model target (~1.4 GB on device)
- Identified Lottery Ticket Hypothesis as theoretical backing for model compression

### Source
- Meeting transcript: `Gemma_Hackathon_2026-04-16` (VTT)
- Reference concept: `07_edu-paciencia.md`
- Reference project: [DeepTutor — HKUDS](https://github.com/HKUDS/DeepTutor)

---

## Version Tagging Convention

```
git tag -a v0.1.0 -m "Initial EducaT technical draft"
git push origin v0.1.0
```

Frozen snapshots live in `versions/vX.Y.Z/snapshot-notes.md`.
