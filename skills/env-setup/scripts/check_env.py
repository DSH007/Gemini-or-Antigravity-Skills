#!/usr/bin/env python3
"""Safe .env audit script: compares env template keys against .env without ever printing values."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ENV_KEY_RE = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$")
TEMPLATE_CANDIDATES = (".env.example", ".env.template", ".env.sample")


def parse_env_keys(path: Path) -> dict[str, bool]:
    """Return mapping of KEY -> has_non_empty_value without retaining values."""
    keys: dict[str, bool] = {}
    if not path.is_file():
        return keys
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = ENV_KEY_RE.match(raw_line)
        if not match:
            continue
        key, raw_val = match.group(1), match.group(2).strip()
        # Strip surrounding quotes when checking emptiness only.
        if len(raw_val) >= 2 and raw_val[0] == raw_val[-1] and raw_val[0] in ("'", '"'):
            raw_val = raw_val[1:-1].strip()
        # Treat inline comment-only values as empty.
        if raw_val.startswith("#"):
            raw_val = ""
        keys[key] = bool(raw_val)
    return keys


def is_git_ignored(root: Path, rel_path: str) -> bool | None:
    """Return True if git ignores rel_path, False if not ignored, None if not a git repo."""
    if not (root / ".git").exists():
        return None
    proc = subprocess.run(
        ["git", "-C", str(root), "check-ignore", "-q", rel_path],
        capture_output=True,
        check=False,
    )
    return proc.returncode == 0


def is_git_tracked(root: Path, rel_path: str) -> bool:
    """Return True if rel_path is tracked by git."""
    if not (root / ".git").exists():
        return False
    proc = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--error-unmatch", rel_path],
        capture_output=True,
        check=False,
    )
    return proc.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit .env completeness and gitignore hygiene safely.")
    parser.add_argument("--root", default=".", help="Project root directory (default: .)")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    env_file = root / ".env"
    template_file = next((root / name for name in TEMPLATE_CANDIDATES if (root / name).is_file()), None)

    print(f"Environment Audit: {root}")
    has_failure = False

    ignored = is_git_ignored(root, ".env")
    tracked = is_git_tracked(root, ".env")
    if tracked:
        print("[FAIL] .env is tracked in git! Untrack immediately (`git rm --cached .env`).")
        has_failure = True
    elif ignored is True:
        print("[PASS] .env is ignored by .gitignore")
    elif ignored is False:
        print("[WARN] .env is NOT ignored by .gitignore")
    else:
        print("[INFO] Not a git repository; skipped .gitignore check")

    if template_file is None:
        print("[INFO] No .env.example / .env.template / .env.sample found")
        return 1 if has_failure else 0

    template_keys = parse_env_keys(template_file)
    print(f"[INFO] Template: {template_file.name} ({len(template_keys)} keys)")

    if not env_file.is_file():
        print("[WARN] .env file does not exist yet")
        return 1 if has_failure else 0

    env_keys = parse_env_keys(env_file)
    missing = [k for k in template_keys if k not in env_keys]
    empty = [k for k in template_keys if k in env_keys and not env_keys[k]]
    extra = [k for k in env_keys if k not in template_keys]

    if missing:
        print(f"[FAIL] Missing keys in .env ({len(missing)}): {', '.join(missing)}")
        has_failure = True
    else:
        print("[PASS] All template keys are present in .env")

    if empty:
        print(f"[WARN] Empty values in .env ({len(empty)}): {', '.join(empty)}")
    if extra:
        print(f"[INFO] Extra keys in .env not in {template_file.name} ({len(extra)}): {', '.join(extra)}")

    return 1 if has_failure else 0


if __name__ == "__main__":
    sys.exit(main())
