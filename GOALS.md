# Connor's Second Brain — Goals (north-star cascade)

> North star: every thought Connor captures, every recurring process he's never written down, and every half-built project he starts — becomes routed, structured, actioned data automatically, so brilliant ideas, brilliant processes, and brilliant code all turn into shipped, monetized work instead of dust.
> Source: VISION.md (v10) · _Last updated: 2026-08-11 · Plan version: v5_

## Milestones — hit in order, no circling back

| # | Milestone | Done when | Status |
|---|---|---|---|
| M1 | Credentials complete | Telegram token + user id + Twilio token in hand (Deepgram already done) | 1/4 |
| M2 | Engine deployed | Goal 1 done — hetznerCO live, bot verified, vault write confirmed, watchdog verified | blocked on M1 |
| M3 | First real loop closed | Goals 2+3 done — a real RightNote voice note becomes a Todoist task, end to end, zero manual steps | blocked on M2 |
| M4 | Multi-channel capture | Goal 4 done — SMS + email also feed the same loop | blocked on M1 (Twilio) |
| M5 | Intelligence layer | Goal 5 done — portfolio scan + workflow audit surface a real finding | blocked on M3 |

**Rule:** a milestone is binary — done or not, no partial credit. Once M1's three architecture decisions (hosting, vault-sync mechanism, engine choice) were locked 2026-08-09, they don't get re-opened without new evidence, not just second-guessing — that flip-flop already cost three docs revisions and is the reason this table exists.

## Alignment anchors (every goal must serve these)

**Pillars:**
- One engine, not three — all capture channels feed one memory/action system
- The vault (Deriv8) is the source of truth
- Interactive session, not headless billing — no `claude -p` in the hot path
- Actionable never just decays — anything actionable reaches Todoist, not just the vault
- Local-first where it matters
- Reuse before rebuild — Todoist stays the task system of record for now
- Autonomous building is opt-in, throttled, never silent
- Untrusted channels (SMS, email) are allow-listed, not open
- This vision is not exempt from its own thesis — no more scope until Now ships

**Non-goals (out of scope now):** RightNote video/text/handwritten capture modes; a full custom task-management system replacing Todoist; Filer-parity features (trust tiers, delegation, chat panel, MCP registry); pulling `myvoice` into this pipeline; the Idle-Capacity Idea Executor (needs its own confirmation pass before any code is written).

**MVP boundary (Now):** Deploy agent-second-brain on `hetznerCO` (settled after a whiteboard discussion on hosting risk). Bridge RightNote's existing voice notes into its ingestion pipeline. Build the triage → Todoist dispatch bridge.

## Goals

### Goal 1 — The engine is live and reachable 24/7  ·  serves: local-first / one-engine-not-three / reuse-before-rebuild
**Done when:** agent-second-brain is deployed on `hetznerCO`, the Telegram bot responds to a real message, a test card writes correctly into the Deriv8 vault, and the watchdog recovers from a killed session without manual intervention.
**Status:** blocked (1a/1c need TELEGRAM_BOT_TOKEN + ALLOWED_USER_IDS; DEEPGRAM_API_KEY done 2026-08-10, verified working, in .env; hosting + sync mechanism resolved)
**Sub-goals:**
- [ ] **1a** Bootstrap agent-second-brain on `hetznerCO` (systemd services from upstream `deploy/`) — _advances:_ gets the persistent session actually running somewhere always-on — _accept:_ `systemctl status` green for bot/watchdog/cron services — **BLOCKED, waiting on Connor for: (1) Telegram bot token via @BotFather, (2) Connor's Telegram user id — both scriptable via `scripts/telegram_bootstrap.py`, needs TG_API_ID/TG_API_HASH from my.telegram.org**
- [ ] **1e** Vault sync: git-init `~/Deriv8`, push to a private repo, `hetznerCO` clones/commits scoped append-only writes, event-triggered pull job locally (resolved via whiteboard discussion 2026-08-09) — _advances:_ unblocks 1a — _accept:_ a round-trip write verified both directions with no conflict on a shared file
- [ ] **1b** Verify `autograph` card output renders correctly in Deriv8's Logseq-based (block-oriented) model, not just Obsidian's (file-oriented) — _advances:_ closes the compatibility gap the vision flagged but didn't verify — _accept:_ a real card written by autograph opens correctly in Deriv8
- [ ] **1c** End-to-end Telegram test: send a real voice note, confirm it becomes a typed card in the vault — _advances:_ proves the already-built half of the loop actually works post-deploy — _accept:_ card appears with correct type/content within the expected processing window
- [ ] **1d** Kill the session, confirm the watchdog restarts it unattended — _advances:_ proves the self-healing claim, not just trusts it — _accept:_ session back up within upstream's documented recovery window

