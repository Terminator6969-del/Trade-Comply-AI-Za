---
name: speckit-plan
description: Execute the implementation planning workflow using the plan template to generate design artifacts. Creates technical context, research, data model, contracts, and quickstart guide.
---

# speckit-plan

Execute the implementation planning workflow using the plan template to generate design artifacts.

## Scope Guard

This skill's work is limited to creating the implementation plan and design artifacts. Do not implement code.

## Pre-Execution Checks

Check for extension hooks (before planning):
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_plan` key
- For each executable hook, output the hook info and invoke it before proceeding.

## Outline

1. **Setup**: Load the feature spec and constitution. Load the plan template.
2. **Execute plan workflow**: Follow the structure in the plan template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Re-evaluate Constitution Check post-design

## Phases

### Phase 0: Outline & Research

1. Extract unknowns from Technical Context:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. Generate and dispatch research agents:
   ```
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. Consolidate findings in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

Output: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Design & Contracts

Prerequisites: `research.md` complete

1. Extract entities from feature spec → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. Define interface contracts (if project has external interfaces) → `/contracts/`:
   - Identify what interfaces the project exposes to users or other systems
   - Document the contract format appropriate for the project type
   - Examples: public APIs for libraries, command schemas for CLI tools, endpoints for web services, grammars for parsers, UI contracts for applications
   - Skip if project is purely internal (build scripts, one-off tools, etc.)

3. Create quickstart validation guide → `quickstart.md`:
   - Document runnable validation scenarios that prove the feature works end-to-end
   - Include prerequisites, setup commands, test/run commands, and expected outcomes
   - Use links or references to contracts and data model details instead of duplicating them
   - Do not include full implementation code, model/service/controller bodies, migrations, or complete test suites
   - Keep this artifact as a validation/run guide; implementation details belong in `tasks.md` and the implementation phase

Output: data-model.md, /contracts/*, quickstart.md

## Mandatory Post-Execution Hooks

Check for `hooks.after_plan` in `.specify/extensions.yml`

## Completion Report

Command ends after Phase 1 design. Report branch, plan path, and generated artifacts.

## Key Rules

- Use absolute paths for filesystem operations; use project-relative paths for references in documentation
- ERROR on gate failures or unresolved clarifications

## Template Structure

The plan template includes these sections:
- **Technical Context**: Language, frameworks, libraries, database, testing, target platform
- **Constitution Check**: Alignment with project principles
- **Phase 0 Research**: Decisions and rationale for unknowns
- **Phase 1 Design**: Data model, contracts, quickstart guide

## Example Usage

```
/speckit.plan The application uses Vite with minimal number of libraries. Use vanilla HTML, CSS, and JavaScript as much as possible. Images are not uploaded anywhere and metadata is stored in a local SQLite database.
```