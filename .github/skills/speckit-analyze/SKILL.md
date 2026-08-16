---
name: speckit-analyze
description: Perform a non-destructive cross-artifact consistency and quality analysis across spec.md, plan.md, and tasks.md after task generation. Run after speckit-tasks, before speckit-implement.
---

# speckit-analyze

Perform a non-destructive cross-artifact consistency and quality analysis across spec.md, plan.md, and tasks.md after task generation.

## Scope Guard

STRICTLY READ-ONLY: Do not modify any files. Output a structured analysis report. Offer an optional remediation plan (user must explicitly approve before any follow-up editing commands would be invoked manually).

Constitution Authority: The project constitution (`.specify/memory/constitution.md`) is non-negotiable within this analysis scope. Constitution conflicts are automatically CRITICAL and require adjustment of the spec, plan, or tasks—not dilution, reinterpretation, or silent ignoring of the principle.

## Pre-Execution Checks

Check for extension hooks (before analysis):
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_analyze` key
- For each executable hook, output the hook info and invoke it before proceeding.

## Goal

Identify inconsistencies, duplications, ambiguities, and underspecified items across the three core artifacts (`spec.md`, `plan.md`, `tasks.md`) before implementation. This command MUST run only after `speckit-tasks` has successfully produced a complete `tasks.md`.

## Execution Steps

### 1. Initialize Analysis Context

Run setup script from repo root and parse JSON for FEATURE_DIR and AVAILABLE_DOCS. Derive absolute paths:
- SPEC = FEATURE_DIR/spec.md
- PLAN = FEATURE_DIR/plan.md
- TASKS = FEATURE_DIR/tasks.md

Abort with an error message if any required file is missing (instruct the user to run missing prerequisite command).

### 2. Load Artifacts (Progressive Disclosure)

Load only the minimal necessary context from each artifact:

**From spec.md:**
- Overview/Context
- Functional Requirements
- Success Criteria (measurable outcomes)
- User Stories
- Edge Cases (if present)

**From plan.md:**
- Architecture/stack choices
- Data Model references
- Phases
- Technical constraints

**From tasks.md:**
- Task IDs
- Descriptions
- Phase grouping
- Parallel markers [P]
- Referenced file paths

**From constitution:**
- Load `.specify/memory/constitution.md` for principle validation

### 3. Build Semantic Models

Create internal representations:
- **Requirements inventory**: For each Functional Requirement (FR-###) and Success Criterion (SC-###), record a stable key. Include only Success Criteria items that require buildable work.
- **User story/action inventory**: Discrete user actions with acceptance criteria
- **Task coverage mapping**: Map each task to one or more requirements or stories (inference by keyword/explicit reference patterns)
- **Constitution rule set**: Extract principle names and MUST/SHOULD normative statements

### 4. Detection Passes (Token-Efficient Analysis)

Focus on high-signal findings. Limit to 50 findings total; aggregate remainder in overflow summary.

**A. Duplication Detection**
- Identify near-duplicate requirements
- Mark lower-quality phrasing for consolidation

**B. Ambiguity Detection**
- Flag vague adjectives (fast, scalable, secure, intuitive, robust) lacking measurable criteria
- Flag unresolved placeholders (TODO, TKTK, ???, `<placeholder>`, etc.)

**C. Underspecification**
- Requirements with verbs but missing object or measurable outcome
- User stories missing acceptance criteria alignment
- Tasks referencing files or components not defined in spec/plan

**D. Constitution Alignment**
- Any requirement or plan element conflicting with a MUST principle
- Missing mandated sections or quality gates from constitution

**E. Coverage Gaps**
- Requirements with zero associated tasks
- Tasks with no mapped requirement/story
- Success Criteria requiring buildable work (performance, security, availability) not reflected in tasks

**F. Inconsistency**
- Terminology drift (same concept named differently across files)
- Data entities referenced in plan but absent in spec (or vice versa)
- Task ordering contradictions (e.g., integration tasks before foundational setup tasks without dependency note)
- Conflicting requirements (e.g., one requires Next.js while other specifies Vue)

### 5. Severity Assignment

Use this heuristic to prioritize findings:
- **CRITICAL**: Violates constitution MUST, missing core spec artifact, or requirement with zero coverage that blocks baseline functionality
- **HIGH**: Duplicate or conflicting requirement, ambiguous security/performance attribute, untestable acceptance criterion
- **MEDIUM**: Terminology drift, missing non-functional task coverage, underspecified edge case
- **LOW**: Style/wording improvements, minor redundancy not affecting execution order

### 6. Produce Compact Analysis Report

Output a Markdown report with the following structure:

**Findings Table:**
| ID | Category | Severity | Location | Finding | Suggested Fix |
|---|---|---|---|---|---|
| A1 | Duplication | HIGH | spec.md:L120-134 | Two similar requirements... | Merge phrasing; keep clearer version |

(Add one row per finding; generate stable IDs prefixed by category initial.)

**Coverage Summary Table:**
| Metric | Value |
|---|---|
| Total Requirements | N |
| Total Tasks | N |
| Coverage % (requirements with >=1 task) | X% |
| Ambiguity Count | N |
| Duplication Count | N |
| Critical Issues Count | N |

**Constitution Alignment Issues:** (if any)

**Unmapped Tasks:** (if any)

### 7. Provide Next Actions

At end of report, output a concise Next Actions block:
- If CRITICAL issues exist: Recommend resolving before `speckit-implement`
- If only LOW/MEDIUM: User may proceed, but provide improvement suggestions
- Provide explicit command suggestions: e.g., "Run speckit-specify with refinement", "Run speckit-plan to adjust architecture", "Manually edit tasks.md to add coverage for 'performance-metrics'"

### 8. Offer Remediation

Ask the user: "Would you like me to suggest concrete remediation edits for the top N issues?" (Do NOT apply them automatically.)

### 9. Check for extension hooks

Check for `hooks.after_analyze` in `.specify/extensions.yml`

## Operating Principles

- **Context Efficiency**: Minimal high-signal tokens; progressive disclosure; token-efficient output; deterministic results
- **Analysis Guidelines**: NEVER modify files; NEVER hallucinate missing sections; Prioritize constitution violations; Use examples over exhaustive rules; Report zero issues gracefully

## Example Usage

```
/speckit.analyze
```