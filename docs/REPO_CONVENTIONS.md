# Repository Conventions

This repo is the source-of-truth library for reusable ChatGPT Skills.

## Top-level structure
- `skills/` - editable source for each skill
- `docs/` - maintenance and release documentation
- `templates/` - starter files for future skills
- `releases/` - optional release notes and packaged artifacts

## Skill folder standard
Each skill should live in:

`skills/<skill-slug>/`

Recommended contents:
- `SKILL.md`
- `agents/openai.yaml`
- `README.md`
- `CHANGELOG.md`
- `scripts/` when deterministic code is useful
- `references/` when guidance is too large for `SKILL.md`
- `assets/` only when truly needed

## Naming rules
- Folder names: lowercase, hyphenated
- `SKILL.md` frontmatter `name`: lowercase
- `SKILL.md` frontmatter `description`: lowercase
- `agents/openai.yaml` display name: human-readable title case

## Release flow
1. Edit the source files in `skills/<skill-slug>/`
2. Test with a real prompt/file
3. Update `CHANGELOG.md`
4. Package `skill.zip`
5. Upload the release into the target workspace

## Versioning guidance
Use simple semantic-style tags inside each skill changelog:
- `v1.0` initial release
- `v1.1` small improvements
- `v2.0` major workflow changes

## Practical rule
Never treat a packaged zip as the master copy.
The repo source is the master. The zip is the deployable artifact.
