# Connor's Second Brain — Vision

> One-sentence north star: every thought Connor captures — spoken, typed, filmed, photographed, or handwritten — and every half-built project he starts, becomes routed, structured, actioned data automatically, so brilliant ideas and brilliant code both turn into shipped, monetized work instead of dust.

_Last updated: 2026-08-07 · Version: v4_

## What it is

A single, always-on personal capture-and-action engine, built on **agent-second-brain** (forked from `smixs/agent-second-brain`): one persistent Claude Code session that reads everything Connor sends it — voice, photos, documents, video, forwarded posts — and files it into a typed knowledge graph (`autograph`) in an Obsidian vault, with Ebbinghaus-decay memory tiers, self-scheduled reminders, nightly processing, and a self-healing watchdog. Capture happens two ways: **Telegram** (already built, works today) and **RightNote** (Connor's native macOS menu-bar recorder — voice today, video/text/handwritten-photo next), both feeding the same engine. A new **inbox/triage layer** sits between capture and action: it guarantees that anything actionable graduates into a real, executable Todoist task instead of quietly aging in the vault.

This consolidates four scattered efforts that were solving the same problem independently: `RightNote` (native capture, built 2026-08-06), `smartfolder-Genius` (a forked folder-watching engine, built 2026-08-06), `agent-second-brain` (a mature, already-working second brain, forked 2026-07-16 and never deployed), and the original ask that started this session (a "voice notes daemon"). `agent-second-brain` is the most complete of the four and becomes the core engine; the others contribute capture surfaces and reusable parts rather than competing as separate live systems.

## Who it's for

Connor alone, running many concurrent projects (aiwholesail, Renovo, Reelwire, Lock Rooms, TradingAgents, Deriv8, opencut-fork, and more), who generates ideas faster than he can file them. The specific failure mode this exists to kill: recording a genius idea, never processing it, and rediscovering it six months later — brilliant and wasted.

## The problem

Capture is cheap; everything after capture is the bottleneck — and this shows up twice in Connor's life. First, at the thought level: voice memos never get re-listened to, typed fragments drown in chat history, nothing closes the loop from "I said/wrote/photographed a thought" to "there is now a task that represents it." Three separate half-built attempts at fixing this (RightNote, smartfolder-Genius, and a never-deployed agent-second-brain fork) existed simultaneously without Connor realizing it. Second, at the project level: the same pattern one layer up — Connor starts building a genuinely good idea, gets pulled toward the next genuinely good idea before shipping it, and ends up with a `~/Developer` and a GitHub account full of brilliant, dormant, zero-to-one-but-never-launched projects (this session alone surfaced four: RightNote, smartfolder-Genius, agent-second-brain, and the ELOHIME/OpenSource-Ai-Glasses/screenrec-studio/sonyobs/pipecat-adjacent scatter). Todoist itself has accumulated project after project the same way. Nothing today surfaces "this is 80% done and worth finishing" or "these two dormant projects actually solve the same problem" or "here's a way to make money from what you already built."

## Core value proposition

Say it, type it, film it, or photograph it — it becomes typed, linked knowledge automatically, and anything actionable becomes a real task you'll actually see. And the same engine watches Connor's own project portfolio (code + Todoist) the same way it watches his thoughts: surfacing dormant-but-valuable projects, connecting related ones, and proposing how to ship and monetize them — without Connor doing the filing, the archaeology, or the go-to-market thinking himself.

## Principles / non-negotiables

- **One engine, not three.** All capture channels feed one memory/action system. No parallel "second brain" implementations running at once.
- **The vault is the source of truth.** Everything lands as plain markdown Connor can read and keep forever, independent of any agent still existing.
- **Interactive session, not headless billing.** Per agent-second-brain's existing v3.0 design: one long-lived Claude Code session, no headless `claude -p` in the hot path — runs on the subscription Connor already pays for, not per-token API bills.
- **Actionable never just decays.** Memory-tier decay is fine for reference material; anything the triage layer classifies as actionable must reach Todoist (or its eventual replacement), not just wait to be randomly resurfaced.
- **Local-first where it matters.** RightNote's captures don't require Telegram as a relay; raw audio/video handling follows RightNote's existing "no upload, no account" stance where practical.
- **Reuse before rebuild.** Todoist (via the existing `todoist` skill) stays the task system of record for now — see MVP boundary. Don't rebuild what already works until the reason to replace it is concrete.
- **Autonomous building is opt-in and throttled, never silent.** The Idle-Capacity Idea Executor may only act when Connor's own Claude Code/Codex usage is genuinely low, must be visible (notified, logged, revertable — new work lands as a branch/PR like everything else in this workflow), and requires its own explicit go-ahead before it's ever wired up, independent of this vision doc capturing the intent.

## Main workflows

1. **Telegram capture → autograph → vault.** Already built and working (upstream v3.0.3): voice/photo/doc/video/forwarded-post → typed card → linked into the graph.
2. **RightNote capture → autograph → vault.** New: bridge RightNote's local `.m4a` output (and later video/text/handwritten-photo) into the same ingestion pipeline Telegram uses today, instead of building a second memory system.
3. **Handwritten note capture.** Confirmed real, not hypothetical: Connor keeps a physical Cornell-style daily notebook (dated pages, cue column, to-do box, highlighter + circles + star marks used inline to flag the ideas he considers strongest). Photo taken on phone → either AirDropped to a watched local folder (local-first, needs a small new bridge) or forwarded to the Telegram bot directly (works today, zero build) → OCR/vision-read, **treating highlight/circle/star marks as an explicit salience signal** the extraction weighs, not just plain transcription → filed like any other photo, plus a recurring backfill pass over past notebook pages already photographed.
4. **Actionable triage → Todoist.** New: after autograph classifies a card, anything actionable is transformed into a well-formed Todoist task via the existing `todoist` skill (project auto-resolved), instead of only living in the vault waiting to be found.
5. **Self-managed reminders and nightly processing.** Already built: plain-language cron ("remind me Friday at 3pm"), a 21:00 daily classification/report pass, self-healing watchdog.
6. **Project portfolio scan → synthesis → ship reminders.** New: a periodic scan across `~/Developer`, Connor's GitHub account, and his Todoist projects, filed into the same graph as a `Project` entity type. Surfaces dormancy ("last touched 3 weeks ago, looked 80% done"), cross-project connections ("these three projects solve overlapping problems"), and reminders to revive/ship — using the same self-scheduled cron already built for #5, not a new scheduler.
7. **Monetization/distribution ideation.** New: for each surfaced project, the engine proposes unconventional ways to ship, distribute, and monetize it — favoring creative angles over the obvious "SaaS + Stripe" default — and files the ideas as linked cards against that project, not as a one-off chat answer that evaporates.
8. **Idle-capacity idea execution.** New, and the highest-leverage/highest-risk piece: when Connor isn't actively driving Claude Code or Codex, the vault is "self-propagating" — it pulls the next highest-salience queued idea (from note extraction or the portfolio scanner) and turns it into an actual build session, using the existing `autonomous` skill. Backs off automatically once Connor's own usage crosses a threshold, so it never competes with active work. This is a distinct, later capability from everything else here — see Principles and Open Questions.

## System modules

- **agent-second-brain engine** (`~/Developer/agent-second-brain`) — the core: Telegram bot, persistent Claude Code session driver, `autograph` memory engine, cron/reminders, nightly processor, watchdog. Mature, untouched fork, not yet deployed.
- **RightNote** (`~/Developer/RightNote`) — native macOS capture surface. Today: voice only. Next: video, text, handwritten-photo ingestion. Feeds the engine instead of running its own processing.
- **Local capture bridge (new)** — the piece that doesn't exist yet: gets RightNote's local files into agent-second-brain's ingestion pipeline. Likely a lightweight watcher plus reuse of `smartfolder-Genius`'s modality-aware content providers (audio/video/image/PDF, already written upstream) rather than writing extraction from scratch.
- **Inbox/triage → Todoist bridge (new)** — the other missing piece: turns "actionable" autograph cards into real Todoist tasks via the existing `todoist` skill.
- **smartfolder-Genius** (`~/Developer/smartfolder-Genius`) — demoted to parts donor. Its content-provider code is worth porting into the local capture bridge; it does not run as its own live engine. Its Filer-inspired "assign an agent to any folder" idea is preserved as a Later bet, not built now.
- **myvoice** (`~/Developer/myvoice`) — explicitly out of scope. Different job (real-time dictation into text fields, not async capture-and-file). Left alone.
- **Portfolio Intelligence Scanner (new)** — the project-level counterpart to capture ingestion: walks `~/Developer` + `gh repo list connorodea` + Todoist projects, extracts state (last activity, apparent completeness, description), and hands it to the same nightly-processing/autograph pipeline that already classifies notes — reusing infrastructure rather than building a second brain for projects.
- **Idle-Capacity Idea Executor (new, Later)** — watches whether Connor is actively using Claude Code/Codex; below a usage threshold, dequeues the highest-salience backlog item and hands it to the `autonomous` skill to actually build. This is unattended code-writing triggered by idle detection rather than a direct request — it needs its own explicit design/confirmation pass before being built, not just a vision-doc mention (see Open Questions).

## Data model implications

- `autograph`'s existing typed-card schema (note/contact/project/CRM, five decay tiers) is the memory model — not rebuilt.
- New: a **triage state** on cards (`untriaged` → `actionable` → `dispatched-to-todoist` / `reference-only`) so nothing actionable silently stays untriaged.
- New: a **capture-source** field so cards know whether they came from Telegram or RightNote (useful once RightNote grows more input modes).
- New: a **`Project` card type** — repo path/URL, last-activity date, dormancy score, related-projects links, and a list of monetization/distribution ideas — added to the same graph `autograph` already maintains for notes/contacts.

## UI/UX implications

- Telegram stays the primary chat interface (already built).
- RightNote stays a minimal menu-bar recorder — no processing UI added there.
- No new UI required for the MVP; the "you'll see it in Todoist" loop is the actionable-item UX.

## MVP boundary

**In:** Deploy agent-second-brain for real (currently forked but never run). Bridge RightNote's existing voice notes into its ingestion pipeline. Build the triage → Todoist dispatch bridge so actionable captures reliably become tasks.

**Out (for now):** RightNote video/text/handwritten-photo capture modes; a full custom task-management system replacing Todoist; Filer-parity features (trust tiers, folder delegation, chat panel, MCP plugin registry) inherited from smartfolder-Genius's original scope; pulling myvoice into this pipeline; the Portfolio Intelligence Scanner (real, wanted soon, but not part of proving the core capture→triage loop first); the Idle-Capacity Idea Executor (needs its own confirmation pass before any code is written for it).

## Roadmap (vision → milestones)

- **Now:** Get agent-second-brain actually running (bootstrap + Telegram bot + vault), bridge RightNote's voice notes in as a second capture channel, ship the triage → Todoist dispatch bridge. This is the whole original ask, done properly instead of three separate half-builds.
- **Next:** Three tracks, roughly in parallel once Now is proven: (a) RightNote grows video/text/handwritten-photo capture (porting smartfolder-Genius's content providers for local ingestion), including the daily-notebook OCR pass with highlight-salience weighting, refine triage confidence-gating; (b) the **Portfolio Intelligence Scanner** — scan `~/Developer` + GitHub + Todoist, surface dormant/connected projects, generate ship-reminders and monetization ideas; (c) a plain **idea backlog** (queued, salience-ranked, from both notes and the portfolio scanner) as the prerequisite for Later's executor. (a) and (b) are called out as high-priority within Next given how acutely Connor feels this specific pain.
- **Later:** Per Connor's explicit direction — **build a fully custom task-management system that replaces Todoist entirely**, native to this engine instead of bridging out to Todoist's API. The **Idle-Capacity Idea Executor** — autonomous building during genuinely idle time, throttled against active usage — once the backlog and portfolio scanner are proven and Connor has explicitly signed off on wiring up unattended builds. Also later: Filer-parity general "any folder gets an agent" features, revisited as their own vision if still wanted once the core loop is proven.

## How to decompose this

Run `/northstar` against this doc to produce `GOALS.md`: goals should track the roadmap milestones above (Deploy the Engine → RightNote Bridge → Triage-to-Todoist → Multi-Modal Capture → Portfolio Intelligence Scanner → Idea Backlog → Idle-Capacity Executor → Custom Task System). Track execution in a new Todoist project once the goal structure exists.

## Open questions

- **Vault destination:** agent-second-brain defaults to Obsidian. Connor also has `Deriv8`, his own AI-agent-controllable PKM fork, with its own vision/goals already in flight. Recommendation: keep Obsidian for the MVP since `autograph` is built specifically for it; revisit a Deriv8 integration later rather than disrupting two projects' roadmaps at once.
- **Deployment target:** upstream agent-second-brain assumes a cheap VPS (systemd services included). Connor has `hetznerCO` already provisioned with an established CI/CD pattern. Recommendation: deploy there when ready, rather than running only on the Mac — but this hasn't been confirmed.
- **Handwritten-note path:** AirDrop-to-local-folder (consistent with RightNote's local-first stance, needs a small new bridge) vs. forward-to-Telegram-bot (works today, zero build, but leaves the local-first principle). Recommendation: start with the Telegram fallback now, build the local bridge when RightNote's other capture modes are built anyway.
- **Portfolio scan scope:** this session found relevant projects in `~/Developer`, `~/Documents/Codex` outputs, and `gh repo list connorodea` — but not, say, other machines or private gists. Recommendation: start with those three sources; widen only if it misses something real.
- **Monetization ideation tone:** Connor explicitly wants unconventional distribution/monetization angles, not default "add a paywall" thinking. Worth a dedicated prompt/rubric once this module is actually designed, rather than leaving it to per-run improvisation.
- **Idle-detection threshold:** what actually counts as "not using Claude Code/Codex aggressively" — no active session in the last N minutes? CPU/API-usage below some rate? Needs a concrete definition before the Idle-Capacity Executor can be built, plus explicit confirmation that unattended builds are wanted at all before that threshold logic ever runs.
- **Notebook backfill scope:** Connor's daily notebook has pages before 2026-08-07 already written. Does the backfill pass cover the whole physical notebook (needs every page photographed first) or only pages from today forward?

## Changelog

- 2026-08-07 v4 — Grounded handwritten-note capture in a real example (dated Cornell-style daily notebook, highlight/circle/star marks as a salience signal) and added the Idle-Capacity Idea Executor: a "self-propagating vault" that turns queued backlog ideas into actual `autonomous`-skill build sessions during genuinely idle time, throttled against active usage. Flagged as needing its own explicit confirmation before implementation, not authorized by this vision doc alone.
- 2026-08-07 v3 — Added the Project Portfolio Intelligence dimension: scanning `~/Developer` + GitHub + Todoist for dormant/connected projects, with ship-reminders and monetization/distribution ideation, reusing the same engine and nightly-processing infrastructure as note capture. Placed as high-priority Next, not Now, to keep the MVP boundary honest.
- 2026-08-07 v2 — Consolidated three previously-independent efforts (RightNote, smartfolder-Genius, and this repo, agent-second-brain) into one vision after discovering all three existed simultaneously. Promoted agent-second-brain to primary engine (most mature, already solves capture/memory/reminders/self-healing). Added the inbox/triage-to-Todoist bridge as new work, with a full custom task-system rebuild named as an explicit Later goal. Superseded the v1 draft written earlier the same day in `smartfolder-Genius/VISION.md`.
