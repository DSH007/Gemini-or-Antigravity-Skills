# Scaffold Manifest Schema (`.scaffold/manifest.json`)

Shared contract used by `scaffolding-init`, `scaffold-update`, and `scaffold-doctor`.

## Schema

```json
{
  "schema_version": 1,
  "template_id": "python-service",
  "template_version": "1.0.0",
  "stack": {
    "language": "python",
    "package_manager": "uv"
  },
  "created_at": "2026-01-01T00:00:00Z",
  "updated_at": "2026-01-01T00:00:00Z",
  "files": [
    {
      "path": ".editorconfig",
      "ownership": "managed",
      "sha256": "<hex-digest>"
    },
    {
      "path": ".gitignore",
      "ownership": "merge",
      "sha256": "<hex-digest>"
    },
    {
      "path": ".agents/AGENTS.md",
      "ownership": "merge",
      "sha256": "<hex-digest>"
    },
    {
      "path": "README.md",
      "ownership": "init-only",
      "sha256": "<hex-digest>"
    }
  ]
}
```

## Ownership Modes

- **`managed`**: Template-controlled files (e.g., `.editorconfig`, CI workflow boilerplate, lint configs). `scaffold-update` may update them automatically if the current file's SHA-256 matches the manifest (no local edits), or prompt/3-way-merge if locally modified.
- **`merge`**: Shared configuration files (e.g., `.gitignore`, `.agents/AGENTS.md`, `pyproject.toml`, `package.json`). Never blindly overwritten; updates append or patch only template-marked sections or missing keys.
- **`init-only`**: Project-owned files created once during `scaffolding-init` (e.g., `README.md`, `.env.example`, starter `src/` and `tests/`). `scaffold-update` never overwrites them unless explicitly requested by the user.

## Generating SHA-256 Checksums

```bash
sha256sum <file> | awk '{print $1}'
```
