#!/usr/bin/env python3
"""
Regenerate the ## Directory Structure and ## Reference Relationships
sections of README.md from frontmatter and cross-references of all
reference .md files.

Usage:
    python regenerate_index.py

Requires PyYAML (pip install pyyaml).
"""

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent
README_PATH = REPO_ROOT / "README.md"

EXCLUDED_FILES = {README_PATH.name, "reference-template.md"}
EXCLUDED_DIRECTORIES = {"scripts", "venv", ".venv", "ToDo"}

SECTION_DESCRIPTIONS = {
    "agents": (
        "Agent-level configuration, subagents, and cross-platform porting."
    ),
    "skills": (
        "Skill (SKILL.md) authoring, best practices, and platform-specific features."
    ),
    "ai-tooling": (
        "Tooling for AI agent execution: deterministic scripts and MCP "
        "server best practices."
    ),
    "harnesses": (
        "Platform-specific best practices, workspace configuration, and "
        "official documentation indexes."
    ),
    "documentation": (
        "Repository documentation standards and reference-file templates."
    ),
    "security": (
        "Security testing and vulnerability assessment references."
    ),
    "design": (
        "Design and architecture guidance for AI systems."
    ),
    "misc": (
        "Cross-cutting topics not covered by the other sections."
    ),
    "webdev": (
        "Building web applications with AI coding agents and open-source tooling."
    ),
}

SECTION_ORDER = ["agents", "skills", "ai-tooling", "harnesses", "documentation", "security", "design", "webdev", "misc"]


# ── frontmatter parsing ──────────────────────────────────────────────

def _parse_yaml_simple(text: str) -> dict | None:
    result = {}
    for line in text.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        elif value.startswith("[") and value.endswith("]"):
            items = value[1:-1].split(",")
            value = [it.strip().strip("\"'") for it in items if it.strip()]
        elif value == "" or value.startswith("<"):
            value = None if value.startswith("<") else ""
        result[key] = value
    return result if result else None


def parse_frontmatter(filepath: Path) -> dict | None:
    content = filepath.read_text(encoding="utf-8-sig")
    match = re.match(r"^---\s*\n(.*?)\n(?:---|\.\.\.)", content, re.DOTALL)
    if not match:
        return None
    raw = match.group(1)
    try:
        return yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        return _parse_yaml_simple(raw)


# ── cross-reference parsing ──────────────────────────────────────────

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+\.md)\)")