### Goal 2 — RightNote's voice notes flow into the same brain  ·  serves: one-engine-not-three
**Done when:** a voice note recorded in RightNote appears as a typed vault card without Connor doing anything beyond recording it.
**Status:** todo
**Sub-goals:**
- [ ] **2a** Confirm agent-second-brain's ingestion pipeline (`src/d_brain/pipeline.py`) has a usable seam for local-file injection, not just Telegram webhooks — _advances:_ resolves the pressure-test's flagged unverified assumption before building on top of it — _accept:_ a documented integration point (function/queue/directory) identified and tested with a dummy file
- [ ] **2b** Build the local capture bridge: watch RightNote's `~/Library/Application Support/RightNote/Voice Notes`, feed new `.m4a` files through that seam — _advances:_ the actual missing piece — _accept:_ a file dropped in the folder reaches the pipeline within the watcher's poll interval
- [ ] **2c** Port `smartfolder-Genius`'s `AudioContentProvider` logic where useful for local transcription/metadata — _advances:_ reuse over rebuild — _accept:_ no duplicate transcription logic written from scratch
- [ ] **2d** End-to-end test with a real RightNote recording, start to finish — _advances:_ the demo-able proof — _accept:_ Connor records a real note and finds the resulting card in the vault

### Goal 3 — Actionable captures become real Todoist tasks  ·  serves: actionable-never-just-decays
**Done when:** something autograph classifies as actionable produces a real, correctly-projected Todoist task without Connor filing it by hand.
**Status:** todo
**Sub-goals:**
- [ ] **3a** Add the `triage state` field to autograph's card schema (`untriaged` → `actionable` → `dispatched-to-todoist` / `reference-only`) — _advances:_ makes "actionable" a checkable state, not an inference — _accept:_ field present and set correctly on new cards
- [ ] **3b** Build the dispatch bridge: actionable card → well-formed Todoist task via the existing `todoist` skill (project auto-resolved) — _advances:_ the core "never decays" guarantee — _accept:_ a real actionable capture produces a task in the right project
- [ ] **3c** End-to-end test: capture something actionable via Telegram, confirm the task lands correctly — _advances:_ proves the full Now loop closes — _accept:_ task visible in Todoist within the expected processing window

