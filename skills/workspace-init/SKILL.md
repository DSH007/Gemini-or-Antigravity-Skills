---
name: workspace-init
description: Prepares an active local developer and agent workspace for an existing or newly cloned repository. Verifies git state and branch/worktree layout, toolchains and runtime managers, editor/IDE settings, git hooks, .agents/ customizations, and baseline smoke checks. Use when the user asks to run "workspace init", set up a cloned repo for work, prepare a monorepo/worktree workspace, or verify local developer tooling readiness.
---

# Workspace Init

Prepare a checked-out repository so both the developer and Antigravity agents can build, edit, lint, and test reliably in the local workspace.

## When to Use

- After cloning a repository or running `scaffolding-init`
- Setting up an isolated git worktree or parallel feature workspace
- Onboarding onto an existing repo where IDE/CLI/toolchain readiness is unverified
- User asks for `workspace init` or "prepare my workspace"

**When NOT to use:** Creating a brand-new repo layout from zero (use `scaffolding-init`), or provisioning `.env` secrets and virtualenvs/containers specifically (pair with `env-setup`).

## Workflow

### Step 1: Audit Repository & Git State

1. Check git status, remote tracking, and worktree layout:
   - `git status -sb`
   - `git worktree list`
2. If working on a new task in a shared/active repo, confirm branch state (create a feature branch or worktree rather than committing straight to `main`/`master` unless instructed).
3. Detect workspace topology: single-package repo, monorepo (`workspaces`, `pnpm-workspace.yaml`, `uv.workspace`, `Cargo.toml` workspace), or multi-root workspace.

### Step 2: Verify Runtime & Toolchain Prerequisites

1. Check pinned version files if present:
   - `.python-version`, `.nvmrc`, `.node-version`, `.tool-versions`, `rust-toolchain.toml`, `go.mod`, `package.json` (`engines`)
2. Verify installed binaries and versions match constraints (`python3 --version`, `node --version`, `uv --version`, `docker --version`, etc.).
3. Report exact mismatches clearly rather than silently running with an incompatible global binary.

### Step 3: Validate `.agents/` & Editor Integration

1. Inspect workspace customizations (`.agents/`, `AGENTS.md`, `GEMINI.md`, `.agents/skills.json`, `.agents/plugins.json`).
2. Verify any referenced paths in `.agents/skills.json` or `.agents/plugins.json` resolve cleanly.
3. Check editor/formatter integration (`.editorconfig`, `.vscode/settings.json` / `.vscode/extensions.json` if used) without overwriting personal user preferences.

### Step 4: Activate Developer Hooks & Task Runners

1. If `.pre-commit-config.yaml` exists and `pre-commit` is installed, verify/install hooks (`pre-commit install`).
2. If `.husky/` or `lefthook.yml` exists, verify hooks are wired up (`npx husky` / `lefthook install`).
3. Identify canonical entrypoints (`Makefile`, `justfile`, `package.json` scripts, `run.sh`, `pyproject.toml` scripts) and record them in your summary.

### Step 5: Chain Environment Setup (If Needed)

If `.env` is missing while `.env.example` exists, or dependencies/venv are not installed yet, invoke or follow the `env-setup` workflow before running verification checks.

### Step 6: Run Workspace Smoke Check

Execute the repository's fastest non-destructive verification checks:
1. Dependency/lockfile integrity check (e.g., `uv sync --check`, `npm ci --dry-run` or `npm ls`, `cargo check`).
2. Fast lint or syntax check.
3. Minimal unit test / smoke test command.

Report a concise readiness checklist (`git`, `toolchain`, `hooks`, `.agents/`, `env`, `smoke-test`) with exact commands and observed pass/fail status.