def parse_related_links(filepath: Path) -> list[tuple[str, str]]:
    """Extract (link_text, resolved_relative_path) from ## Related Documents."""
    content = filepath.read_text(encoding="utf-8-sig")
    match = re.search(r"^## Related Documents\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL | re.MULTILINE)
    if not match:
        return []
    section = match.group(1)
    links = []
    for text, path in LINK_RE.findall(section):
        resolved = (filepath.parent / path).resolve()
        try:
            rel = resolved.relative_to(REPO_ROOT)
            links.append((text, str(rel).replace("\\", "/")))
        except ValueError:
            continue
    return links


# ── file collection ──────────────────────────────────────────────────

def collect_files() -> dict[str, list[tuple[str, dict]]]:
    groups: dict[str, list[tuple[str, dict]]] = {}
    for md_file in sorted(REPO_ROOT.rglob("*.md")):
        rel = md_file.relative_to(REPO_ROOT)
        parts = rel.parts
        if len(parts) < 2:
            continue
        directory = parts[0]
        filename = parts[-1]
        if filename in EXCLUDED_FILES:
            continue
        if directory.startswith(".") or directory in EXCLUDED_DIRECTORIES:
            continue
        if not (REPO_ROOT / directory).is_dir():
            continue
        fm = parse_frontmatter(md_file)
        if fm is None:
            print(f"  [warn] No frontmatter: {rel}", file=sys.stderr)
            fm = {}
        groups.setdefault(directory, []).append((filename, fm))
    return groups


def collect_all_entries() -> dict[str, dict]:
    entries: dict[str, dict] = {}
    for md_file in REPO_ROOT.rglob("*.md"):
        rel = md_file.relative_to(REPO_ROOT)
        parts = rel.parts
        if len(parts) < 2:
            continue
        filename = parts[-1]
        if filename in EXCLUDED_FILES:
            continue
        directory = parts[0]
        if directory.startswith(".") or directory in EXCLUDED_DIRECTORIES:
            continue
        if not (REPO_ROOT / directory).is_dir():
            continue
        fm = parse_frontmatter(md_file)
        if fm is not None:
            entries[str(rel).replace("\\", "/")] = fm
    return entries


# ── table generation ─────────────────────────────────────────────────

def truncate(text: str, max_len: int = 250) -> str:
    if not text:
        return ""
    text = str(text).strip()
    if len(text) <= max_len:
        return text
    cut = text[: max_len - 3].rstrip()
    boundary = cut.rfind(" ")
    if boundary != -1:
        cut = cut[:boundary].rstrip()
    return cut + "..."


def layer_badge(layer: str) -> str:
    return {"hot": "🔥", "warm": "☀️", "cold": "❄️"}.get(layer, layer)


def generate_table(directory: str, files: list[tuple[str, dict]]) -> str:
    if not files:
        return "_(no files)_\n"
    header = "| File | Layer | Title | Description |"
    sep = "|------|-------|-------|-------------|"
    rows = []
    for filename, fm in files:
        title = (fm.get("title") or "").replace("|", "\\|")
        desc = truncate(fm.get("description") or "").replace("|", "\\|")
        layer = (fm.get("layer") or "warm").strip().lower()
        link = f"[{filename}]({directory}/{filename})"
        rows.append(f"| {link} | {layer_badge(layer)} | {title} | {desc} |")
    return "\n".join([header, sep] + rows) + "\n"


def build_directory_section(groups: dict[str, list[tuple[str, dict]]]) -> str:
    lines = [
        "## Directory Structure\n",
        "Layer column shows loading intent: 🔥 always in context, ☀️ "
        "task-loaded, ❄️ fetched via links. Sizes are guidance, not limits. "
        "See `AGENTS.md` for the loading protocol.\n",
    ]
    for section_name in SECTION_ORDER:
        files = groups.get(section_name, [])
        files.sort(key=lambda x: x[0].lower())
        desc = SECTION_DESCRIPTIONS.get(section_name, "")
        lines.append(f"### {section_name}/\n")
        if desc:
            lines.append(f"{desc}\n")
        lines.append(generate_table(section_name, files))
    return "\n".join(lines)


# ── relationship tree ────────────────────────────────────────────────

def build_relationships(entries: dict[str, dict]) -> list[tuple[str, str, str]]:
    edges: list[tuple[str, str, str]] = []
    for rel_path in entries:
        md_file = REPO_ROOT / rel_path
        if not md_file.exists():
            continue
        for text, target_rel in parse_related_links(md_file):
            if target_rel in entries:
                edges.append((rel_path, target_rel, text))
    return edges


def tree_item(title: str, layer: str, link: str = "") -> str:
    badge = layer_badge(layer)
    if link:
        return f"[{title}]({link}) ({badge})"
    return f"{title} ({badge})"


def generate_relationship_tree(
    entries: dict[str, dict],
    edges: list[tuple[str, str, str]],
    groups: dict[str, list[tuple[str, dict]]],
) -> str:
    """Build overview→companion children map from related-document links.

    Any file may nest under a warm overview regardless of its own layer.
    Warm↔warm companion links (which are mutual) are disambiguated by
    outgoing-link count, then by filename prefix (an overview name is a
    prefix of its companions' names). Cold→warm links are back-references,
    not branches.
    """
    def layer_of(rel: str) -> str:
        return (entries[rel].get("layer") or "warm").strip().lower()

    out_degree: dict[str, int] = {}
    for src, tgt, _ in edges:
        if layer_of(src) == "warm":
            out_degree[src] = out_degree.get(src, 0) + 1

    children: dict[str, list[str]] = {}
    nested: set[str] = set()

    for src, tgt, _ in edges:
        if layer_of(src) != "warm":
            continue  # only warm overviews branch
        tgt_layer = layer_of(tgt)
        nest = False
        if tgt_layer == "cold":
            nest = True
        elif tgt_layer in ("warm", "hot"):
            src_stem = Path(src).stem
            tgt_stem = Path(tgt).stem
            if out_degree.get(src, 0) > out_degree.get(tgt, 0):
                nest = True
            elif (
                out_degree.get(src, 0) == out_degree.get(tgt, 0)
                and tgt_stem != src_stem
                and tgt_stem.startswith(src_stem)
            ):
                nest = True
        if nest:
            children.setdefault(src, set()).add(tgt)
            nested.add(tgt)

    def render_entries(rels: list[str], indent: str) -> list[str]:
        lines: list[str] = []
        for i, rel in enumerate(sorted(rels)):
            is_last = (i == len(rels) - 1)
            branch = "└── " if is_last else "├── "
            title = (entries[rel].get("title") or Path(rel).stem).strip()
            display = tree_item(title, layer_of(rel), rel)
            lines.append(f"{indent}{branch}{display}\n")
            kids = sorted(children.get(rel, []))
            if kids:
                kid_indent = indent + ("    " if is_last else "│   ")
                lines.extend(render_entries(kids, kid_indent))
        return lines

    lines = ["## Reference Relationships\n"]
    lines.append(
        "Warm overviews branch into their companions — deep references and "
        "related guides — regardless of layer. Files that no overview "
        "references appear standalone.\n"
    )

    for section_name in SECTION_ORDER:
        section_files = groups.get(section_name, [])
        section_files.sort(key=lambda x: x[0].lower())

        top_level = [
            f"{section_name}/{filename}" for filename, _ in section_files
            if f"{section_name}/{filename}" not in nested
        ]
        if not top_level:
            continue

        lines.append(f"### {section_name}/\n")
        lines.append("```\n")
        lines.extend(render_entries(top_level, ""))
        lines.append("```\n")

    return "".join(lines)


# ── file update ──────────────────────────────────────────────────────

MARKER = "## Directory Structure"

def update_readme(full_section: str) -> bool:
    old_text = README_PATH.read_text(encoding="utf-8-sig")
    idx = old_text.find(f"\n{MARKER}")
    if idx == -1:
        idx = old_text.find(MARKER)
        if idx == -1:
            print("Error: Could not find '## Directory Structure' in README.md", file=sys.stderr)
            return False
    new_text = old_text[:idx] + "\n" + full_section.rstrip("\n") + "\n"
    if new_text == old_text:
        return False
    README_PATH.write_text(new_text, encoding="utf-8", newline="\n")
    return True


# ── main ─────────────────────────────────────────────────────────────

def main():
    print("Scanning reference files...")
    groups = collect_files()
    entries = collect_all_entries()
    for directory, files in groups.items():
        print(f"  {directory}/: {len(files)} files")

    print("\nParsing cross-references...")
    edges = build_relationships(entries)
    print(f"  {len(edges)} total cross-references")

    print("\nBuilding directory index...")
    section = build_directory_section(groups)

    print("Building relationship tree...")
    tree = generate_relationship_tree(entries, edges, groups)
    section += "\n" + tree

    print("Updating README.md...")
    if update_readme(section):
        print("  README.md updated.")
    else:
        print("  No changes needed.")

    print("Done.")


if __name__ == "__main__":
    main()
