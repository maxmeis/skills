#!/usr/bin/env python3
"""Validate this repository's installable skills and local Markdown links."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml


NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
LINK = re.compile(r"!?\[[^\]]*\]\(\s*(<[^>]+>|[^\s)]+)")


def inside(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def load_yaml(path: Path, errors: list[str]) -> object:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        errors.append(f"{path}: invalid YAML: {exc}")
        return None


def validate_frontmatter(path: Path, directory: str, errors: list[str]) -> str | None:
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"{path}: cannot read skill: {exc}")
        return None
    parts = re.split(r"^---\s*$", content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) != 3 or parts[0].strip():
        errors.append(f"{path}: expected YAML frontmatter between opening and closing --- lines")
        return None
    try:
        metadata = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        errors.append(f"{path}: invalid frontmatter YAML: {exc}")
        return None
    if not isinstance(metadata, dict):
        errors.append(f"{path}: frontmatter must be a YAML mapping")
        return None
    name = metadata.get("name")
    description = metadata.get("description")
    if not isinstance(name, str) or not NAME.fullmatch(name) or len(name) > 64:
        errors.append(f"{path}: name must be lowercase hyphenated text, at most 64 characters")
        name = None
    elif name != directory:
        errors.append(f"{path}: name {name!r} must match directory {directory!r}")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{path}: description must be a nonempty string")
    if not parts[2].strip():
        errors.append(f"{path}: skill body is empty")
    return name


def validate_openai_yaml(path: Path, root: Path, errors: list[str]) -> None:
    if not path.exists() and not path.is_symlink():
        return
    if path.is_symlink() and not inside(path.resolve(), root):
        errors.append(f"{path}: symlink escapes repository")
        return
    before = len(errors)
    config = load_yaml(path, errors)
    if len(errors) > before:
        return
    if not isinstance(config, dict):
        errors.append(f"{path}: agents/openai.yaml must be a YAML mapping")
        return
    interface = config.get("interface")
    if interface is not None and not isinstance(interface, dict):
        errors.append(f"{path}: interface must be a YAML mapping")
    elif isinstance(interface, dict):
        for key in ("display_name", "short_description", "default_prompt"):
            if key in interface and (not isinstance(interface[key], str) or not interface[key].strip()):
                errors.append(f"{path}: interface.{key} must be a nonempty string")


def validate_links(path: Path, root: Path, errors: list[str]) -> None:
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"{path}: cannot read Markdown: {exc}")
        return
    for match in LINK.finditer(content):
        href = match.group(1).strip("<>")
        if href.startswith("#"):
            continue
        if href.startswith("/") or "\\" in href or re.match(r"^[A-Za-z]:", href):
            errors.append(f"{path}: nonportable local link {href!r}")
            continue
        parsed = urlsplit(href)
        if parsed.scheme == "file":
            errors.append(f"{path}: nonportable local link {href!r}")
            continue
        if parsed.scheme or parsed.netloc:
            continue
        target_name = unquote(parsed.path)
        if not target_name:
            continue
        target = (path.parent / target_name).resolve()
        if not inside(target, root):
            errors.append(f"{path}: local link escapes allowed root: {href!r}")
        elif not target.exists():
            errors.append(f"{path}: missing local link target: {href!r}")


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    skills = root / "skills"
    if not skills.is_dir():
        return [f"{skills}: missing skills directory"]
    entries = sorted(path for path in skills.iterdir() if path.is_dir() or path.is_symlink())
    if not entries:
        errors.append(f"{skills}: expected at least one skills/*/SKILL.md")
    names: set[str] = set()
    for skill in entries:
        if not inside(skill.resolve(), skills.resolve()):
            errors.append(f"{skill}: skill directory escapes skills/")
            continue
        entrypoint = skill / "SKILL.md"
        if not entrypoint.is_file():
            errors.append(f"{entrypoint}: missing SKILL.md")
            continue
        for item in skill.rglob("*"):
            if not inside(item.resolve(), root):
                errors.append(f"{item}: symlink escapes repository")
        if not inside(entrypoint.resolve(), root):
            errors.append(f"{entrypoint}: symlink escapes repository")
            continue
        name = validate_frontmatter(entrypoint, skill.name, errors)
        if name in names:
            errors.append(f"{entrypoint}: duplicate skill name {name!r}")
        elif name:
            names.add(name)
        validate_openai_yaml(skill / "agents" / "openai.yaml", root, errors)
        for markdown in skill.rglob("*.md"):
            if inside(markdown.resolve(), root):
                validate_links(markdown, skill.resolve(), errors)
    readme = root / "README.md"
    if readme.is_file():
        if inside(readme.resolve(), root):
            validate_links(readme, root, errors)
        else:
            errors.append(f"{readme}: symlink escapes repository")
    return errors


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) == 2 else Path.cwd()
    if len(sys.argv) > 2:
        print("usage: python scripts/validate_skills.py [repo-root]", file=sys.stderr)
        return 2
    errors = validate(root)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Skill validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
