---
name: speckit-specify
description: Create or update the feature specification from a natural language feature description. Focus on the what and why, not the tech stack.
---

# speckit-specify

Create or update the feature specification from a natural language feature description. Focus on the what and why, not the tech stack.

## Scope Guard

This skill's work is limited to creating/updating the feature specification. Do not create implementation plans, tasks, or code.

## Pre-Execution Checks

Check for extension hooks (before specification):
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_specify` key
- For each executable hook, output the hook info and invoke it before proceeding.

## Outline

Given a feature description, do this:

1. **Generate a concise short name** (2-4 words) for the feature:
   - Analyze the feature description and extract the most meaningful keywords
   - Create a 2-4 word short name that captures the essence of the feature
   - Use action-noun format when possible (e.g., "add-user-auth", "fix-payment-bug")
   - Preserve technical terms and acronyms (OAuth2, API, JWT, etc.)

2. **Create the spec feature directory**:
   - Specs live under the default `specs/` directory
   - Resolution order for feature directory:
     - If user explicitly provided `SPECIFY_FEATURE_DIRECTORY`, use it as-is
     - Otherwise, auto-generate under `specs/`:
       - Check `.specify/init-options.json` for `feature_numbering` (preferred) or `branch_numbering` (deprecated)
       - If `"timestamp"`: prefix is `YYYYMMDD-HHMMSS` (current timestamp)
       - If `"sequential"` or absent: prefix is `NNN` (next available 3-digit number)
       - Construct directory name: `<prefix>-<short-name>` (e.g., `003-user-auth` or `20260319-143022-user-auth`)
   - Create directory: `mkdir -p SPECIFY_FEATURE_DIRECTORY`
   - Resolve the active `spec-template` through the Spec Kit preset/template resolution stack
   - Copy the resolved `spec-template` file to `SPECIFY_FEATURE_DIRECTORY/spec.md` as the starting point
   - Set `SPEC_FILE` to `SPECIFY_FEATURE_DIRECTORY/spec.md`
   - Persist the resolved path to `.specify/feature.json`

3. **Load the resolved active `spec-template`** file to understand required sections.

4. **IF EXISTS**: Load `.specify/memory/constitution.md` for project principles and governance constraints.

5. **Follow this execution flow**:
   - Parse user description from arguments. If empty: ERROR "No feature description provided"
   - Extract key concepts from description: actors, actions, data, constraints
   - For unclear aspects:
     - Make informed guesses based on context and industry standards
     - Only mark with `[NEEDS CLARIFICATION: specific question]` if:
       - The choice significantly impacts feature scope or user experience
       - Multiple reasonable interpretations exist with different implications
       - No reasonable default exists
     - LIMIT: Maximum 3 `[NEEDS CLARIFICATION]` markers total
     - Prioritize clarifications by impact: scope > security/privacy > user experience > technical details
   - Fill User Scenarios & Testing section. If no clear user flow: ERROR "Cannot determine user scenarios"
   - Generate Functional Requirements. Each requirement must be testable. Use reasonable defaults for unspecified details (document assumptions in Assumptions section)
   - Define Success Criteria. Create measurable, technology-agnostic outcomes. Include both quantitative metrics (time, performance, volume) and qualitative measures (user satisfaction, task completion). Each criterion must be verifiable without implementation details.
   - Identify Key Entities (if data involved)
   - Return: SUCCESS (spec ready for planning)

6. **Write the specification** to `SPEC_FILE` using the template structure, replacing placeholders with concrete details derived from the feature description while preserving section order and headings.

7. **Specification Quality Validation**: After writing the initial spec, validate it against quality criteria:
   - Create Spec Quality Checklist at `SPECIFY_FEATURE_DIRECTORY/checklists/requirements.md`
   - Run Validation Check: Review the spec against each checklist item
   - Handle Validation Results:
     - If all items pass: Mark checklist complete and proceed
     - If items fail (excluding `[NEEDS CLARIFICATION]`): List failing items, update spec, re-run validation (max 3 iterations)
     - If `[NEEDS CLARIFICATION]` markers remain (max 3): Present options to user in table format, wait for responses, update spec, re-run validation

8. **Mandatory Post-Execution Hooks**: Check for `hooks.after_specify` in `.specify/extensions.yml`

9. **Completion Report**: Report to user with:
   - `SPECIFY_FEATURE_DIRECTORY` — the feature directory path
   - `SPEC_FILE` — the spec file path
   - Checklist results summary
   - Readiness for the next phase (`speckit-clarify` or `speckit-plan`)

## Template Structure

The spec template includes these sections:
- **Feature Name**: Short descriptive name
- **User Scenarios & Testing**: Primary user flows, acceptance scenarios
- **Functional Requirements**: Numbered, testable requirements
- **Non-Functional Requirements**: Performance, security, accessibility
- **Key Entities**: Data models if applicable
- **Success Criteria**: Measurable, technology-agnostic outcomes
- **Assumptions**: Documented defaults for unspecified details
- **Out of Scope**: Explicitly excluded functionality

## Success Criteria Guidelines

Success criteria must be:
1. Measurable: Include specific metrics (time, percentage, count, rate)
2. Technology-agnostic: No mention of frameworks, languages, databases, or tools
3. User-focused: Describe outcomes from user/business perspective
4. Verifiable: Can be tested/validated without knowing implementation details

Good examples:
- "Users can complete checkout in under 3 minutes"
- "System supports 10,000 concurrent users"
- "95% of searches return results in under 1 second"

Bad examples (implementation-focused):
- "API response time is under 200ms" (too technical)
- "Database can handle 1000 TPS" (implementation detail)
- "React components render efficiently" (framework-specific)

## Example Usage

```
/speckit.specify Build an application that can help me organize my photos in separate photo albums. Albums are grouped by date and can be re-organized by dragging and dropping on the main page. Within each album, photos are previewed in a tile-like interface.
```