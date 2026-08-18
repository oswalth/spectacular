---
status: todo
story: story-NNN
repo: <registry-name>
depends_on: []
---

<!-- story: is required for a task that delivers a story. A standalone task
(maintenance work with no story, written by plan's standalone mode) drops the
line entirely — repo: and Verification alone make it ready. -->

# task-NNN — <one repo's share of the story, or the maintenance change>

## Description

## Design references

<!-- Only for UI tasks: the design spec sections and source frames this task
implements. Drop the section otherwise. -->

- design-NNN <flow / screen> — <source frame link>

## Verification

<written before any code; repeatable by anyone in this repo>

- Preconditions: <state or setup needed>
- Steps: <numbered commands or actions>
- Expected: <observable result — pass/fail>

## Learnings

<!-- Story-level only: what this story's next task must know. Repo-level
facts — toolchain, versions, CLI and lint traps, layout — go to the repo
contract's Toolchain notes at the landing gate. Not a diary. -->
