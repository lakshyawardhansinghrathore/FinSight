# Deployment Guide — AI-Powered Investor Intelligence Platform

## Overview

This document explains how to build, test, and deploy the application using Docker. The project uses **Render** for cloud hosting.

Deployment Flow:
```text
Local Code + Dockerfile
        ↓
  GitHub Repository
        ↓
    Render.com
        ↓
  Public Application URL
```

---

# Part 1: Local Deployment (Testing)

Always verify the application works locally before pushing to the cloud.

### Step 1: Build the Docker Image

Open your terminal in the project root and run:

```bash
docker build -t invint .
```

This uses `python:3.12-slim` as the base image and installs all dependencies via `uv` with the `--index-strategy unsafe-best-match` flag, which is needed to correctly resolve PyTorch (CPU build) alongside PyPI packages.

Verify the image was created:

```bash
docker images
```

**Expected Output:**
```text
REPOSITORY    TAG       IMAGE ID       CREATED          SIZE
invint        latest    <image-id>     <time>           ~2.4GB
```

### Step 2: Run the Container Locally

Pass your `.env` file to the container. Values in `.env` must **NOT** have quotes around them (Docker's `--env-file` does not strip quotes like `python-dotenv` does):

```bash
docker run -p 8000:8000 --env-file .env invint
```

**Expected startup output:**
```text
INFO:     Started server process [1]
INFO:     Waiting for application startup.
Database 'postgres' already exists.
financial_metrics table created.
ChromaDB collection 'documents' initialized at ./chroma_data
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Verify the app is running:**
- Open your browser: `http://localhost:8000`
- Dashboard renders with the KPI table
- PDF upload panel is visible
- Chat panel is functional

**Stop the container:**
```
Ctrl + C
```

---

# Part 2: Cloud Deployment (Render)

Render is a cloud platform that natively supports Docker. It will automatically build your `dockerfile` and host your app.

### Step 1: Push Your Code to GitHub

Render pulls your source code from a Git repository.

```bash
git add .
git commit -m "Ready for deployment"
git branch -M main
git remote add origin https://github.com/your-username/your-repo-name.git
git push -u origin main
```

> Your `.env` file is already listed in `.gitignore` and will never be committed. Keep it that way — **never push your secrets to GitHub**.

### Step 2: Create a Web Service on Render

1. Go to [Render.com](https://render.com) and sign in with your GitHub account.
2. Click **"New +"** → Select **"Web Service"**.
3. Connect your GitHub account and select your repository.
4. Render will automatically detect the `dockerfile`.
5. Set the **Name** (e.g., `invint-app`).
6. Select the **Free** plan.

### Step 3: Add Environment Variables

Since `.env` is not on GitHub, manually add each variable in the Render dashboard:

1. Scroll to the **Environment Variables** section.
2. Add each of the following:

| Key | Value |
|---|---|
| `GEMINI_API_KEY` | Your Google AI Studio API key |
| `GEMINI_CHAT_MODEL` | `gemini-3.6-flash` |
| `POSTGRES_HOST` | Your Supabase Transaction Pooler host |
| `POSTGRES_PORT` | `6543` |
| `POSTGRES_USER` | Your Supabase user (e.g., `postgres.yourprojectref`) |
| `POSTGRES_PASSWORD` | Your Supabase database password |
| `POSTGRES_DATABASE` | `postgres` |

> Do NOT wrap values in quotes in the Render dashboard — just paste the raw value.

### Step 4: Deploy

1. Click **"Create Web Service"**.
2. Render will clone your repo, build the Docker image, and deploy it.
3. Once the status shows **"Live"**, click the URL at the top (e.g., `https://invint-app.onrender.com`).

Your application is now live on the internet!

---

# Common Issues & Fixes

| Issue | Cause | Fix |
|---|---|---|
| `failed to connect to docker API` | Docker Desktop is not running | Open Docker Desktop and wait for it to fully start |
| `invalid integer value ""6543""` | Quotes around values in `.env` | Remove all quotes from `.env` values |
| `No such file or directory` (psycopg2 socket) | Missing env vars — app tried local PostgreSQL | Always use `--env-file .env` when running the container |
| `No solution found` (uv dependency error) | PyTorch index conflict | The `dockerfile` already includes `--index-strategy unsafe-best-match` to fix this |
