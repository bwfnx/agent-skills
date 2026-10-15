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

## Public repo rules

### README: sell it in 5 seconds
For SBDC repos, build the README with the `sbdc-repo-readme` skill (`skills/sbdc-repo-readme/`); [bwfnx/sbdc-toolkit](https://github.com/bwfnx/sbdc-toolkit) is the reference. The rules it follows:
1. **One-line promise at the very top.** The banner carries it, and the H1 repeats it under the hero. Plain words, not the tech.
2. **Hero image right under the banner.** A before/after of a real output with fictional data, not a diagram or logo.
3. **Install one click away.** An "Install" link in the top nav row; the full steps sit lower, one folded `<details>` per platform.
4. **Everything else after.** Highlights, catalog, FAQ, notes, license.

### SBDC and client-work repos
5. **No real client data in screenshots, examples, or test files.** Use a fictional business (made-up name, numbers, and location) for the hero image and every sample. Check names, emails, dollar figures, and Neoserra IDs before committing.

### Where repos live
6. **GitHub is the source of truth** for anything public. Edit there, or in a clone, never in a loose copy.
7. **Clone each repo into the Playground workstation it belongs to** (e.g., `sbdc-advising\outputs\<repo>\`), never the Playground root.
8. **Git-ignore the clone in the Playground** by adding `<workstation>/outputs/<repo>/` to the Playground's `.gitignore`, so the two repos don't collide.

### Before going public
9. **Add a license** (MIT for code and skills, CC BY 4.0 for written content).
10. **Add GitHub topic tags** so people can find it (e.g., `claude-skills`, `agent-skills`, `small-business`).
