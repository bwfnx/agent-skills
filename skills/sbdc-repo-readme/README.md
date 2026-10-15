# SBDC Repo README

Version: v1.0

## Purpose

Gives every SBDC-related repo the same polished front page as [bwfnx/sbdc-toolkit](https://github.com/bwfnx/sbdc-toolkit): a navy Maryland SBDC banner, a before/after hero of the star tool, a three-tool highlights strip, a grouped catalog linked to guides, folded install steps, and a short FAQ. Light and dark images come from HTML, so they can be rebuilt any time.

## Typical inputs

- a repo (new or existing) with its tools, guides, and current README
- which tool is the star, and any public claims Brandon has cleared

## Typical outputs

- `README.md` in the house layout
- `docs/img/banner.png`, `hero-light/dark.png`, `highlights-light/dark.png`
- `docs/img/src/` with the HTML sources, fonts, and `render.py`
- a pull request ready for Brandon's review

## What's inside

| Path | What it is |
|---|---|
| `SKILL.md` | The workflow and rules |
| `references/readme-template.md` | README skeleton with placeholders |
| `assets/readme-kit/` | Image sources (worked example: Harbor Lane Bakery), tokens, fonts, render script |
| `scripts/check_readme.py` | Fails on missing images/files or guide links with no page (`--self-test` included) |
