---
name: scaffolding-init
description: Initializes a new or uninitialized project scaffold with standard directory layout, git hygiene, baseline lint/test/CI config, Antigravity .agents/ customizations, and a .scaffold/manifest.json tracking file ownership. Use when the user asks to run "scaffolding init", bootstrap a new repository, standardize a starter project layout, or initialize .agents/ and scaffold tracking in a repo.
---

# Scaffolding Init

Initialize a reproducible project scaffold with clear file ownership so future updates (`scaffold-update`) and diagnostics (`scaffold-doctor`) work cleanly without clobbering project code.

## When to Use

- Starting a brand-new project or service from scratch
- Retrofitting a standard scaffold and `.agents/` structure onto an existing uninitialized directory
- User asks for `scaffolding init`, project bootstrapping, or template initialization

**When NOT to use:** Setting up local developer secrets/venv on an already-scaffolded repo (use `env-setup` or `workspace-init`), or upgrading an existing scaffold (use `scaffold-update`).

## Workflow

### Step 1: Inspect Target & Gather Minimal Decisions

1. Inspect the target directory (`ls -la`, `git status` if a git repo exists). Never silently overwrite existing source files.
2. Determine (or confirm with the user if ambiguous):
   - **Project type / stack** (e.g., Python, Node/TypeScript, Go, Rust, polyglot)
   - **Package/runtime manager** (e.g., `uv`/`pip`, `pnpm`/`npm`, `cargo`, `go`)
   - **Template profile** (`minimal`, `service`, `library`, `fullstack`)
   - **Existing-file policy** (skip existing files vs. merge vs. abort on conflicts)

### Step 2: Initialize Core Repository Hygiene

Create missing foundational files (preserve existing ones unless explicitly approved):

1. **Git repository** (if not initialized): `git init` with a clean default branch (`main`).
2. **`.gitignore`**: Include stack-specific ignores plus secret/local-state exclusions (`.env`, `.env.local`, `.env.*.local`, `*.pem`, `*.key`, build/cache/venv dirs).
3. **`.editorconfig`** & **`.gitattributes`**: Consistent line endings (`lf`), charset (`utf-8`), and indentation defaults.
4. **`README.md`**: Concise project overview, prerequisites, quickstart commands (setup, test, lint, run).

### Step 3: Create Stack Directory Layout & Baseline Tooling

1. Create clean source and test separation matching the stack's idiomatic layout (e.g., `src/` + `tests/`).
2. Create or verify the primary project manifest (`pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml`) with explicit **lint**, **format**, **typecheck**, and **test** commands.
3. Add a `.env.example` documenting required non-secret config keys and placeholders (never real secrets).
4. Add a minimal passing smoke test so the test runner executes cleanly from day one.

### Step 4: Initialize Antigravity Customizations (`.agents/`)

Create project-scoped Antigravity structure under `.agents/`:

1. `.agents/AGENTS.md` (or root `AGENTS.md`): Concise project map covering:
   - Architecture & key directories
   - Exact build, lint, typecheck, and test commands
   - Project boundaries (always do / ask first / never do)
2. `.agents/skills/` (optional empty placeholder or project-specific skills if needed).

### Step 5: Write `.scaffold/manifest.json`

Record every generated scaffold file in `.scaffold/manifest.json` using the schema in [references/manifest-schema.md](./references/manifest-schema.md):
- Assign each file an ownership mode:
  - `managed`: Owned by scaffold template; safe to update on `scaffold-update` if unmodified
  - `merge`: Shared config (e.g., `.gitignore`, `AGENTS.md`, `pyproject.toml`) merged non-destructively
  - `init-only`: Created once on init (e.g., `README.md`, starter source/tests); never overwritten automatically
- Compute and store `sha256` checksums for all tracked files.

### Step 6: Verify Scaffold

Run all checks and confirm `PASS` before finishing:
1. Verify git ignores `.env` (`git check-ignore -v .env` or dry check) and no secrets are staged.
2. Run the project's lint/test baseline command and verify exit code 0.
3. Confirm `.scaffold/manifest.json` is valid JSON and every listed path exists on disk.
