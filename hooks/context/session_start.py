#!/usr/bin/env python3
"""SessionStart hook: initialize brain, check dependencies, inject context."""
import os
import json
import glob
import shutil
import subprocess
from datetime import date

BRAIN_TEMPLATE = """# Wavelength Brain

Last updated: {date}

## Companies (0)
| Company | Industry | Verdict | Score | Date |
|---------|----------|---------|-------|------|

## Industries (0)
_No industries researched yet._

## Key Learnings
_No learnings captured yet. Use `/deal-analysis` or `/red-team` to analyze a deal, then compile findings into the brain._

## Recent Activity
- {date}: Brain initialized
"""


def resolve_brain_dir():
    data_dir = os.environ.get(
        "CLAUDE_PLUGIN_DATA", os.path.expanduser("~/.wavelength")
    )
    return os.path.join(data_dir, "brain")


def init_brain(brain_dir):
    """Create brain directory structure and seed BRAIN.md if first run."""
    for subdir in ["companies", "industries", "people", "learnings"]:
        os.makedirs(os.path.join(brain_dir, subdir), exist_ok=True)

    brain_md = os.path.join(brain_dir, "BRAIN.md")
    if not os.path.exists(brain_md):
        with open(brain_md, "w") as f:
            f.write(BRAIN_TEMPLATE.format(date=date.today().isoformat()))


def count_articles(brain_dir):
    """Count wiki articles by category."""
    counts = {}
    for subdir in ["companies", "industries", "people", "learnings"]:
        path = os.path.join(brain_dir, subdir)
        files = glob.glob(os.path.join(path, "*.md"))
        counts[subdir] = len(files)
    return counts


def read_brain_index(brain_dir):
    """Read BRAIN.md content for injection."""
    brain_md = os.path.join(brain_dir, "BRAIN.md")
    if os.path.exists(brain_md):
        with open(brain_md, "r") as f:
            content = f.read()
        # Truncate if too long to avoid context bloat
        if len(content) > 4000:
            content = content[:4000] + "\n\n... (index truncated, read full BRAIN.md for complete index)"
        return content
    return None


def check_dependencies():
    """Check required dependencies and return list of missing items with install commands."""
    missing = []

    # Check Python 3.9+
    python_path = shutil.which("python3")
    if not python_path:
        missing.append({
            "name": "Python 3.9+",
            "status": "NOT FOUND",
            "install": "brew install python3 (macOS) or https://python.org/downloads/",
            "required_by": "Grata scoring, company processing",
        })
    else:
        try:
            result = subprocess.run(
                ["python3", "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"],
                capture_output=True, text=True, timeout=5,
            )
            version = result.stdout.strip()
            major, minor = version.split(".")
            if int(major) < 3 or (int(major) == 3 and int(minor) < 9):
                missing.append({
                    "name": f"Python 3.9+ (found {version})",
                    "status": "VERSION TOO OLD",
                    "install": "brew upgrade python3 (macOS) or https://python.org/downloads/",
                    "required_by": "Grata scoring, company processing",
                })
        except Exception:
            pass

    # Check openpyxl
    try:
        result = subprocess.run(
            ["python3", "-c", "import openpyxl; print(openpyxl.__version__)"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode != 0:
            missing.append({
                "name": "openpyxl (Python package)",
                "status": "NOT INSTALLED",
                "install": "pip3 install openpyxl",
                "required_by": "Grata scoring (xlsx file processing)",
            })
    except Exception:
        missing.append({
            "name": "openpyxl (Python package)",
            "status": "CHECK FAILED",
            "install": "pip3 install openpyxl",
            "required_by": "Grata scoring (xlsx file processing)",
        })

    return missing


def main():
    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
    brain_dir = resolve_brain_dir()

    # Initialize on first run
    init_brain(brain_dir)

    # Check dependencies
    missing_deps = check_dependencies()

    # Count articles
    counts = count_articles(brain_dir)

    # Read the wiki index
    brain_index = read_brain_index(brain_dir)

    # Build context injection
    lines = [
        "WAVELENGTH BRAIN",
        f"Plugin root: {plugin_root}",
        f"Brain directory: {brain_dir}",
        f"Wiki: {counts['companies']} companies, {counts['industries']} industries, {counts['people']} people, {counts['learnings']} learnings",
        "",
    ]

    # Dependency warnings — Claude should offer to install these
    if missing_deps:
        lines.append("--- MISSING DEPENDENCIES ---")
        lines.append("The following dependencies are missing. Offer to install them for the user.")
        for dep in missing_deps:
            lines.append(f"  - {dep['name']}: {dep['status']}")
            lines.append(f"    Install: {dep['install']}")
            lines.append(f"    Required by: {dep['required_by']}")
        lines.append("Run the install commands above via Bash to fix these.")
        lines.append("--- END DEPENDENCIES ---")
        lines.append("")

    if brain_index:
        lines.append("--- BRAIN INDEX ---")
        lines.append(brain_index)
        lines.append("--- END INDEX ---")

    lines.append("")
    lines.append("Thesis: context/thesis.md (in plugin root)")
    lines.append("Sources: context/sources.md (in plugin root)")
    lines.append("")
    lines.append("Load context/thesis.md before scoring or analyzing deals.")
    lines.append("After analyzing a company, ask to compile findings into the brain.")

    result = {"additionalContext": "\n".join(lines)}
    print(json.dumps(result))


if __name__ == "__main__":
    main()
