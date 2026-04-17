"""Skill handlers: router for automatic skill activation."""

import json
import os
import subprocess
from pathlib import Path
from typing import Optional

from ..models import HandlerResult


def skill_router(input_data: dict) -> Optional[HandlerResult]:
    """UserPromptSubmit: evaluate prompt for skill activation suggestions."""
    prompt = input_data.get("prompt", "")
    if not prompt or not prompt.strip():
        return None

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    router_dir = Path(project_dir) / ".claude" / "hooks" / "router" / "skill-router"
    rules_path = router_dir / "skill-rules.json"
    generate_script = router_dir / "generate-rules.py"
    router_script = router_dir / "skill-router.py"

    if not router_script.exists():
        return None

    # Auto-regenerate rules if needed
    skills_dir = Path(project_dir) / ".claude" / "skills"
    regenerate = False

    if not rules_path.exists():
        regenerate = True
    elif skills_dir.exists():
        try:
            rules_mtime = rules_path.stat().st_mtime
            for skill_md in skills_dir.rglob("SKILL.md"):
                if skill_md.stat().st_mtime > rules_mtime:
                    regenerate = True
                    break
        except Exception:
            pass

    if regenerate and generate_script.exists():
        try:
            subprocess.run(
                ["python3", str(generate_script)],
                capture_output=True,
                timeout=5,
                cwd=project_dir,
            )
        except Exception:
            pass

    # Run the skill router
    try:
        result = subprocess.run(
            ["python3", str(router_script)],
            input=json.dumps(input_data),
            capture_output=True,
            text=True,
            timeout=5,
            cwd=project_dir,
        )

        if result.stdout.strip():
            return HandlerResult(additional_context=result.stdout.strip())

    except (subprocess.TimeoutExpired, Exception):
        pass

    return None
