# Bilaad AI: Luxury Real Estate RAG Portfolio Assistant

Bilaad AI is an enterprise-grade, investor-focused real estate RAG (Retrieval-Augmented Generation) prototype. It connects high-net-worth investors with the sustainable, destination-themed property portfolio of **Bilaad Realty** in Abuja, Nigeria. 

The application features a modern dual-theme workstation dashboard built with **Next.js 15 (App Router, Turbopack)** and a resilient asynchronous search agent built with **FastAPI**, **LangGraph**, and **Supabase (pgvector)**.

---

## 🏗️ Architecture Overview

The project is structured as a monorepo separated into two decoupled components:

```mermaid
graph TD
    A[Next.js 15 Workstation Client] <-->|HTTP /chat| B[FastAPI Backend Server]
    B -->|State Machine Execution| C[LangGraph Agent Engine]
    C -->|Query Embeddings| D[Google Gemini API]
    C -->|pgvector Query| E[Supabase Vector Database]
    B -->|Live Web Crawler| F[Bilaad WordPress Site]
```

### 1. Backend Workstation (`/backend`)
* **FastAPI Server**: Lightweight API controller exposing `/chat` and `/ingest` endpoints.
* **LangGraph Agent Engine**: Formulates retrieval-augmented system responses by checking user intents and dynamically routing logic between semantic searches and structural component renders.
* **Supabase pgvector Adaptor**: Implements low-latency vector similarity searching using Google's `gemini-embedding-001` model (dimension 768).
* **Robust Ingestion Pipeline**: Live WordPress site scraping merged with high-fidelity, hand-verified property specifications. Features batch-10 upload sizing and 20-second pauses to guarantee safety under strict Gemini Free Tier rate limits (100 RPM).

### 2. Frontend Workstation (`/frontend`)
* **Next.js 15 (App Router, TS)**: Optimized production client built for performance and speed.
* **Luxury CSS Workspace Layout**: Ivory-Alabaster (light) and Obsidian-Charcoal (dark) color systems utilizing a custom glassmorphism style sheet.
* **Split-Pane Workstation**: Multi-column desktop layout that renders the interactive chat interface on the left and a persistent, detailed Property Showcase card on the right.

---

## 📁 Repository Directory Structure

```text
Bilaad-AI/
├── backend/
│   ├── app/
│   │   ├── config.py         # Configuration validation & environment loaders
│   │   ├── main.py           # FastAPI endpoints & CORS config
│   │   ├── graph.py          # LangGraph state machine, intents, LLM validations
│   │   ├── scraper.py        # 14-property live crawler & rate-limited ingestion
│   │   ├── vector_store.py   # Embedding setup, Supabase client, Postgrest patches
│   │   └── test_agent.py     # System routing & intent verification tests
│   └── requirements.txt      # Python package dependencies
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js App Router root layout & landing page
│   │   └── components/       # Custom React UI components (PropertyCard, ChatInterface)
│   ├── package.json          # Node package dependencies
│   └── tsconfig.json         # TypeScript project configurations
└── .gitignore                # Global version control ignores (locks, environment files)
```

---

## 🗄️ Database & Schema Specifications

### 1. Database Schema
Ensure your Supabase project contains the `documents` table configured with `pgvector` extension:

```sql
-- Enable the pgvector extension to work with embeddings
create extension if not exists vector;

-- Create the documents table
create table documents (
  id bigint primary key generated always as identity,
  content text,
  metadata jsonb,
  embedding vector(768) -- Matches models/gemini-embedding-001 output
);
```

### 2. Similarity Search Function (`match_documents`)
Because newer versions of the Supabase Postgrest SDK enforce named RPC parameters, verify your SQL search function is declared exactly as follows:

```sql
create or replace function match_documents (
  query_embedding vector(768),
  match_threshold float default 0.2,
  match_count int default 5
)
returns table (
  id bigint,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    documents.id,
    documents.content,
    documents.metadata,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where 1 - (documents.embedding <=> query_embedding) > match_threshold
  order by documents.embedding <=> query_embedding asc
  limit match_count;
end;
$$;
```
```

---

## 🛠️ Local Running Guide

### Prerequisites
* Python 3.10+ installed
* Node.js 18+ installed

### 1. Backend Setup
1. Open a terminal and navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Install python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file under `backend/` and configure your API credentials:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_KEY=your_supabase_anon_or_service_key
   ```
