# Skill Creation Checklist

Use this checklist when adding a new skill.

## Before building
- Define the exact user input
- Define the exact output
- Identify any tools or connectors needed
- Decide whether the skill needs scripts, references, or assets

## Required files
- `SKILL.md`
- `agents/openai.yaml`
- `README.md`
- `CHANGELOG.md`

## Quality checks
- Frontmatter `name` is lowercase
- Frontmatter `description` is lowercase and clearly states when to use the skill
- Instructions are specific and reusable
- Extra files are included only if they materially improve performance
- Example or placeholder files are removed

## Release checks
- Test with at least one real example
- Update `CHANGELOG.md`
- Package fresh `skill.zip`
- Upload to destination workspace
