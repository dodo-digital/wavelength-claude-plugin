#!/usr/bin/env python3
"""UserPromptSubmit event router: skill activation."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from router.framework import dispatch
from router.models import HandlerConfig
from router.handlers.skills import skill_router

HANDLERS = [
    HandlerConfig(fn=skill_router, name="skill-router"),
]

if __name__ == "__main__":
    dispatch(HANDLERS, "UserPromptSubmit")
