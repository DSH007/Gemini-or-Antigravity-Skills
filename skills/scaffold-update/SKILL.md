---
name: scaffold-update
description: Safely upgrades and synchronizes an existing project scaffold, tooling configs, and .agents/ customizations against newer template conventions without clobbering user modifications. Use when the user asks to run "scaffold update", sync project boilerplate, upgrade .agents/ or lint/CI templates, or reconcile scaffold drift.
---

# Scaffold Update

Upgrade an existing project's scaffolded files and `.agents/` customizations safely using ownership-aware diffs and dry-run previews.

## When to Use

- Upgrading a project created with `scaffolding-init` to newer template conventions
- Syncing updated `.agents/` rules, CI workflows, `.editorconfig`, or `.gitignore` rules across repositories
- User asks for `scaffold update`, "sync scaffold", or "update boilerplate"

**When NOT to use:** Fresh bootstrapping (use `scaffolding-init`), or read-only diagnostics (use `scaffold-doctor`).

## Safety Guarantees

- **Dry-run first**: Always present a file-by-file change plan before modifying modified or user-owned files.
- **Respect ownership modes** (see `~/.gemini/config/skills/scaffolding-init/references/manifest-schema.md`):
  - `managed` + unchanged SHA-256 -> safe to update automatically
  - `managed` + locally modified SHA-256 -> **must** show diff / three-way merge and ask before overwriting
  - `merge` -> patch only missing sections/keys or template-fenced blocks; preserve all user customizations
  - `init-only` -> **never overwrite** unless the user explicitly names the file and requests replacement
- **Never touch secrets or data**: Never modify `.env`, credentials, or application data directories.

## Workflow

### Step 1: Load Baseline & Detect Current State

1. Check for `.scaffold/manifest.json`:
   - If present: parse `template_id`, `template_version`, and each tracked file's `ownership` and recorded `sha256`. Compute current `sha256` on disk to detect local modifications.
   - If absent (legacy repo): inspect existing files (`.gitignore`, `.editorconfig`, `.agents/`, CI workflows, lint configs) and treat all existing files as `merge` or `init-only` until the user opts into a manifest.
2. Identify the update target (new template version, updated `.agents/` standard, or specific config updates requested by the user).

### Step 2: Build Dry-Run Update Plan

Classify every candidate file into one of four buckets and show the summary table to the user:

| Action | Meaning |
|---|---|
| `CREATE` | New scaffold file missing from repo |
| `UPDATE` | `managed` file matching recorded SHA-256 (clean upgrade) |
| `MERGE` | `merge` file or locally modified `managed` file requiring selective merge |
| `SKIP` | `init-only` file or already up-to-date |

If any `MERGE` or conflict exists, show the exact proposed diff or section changes before applying.

### Step 3: Apply Non-Destructive Updates

1. Apply `CREATE` and clean `UPDATE` files.
2. Perform `MERGE` updates carefully:
   - For `.gitignore`: append missing rules under a clearly commented section header without removing user entries.
   - For `.agents/AGENTS.md` / `GEMINI.md`: preserve project-specific sections and update only shared template blocks or missing required sections.
   - For structured configs (`pyproject.toml`, `package.json`): update/add targeted tool keys while preserving project dependencies and custom scripts.
3. Never delete user files unless explicitly approved.

### Step 4: Update `.scaffold/manifest.json`

Update `template_version`, `updated_at`, and recompute `sha256` digests for all tracked files (or initialize `.scaffold/manifest.json` if retrofitting).

### Step 5: Verify Post-Update Health

1. Run `scaffold-doctor` checks (e.g., `python3 ~/.gemini/config/skills/scaffold-doctor/scripts/doctor_check.py --root .`).
2. Run the project's lint, typecheck, and test suite to confirm zero regressions.
3. Report files created/updated/merged/skipped and verification command results.
