---
name: scaffold-doctor
description: Diagnoses drift, broken Antigravity .agents/ customizations, secret/gitignore hygiene issues, missing environment keys, and broken project entrypoints across a repository scaffold. Use when the user asks to run "scaffold doctor", audit repo health, verify .agents/ skills/configs, check scaffold drift, or troubleshoot project setup issues.
---

# Scaffold Doctor

Run a deterministic, read-only health audit across project scaffolding, `.agents/` customizations, secret hygiene, environment setup, and baseline commands, then propose targeted remediations.

## When to Use

- Verifying repository health after `scaffolding-init`, `workspace-init`, `env-setup`, or `scaffold-update`
- Debugging why Antigravity skills, rules, `skills.json`, or `plugins.json` aren't loading
- Auditing a repo for tracked secrets, missing `.gitignore` rules, stale lockfiles, or scaffold drift
- User asks for `scaffold doctor`, "check scaffold health", or "audit project setup"

## Workflow

### Step 1: Run Automated Scaffold & Customization Audit

Run the bundled diagnostic script (read-only):

```bash
python3 ~/.gemini/config/skills/scaffold-doctor/scripts/doctor_check.py --root .
```

To also audit global Antigravity skills in `~/.gemini/config/skills/`:

```bash
python3 ~/.gemini/config/skills/scaffold-doctor/scripts/doctor_check.py --skills-dir ~/.gemini/config/skills
```

### Step 2: Check Toolchain, Dependencies & Entrypoints

Beyond static file checks, verify runtime health:
1. **Runtime versions**: Compare active `python3`/`node`/`go`/`rust` versions against pinned version files (`.python-version`, `.nvmrc`, `pyproject.toml`, `package.json`).
2. **Lockfile & dependency sync**: Check if dependencies are installed and lockfiles are in sync (e.g., `uv sync --check`, `npm ls --depth=0`, `cargo check`).
3. **Environment readiness**: Run `~/.gemini/config/skills/env-setup/scripts/check_env.py --root .` if `.env.example` exists (never print secret values).
4. **Baseline quality commands**: Verify documented lint, typecheck, and smoke-test commands execute cleanly.

### Step 3: Present Structured Health Report

Group findings into clear statuses:
- **`[PASS]`**: Verified healthy
- **`[WARN]`**: Non-blocking drift or missing optional baseline (include exact fix)
- **`[FAIL]`**: Broken contract, invalid YAML/JSON, tracked secret, or failing baseline check (include exact remediation command)

### Step 4: Remediate Only With Explicit Approval

Never silently overwrite user files or delete tracked data. Present prioritized fixes (`FAIL` first, then `WARN`), apply approved fixes cleanly, and re-run `doctor_check.py` to confirm all failures are resolved.
