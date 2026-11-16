#!/usr/bin/env python3
"""Smoke-test local installation for Claude Code and Codex in a temp project."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    if len(sys.argv) > 2:
        print("usage: python scripts/smoke_install.py [repo-root]", file=sys.stderr)
        return 2
    root = (Path(sys.argv[1]) if len(sys.argv) == 2 else Path.cwd()).resolve()
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    if not skills:
        print(f"{root}: no skills/*/SKILL.md to install", file=sys.stderr)
        return 1
    with tempfile.TemporaryDirectory(prefix="skills-install-") as project:
        env = os.environ.copy()
        env.update(
            DISABLE_TELEMETRY="1",
            DO_NOT_TRACK="1",
        )
        command = ["pnpm", "dlx", "skills@1.8.1", "add", str(root), "--skill", "*", "-a", "claude-code", "codex", "--copy", "-y"]
        try:
            result = subprocess.run(command, cwd=project, env=env, text=True, capture_output=True, timeout=180, check=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            print(f"install command failed: {exc}", file=sys.stderr)
            return 1
        if result.returncode:
            print(result.stdout, file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            print(f"install command exited {result.returncode}", file=sys.stderr)
            return 1
        failures = []
        for entrypoint in skills:
            source = entrypoint.parent
            for agent_path in (".claude/skills", ".agents/skills"):
                installed = Path(project) / agent_path / source.name
                if installed.is_symlink() or not installed.is_dir():
                    failures.append(f"{agent_path}/{source.name}: expected a copied skill directory")
                    continue
                for original in source.rglob("*"):
                    if not original.is_file():
                        continue
                    relative = original.relative_to(source)
                    copy = installed / relative
                    if copy.is_symlink() or not copy.is_file() or copy.read_bytes() != original.read_bytes():
                        failures.append(f"{agent_path}/{source.name}/{relative}: missing or differs from source")
        if failures:
            print("\n".join(failures), file=sys.stderr)
            return 1
    print(f"Installed {len(skills)} skill(s) into both temporary agent directories; copies match.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
