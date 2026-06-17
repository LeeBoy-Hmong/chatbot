# AskLee AI — RAG Chatbot for GolieXeeGardens

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-DC143C?style=flat)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=flat&logo=supabase&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat)

AskLee AI is a Retrieval-Augmented Generation (RAG) chatbot embedded into the [GolieXeeGardens](https://golieXeegardens.com) website. It helps site visitors get instant answers to frequently asked questions while passively collecting insight data for the team — all powered by a self-hosted language model running on edge hardware.

---

## Why This Project

This chatbot serves two purposes. For the business, it reduces repetitive support load by giving visitors a conversational way to find answers directly from GolieXeeGardens' own documentation. For me as a developer, it's a hands-on production project that deepens my skills in AI engineering — specifically RAG pipelines, vector search, embedding models, and deploying LLMs on constrained hardware.

RAG is one of my favorite AI frameworks because it keeps the model grounded in real, up-to-date knowledge rather than hallucinated outputs — making it genuinely useful in a business context.

---

## Features

- 💬 **Conversational FAQ** — answers visitor questions using content from GolieXeeGardens' knowledge base
- 🔍 **RAG Pipeline** — retrieves semantically relevant context before generating a response
- 🧠 **Chat History** — maintains conversation context across turns
- 📦 **REST API** — clean `/api/chat` endpoint for frontend integration
- 🌱 **Edge Inference** — LLM runs locally on a Jetson Orin Nano (8GB), keeping costs low
- 📊 **Data Collection** — conversation data stored in Supabase for team analysis
- 📎 **Knowledge Sync** — pulls documentation via BetterDocs REST API (Hostinger)

---

## Architecture

```
User (Browser)
     │
     ▼
Chat Widget (HTML / CSS / JS)
     │
     ▼
FastAPI Backend  ──────────────────────────────────────┐
     │                                                  │
     ├── Embedding (Sentence Transformers)              │
     │        │                                         │
     │        ▼                                         │
     ├── Qdrant Cloud (Vector Search)                   │
     │        │                                         │
     │        ▼                                         │
     ├── LangChain RAG Pipeline                         │
     │        │                                         │
     │        ▼                                         │
     ├── Ollama LLM (Jetson Orin Nano 8GB)              │
     │                                                  │
     ├── Supabase / PostgreSQL (Chat History + Data)    │
     │                                                  │
     └── BetterDocs API (Knowledge Base Source) ────────┘
```

---

## Tech Stack

| Layer | Technology | Reason |
|---|---|---|
| **Frontend** | HTML, CSS, JavaScript | Lightweight embeddable chat widget |
| **Backend** | Python + FastAPI | Async performance, auto-generated API docs |
| **Vector DB** | Qdrant Cloud | Scalable semantic search, cloud-managed |
| **Knowledge Storage** | Supabase (PostgreSQL) | Managed Postgres, real-time, free tier |
| **Knowledge Source** | BetterDocs (Hostinger) | REST API access to site documentation |
| **Embeddings** | Sentence Transformers (HuggingFace) | Open-source, runs fully local |
| **LLM Inference** | Ollama on Jetson Orin Nano 8GB | Self-hosted, zero API costs |
| **Hosting** | Render (free tier) | Easy FastAPI deployment, overlaps with site |

---

## Project Structure

```
asklee-ai/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── api/
│   │   └── chat.py          # /api/chat endpoint
│   ├── rag/
│   │   ├── pipeline.py      # LangChain RAG chain
│   │   ├── retriever.py     # Qdrant vector search
│   │   └── embedder.py      # Sentence Transformers embedding
│   ├── db/
│   │   └── supabase.py      # Chat history read/write
│   └── knowledge/
│       └── betterDocs.py    # BetterDocs API sync
├── frontend/
│   ├── widget.html          # Embeddable chat widget
│   ├── widget.css
│   └── widget.js
├── scripts/
│   └── ingest.py            # Knowledge base ingestion into Qdrant
├── .env.example             # Environment variable template
├── requirements.txt
└── README.md
```

> **Note:** Update this tree to match your actual structure as the project evolves.

---

## Getting Started

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai) installed and running (locally or on your Jetson Orin Nano)
- A [Qdrant Cloud](https://cloud.qdrant.io) account and cluster
- A [Supabase](https://supabase.com) project with PostgreSQL enabled
- BetterDocs API credentials (via Hostinger)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/asklee-ai.git
cd asklee-ai
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your credentials (see [Environment Variables](#environment-variables) below).

### 5. Pull your Ollama model

```bash
ollama pull <your-model-name>
```

### 6. Ingest your knowledge base

```bash
python scripts/ingest.py
```

This fetches content from BetterDocs, generates embeddings, and upserts them into Qdrant.

### 7. Run the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Docs at `http://localhost:8000/docs`.

---

## Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```env
# Qdrant
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION=asklee

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key

# BetterDocs / Hostinger
BETTERDOCS_API_URL=https://your-site.com/wp-json/betterdocs/v1
BETTERDOCS_API_KEY=your_api_key

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=your-model-name

# Embedding
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

---

## API Reference

### `POST /api/chat`

Send a user message and receive a RAG-generated response.

**Request body:**

```json
{
  "session_id": "abc123",
  "message": "What are your store hours?"
}
```

**Response:**

```json
{
  "session_id": "abc123",
  "response": "GolieXeeGardens is open Monday–Saturday, 9am–6pm.",
  "sources": ["faq-hours.md"]
}
```

**Example curl:**

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "abc123", "message": "What are your store hours?"}'
```

---

## Roadmap

- [ ] Admin dashboard for reviewing collected conversation data
- [ ] Support for streaming responses (SSE)
- [ ] Multi-language support
- [ ] Feedback thumbs-up/down on responses for fine-tuning signals
- [ ] Swap Ollama model without restarting the server
- [ ] Docker + docker-compose setup for easier local dev

---

## Known Limitations

- Inference speed is dependent on the Jetson Orin Nano — responses may be slower under load
- Knowledge base must be manually re-ingested after documentation updates (automation planned)
- Free tier Render hosting may cause cold starts on the API

---

## Contributing

Contributions are welcome! Here's how to get involved:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to your branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please open an issue first for major changes so we can discuss the direction.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Author

Built by **Michael** — an aspiring AI engineer learning by building real production systems.

> *AskLee AI is part of a larger effort to modernize the GolieXeeGardens web experience through thoughtful AI integration.*
