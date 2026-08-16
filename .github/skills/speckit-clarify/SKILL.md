---
name: speckit-clarify
description: Identify underspecified areas in the current feature spec by asking up to 5 highly targeted clarification questions and encoding answers back into the spec. Run before speckit-plan.
---

# speckit-clarify

Identify underspecified areas in the current feature spec by asking up to 5 highly targeted clarification questions and encoding answers back into the spec.

## Scope Guard

This skill's work is limited to clarifying the feature specification. Do not create implementation plans, tasks, or code.

## Pre-Execution Checks

Check for extension hooks (before clarification):
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_clarify` key
- For each executable hook, output the hook info and invoke it before proceeding.

## Outline

Goal: Detect and reduce ambiguity or missing decision points in the active feature specification and record the clarifications directly in the spec file.

Note: This clarification workflow is expected to run (and be completed) BEFORE invoking `speckit-plan`. If the user explicitly states they are skipping clarification (e.g., exploratory spike), you may proceed, but must warn that downstream rework risk increases.

### Execution Steps:

1. **Run setup script** from repo root to get FEATURE_DIR and FEATURE_SPEC paths.
2. **Load constitution** (if exists): `.specify/memory/constitution.md` for project principles and governance constraints.
3. **Load the current spec file**. Perform a structured ambiguity & coverage scan using this taxonomy. For each category, mark status: Clear / Partial / Missing.

**Taxonomy Categories:**
- **Functional Scope & Behavior**: Core user goals, success criteria, out-of-scope declarations, user roles/personas
- **Domain & Data Model**: Entities, attributes, relationships, identity/uniqueness rules, lifecycle/state transitions, data volume/scale assumptions
- **Interaction & UX Flow**: Critical user journeys, error/empty/loading states, accessibility/localization notes
- **Non-Functional Quality Attributes**: Performance, scalability, reliability/availability, observability, security/privacy, compliance/regulatory
- **Integration & External Dependencies**: External services/APIs and failure modes, data import/export formats, protocol/versioning assumptions
- **Edge Cases & Failure Handling**: Negative scenarios, rate limiting/throttling, conflict resolution
- **Constraints & Tradeoffs**: Technical constraints, explicit tradeoffs or rejected alternatives
- **Terminology & Consistency**: Canonical glossary terms, avoided synonyms/deprecated terms
- **Completion Signals**: Acceptance criteria testability, measurable Definition of Done indicators
- **Misc / Placeholders**: TODO markers, ambiguous adjectives lacking quantification

For each category with Partial or Missing status, add a candidate question opportunity unless clarification would not materially change implementation or validation strategy.

4. **Generate prioritized queue** of candidate clarification questions (maximum 5). Apply constraints:
   - Maximum of 5 total questions across the whole session
   - Each question must be answerable with EITHER: multiple-choice (2-5 options) OR short-answer (<=5 words)
   - Only include questions whose answers materially impact architecture, data modeling, task decomposition, test design, UX behavior, operational readiness, or compliance validation
   - Ensure category coverage balance: highest impact unresolved categories first
   - Exclude questions already answered, trivial stylistic preferences, or plan-level execution details
   - Favor clarifications that reduce downstream rework risk or prevent misaligned acceptance tests

5. **Sequential questioning loop** (interactive):
   - Present EXACTLY ONE question at a time
   - Question format: `**Question:** <interrogative>?` (optionally with requirement ID: `**Question:** <interrogative>? (FR-023)`)
   - Immediately after: one plain-language "Why it matters" sentence
   - For multiple-choice: Analyze options, determine recommended option, present with reasoning, render as Markdown table
   - For short-answer: Provide suggested answer with reasoning
   - After user answers: validate, record in working memory, move to next question
   - Stop when: all critical ambiguities resolved, user signals completion, or 5 questions asked

6. **Integration after EACH accepted answer** (incremental update):
   - Maintain in-memory representation of the spec
   - For first answer: Ensure `## Clarifications` section exists, create `### Session YYYY-MM-DD` subheading
   - Append bullet: `- Q: <question> → A: <final answer>`
   - Apply clarification to most appropriate section(s):
     - Functional ambiguity → Functional Requirements
     - User interaction/actor distinction → User Stories or Actors
     - Data shape/entities → Data Model
     - Non-functional constraint → Success Criteria > Measurable Outcomes
     - Edge case/negative flow → Edge Cases / Error Handling
     - Terminology conflict → Normalize term across spec
   - Save spec file AFTER each integration (atomic overwrite)
   - Preserve formatting, heading hierarchy

7. **Validation** (after EACH write plus final pass):
   - Clarifications session contains exactly one bullet per accepted answer
   - Total asked questions ≤ 5
   - Updated sections contain no lingering vague placeholders
   - No contradictory earlier statements remain
   - Markdown structure valid
   - Terminology consistency

8. **Write updated spec** back to FEATURE_SPEC.

9. **Re-validate Spec Quality Checklist** (if exists):
   - Read `FEATURE_DIR/checklists/requirements.md`
   - Re-evaluate each checkbox item against updated spec
   - Update markers: `[ ]` → `[x]` if now passes, `[x]` → `[ ]` if now fails
   - Save updated checklist file
   - Compute before/after pass counts

## Mandatory Post-Execution Hooks

Check for `hooks.after_clarify` in `.specify/extensions.yml`

## Completion Report

Report completion with:
- Number of questions asked & answered
- Path to updated spec
- Sections touched (list names)
- Spec quality checklist status (before/after pass counts, items that changed state)
- Coverage summary table: each taxonomy category with Status (Resolved/Deferred/Clear/Outstanding)
- If any Outstanding or Deferred remain, recommend whether to proceed to `speckit-plan` or run `speckit-clarify` again later
- Suggested next command

## Example Usage

```
/speckit.clarify
```