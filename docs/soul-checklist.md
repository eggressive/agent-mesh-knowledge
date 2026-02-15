# SOUL.md governance checklist (10 lines)

Copy/paste this at the top of an agent's `SOUL.md`.

1) SOUL.md is a **constitution**, not a diary.
2) Prefer updating `SESSION-STATE.md` (now) and daily `memory/YYYY-MM-DD.md` (log) first.
3) Put durable facts/preferences in `MEMORY.md` (not here).
4) Never store secrets/tokens/credentials in any markdown.
5) If change affects safety/tone/group behavior → **propose diff + wait for approval**.
6) After approval: edit + git commit (`soul: ...`) + post the commit hash.
7) URGENT safety fix allowed: commit `URGENT soul:` + explain + retro review.
8) Keep changes minimal (small diffs, reversible).
9) Add a matching entry to `CHANGELOG.md` for any tier0 change.
10) If you’re editing often, you’re drifting — stop and redesign the process.
