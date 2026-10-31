# PLAN v2 — qprivately-native everything, versions to profile, chat per text

Supersedes the phase list in PLAN.md with three named pillars. Lane rules unchanged.
Prior art folded in: Ochema.app (grimoirer: profiles, diaries/saved passages,
bookmarks, community — the profile pattern for grimoires) and nibbanahelp
(relay: embeddings loop + local profile JSON + per-text scoping).

## Pillar 1 — Everything qprivately-native
Status: kernel vendored, 5 gates live, 463 transition() receipts, tamper-checked.
Remaining, in order:
1. **Grants for display.** `accepted_by` becomes a signed grant; build checks the
   grant before rendering English. Unsigned = withheld, enforced at verify.
2. **ATASK tasks.** CLAIMS whiteboard → task objects (acceptance + evidence_required);
   DONE derived from receipts, never asserted. Kills DONE-with-0-PASS structurally.
3. **RUN ledger.** Every roll/ingest/build wrapped in run receipts (worker, model,
   tokens, cost) → quota enforcement (Kaggle hours, CF neurons) instead of prose limits.
4. **Receipts for everything else.** Essays (traceability verdicts), themes
   (adjudication accept/merge/split as transitions), scholars (entry checks).
   Same kernel, same shape, one audit log.

## Pillar 2 — Produce and save a new version (to profile)
The Ochema diary pattern, applied to translation:
1. **Version record.** `en_variants[]` entry: `{style, text, model, date, run_id,
   gate_verdicts, accepted}` + parent chunk id + immutable lineage. Variants are
   first-class records, never overwrites.
2. **Produce.** Three paths: (a) re-roll button (processor RUN, N candidates);
   (b) paste-own (scholar's verse); (c) style-render (style module over chunk).
   Every path runs the FULL gate battery; failures still emit FAIL receipts.
3. **Save to profile.** Worker + D1 backend: `profiles/{user}` holds variants,
   bookmarks (saved passages — Ochema diary verb), recitation playlists, progress.
   Local-first shape mirrors nibbanahelp `profile/me.json`; sync when logged in.
4. **Variations display.** Chunk page shows all PASS variants with style tabs;
   community styles namespaced `owner:style`; commercial witnesses never included.

## Pillar 3 — Chat assistant per text (then multi-text)
Per `specs/use-cases/embeddings-loop.md`, plus:
1. **Per-text chat.** Namespace filter `work == X`; bot answers only from that
   text's records + its argmaps + its essays. No leakage by construction.
2. **Multi-text.** Union namespaces on user request; answers cite which text each
   span came from.
3. **Growth loop.** Answered pairs appended with gate labels; abstentions file
   corpus gaps (drives translation priority). Same relay nibbanahelp proved.
4. **Voice.** Recitation player as the answer renderer (verse-first Sanskrit,
   then English) for the recite-capable works.

## Build order (gated)
1. Grants for display (site lane + pipeline handshake on `accepted_by`).
2. Profile backend skeleton (Worker + D1: variants save/list; bookmarks).
3. Version produce paths (re-roll UI first — no auth needed to roll, auth to save).
4. Per-text chat (1 work pilot: bhairavastava — smallest complete: 10 verses,
   8 PASS, chants, karaoke).
5. ATASK tasks + RUN ledger (governance hardening once the loop runs).
6. Multi-text union + community styles.

## Owner inputs needed (only these)
1. 5–10 Bhairavastava verses in your voice (fixes gen-z exemplars; unblocks P2/pilot).
2. Patreon URL (Support page still says "launching soon").
3. Accept/reject on CL-3 theme adjudication (unblocks themes layer).

## Ochema assets (checked 2026-10-31 — the comparative wing)
- **ochema-site** (ochema.xyz vision): comparative metaphysics, razor aesthetic
  (monochrome + gold, Source Serif, argument-diagram motif — corroborates our type
  system), brand law "a position is only as strong as the objection it survives"
  (= adversarial review as brand, cf. our verify gates).
- **Contentions** (`basecamp/knowledge/contentions/`, 16 files incl. 8 Abhinava):
  claim + source_span (work + line numbers) + quote + hetu/sadhya/vyapti +
  explicit **falsifier** + support/attack targets + crux links. This is the seed
  layer between pushing probes and essays that we were missing: every contention
  carries its own defeat condition. Wire contentions as essay-traceability
  targets (essay claim → contention → source span) and as adversarial-review gates.
- **TIME-PARALLEL-IPK-OCHEMA.md** (research-library): IPK time-structure =
  thermal time = Spanda/Ñāṇavīra/Seth/Ibn Arabi/Proclus. Proof that cross-tradition
  synthesis works — validates the multi-text chat pillar.
- **Hermetica sources** (`source-library/hermetica/` + render packs in
  tantraloka/goldrender) remain the first pushing-service target.
- Note: `ochema2/` is a dead symlink (volume gone); `blog/content/sources/` paths
  in ochema-site docs don't exist on this volume (sources live elsewhere).
  Ochema.app platform (grimoirer docs: profiles, diaries, bookmarks) already folded
  into Pillar 2 above.
