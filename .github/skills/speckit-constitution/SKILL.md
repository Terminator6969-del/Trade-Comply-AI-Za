---
name: speckit-constitution
description: Create or update the project constitution from interactive or provided principle inputs. The constitution defines governing principles and development guidelines that guide all subsequent development.
---

# speckit-constitution

Create or update the project constitution at `.specify/memory/constitution.md`. The constitution defines governing principles and development guidelines that guide all subsequent development.

## Scope Guard

This skill's work is limited to updating the project constitution itself. Dependent templates and commands read the constitution at runtime and are not modified here.

- Classify every part of the user input as either constitution content or a separate, non-governance intent.
- If the input includes feature implementation, code generation, refactoring, building, or deployment requests, you MUST NOT execute them. Extract them as deferred intents instead.
- You MUST NOT create, modify, or delete application source files, feature routes, components, tests, deployment files, or other artifacts unrelated to the constitution workflow.
- If it is unclear whether an instruction is constitution content, ask for clarification before making changes.
- After completing the constitution update, include a `Next Actions` section for each deferred intent. List the original intent and suggest the appropriate follow-up Spec Kit command, such as `speckit-specify`, without invoking it.

## Pre-Execution Checks

Check for extension hooks (before constitution update):
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_constitution` key
- For each executable hook, output the hook info and invoke it before proceeding.

## Outline

You are updating the project constitution at `.specify/memory/constitution.md`. The active constitution scaffold is resolved at command time from the constitution template through the Spec Kit preset/template resolution stack.

Follow this execution flow:

1. **Resolve the active template**: Run the template resolver to get the active `constitution-template.md` content.
2. **Load existing constitution**: If `.specify/memory/constitution.md` exists, load it as the source of current project-specific values and amendments. Preserve information that is still applicable when applying the newly resolved scaffold.
3. **Identify placeholders**: Find every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
4. **Collect/derive values for placeholders**:
   - If user input supplies a value, use it.
   - Otherwise infer from existing repo context (README, docs, prior constitution versions).
   - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made.
   - `CONSTITUTION_VERSION` must increment according to semantic versioning rules:
     - MAJOR: Backward incompatible governance/principle removals or redefinitions.
     - MINOR: New principle/section added or materially expanded guidance.
     - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
5. **Draft the updated constitution**: Replace every placeholder with concrete text. Preserve heading hierarchy. Ensure each Principle section has: succinct name line, paragraph capturing non-negotiable rules, explicit rationale if not obvious. Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.
6. **Produce a Sync Impact Report** (prepend as HTML comment at top of constitution file):
   - Version change: old → new
   - List of modified principles (old title → new title if renamed)
   - Added sections
   - Removed sections
   - Follow-up TODOs if any placeholders intentionally deferred.
7. **Validation before final output**:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - Principles are declarative, testable, and free of vague language ("should" → replace with MUST/SHOULD rationale where appropriate).
8. **Write the completed constitution** back to `.specify/memory/constitution.md` (overwrite).
9. **Output a final summary** to the user with:
   - New version and bump rationale.
   - Any TODO placeholders or deferred items requiring manual follow-up.
   - Suggested commit message.
   - A `Next Actions` section for any deferred non-governance intents.

## Post-Execution Checks

Check for extension hooks (after constitution update): Check if `.specify/extensions.yml` exists and look for entries under `hooks.after_constitution`.

## Template Structure

The constitution template includes these sections:
- **Preamble**: Project name, purpose, scope
- **Principles**: Numbered list of governing principles (each with name, rule, rationale)
- **Governance**: Amendment procedure, versioning policy, compliance review
- **Appendices**: Glossary, references, change log

## Example Usage

```
/speckit.constitution Create principles focused on code quality, testing standards, user experience consistency, and performance requirements
```