# Release Workflow

Use this process whenever you update or publish a skill.

## Core principle
The source in `skills/<skill-slug>/` is always the master copy.
A packaged `skill.zip` is a deployment artifact, not the source of truth.

## Recommended release sequence

### 1. Update the source
Edit the canonical skill folder:
- `skills/<skill-slug>/SKILL.md`
- `skills/<skill-slug>/agents/openai.yaml`
- `skills/<skill-slug>/README.md`
- `skills/<skill-slug>/CHANGELOG.md`
- any `scripts/`, `references/`, or `assets/` files

### 2. Test with a real example
Run at least one realistic input through the skill workflow.
Examples:
- transcript upload
- pasted text
- a representative consultant prompt

Document:
- what was tested
- what worked
- what still needs improvement

### 3. Decide version bump
Suggested rule:
- `v1.0` initial release
- `v1.1` small improvements, wording changes, minor fixes
- `v1.2` added references, helper scripts, or output improvements
- `v2.0` major workflow, structure, or trigger changes

### 4. Update changelog
In `skills/<skill-slug>/CHANGELOG.md`:
- add the new version heading
- summarize what changed
- keep the newest version at the top

### 5. Update the inventory files
Update these files when relevant:
- `skills/manifest.json`
- `SKILLS_INDEX.md`

Recommended fields to keep current:
- version
- status
- owner
- target workspaces
- whether packaged zip has been generated
- whether approved for sharing

### 6. Create release note
Create a release note from:
- `templates/RELEASE_NOTE_TEMPLATE.md`

Suggested location:
- `releases/<skill-slug>-vX.Y.md`

### 7. Package the skill
Generate a fresh `skill.zip` from the canonical skill folder.

Recommended packaging rule:
- package only the contents of `skills/<skill-slug>/`
- keep the output file named exactly `skill.zip`
- do not package from legacy or duplicate folders outside `skills/`

### 8. Deploy
Typical deployment path:
- upload `skill.zip` to personal workspace for final sanity check
- upload `skill.zip` to UMD / enterprise workspace
- share with the intended consultant group once approved

### 9. Mark release status
After deployment, update:
- `skills/manifest.json`
- release note file

Change fields as needed:
- `packaged_zip_generated`
- `approved_for_sharing`
- release date
- deployment notes

## Approval guidance
Suggested practical statuses:
- `draft` - under active development
- `active` - working canonical version
- `pilot` - being tested by a small group
- `approved` - ready for broader sharing
- `deprecated` - do not use for new deployments

## Personal to UMD workflow
Recommended operating model:
1. Build and refine in personal workspace/repo flow
2. Keep GitHub as the long-term source of truth
3. Release tested versions into the UMD workspace
4. Collect colleague feedback
5. Revise the canonical skill source
6. Publish a new release

## Important housekeeping rule
If a skill exists both inside and outside `skills/`, only the copy inside `skills/` is canonical.
Legacy copies should be ignored or removed when practical.
