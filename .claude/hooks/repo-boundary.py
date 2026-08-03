#!/usr/bin/env python3
"""PreToolUse guard for the spectacular plugin repo.

Sessions here must never MODIFY anything outside this repo — in particular
project/workspace repos that use the plugin (Ways of working #7). Reading
other repos stays allowed (the owner may ask for read-only analysis).

Blocks:
  - Write/Edit/NotebookEdit whose file_path is outside the allowed roots;
  - Bash commands that reference an outside path AND contain a mutating
    token (git commit, rm, mv, redirection, ...). Heuristic by design —
    the file-tool guard above is the airtight layer.

Allowed roots: this repo, /tmp + /private/tmp (scratchpads), ~/.claude
(session memory/config).
"""
import json
import os
import re
import sys

REPO = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
ALLOWED = [REPO, "/tmp", "/private/tmp", os.path.expanduser("~/.claude")]

MUTATING = re.compile(
    r"(?:^|[\s;&|])(?:rm|mv|cp|mkdir|touch|tee|truncate|ln|chmod|chown|rsync)\b"
    r"|\bgit\b[^;&|]*\b(?:add|commit|push|rm|mv|reset|checkout|restore|merge|rebase|apply|stash|clean|init)\b"
    r"|\bsed\s+-i\b"
    r"|>{1,2}\s*[~/]"
)
PATH_TOKEN = re.compile(r"(?:/Users/[^\s'\";|&)]+|~/[^\s'\";|&)]+)")


def is_allowed(path: str) -> bool:
    rp = os.path.realpath(os.path.expanduser(path))
    for root in ALLOWED:
        rr = os.path.realpath(root)
        if rp == rr or rp.startswith(rr + os.sep):
            return True
    return False


def block(message: str) -> None:
    print(message, file=sys.stderr)
    sys.exit(2)


data = json.load(sys.stdin)
tool = data.get("tool_name", "")
tool_input = data.get("tool_input", {})

if tool in ("Write", "Edit", "NotebookEdit"):
    path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    if path and not is_allowed(path):
        block(
            f"BLOCKED by repo-boundary hook: {path} is outside the spectacular "
            "repo. Sessions in this repo never modify project/workspace repos "
            "(Ways of working #7) — suggest the steps for the owner to run "
            "there instead (a plugin skill if one fits, else precise manual "
            "steps)."
        )
elif tool == "Bash":
    command = tool_input.get("command", "")
    outside = [p for p in PATH_TOKEN.findall(command) if not is_allowed(p)]
    if outside and MUTATING.search(command):
        block(
            "BLOCKED by repo-boundary hook: this Bash command references a "
            f"path outside the spectacular repo ({outside[0]}) and looks "
            "mutating. Sessions in this repo never modify project/workspace "
            "repos (Ways of working #7). Read-only inspection is fine; "
            "for changes, suggest steps for the owner to run there instead."
        )

sys.exit(0)
