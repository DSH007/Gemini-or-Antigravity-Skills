#!/usr/bin/env python3
"""Read-only health audit for project scaffolds, .agents/ customizations, and skill directories."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

SENSITIVE_PATTERNS = (
    ".env",
    ".env.local",
    "*.pem",
    "*.key",
    "id_rsa",
    "id_ed25519",
)
LINK_RE = re.compile(r"\[[^\]]+\]\(\./([^)#]+)\)")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_frontmatter(skill_md: Path) -> dict[str, str] | None:
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return None

    data: dict[str, str] = {}
    current_key: str | None = None
    for line in lines[1:end_idx]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith((" ", "\t")) and ":" in line:
            k, v = line.split(":", 1)
            current_key = k.strip()
            val = v.strip()
            data[current_key] = "" if val in (">-", "|", ">", "|-") else val.strip("\"'")
        elif current_key and line.startswith((" ", "\t")):
            sep = " " if data[current_key] else ""
            data[current_key] += sep + line.strip()
    return data


def audit_skills_dir(skills_dir: Path) -> tuple[int, int]:
    """Audit all skill subdirectories under skills_dir. Returns (warnings, failures)."""
    warns = 0
    fails = 0
    if not skills_dir.is_dir():
        print(f"[INFO] Skills directory not present: {skills_dir}")
        return warns, fails

    skill_dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir() and not p.name.startswith("."))
    if not skill_dirs:
        print(f"[WARN] No skill subdirectories found in {skills_dir}")
        return warns + 1, fails

    for sdir in skill_dirs:
        skill_md = sdir / "SKILL.md"
        if not skill_md.is_file():
            print(f"[FAIL] {sdir.name}: missing SKILL.md")
            fails += 1
            continue
        fm = parse_frontmatter(skill_md)
        if fm is None:
            print(f"[FAIL] {sdir.name}: missing or unclosed YAML frontmatter in SKILL.md")
            fails += 1
            continue
        name = fm.get("name", "")
        desc = fm.get("description", "")
        if not name:
            print(f"[FAIL] {sdir.name}: frontmatter missing 'name'")
            fails += 1
        elif name != sdir.name:
            print(f"[WARN] {sdir.name}: frontmatter name '{name}' differs from directory '{sdir.name}'")
            warns += 1
        if not desc or len(desc) < 15:
            print(f"[FAIL] {sdir.name}: frontmatter missing meaningful 'description'")
            fails += 1
            continue

        # Verify relative ./ links in SKILL.md exist
        body = skill_md.read_text(encoding="utf-8", errors="replace")
        broken_links = [m.group(1) for m in LINK_RE.finditer(body) if not (sdir / m.group(1)).exists()]
        if broken_links:
            print(f"[FAIL] {sdir.name}: broken relative link(s): {', '.join(broken_links)}")
            fails += 1
        else:
            print(f"[PASS] skill '{sdir.name}' valid")
    return warns, fails


def audit_manifest(root: Path) -> tuple[int, int]:
    warns = 0
    fails = 0
    manifest_path = root / ".scaffold" / "manifest.json"
    if not manifest_path.is_file():
        print("[INFO] No .scaffold/manifest.json found (legacy/unscaffolded repo)")
        return warns, fails

    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"[FAIL] .scaffold/manifest.json is invalid JSON: {exc}")
        return warns, fails + 1

    files = data.get("files", [])
    if not isinstance(files, list):
        print("[FAIL] .scaffold/manifest.json 'files' must be a list")
        return warns, fails + 1

    print(f"[PASS] .scaffold/manifest.json loaded (template={data.get('template_id', '?')} v{data.get('template_version', '?')})")
    for entry in files:
        rel = entry.get("path")
        ownership = entry.get("ownership", "init-only")
        expected_sha = entry.get("sha256")
        if not rel:
            continue
        target = root / rel
        if not target.exists():
            print(f"[FAIL] Manifest entry missing on disk: {rel}")
            fails += 1
            continue
        if target.is_file() and expected_sha:
            actual_sha = sha256_file(target)
            if actual_sha != expected_sha:
                level = "WARN" if ownership in ("managed", "merge") else "INFO"
                print(f"[{level}] Drift detected ({ownership}): {rel}")
                if level == "WARN":
                    warns += 1
    return warns, fails


def audit_agents_dir(root: Path) -> tuple[int, int]:
    warns = 0
    fails = 0
    agents_dir = next((root / d for d in (".agents", ".agent", "_agents", "_agent") if (root / d).is_dir()), None)
    has_root_rules = any((root / f).is_file() for f in ("AGENTS.md", "GEMINI.md"))

    if agents_dir is None and not has_root_rules:
        print("[WARN] No .agents/ directory, AGENTS.md, or GEMINI.md found")
        return warns + 1, fails

    if agents_dir is not None:
        print(f"[PASS] Found workspace customization root: {agents_dir.name}/")
        for cfg_name in ("skills.json", "plugins.json"):
            cfg_path = agents_dir / cfg_name
            if cfg_path.is_file():
                try:
                    json.loads(cfg_path.read_text(encoding="utf-8"))
                    print(f"[PASS] {agents_dir.name}/{cfg_name} is valid JSON")
                except json.JSONDecodeError as exc:
                    print(f"[FAIL] {agents_dir.name}/{cfg_name} invalid JSON: {exc}")
                    fails += 1
        w, f = audit_skills_dir(agents_dir / "skills")
        warns += w
        fails += f
    return warns, fails


def audit_git_hygiene(root: Path) -> tuple[int, int]:
    warns = 0
    fails = 0
    if not (root / ".git").exists():
        print("[WARN] Not a git repository")
        return warns + 1, fails

    tracked = subprocess.run(
        ["git", "-C", str(root), "ls-files"],
        capture_output=True,
        text=True,
        check=False,
    )
    if tracked.returncode == 0:
        tracked_files = set(tracked.stdout.splitlines())
        risky = [
            f
            for f in tracked_files
            if Path(f).name in (".env", ".env.local", "id_rsa", "id_ed25519")
            or f.endswith((".pem", ".key"))
        ]
        if risky:
            print(f"[FAIL] Potentially sensitive file(s) tracked in git: {', '.join(sorted(risky))}")
            fails += 1
        else:
            print("[PASS] No obvious secret files tracked in git")

    ignore_check = subprocess.run(
        ["git", "-C", str(root), "check-ignore", "-q", ".env"],
        capture_output=True,
        check=False,
    )
    if ignore_check.returncode == 0:
        print("[PASS] .env is covered by .gitignore")
    else:
        print("[WARN] .env is not ignored by .gitignore")
        warns += 1
    return warns, fails


def main() -> int:
    parser = argparse.ArgumentParser(description="Run scaffold-doctor static health checks.")
    parser.add_argument("--root", help="Project root directory to audit")
    parser.add_argument("--skills-dir", help="Specific skills directory to audit (e.g. ~/.gemini/config/skills)")
    args = parser.parse_args()

    if not args.root and not args.skills_dir:
        args.root = "."

    total_warns = 0
    total_fails = 0

    if args.root:
        root = Path(args.root).resolve()
        print(f"=== Scaffold Doctor Report: {root} ===")
        for fn in (audit_manifest, audit_agents_dir, audit_git_hygiene):
            w, f = fn(root)
            total_warns += w
            total_fails += f

    if args.skills_dir:
        sdir = Path(args.skills_dir).expanduser().resolve()
        print(f"=== Skills Audit: {sdir} ===")
        w, f = audit_skills_dir(sdir)
        total_warns += w
        total_fails += f

    print(f"Summary: {total_fails} failure(s), {total_warns} warning(s)")
    return 1 if total_fails > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
