---
name: speckit-taskstoissues
description: Convert existing tasks into actionable, dependency-ordered GitHub issues for the feature based on available design artifacts. Requires GitHub MCP server.
---

# speckit-taskstoissues

Convert existing tasks into actionable, dependency-ordered GitHub issues for the feature based on available design artifacts.

## Scope Guard

This skill's work is limited to creating GitHub issues from tasks.md. Do not modify spec.md, plan.md, or tasks.md.

## Pre-Execution Checks

Check for extension hooks (before tasks-to-issues conversion):
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_taskstoissues` key
- For each executable hook, output the hook info and invoke it before proceeding.

## Outline

1. **Run setup script** from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute.
2. **Load constitution** (if exists): `.specify/memory/constitution.md` for project principles and governance constraints.
3. **Extract the path to tasks** from the executed script.
4. **Get the Git remote** by running: `git config --get remote.origin.url`
   - **CAUTION**: ONLY PROCEED TO NEXT STEPS IF THE REMOTE IS A GITHUB URL
5. **Fetch existing issues for deduplication:
   - Build the set of task IDs from `tasks.md` (each is a `T` followed by three digits, e.g. `T001`)
   - Use the GitHub MCP server's `list_issues` tool to look for issues that already cover those IDs
   - Do not pass a `state` value (omitting it returns both open and closed issues)
   - Request `perPage: 100` and use cursor-based pagination with `after` parameter
   - For each issue title, match it against the task ID pattern `\bT\d{3}\b` (word boundaries so tokens like `ST001` or `T0010` are not matched)
   - When it matches one of your task IDs, mark that ID as already having an issue
   - Stop paginating as soon as every task ID has been matched, or when there are no more pages

6. **For each task in the list**, use the GitHub MCP server to create a new issue:
   - Task lines in `tasks.md` start with a markdown checkbox, so first strip the leading `- [ ]` (and any `[P]` / `[US#]` markers) to recover the task ID and its description
   - Create the issue with a single canonical title of the form `T001: <description>`, with the ID written once followed by the task description
   - Skip any task whose ID is already present in the set of existing issues from the previous step, and report it (e.g., `T001 already has an issue, skipping`)
   - Only create issues for tasks that do not yet have a matching issue

**CAUTION**: UNDER NO CIRCUMSTANCES EVER CREATE ISSUES IN REPOSITORIES THAT DO NOT MATCH THE REMOTE URL

## Post-Execution Checks

Check for extension hooks (after tasks-to-issues conversion): Check for `hooks.after_taskstoissues` in `.specify/extensions.yml`

## Requirements

- GitHub MCP server must be available and configured
- Repository must have a GitHub remote URL
- tasks.md must exist and be complete

## Example Usage

```
/speckit.taskstoissues
```