### Goal 4 — Capture works from anywhere, not just Telegram/RightNote  ·  serves: the-specific-gap-named ("thought while walking, phone in pocket") / untrusted-channels-allow-listed
**Done when:** texting the Twilio number or labeling a Gmail thread produces the same vault card Telegram/RightNote would.
**Status:** blocked (4a needs Connor's Twilio console credentials)
**Sub-goals:**
- [ ] **4a** Finish Twilio CLI login (Account SID + Auth Token from console.twilio.com) and provision the number — _advances:_ unblocks everything else in this goal — _accept:_ `twilio profiles:list` shows a working, authenticated profile — **BLOCKED, waiting on Connor**
- [ ] **4b** SMS webhook → ingestion bridge, sender allow-listed to Connor's own number only — _advances:_ closes the real gap named, safely — _accept:_ a text from Connor's number ingests; a text from any other number is silently dropped
- [ ] **4c** Gmail label-scan bridge, allow-listed to the capture label only, never the full inbox — _advances:_ solves the stated noise problem — _accept:_ only labeled threads ingest; unlabeled mail is untouched

### Goal 5 — Dormant projects and unwritten workflows get surfaced, not just thoughts  ·  serves: half-built-projects-shipped-monetized / recurring-processes-never-written-down
**Done when:** a scan names at least one real dormant project with a monetization angle, and the Workflow Audit has produced at least one real `skill-creator` skill from a described process.
**Status:** todo
**Sub-goals:**
- [ ] **5a** Portfolio Intelligence Scanner: walk `~/Developer` + `gh repo list connorodea` + Todoist projects, add the `Project` card type, surface dormancy + connections — _advances:_ the project-level counterpart to note capture — _accept:_ scanner output includes at least one project Connor confirms is genuinely dormant-but-valuable
- [ ] **5b** Monetization/distribution ideation pass on surfaced projects, favoring unconventional angles — _advances:_ turns "dormant" into "here's how to ship it" — _accept:_ at least one idea per surfaced project that isn't the default "add a paywall"
- [ ] **5c** Workflow Audit interview prompt + Clone-Score table (repeatability × judgment-required) — _advances:_ the third discovery source the vision names — _accept:_ a completed audit table for at least one real recurring workflow (e.g. the BD/sponsor-style pipeline pattern)
- [ ] **5d** Skill-authoring bridge: high-scoring workflow → real skill via `skill-creator` — _advances:_ closes the loop from "described process" to "reusable automation" — _accept:_ at least one real, working skill produced this way

## Loop — Idea backlog stays triaged, not a landfill
**Serves:** actionable-never-just-decays / the vision's own anti-sprawl thesis
Runs once Goal 1–3 are live; folds in Goal 4/5 sources as they come online.
- **Each cycle:** the existing nightly processor (21:00) reviews cards still in `untriaged` state.
- **Pick next by:** oldest untriaged first, salience-weighted (highlight/circle/star-derived score where available).
- **Ship:** re-classify or dispatch each one — actionable → Todoist, reference → stays in vault at its decay tier, still-unclear → stays `untriaged` but flagged in the daily report so it doesn't silently persist forever.
- **Stop/exit:** never stops (ongoing); this loop *is* the mechanism that prevents the six-months-later-rediscovery failure mode named in the vision.

## Sequencing

- **Now:** Goals 1, 2, 3 — deploy, bridge RightNote, close the triage-to-Todoist loop. Nothing else starts until these are demonstrably live (per the vision's own anti-sprawl rule).
- **Next:** Goal 4 (capture channels — 4a blocked on Connor), Goal 5 (portfolio + workflow audit).
- **Later (not yet goals, named in VISION.md only):** Idle-Capacity Idea Executor (needs explicit separate go-ahead), a full custom task-management system replacing Todoist, the self-contained HTML visual workflow map, Filer-parity platform features, the AMANI/ELOHIME/SUPERGLUU ecosystem flywheel.

## Drift watch

None currently — every active goal traces to a named pillar, and nothing in flight falls outside the stated MVP boundary. (Worth re-checking here specifically, since the vision doc itself already drifted once this session before the pressure-test caught it.)

## Runnable prompts

```text
/goal Goal 1: The engine is live and reachable 24/7
Serves vision pillar: local-first / one-engine-not-three / reuse-before-rebuild.
Done when: agent-second-brain deployed on hetznerCO, Telegram bot verified end-to-end,
a test card confirmed in the Deriv8 vault, watchdog recovery verified by killing the session.
Vault sync (1e) is resolved: git-sync, scoped append-only writes, event-triggered pull.
Blocked on: Telegram bot token + Connor's Telegram user id + a Deepgram API key.
Confirm all three exist before starting 1a.
Non-goals: don't build RightNote/SMS/email bridges here — that's Goals 2 and 4.
Read GOALS.md + VISION.md first. Report what shipped + what's left.
```

```text
/goal Goal 2: RightNote's voice notes flow into the same brain
Serves vision pillar: one-engine-not-three.
Done when: a voice note recorded in RightNote appears as a typed vault card with no
manual steps. First confirm the actual integration seam in
src/d_brain/pipeline.py exists before building the bridge around it.
Non-goals: don't add video/text/handwritten capture here — RightNote voice only, for now.
Read GOALS.md + VISION.md first. Report what shipped + what's left.
```

```text
/goal Goal 3: Actionable captures become real Todoist tasks
Serves vision pillar: actionable-never-just-decays.
Done when: an autograph card classified as actionable produces a real, correctly-projected
Todoist task via the existing todoist skill, with no manual filing.
Non-goals: don't build a custom task system — that's explicitly Later.
Read GOALS.md + VISION.md first. Report what shipped + what's left.
```

```text
/goal Goal 4: Capture works from anywhere
Serves vision pillar: untrusted-channels-allow-listed.
Done when: SMS (Twilio, allow-listed to Connor's number) and email (Gmail label, never
full inbox) both ingest into the same pipeline as Telegram/RightNote.
Blocked on 4a: Twilio Account SID + Auth Token from Connor. Do not build 4b/4c's allow-list
logic assuming credentials that don't exist yet — confirm 4a is actually done first.
Read GOALS.md + VISION.md first. Report what shipped + what's left.
```

```text
/goal Goal 5: Dormant projects and unwritten workflows get surfaced
Serves vision pillar: half-built-projects-shipped-monetized / recurring-processes-never-written-down.
Done when: the Portfolio Intelligence Scanner names a real dormant project with a
monetization angle, and the Workflow Audit has produced one real skill-creator skill.
Non-goals: don't build the Idle-Capacity Executor here — surfacing and ideation only,
not autonomous execution. That needs its own separate confirmation per VISION.md.
Read GOALS.md + VISION.md first. Report what shipped + what's left.
```

```text
/loop Idea backlog — iterate
Each cycle: re-read GOALS.md + VISION.md, check the nightly processor's untriaged-card
list, dispatch or re-classify each by the rule in the Loop section above, check every
action against the actionable-never-just-decays pillar, report, continue.
Stop when: never — this is the ongoing anti-decay mechanism. Don't repeat completed work;
skip cards already triaged this cycle.
```

## Changelog
- 2026-08-11 v5 — Added a Milestones table (M1-M5, sequential, binary done/not-done) so progress is trackable without re-deriving it from goal prose each time. Codified the "locked decisions don't reopen without new evidence" rule explicitly, after the hetznerCO→hetznerLR→hetznerCO flip-flop cost three docs revisions.
- 2026-08-10 v4 — DEEPGRAM_API_KEY resolved: CLI login had dead/under-scoped keys twice (a stale keyring key, then a device-flow session missing keys:write), worked around via a console-generated key, verified live against the API, stored in `agent-second-brain/.env` (gitignored). Goal 1's remaining blockers are now just the Telegram bot token and Connor's user id.
- 2026-08-09 v3 — Hosting corrected again: hetznerLR → hetznerCO, after a four-perspective whiteboard discussion flagged blast-radius risk to Lock Rooms' production traffic. Vault-sync mechanism resolved (git-sync, scoped append-only writes, event-triggered pull) — both whiteboard perspectives converged on this shape independently. Goal 1's remaining blockers are now just the three missing credentials.
- 2026-08-09 v2 — Corrected deployment target hetznerCO → hetznerLR (Connor's direct correction). Added sub-goal 1e (vault-sync mechanism, still open) and named Goal 1's other real blockers explicitly: Telegram bot token, Connor's Telegram user id, a Deepgram API key — none of which exist yet.
- 2026-08-08 v1 — Initial cascade from VISION.md v8. Five goals (three Now, two Next) plus one ongoing loop. Goal 4 flagged blocked pending Connor's Twilio credentials.
