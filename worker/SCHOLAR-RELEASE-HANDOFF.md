# Scholar release handoff — 2026-11-03

The recovered suite is checkpointed in three **draft pull requests**, not yet
deployed: [translation-work #7](https://github.com/prx0r/translation-work/pull/7),
[ipvv #9](https://github.com/prx0r/ipvv/pull/9), and
[svread #3](https://github.com/prx0r/svread/pull/3). Integrate the latest base
branches without force-pushing over concurrent work. GitHub branches are durable
checkpoints; they are not a production release. On 2026-11-03 the public Scholar
Worker endpoint still returned 404, and the reader workspace script URL returned
the static HTML fallback instead of JavaScript.

## What is present and what is not

| Inspiration | Present in these branches | Remaining work / limit |
| --- | --- | --- |
| Bilara, segment-based translation | Layer drafts reference a work and passage ID; published versions can fork from other versions; private saves have history and comparison. | A complete cross-edition segment identity and source-alignment audit is not complete. Each draft is not automatically public Git. |
| OpenReview, review of a particular revision | A reviewer receives a private immutable snapshot and can record one decision and reasoning against its hash. | These private decisions are not signed or exported to Git; reviewer identity and independence are not independently established. |
| Hypothesis, private annotations | An account can keep private notes against a passage. | There are no selected-text/range anchors, threaded annotation conversations, or public annotation layer. |
| Weblate, personal translation memory | Opt-in style drafts use only the owner's eligible human-written examples from the same work and their selected L0 gloss changes. | This is not a searchable, editable translation-memory system or a cross-work personal lexicon. Only the selected examples are sent to the provider with consent. |
| Sefaria, versions and collections | The Scholar reader exposes versions and layer data. | Source sheets and curated learning pathways are not built here. |
| Ambuda/Vidyut, Sanskrit tooling | Existing L0 analyses can be used as evidence. | Vidyut segmentation/morphology is not integrated or evaluated, and existing L0 entries are not thereby independently verified. |
| 84000, aligned commentary | The reader uses existing passage identifiers. | A root-text/commentary/embedded-quotation alignment model is not implemented. |

Author sign-off is self-attested account approval, not an independent review or
proof of copyright. The submission bridge validates an explicitly signed snapshot
and may create a public Git branch; merging that branch and releasing the reader
are separate actions. Review signatures in canonical Git have different legacy and
v2 semantics documented in `translation-work/SCHOLAR.md`. Do not interchange the
two canonical hash schemes.

## Release sequence and gates

1. Review and integrate translation-work #7, ipvv #9, and svread #3 in dependency
   order, including any newer changes from other agents. Run `python3 check.py` in
   translation-work; run the focused Worker tests in `SCHOLAR-WORKSPACE.md` plus
   `tests/scholar-publish-e2e.test.mjs`; run the reader checks in
   `svread/SCHOLAR-PRIVACY.md`. The end-to-end test uses a real temporary Git remote,
   SQLite and the bridge, with external provider APIs mocked.
2. Reproduce the full site build and `python3 tools/verify_site.py` in ipvv with the
   required source-library volume and generated `site/dist/data/receipts.jsonl`.
   The original environment recorded passing gates, but a fresh checkout here lacks
   those inputs. Do not claim a fresh-checkout gate has passed until it does.
3. On the authorized deployment host, back up the **correct** production D1
   database securely outside the repository. From `ipvv/worker`, apply
   `migrations/0002_scholar_workspace.sql` and then
   `migrations/0003_scholar_history.sql` and `migrations/0004_scholar_ai_limits.sql`
   to the remote database (for example,
   `wrangler d1 execute ipvv --remote --file migrations/0002_scholar_workspace.sql`,
   then the corresponding 0003 and 0004 commands). Check results and deploy the Worker;
   deploy svread only after the compatible Worker and projections are available.
4. Configure the bridge on an HTTPS host with the secret stored outside Git and
   the identical secret configured in the Worker. Confirm the Git remote and its
   permissions with a disposable test submission before exposing submissions.
5. Leave Qwen text and voice disabled until the operator has a provider-side cap
   that prevents paid overage, the dedicated Scholar secret and request limits, and
   a real provider test. Atomic account/global request and concurrency reservations
   exist in this branch, but cannot guarantee a provider spending cap. Legacy model
   endpoints use a separate secret and need their own security and quota review.
   The free-tier flag alone is not a spending cap.
   Perform browser tests for login, account switching, private save/history, reviewer
   isolation, sign-off, consent, and voice permissions before declaring release.

Known content work remains: confirmed Sanskrit omissions and alignment issues must
be corrected at their authoritative sources and independently checked. Existing L0
records must not be represented as a completed independent philological audit.
