#!/usr/bin/env python3
from __future__ import annotations
"""
Generate skill-rules.json from SKILL.md files.

Scans skills/*/SKILL.md and extracts:
1. Frontmatter: name, description
2. <auto_trigger> blocks: explicit trigger patterns
3. Falls back to keyword extraction from description

This enables zero-config skill evaluation across any project.
"""

import json
import os
import re
import sys
from pathlib import Path


def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    pattern = r"^---\s*\n(.*?)\n---"
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        return {}

    frontmatter_text = match.group(1)
    result = {}

    for line in frontmatter_text.split("\n"):
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            result[key] = value

    return result


def extract_auto_trigger(content: str) -> dict:
    """Extract <auto_trigger> block and parse trigger patterns."""
    pattern = r"<auto_trigger>(.*?)</auto_trigger>"
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        return {}

    trigger_content = match.group(1)

    triggers = {
        "keywords": [],
        "keywordPatterns": [],
        "intentPatterns": [],
    }

    # Extract quoted strings as keywords
    quoted = re.findall(r'"([^"]+)"', trigger_content)
    for q in quoted:
        if "/" in q or "." in q or q.startswith("-"):
            continue
        if len(q.split()) <= 4:
            triggers["keywords"].append(q.lower())

    # Extract patterns from bullet points
    bullets = re.findall(r'[-*]\s*["\']?([^"\'\n,]+)["\']?', trigger_content)
    for bullet in bullets:
        bullet = bullet.strip().lower()
        if len(bullet) > 40:
            continue
        if bullet.endswith(":"):
            continue
        if bullet and bullet not in triggers["keywords"]:
            triggers["keywords"].append(bullet)

    # Look for intent patterns
    intent_verbs = ["write", "create", "add", "fix", "debug", "implement", "build", "draft", "generate", "make"]
    for verb in intent_verbs:
        if verb in trigger_content.lower():
            patterns = re.findall(rf'\b{verb}\b[^."\n]{{0,30}}', trigger_content.lower())
            for p in patterns:
                if len(p) > 5:
                    escaped = re.escape(p.strip())
                    triggers["intentPatterns"].append(escaped)

    triggers["keywords"] = list(set(triggers["keywords"]))
    triggers["intentPatterns"] = list(set(triggers["intentPatterns"]))[:5]

    return triggers


def extract_keywords_from_description(description: str) -> list:
    """Extract meaningful keywords from skill description."""
    if not description:
        return []

    stop_words = {
        "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "must", "shall", "can", "need", "dare",
        "to", "of", "in", "for", "on", "with", "at", "by", "from", "as",
        "into", "through", "during", "before", "after", "above", "below",
        "between", "under", "again", "further", "then", "once", "here",
        "there", "when", "where", "why", "how", "all", "each", "few",
        "more", "most", "other", "some", "such", "no", "nor", "not",
        "only", "own", "same", "so", "than", "too", "very", "just",
        "and", "but", "if", "or", "because", "until", "while", "this",
        "that", "these", "those", "what", "which", "who", "whom",
        "use", "uses", "using", "used", "invoke", "invokes", "invoked",
        "tool", "tools", "skill", "skills", "agent", "agents",
    }

    words = re.findall(r'\b[a-z]{3,}\b', description.lower())
    keywords = [w for w in words if w not in stop_words and len(w) >= 3]

    quoted = re.findall(r'"([^"]+)"', description)
    keywords.extend([q.lower() for q in quoted if len(q) <= 30])

    return list(set(keywords))


def parse_skill_file(skill_path: Path) -> dict | None:
    """Parse a single SKILL.md file and return rule configuration."""
    try:
        content = skill_path.read_text()
    except Exception:
        return None

    frontmatter = extract_frontmatter(content)
    name = frontmatter.get("name", skill_path.parent.name)
    description = frontmatter.get("description", "")

    triggers = {
        "keywords": [],
        "keywordPatterns": [],
        "intentPatterns": [],
        "pathPatterns": [],
    }

    # Priority 1: Explicit auto_trigger block
    auto_triggers = extract_auto_trigger(content)
    if auto_triggers:
        triggers["keywords"].extend(auto_triggers.get("keywords", []))
        triggers["keywordPatterns"].extend(auto_triggers.get("keywordPatterns", []))
        triggers["intentPatterns"].extend(auto_triggers.get("intentPatterns", []))

    # Priority 2: Keywords from description
    desc_keywords = extract_keywords_from_description(description)
    triggers["keywords"].extend(desc_keywords)

    # Priority 3: Skill name itself
    name_parts = name.replace("-", " ").replace("_", " ").split()
    triggers["keywords"].extend([p.lower() for p in name_parts if len(p) >= 3])

    triggers["keywords"] = list(set(triggers["keywords"]))

    has_auto_trigger = bool(auto_triggers.get("keywords") or auto_triggers.get("intentPatterns"))
    priority = 8 if has_auto_trigger else 5

    return {
        "description": description[:500] if description else f"Skill: {name}",
        "priority": priority,
        "triggers": triggers,
        "excludePatterns": [],
        "source": "auto_trigger" if has_auto_trigger else "description",
    }


def generate_rules(project_dir: str) -> dict:
    """Generate complete skill-rules.json from project skills."""
    skills_dir = Path(project_dir) / "skills"

    rules = {
        "version": "2.0",
        "generated": True,
        "config": {
            "minConfidenceScore": 3,
            "maxSkillsToShow": 5,
            "showMatchReasons": True,
        },
        "scoring": {
            "keyword": 2,
            "keywordPattern": 3,
            "pathPattern": 4,
            "directoryMatch": 5,
            "intentPattern": 4,
            "contextPattern": 2,
            "contentPattern": 3,
        },
        "directoryMappings": {},
        "skills": {},
    }

    if not skills_dir.exists():
        return rules

    for skill_md in skills_dir.glob("*/SKILL.md"):
        skill_name = skill_md.parent.name
        skill_config = parse_skill_file(skill_md)

        if skill_config:
            rules["skills"][skill_name] = skill_config
            skill_rel_path = f"skills/{skill_name}"
            rules["directoryMappings"][skill_rel_path] = skill_name

    return rules


def main():
    """Generate skill-rules.json and write to disk."""
    project_dir = os.environ.get(
        "CLAUDE_PLUGIN_ROOT",
        os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()),
    )

    rules = generate_rules(project_dir)

    output_path = Path(__file__).parent / "skill-rules.json"

    with open(output_path, "w") as f:
        json.dump(rules, f, indent=2)

    skill_count = len(rules.get("skills", {}))
    auto_trigger_count = sum(
        1 for s in rules.get("skills", {}).values()
        if s.get("source") == "auto_trigger"
    )

    print(f"Generated rules for {skill_count} skills ({auto_trigger_count} with auto_trigger)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
