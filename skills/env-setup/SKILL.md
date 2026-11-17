---
name: env-setup
description: Sets up reproducible local runtime environments, dependencies, and .env configuration safely without overwriting existing secrets or leaking secret values. Use when the user asks for "env setup", setting up .env files, provisioning a virtual environment or container dependencies, onboarding a local environment, or debugging missing environment variables.
---

# Env Setup

Provision a clean, isolated, reproducible local runtime environment and verify all required configuration keys without exposing or clobbering secrets.

## Security Rules (Non-Negotiable)

- **Never print, log, or echo secret values** from `.env`, API key files, or environment variables. Inspect and report **key names only**.
- **Never overwrite an existing `.env`** or populated secret without explicit user approval.
- **Never commit `.env`** or credential files. Always verify `.gitignore` excludes them before creating `.env`.

## Workflow

### Step 1: Discover Environment Requirements

Inspect the project root for environment and dependency declarations:
- Env templates: `.env.example`, `.env.template`, `.env.sample`, `config.py` / `settings` files
- Dependency manifests: `pyproject.toml`, `requirements*.txt`, `uv.lock`, `package.json`, `package-lock.json`, `pnpm-lock.yaml`, `go.mod`, `Cargo.toml`
- Service/container specs: `docker-compose.yml`, `compose.yaml`, `Dockerfile*`
- System dependencies: `Brewfile`, `apt` notes in `README.md`, native libraries (e.g., `tesseract`, `poppler`, `ffmpeg`, `sqlite`)

### Step 2: Verify `.gitignore` Protection

Run the bundled env checker script first in audit mode:

```bash
python3 ~/.gemini/config/skills/env-setup/scripts/check_env.py --root .
```

If `.env` is not ignored by git (`git check-ignore`), add `.env`, `.env.local`, and `.env.*.local` to `.gitignore` **before** creating `.env`.

### Step 3: Provision Isolated Runtime & Dependencies

Choose the repo's native isolation mechanism (do not install blindly into system Python/global node):
- **Python (`uv`)**: `uv sync` (or `uv venv && uv pip install -r requirements.txt`)
- **Python (`venv`/`pip`)**: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`
- **Node**: `pnpm install --frozen-lockfile` / `npm ci` / `npm install` (matching lockfile)
- **Containers**: Check `docker compose config` and verify required ports are free (`ss -tlnp` or `lsof`)

### Step 4: Initialize `.env` Safely

1. If `.env` does **not** exist and `.env.example` (or `.env.template`) exists:
   - Copy `.env.example` to `.env` (preserving placeholders).
   - List which keys require user-supplied values (e.g., `OPENAI_API_KEY`, `DATABASE_URL`) and ask the user to fill sensitive values directly or confirm local defaults.
2. If `.env` **already exists**:
   - Use `check_env.py` output to detect **missing keys** present in `.env.example` but absent from `.env`.
   - Offer to append only missing template keys (commented or placeholder) without touching existing values.

### Step 5: Verify Runtime & Services

1. Re-run the env checker:
   ```bash
   python3 ~/.gemini/config/skills/env-setup/scripts/check_env.py --root .
   ```
2. Verify imports / runtime entrypoints inside the isolated environment (e.g., `.venv/bin/python -c "..."` or `npm run build --dry-run` / health check).
3. If local backing services (Postgres, Redis, Ollama, Qdrant) are configured, check connectivity/health endpoints and report status (`UP` / `DOWN` / `NOT CONFIGURED`).
