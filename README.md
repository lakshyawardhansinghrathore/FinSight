# 🧠 AI-Powered Investor Intelligence Platform

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-FF6B35?style=for-the-badge)](https://www.trychroma.com)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Render](https://img.shields.io/badge/Deploy%20on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-finsight--64nj.onrender.com-00C7B7?style=for-the-badge&logo=render&logoColor=white)](https://finsight-64nj.onrender.com)

**An intelligent RAG-powered platform that ingests corporate financial reports (PDFs), automatically extracts KPIs, and lets investors query insights using natural language.**

🔗 **Live App:** [https://finsight-64nj.onrender.com](https://finsight-64nj.onrender.com)

</div>

---

## ✨ What It Does

Upload a company's annual report PDF and the platform will:

1. **Parse** the PDF into structured markdown using PyMuPDF
2. **Chunk** the content using HuggingFace semantic chunking for high-quality retrieval
3. **Embed** the chunks locally using `all-MiniLM-L6-v2` (runs on CPU, 100% free)
4. **Store** embeddings in a local ChromaDB vector store (persisted to `./chroma_data`)
5. **Extract** key financial KPIs (Revenue, Net Income, Cash Flow, Risk Factors, Growth Drivers) using Google Gemini AI with structured output
6. **Save** extracted metrics to PostgreSQL (Supabase) for dashboard display
7. **Chat** with your financial data using a RAG-powered conversational interface powered by Gemini

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Application                          │
├──────────────────┬──────────────────────┬───────────────────────┤
│  POST /api/upload│  POST /api/chat      │  GET /api/metrics     │
│  PDF Ingestion   │  RAG Chatbot         │  KPI Dashboard        │
└────────┬─────────┴────────┬─────────────┴──────────┬────────────┘
         │                  │                         │
         ▼                  ▼                         ▼
┌─────────────────┐ ┌──────────────────┐ ┌────────────────────────┐
│  PDF → Markdown │ │  HuggingFace     │ │  Supabase              │
│  (PyMuPDF4LLM)  │ │  all-MiniLM-L6  │ │  (PostgreSQL)          │
│                 │ │  + ChromaDB      │ │                        │
│  Semantic       │ │  Similarity      │ │  financial_metrics     │
│  Chunking       │ │  Search (top_k=20│ │  table                 │
└────────┬────────┘ └──────────────────┘ └────────────────────────┘
         │
         ▼
┌─────────────────┐
│  Google Gemini  │
│  KPI Extraction │
│  (Structured    │
│   JSON Output)  │
└─────────────────┘
```

---

## 🚀 Tech Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | FastAPI + Uvicorn |
| **AI / LLM** | Google Gemini (`gemini-3.6-flash`) via `langchain-google-genai` |
| **Vector Embeddings** | HuggingFace `all-MiniLM-L6-v2` (local, CPU, free) |
| **Vector Store** | ChromaDB (local persistence at `./chroma_data`) |
| **Document Parsing** | PyMuPDF4LLM (PDF → Markdown) |
| **Semantic Chunking** | LangChain Experimental `SemanticChunker` |
| **Database** | PostgreSQL via Supabase (Transaction Pooler, SSL) |
| **ORM / Driver** | SQLAlchemy + psycopg2-binary |
| **Package Manager** | UV |
| **Containerization** | Docker (`python:3.12-slim`) |
| **Cloud Hosting** | Render |
| **CI Pipeline** | GitHub Actions |

---

## 📋 Prerequisites

- Python 3.12
- [UV Package Manager](https://docs.astral.sh/uv/)
- A free [Google AI Studio](https://aistudio.google.com/app/apikey) account (for the Gemini API key)
- A free [Supabase](https://supabase.com) account (for PostgreSQL)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (for containerized runs)

---

## ⚡ Quick Start

### 1. Install UV

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone & Setup

```bash
git clone https://github.com/lakshyawardhansinghrathore/FinSight.git
cd A2

# Create virtual environment
uv venv

# Activate it
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies (PyTorch CPU build from separate index)
uv pip install --index-strategy unsafe-best-match --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory (no quotes around values):

```env
# Google Gemini (Free — get key at https://aistudio.google.com/app/apikey)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_CHAT_MODEL=gemini-3.6-flash

# Supabase PostgreSQL (Free — get from Supabase Dashboard > Settings > Database > Transaction Pooler)
POSTGRES_HOST=aws-0-xx-xxxx-x.pooler.supabase.com
POSTGRES_PORT=6543
POSTGRES_USER=postgres.your_project_ref
POSTGRES_PASSWORD=your_database_password
POSTGRES_DATABASE=postgres
```

> **Important:** Use the **Transaction Pooler** connection string from Supabase (port `6543`), not the Direct Connection. It supports both IPv4 and IPv6 and is required when running inside Docker.

> **Important:** Do NOT use quotes around values in `.env` — the Docker `--env-file` flag will include the quotes as part of the value, breaking the database connection.

### 4. Run the Application

**Option A: Directly with Python**
```bash
python app.py
```

**Option B: With Docker**
```bash
# Build the image
docker build -t invint .

# Run the container (pass env vars without quotes in .env)
docker run -p 8000:8000 --env-file .env invint
```

Open your browser and navigate to **[http://localhost:8000](http://localhost:8000)**

---

## 📁 Project Structure

```
A2/
├── app.py                      # FastAPI entry point, startup events, route registration
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker container definition (python:3.12-slim + uv)
├── .env                        # Local secrets — never commit this!
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI — builds Docker image on every push
│
├── routes/
│   ├── ingestion.py            # POST /api/upload — handles PDF upload & triggers pipeline
│   └── chat.py                 # POST /api/chat — RAG chatbot using Gemini + ChromaDB
│
├── ingestion/
│   ├── pdf_to_markdown.py      # PDF → Markdown conversion (PyMuPDF4LLM)
│   ├── semantic_chunker.py     # Semantic chunking (HuggingFace all-MiniLM-L6-v2)
│   └── ingest_documents.py     # Full ingestion pipeline orchestrator
│
├── rag/
│   └── kpi_extractor_rag.py    # KPI extraction via RAG + Gemini structured output
│
├── llm/
│   └── gemini_client.py        # Google Gemini structured output client
│
├── vectorstore/
│   ├── chroma_db.py            # ChromaDB vector store wrapper + Retriever class
│   └── create_index.py         # Collection initialization at startup
│
├── database/
│   ├── postgres_sql.py         # PostgreSQL connection via SQLAlchemy (SSL, URL-encoded creds)
│   ├── create_table.py         # financial_metrics table schema
│   ├── save_metrics.py         # Upsert KPI records to PostgreSQL
│   └── metrics.py              # Query layer for dashboard metrics
│
├── templates/
│   └── dashboard.html          # Jinja2 investor dashboard UI
│
├── static/
│   └── style.css               # Dashboard styles
│
├── data/
│   └── raw_pdfs/               # Uploaded PDF storage directory
│
└── chroma_data/                # Local ChromaDB vector store (auto-created on first run)
```

---

## 🧪 How to Use

1. **Start the server**: `python app.py` or `docker run -p 8000:8000 --env-file .env invint`
2. **Open the dashboard**: [http://localhost:8000](http://localhost:8000)
3. **Upload a PDF**: Use the upload panel to upload a company's annual report. Name the file as `YEAR_CompanyName.pdf` (e.g., `2024_Apple.pdf`) so the ingestion pipeline can automatically parse the company and year.
4. **View KPIs**: After processing, the dashboard will display the extracted financial metrics in a table.
5. **Chat**: Ask questions in the chat panel, e.g.:
   - *"What were Apple's top risk factors in 2024?"*
   - *"What was Tesla's revenue in 2023?"*
   - *"Compare Apple's net income with Microsoft's"*

---

## 📊 Extracted KPIs

The platform automatically extracts the following metrics from each report using Gemini structured output:

| KPI | Description |
|---|---|
| **Revenue** | Total annual revenue |
| **Net Income** | Net profitability after all expenses |
| **Operating Income** | Earnings from core business operations |
| **Operating Cash Flow** | Cash generated from operations |
| **Total Assets** | Total economic resources |
| **Total Liabilities** | Total outstanding obligations |
| **Top Risk Factors** | Key risks identified in the annual report |
| **Top Growth Drivers** | Key growth catalysts identified in the report |



## 🐳 Docker

```bash
# Build the image (uses uv for fast installs, --index-strategy for PyTorch CPU)
docker build -t invint .

# Run the container
docker run -p 8000:8000 --env-file .env invint
```

> The `Dockerfile` uses `python:3.12-slim` as the base image and installs dependencies via `uv` with `--index-strategy unsafe-best-match` to correctly resolve PyTorch and other packages across multiple indexes (PyPI + PyTorch CPU).

---


<div align="center">
  Built with ❤️ using FastAPI, Google Gemini, ChromaDB & Supabase
</div>
