#!/usr/bin/env python3
"""SessionStart hook: check dependencies and inject Wavelength context."""
import json
import os
import shutil
import subprocess


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

    # Check dependencies
    missing_deps = check_dependencies()

    # Build context injection
    lines = [
        "WAVELENGTH SHARED MEMORY",
        f"Plugin root: {plugin_root}",
        "Memory is MCP-backed and shared across authenticated Wavelength users.",
        "List memory with query_context {}. Search by slug, tags, or keyword. Save durable context with update_context.",
        "Virtual areas: /thesis, /companies, /industries, /people, /learnings, /sources, /criteria, /templates.",
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

    lines.append("")
    lines.append("Thesis: context/thesis.md (in plugin root)")
    lines.append("Sources: context/sources.md (in plugin root)")
    lines.append("")
    lines.append("Load context/thesis.md before scoring or analyzing deals.")
    lines.append("Before deal or company work, query memory for relevant company, industry, person, or thesis context.")
    lines.append("After durable analysis, calibration, red-team work, call notes, or thesis updates, ask whether to save to memory.")

    result = {"additionalContext": "\n".join(lines)}
    print(json.dumps(result))


if __name__ == "__main__":
    main()
