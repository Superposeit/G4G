---
title: Research Index — EducaT
date: 2026-04-17
version: 0.2.0
tags:
  - research
  - index
status: stable
---

# Research Index

All academic papers, technical reports, curriculum documents, and reference projects relevant to EducaT.
Each entry must have a corresponding note before being cited in `docs/` or `main.md`.

---

## Reading Status Legend

| Symbol | Meaning |
|---|---|
| ✅ | Note written, relevance assessed |
| 🔄 | Reading in progress |
| 📋 | Queued — not yet read |
| ❌ | Read, determined not relevant |

---

## Curriculum Sources (MINERD Official)

> These are the authoritative curriculum documents for EducaT topic alignment.
> Both extracted from official MINERD Adecuación Curricular PDFs (2023).

| Status | Document | Coverage | EducaT Use |
|---|---|---|---|
| ✅ | [[MINERD_curriculum-primaria\|MINERD Matemática Nivel Primario (2023)]] | Grades 1–6 full: numeración, geometría, medición, estadística per grade; competencias, procedimientos, indicadores de logro | **Phase 1 MVP** — all pilot topics (addition→fractions) directly traceable to MINERD refs; localization context; evaluation types |
| ✅ | [[MINERD_curriculum-secundaria\|MINERD Matemática Nivel Secundario (2023)]] | Grades 7–12 full: 1er Ciclo (integers, rationals, algebra, polynomials, functions) + 2do Ciclo (geometry, trigonometry, calculus) | **Phase 2** reference — Grades 7–9 expansion planning; complete topic map for long-term roadmap |

**How to use these files:**
- Topic YAML `curriculum_ref` field → `MINERD-Primaria-2023-G[grade]-[block]` or `MINERD-Secundaria-2023-G[grade]-[block]`
- Localization examples must follow MINERD cross-curricular axes (health, environment, citizenship, personal development)
- Pilot topic alignment → see EducaT Alignment section at bottom of `MINERD_curriculum-secundaria.md`

---

## Model Compression & Edge Deployment

| Status | Paper | Key Claim | EducaT Relevance |
|---|---|---|---|
| ✅ | [[papers/LTH_lottery-ticket-hypothesis\|LTH — Frankle & Carlin (ICLR 2019)]] | Dense networks contain sparse winning-ticket subnetworks at 10–20% size | Prune Gemma 4 E2B before INT4 quant → compound compression for 2 GB RAM target |
| 📋 | SparseGPT — Frantar & Alistarh (ICML 2023) | One-shot pruning of LLMs to 50%+ sparsity without retraining | Implementation tool for LTH strategy on Gemma 4 |
| 📋 | Wanda — Sun et al. (ICLR 2024) | Weight pruning via activation statistics, faster than SparseGPT | Faster alternative to SparseGPT for hackathon timeline |
| 📋 | GPTQ — Frantar et al. (ICLR 2023) | Layer-wise INT4 quantization with minimal perplexity loss | Backing theory for our Q4_K_M quantization choice |
| 📋 | LLM in a Flash — Apple (2024) | LLM inference on devices with limited DRAM via flash storage | Relevant if SD680 RAM proves insufficient even after compression |

---

## Pedagogy & Adaptive Learning

| Status | Paper | Key Claim | EducaT Relevance |
|---|---|---|---|
| 📋 | Vygotsky — Zone of Proximal Development (1978) | Learning optimal in ZPD: tasks slightly beyond current ability with guidance | Theoretical basis for scaffolding in Thinking Mode prompt |
| 📋 | Bloom's 2-Sigma Problem — Bloom (1984) | 1-on-1 tutoring produces 2 standard deviation improvement over classroom | Justifies AI tutor as transformative, not just convenient |
| 📋 | DeepTutor — HKUDS (2025) | Multi-agent dual-loop tutoring with RAG + web search | Architecture reference for agent reasoning structure |

---

## P2P & Offline Systems

| Status | Paper | Key Claim | EducaT Relevance |
|---|---|---|---|
| 📋 | Gossip Protocols — Demers et al. (1987) | Epidemic information dissemination in distributed systems | Theoretical basis for knowledge capsule propagation in mesh |
| 📋 | Wi-Fi Direct: A Survey — Camps-Mur et al. (2013) | P2P Wi-Fi Direct capability, latency, and range characteristics | Technical backing for our primary P2P transport choice |

---

## Reference Projects

| Status | Project | Relevance |
|---|---|---|
| ✅ | [DeepTutor — HKUDS](https://github.com/HKUDS/DeepTutor) | Multi-agent tutoring: dual-loop reasoning, RAG pipeline, Docker patterns |
| 📋 | [llama.cpp](https://github.com/ggml-org/llama.cpp) | INT4 quantization and CPU inference for Gemma 4 E2B |
| 📋 | [Coqui TTS](https://github.com/coqui-ai/TTS) | Local Spanish TTS engine for voice output |
| 📋 | [SparseGPT](https://github.com/IST-DASLab/sparsegpt) | LTH implementation tool for Gemma 4 pruning |

---

## Priority Reading Order (by deadline impact)

1. ✅ **MINERD Primaria** — done; use directly for pilot topic YAMLs
2. ✅ **MINERD Secundaria** — done; Phase 2 reference locked
3. ✅ **LTH** — documented; informs Week 4 model optimization
4. 📋 **SparseGPT / Wanda** — needed before attempting pruning experiment
5. 📋 **Bloom 2-Sigma** — strengthens judging narrative (education track)
6. 📋 **Vygotsky ZPD** — tightens pedagogical prompt engineering rationale
7. 📋 **Wi-Fi Direct survey** — validates P2P design assumptions

---

## How to Add a Document

**For curriculum/official docs (root `research/`):**
1. Create `research/ACRONYM_descriptor.md` with frontmatter + full content extraction
2. Add row to Curriculum Sources table above
3. Add `curriculum_ref` mapping note in EducaT alignment section of the doc
4. Update [[CHANGELOG]]

**For academic papers (`research/papers/`):**
1. Write note in `research/papers/ACRONYM_title.md` following the LTH template
2. Add row to appropriate table above (mark 🔄 while writing, ✅ when complete)
3. Add citation to relevant `docs/` section
4. Update [[CHANGELOG]]
