# Scholar release handoff — updated 2026-11-04

The recovered suite is checkpointed in three **draft pull requests**, not yet
deployed: [translation-work #7](https://github.com/prx0r/translation-work/pull/7),
[ipvv #9](https://github.com/prx0r/ipvv/pull/9), and
[svread #3](https://github.com/prx0r/svread/pull/3). Integrate the latest base
branches without force-pushing over concurrent work. GitHub branches are durable
checkpoints; they are not a production release. On 2026-11-04 the public Scholar
documents endpoint still returned 404 and the live reader showed the older
Scholar experience. Neither verifies this release.

## What is present and what is not

| Inspiration | Present in these branches | Remaining work / limit |
| --- | --- | --- |
| Bilara, segment-based translation | Layer drafts reference a work and passage ID; published versions can fork from other versions; private saves have history and comparison. | A complete cross-edition segment identity and source-alignment audit is not complete. Each draft is not automatically public Git. |
| OpenReview, review of a particular revision | An invited reviewer receives a private immutable snapshot, can give a structured report, revise the report with history, and discuss it privately with the author. The author can select permitted feedback for an AI essay revision. | Private reports are not signed or exported to Git; reviewer identity and independence are not independently established. |
| Hypothesis, private annotations | Accounts can keep passage notes and source links; authors and reviewers can anchor private comments to selected text in an immutable review snapshot. | Anchors use UTF-16 offsets in that snapshot; there is no threaded annotation conversation or public annotation layer. |
| Weblate, personal translation memory | The author can select exact before/after private revisions from their own writing as style examples and choose them for a draft. | This is retrieval, not fine-tuning or a complete translation-memory system. Only selected examples go to the provider with consent. |
| Sefaria, versions and collections | The Scholar reader exposes versions and layers; private notebook references can be selected and attached to an essay as citations. | Public source sheets and curated learning pathways are not built here. |
| Ambuda/Vidyut, Sanskrit tooling | The optional local MCP tool can produce unreviewed transliteration and, with separately licensed data, metre candidates. Existing L0 analyses can be used as evidence. | Segmentation and morphology are not integrated or evaluated; existing L0 entries are not independently verified by this tool. |
| 84000, aligned commentary | The reader uses existing passage identifiers. | A root-text/commentary/embedded-quotation alignment model is not implemented. |

Author sign-off is self-attested account approval, not an independent review or
proof of copyright. The submission bridge validates an explicitly signed snapshot
and may create a public Git branch; merging that branch and releasing the reader
are separate actions. Review signatures in canonical Git have different legacy and
v2 semantics documented in `translation-work/SCHOLAR.md`. Do not interchange the
two canonical hash schemes.

## Review and test checkpoint — 2026-11-04

- `translation-work` passed its canonical check with zero failures and 29 Python
  unit tests, of which two optional Vidyut tests were skipped. Its historical review warning
  remains: the legacy signature covers the review ID, not the full statement.
- The focused Worker/authentication/MCP/publication suite passed 20 tests with
  local SQLite, a temporary Git remote and a mocked Qwen provider. Real D1,
  external provider credentials and production hosting have not been exercised.
- `svread` passed 23 Node tests and two extra real Chromium tests. The latter
  include a browser → local Worker → SQLite path covering a private decision,
  source, citation, AI draft and selected-text review; Qwen is mocked. This
  exposed encoded colon IDs returning 404, fixed on this branch. Production
  ORCID, D1, microphone permissions and Qwen still need acceptance tests.
- The reader bundle now verifies 291 assets, 55 works and 22 Scholar projections.
  The canonical emitter reproduced all the vendored projections. Thirty-seven
  works have no named source edition in the bundled metadata. The Ghaṭakarpara
  coverage hold applies to the projection; upstream site payloads must also be
  repaired or withheld before release.
- The full site gate failed here: generated `site/dist/data/receipts.jsonl` and
  the source-library volume for the build are unavailable. These are not proof
  that production data passed; use the authorized build host to reproduce the gate.

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
   `migrations/0003_scholar_history.sql` through `migrations/0011_scholar_source_links.sql`
   to the remote database (for example,
   `wrangler d1 execute ipvv --remote --file migrations/0002_scholar_workspace.sql`,
   then the corresponding 0003–0011 commands in order). Check results and deploy the Worker;
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