4. Start the FastAPI development server:
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### 2. Frontend Setup
1. Open a new terminal and navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Create a `.env.local` file under `frontend/` to point to the local backend:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```
4. Start the Next.js development server:
   ```bash
   npm run dev
   ```

---

## 🚀 MVP Production Deployment Guide

### 📍 Step 1: Deploy Backend (Render)
1. Log in to [Render](https://render.com) and select **New > Web Service**.
2. Connect your GitHub repository (`Bilaad-AI`).
3. Configure the Web Service settings:
   * **Name**: `bilaad-ai-backend`
   * **Runtime**: `Python 3`
   * **Branch**: `main`
   * **Root Directory**: `backend`
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
4. Expand **Advanced** and add the following Environment Variables:
   * `PYTHONPATH`: `..` (This is required so Python can resolve the `backend.app` module imports from the parent directory.)
   * `GEMINI_API_KEY`: Your Google Gemini API Key
   * `SUPABASE_URL`: Your Supabase Project URL
   * `SUPABASE_KEY`: Your Supabase API Key
5. Click **Create Web Service**.

> [!NOTE]
> Render Free Tier instances spin down after 15 minutes of inactivity. The first request to your API after a period of inactivity may take up to 50 seconds to complete while the instance spins back up.

### 📍 Step 2: Deploy Frontend (Vercel)
1. Link your GitHub repository to [Vercel](https://vercel.com).
2. Configure the deployment:
   * **Root Directory**: `frontend`
   * **Environment Variables**:
     * `NEXT_PUBLIC_API_URL` pointing to the public URL of your deployed Render app (e.g., `https://bilaad-ai-backend.onrender.com`).

### 📍 Step 3: Trigger Initial Ingestion
Once the backend is live on Render, call the `/ingest` REST endpoint once to populate the Supabase database with all 14 property specifications:
```powershell
Invoke-WebRequest -Uri https://your-render-app.onrender.com/ingest -Method POST
```


---

## 📱 Premium UX Polish & Error Boundaries

Bilaad AI includes high-end visual alignment, responsive structures, and robust error masking, optimizing the system for executive presentations:

### 1. Mobile Responsive Overhaul
* **Full-Screen Panel Overlays**: On viewports under `768px`, the split-pane property details panel transitions to a dedicated full-screen drawer (`z-index: 100`) containing its own close controls, completely resolving "double-header" stacked layouts.
* **Auto-Stacking Form & Spec Grids**: Mobile layouts automatically drop double-column features and consultation form inputs into structured single-column grids, preventing text truncation or layout overlap.
* **Horizontal Suggestion Chips**: Suggestion query chips slide horizontally in a smooth scrollable list instead of wrapping vertically, saving valuable screen real estate on mobile devices.
* **Mobile Header Resizing**: Logo sizes automatically scale down on mobile layouts to prevent navigation overlaps.

### 2. Client-Facing Error boundaries
* **Gemini Quota Masking**: If a user hits Gemini API Free Tier limits (429 Rate Limits), the backend catches the `RESOURCE_EXHAUSTED` exception and returns a polite, investor-focused notice rather than displaying a raw system traceback.
* **Server Connection Fallback**: If the client fails to connect to the backend (e.g. during a cold-start deployment phase), the interface displays a clean retry fallback notice instead of hardcoded developer paths.

### 3. Contact & Corporate Metadata Scraping
* The web scraper parses the official Bilaad contact page (`https://www.bilaadnigeria.com/contact-us/`) during the ingestion pipeline. All customer care hotlines, social handles, and office addresses are chunked and searchable via the RAG retrieval engine.

---

## 🧪 System Verification

To run intent routing, agent schemas, and Pydantic response contract validation tests, execute:
```bash
python backend/app/test_agent.py
```
Expected output:
```text
[TESTS] Starting LangGraph Routing & Intent Tests...
[RUN] Maldives Intent Routing -> [SUCCESS]
[RUN] Bali Island Intent Routing -> [SUCCESS]
[RUN] General Query (RAG Routing) -> [SUCCESS]
[SUCCESS] All LangGraph routing tests passed successfully!
```
