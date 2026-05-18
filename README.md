# EducaT — Adaptive Offline AI Tutor with P2P Knowledge Mesh

> **One-Liner**
> EducaT is a **100% offline-first adaptive tutoring system** (built as a fork of the open-source **DeepTutor** project) powered by quantized Gemma 4, democratizing personalized education in disconnected, crisis-prone communities.

**Hackathon:** [Gemma 4 Good — Kaggle × Google DeepMind](https://www.kaggle.com/competitions/gemma-4-good-hackathon)  
**Tracks:** `Future of Education` · `Global Resilience`  
**Model:** Gemma 4 E2B (INT4 quantized) + Gemma 4 E4B (fallback)  
**License:** Apache 2.0  

---

## 🚀 Get Started

The easiest way to evaluate the project is to run it using Docker Compose. This provides a one-command setup for the full stack (LiteRTLM API and FastAPI backend).

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
