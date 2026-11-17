# Gemini-or-Antigravity-Skills

Reusable Antigravity / Gemini skills for project scaffolding, workspace & environment setup, diagnostics, metric-driven improvement planning, and devil's-advocate to-the-spec implementation.

## Included Skills (`skills/`)

| Skill | Purpose |
|---|---|
| `scaffolding-init` | Initialize repository layout, `.agents/` customizations, quality baselines, and `.scaffold/manifest.json` |
| `workspace-init` | Prepare local developer/agent workspace (git state, toolchains, hooks, `.agents/`, smoke checks) |
| `env-setup` | Provision isolated runtime/venv and `.env` safely without overwriting or exposing secrets |
| `scaffold-update` | Safely upgrade managed scaffold files and `.agents/` templates using ownership-aware merges |
| `scaffold-doctor` | Diagnose scaffold drift, `.agents/` validity, `.gitignore`/secret hygiene, and broken entrypoints |
| `improvement-plan-with-metrics` | Create improvement plans grounded in reproducible baselines, target metrics, and non-regression guardrails |
| `devils-advocate-spec-implementation` | Implement plans strictly to spec with Devil's Advocate decision gates and traceability audits |

## Installing Globally

Copy `skills/*` into `~/.gemini/config/skills/` so Antigravity CLI (`agy`) and Antigravity IDE discover them across all workspaces:

```bash
mkdir -p ~/.gemini/config/skills
cp -a skills/* ~/.gemini/config/skills/
```

Verify all skills:

```bash
python3 skills/scaffold-doctor/scripts/doctor_check.py --skills-dir skills
```
