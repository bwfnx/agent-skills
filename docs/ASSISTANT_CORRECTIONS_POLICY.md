# Assistant Corrections Policy

## Workflow rule
When a correction is logged in `docs/ASSISTANT_CORRECTIONS.md`, also update the most relevant template, checklist, or repository convention file so the fix becomes part of the workflow and not just a historical note.

## Application guidance
Choose the most relevant follow-on location based on the correction type:
- packaging or install issue -> update packaging checklist or release workflow
- naming issue -> update repo conventions, starter templates, or validation checklist
- metadata issue -> update manifest guidance, example files, or template frontmatter examples
- connector or tool limitation -> update workflow docs with the workaround step

## Minimum expectation
Every correction should result in:
1. a logged registry entry in `docs/ASSISTANT_CORRECTIONS.md`
2. at least one preventive update to a workflow-facing file when applicable

## Intent
The registry is the memory.
The workflow files are the prevention.
