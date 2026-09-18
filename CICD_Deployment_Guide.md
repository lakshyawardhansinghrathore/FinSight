# GitHub Actions CI/CD Reference Guide

This document explains the Continuous Integration (CI) and Continuous Deployment (CD) pipeline for the Investor Intelligence Platform.

Since we are using **Render** for hosting, our CI/CD pipeline is vastly simpler.

---

# How the Pipeline Works

```text
You push code to GitHub (git push)
        ↓
GitHub Actions (CI)
  → Builds Docker image to verify code is not broken
  → Runs on every push to main & every Pull Request
        ↓
Render (CD — automatic)
  → Detects new commit on main branch
  → Pulls latest code from GitHub
  → Builds Docker image on their servers
  → Deploys new version with zero downtime
```

You never need to manually deploy. As soon as `git push` is done:
- GitHub Actions checks the build
- Render ships the new version to the internet

---

# Continuous Deployment (CD) with Render

Render has **built-in CD**. Once your GitHub repository is connected to a Render Web Service (see `deployment-Document.md`), every push to the `main` branch automatically triggers a new build and deployment.

You do not need any YAML file or extra configuration for this — Render handles it entirely.

---

# Continuous Integration (CI) with GitHub Actions

GitHub Actions runs a CI check to verify that your Docker image builds successfully before code reaches `main`. This catches broken `Dockerfile` configs or missing dependencies early.

## CI Workflow File

Location: `.github/workflows/ci.yml`

```yaml
name: CI Pipeline

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build Docker Image
        run: |
          docker build -t invint:test .
```

---

## Field-by-Field Breakdown

### `name`

```yaml
name: CI Pipeline
```

The label shown in the GitHub Actions dashboard. It helps you identify this pipeline at a glance.

---

### `on`

```yaml
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
```

Defines when to run the pipeline.

- **`push` to `main`**: Runs after every direct commit to `main`.
- **`pull_request` to `main`**: Runs when someone opens or updates a Pull Request targeting `main`.

This ensures that no broken code can land on `main` undetected.

---

### `runs-on`

```yaml
runs-on: ubuntu-latest
```

GitHub spins up a fresh Ubuntu virtual machine in the cloud to execute the job. It is destroyed immediately after the job finishes. This is your temporary build server.

---

### `Checkout Repository`

```yaml
uses: actions/checkout@v4
```

Downloads your repository's source code into the runner's filesystem. Without this step:

```text
Dockerfile → Not Found
Source Code → Not Found
Build → Fails Immediately
```

---

### `Set up Docker Buildx`

```yaml
uses: docker/setup-buildx-action@v3
```

Installs the latest Docker build tooling on the runner. Required for modern, efficient `docker build` commands.

---

### `Build Docker Image`

```yaml
run: |
  docker build -t invint:test .
```

Executes the same `docker build` you run locally. It reads the project's `dockerfile` and installs all dependencies.

**Why this matters for CI:**
- If `requirements.txt` has a broken package version → build fails → GitHub shows a red ❌ on the Pull Request → you know not to merge.
- If the `dockerfile` has a syntax error → same result.
- If everything is fine → green ✅ → safe to merge.

---

# Summary

| Tool | Role | When it runs |
|---|---|---|
| **GitHub Actions** | CI — verifies the Docker image builds | On every `push` and `pull_request` to `main` |
| **Render** | CD — builds and deploys the app to the internet | Automatically on every `push` to `main` |

This gives you a fully automated, professional workflow with no manual deployment steps.
