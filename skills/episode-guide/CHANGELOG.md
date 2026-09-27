# Changelog

## v1.5
- added a lessons-from-testing section: pull tables verbatim, reread notes against the data before publishing, test rule changes on a deliberately different show

## v1.4
- when parent guides rate only the whole show, report the show-level age in a family note and leave episodes unmarked instead of guessing
- new optional input for entries already watched: marked as seen, and paths start at the first unseen entry
- tested on mythbusters (show-level 9+ only) and the star wars films for a 6-year-old who has seen episodes iv and v

## v1.3
- added an optional family flag for watching with kids: kid pick, not for this age, or unmarked, calibrated to the child's age
- family flag is separate from quality tiers; god mode episodes still get a not-for-this-age warning when needed
- added a family path output and parent-guide sources (common sense media, imdb parents guide)
- tested on star trek: the next generation for a 6-year-old

## v1.2
- series best must be a regular episode; retrospective and reunion specials can be fan favorites but not the top pick
- clip shows that reuse aired footage are skippable by default
- exception: clip-show parodies made of new material are tiered like normal episodes
- tested on mythbusters (docuseries, calendar-year seasons)

## v1.1
- long-series mode now branches on show type: serialized shows get an arc-only path, episodic shows (sitcoms, procedurals, docuseries) get a best-of path
- multi-part episodes that aired as one block count as a single entry with a code range
- added a rule for sources that disagree on season or episode numbering
- tested on 30 rock (7 seasons, 138 episodes)

## v1.0
- initial release: tiered season-by-season episode guide for tv, podcasts, and movie franchises
- tiers: series best, god mode, fan favorite, core arc, skim, skippable
- separate arc flag so fan favorites and god mode episodes the story needs stay on the arc-only path
- added skim tier for weak episodes that contain a key scene
- added a source fallback order for when reddit, fandom, or imdb pages are blocked
- long-series mode with an arc-only path and hours saved
- tested on supernatural (15 seasons, 327 episodes)
