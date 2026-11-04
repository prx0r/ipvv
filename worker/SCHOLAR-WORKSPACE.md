# Scholar account workspace: review branch

For the other agent's release sequence, feature-by-feature status, and remaining
gates, start with `SCHOLAR-RELEASE-HANDOFF.md` in this directory.

This branch adds an **account-private API**, not a deployed reader feature. Apply
`migrations/0002_scholar_workspace.sql` to the correct D1 database only as part of a
reviewed rollout and after a backup. Apply `migrations/0003_scholar_history.sql`
`migrations/0004_scholar_ai_limits.sql`, `migrations/0005_scholar_peer_review.sql`,
`migrations/0006_scholar_style_examples.sql` and `migrations/0007_scholar_review_versions.sql`
afterwards; all are additive and repeatable.
Authenticated calls use the existing `svsess` cookie, require a strong session
secret, enforce the reader-origin allowlist, and return `Cache-Control: no-store`.

| Endpoint | Behavior |
|---|---|
| `GET /api/scholar/documents?work=...&offset=...` | Account's private paginated documents |
| `PUT /api/scholar/documents/<id>` | Create/update a document using `expected_revision`; concurrent edits return 409 |
| `DELETE /api/scholar/documents/<id>` | Delete that account's specified revision; shared reviews remain |
| `GET /api/scholar/documents/<id>/history?before=<revision>` | Account-private revision snapshots, newest first, 50 per page |
| `GET/POST /api/scholar/style-examples` | List or explicitly mark two revisions of the author's own document as a private style example |
| `DELETE /api/scholar/style-examples/<id>` | Revoke a selected example for future use |
| `GET/POST /api/scholar/reviews` | List or privately share an immutable saved snapshot with another account ID |
| `POST /api/scholar/reviews/<id>/decision` | Selected reviewer records an initial decision, reasoning and optional structured rubric |
| `POST /api/scholar/reviews/<id>/revise` | Reviewer amends their report using the expected report revision and explicit AI permission |
| `GET /api/scholar/reviews/<id>/report-history` | Author and reviewer can inspect earlier report versions |
| `GET/POST /api/scholar/reviews/<id>/messages` | Private discussion between the author and the invited reviewer |
| `POST /api/scholar/reviews/<id>/ai-consent` | The reviewer can grant or revoke permission for their report to be sent to an AI provider |
| `POST /api/scholar/signoffs` | Author approves exact saved revision and declares rights; record remains private |
| `POST /api/scholar/submit` | Explicitly submit an unchanged signed revision to the authenticated Git bridge |
| `POST /api/scholar/assist` | With explicit consent, request a grounded Qwen draft or revise a saved essay using selected style edits and eligible reviews |
| `GET /api/scholar/voice` | Authenticated WebSocket relay for grounded push-to-talk; disabled until separately configured |

Private records live in D1, not public Git. A review snapshot remains with its
participants even if the owner deletes the original private document. A sign-off is
self-attested, not a cryptographic signature or independent peer review. The SHA-256
snapshot hash uses compact sorted-key Scheme A; do not interchange it with the
ReviewEvent/PromotionEvent Scheme B in translation-work `SCHOLAR.md`. Rights are a
contributor declaration, not proof of ownership or legal copyright.
Private peer-review decisions remain in D1 and are not automatically exported into
Git; the bridge records the author's own approval only.
Reviewers may separately opt in to AI use of their report and later revoke that
permission. Discussion messages are never included automatically. A review concerns
the exact snapshot hash shared with the reviewer; it does not assert independently
verified identity, independence, or academic endorsement.
Report revisions preserve earlier decisions and use optimistic concurrency. They
remain attached to the same essay snapshot; a newly edited essay requires a new
review invitation. AI draft provenance records the selected report revision and
content hash, not an independent reviewer signature.

Successful private saves create a snapshot atomically using D1 triggers. Restoring
an older snapshot is an ordinary new revision: it does not replace history and it
invalidates an earlier sign-off. Deleting the private document deletes its history;
previously shared review snapshots and separately submitted Git objects remain.
The migration can backfill only the current revision of existing documents, not
previously overwritten saves. Private histories never enter Git automatically.
Style examples point to two exact private revisions, record their hashes and require
the author's explicit selection. They are deleted with the private document and are
not themselves a model fine-tune. Sending examples to a provider requires a separate
per-request consent; using reviewer comments requires the reviewer's permission too.

For `kind: essay_revision`, supply the author's `document_id` and exact saved
`revision`. The author may select up to six `style_example_ids` from their own
revision pairs and up to five `review_ids`. A review must target the same revision
and snapshot hash, have a submitted report and the reviewer's current AI consent.
The provider receives only those selected reports, not discussion messages. Selected
style pairs may come from the author's other works; the kind must match. Excerpts
over 3,500 characters are marked as truncated. The resulting agent draft retains
private provenance about the source revision and selected IDs; the author must copy,
review, save, sign off and explicitly submit before any public Git branch is created.
Reusing these examples is retrieval, not model weight training. The essay validator
checks object structure and source linkage, not the truth of scholarly claims.

Qwen is disabled unless `SCHOLAR_QWEN_FREE_TIER_CONFIRMED=true`, the dedicated
server-side secret `SCHOLAR_DASHSCOPE_API_KEY` is available, and the numeric
`SCHOLAR_QWEN_DAILY_ACCOUNT_LIMIT` (1–50) and `SCHOLAR_QWEN_DAILY_GLOBAL_LIMIT`
(1–500) are configured. These apply to Scholar text and voice together. Atomic
D1 reservations cap concurrent Scholar requests to one per account and three
globally, with a three-minute expiry if a Worker disappears. Failed provider calls
still count toward the daily request limit. Usage rows contain account ID and time,
not prompts, audio, responses, or credentials. Account deletion and usage-row
retention need an operator policy before launch.

The free-tier flag is an **operator assertion**, not a
billing cap: enable it only after a provider-side quota preventing paid overage is in
place. Request counts cannot guarantee a monetary cap. The dedicated secret prevents
Scholar configuration from accidentally enabling legacy endpoints that use
`DASHSCOPE_API_KEY`; existing legacy endpoints must be separately audited and limited.
Consent is required for each request. The source and gated layers are fetched
from `svread/data/scholar/<work>.json`; missing source or gated T1 fails closed.
Long layers are marked as excerpts. The projection must be rebuilt and deployed from
the corresponding translation-work recovery branch before this endpoint can work.
Private examples are sent to the model only when explicitly selected, require three
distinct human-written examples in the same work, and exclude drafts marked as AI
assisted. For translation tasks, up to 20 changed, human-selected L0 gloss choices
and their recorded grounds are included with those explicitly selected style examples.
Output is account-private and labelled as agent-generated.

Realtime additionally requires `QWEN_REALTIME_ENABLED=true` and a workspace-specific
`QWEN_REALTIME_WS_URL` matching the official Beijing or Singapore Qwen3.8 realtime
endpoint. The Worker keeps the provider key server-side, supplies evidence itself,
rejects client instruction changes, caps input and closes sessions after two minutes.
The browser must request explicit microphone and provider consent. Audio and its
associated text can both count against provider quota; the configuration flag does
not enforce billing limits. Live provider testing is still required.
Before a public rollout, verify the provider cannot bill above the intended free
quota and exercise these limits against real D1 and the real provider.

The matching translation-work bridge branch accepts HMAC-SHA256 requests authenticated
with `SCHOLAR_BRIDGE_SECRET`, validates the exact sign-off and translation layers,
and creates a separate Git branch. Configure `SCHOLAR_BRIDGE_URL` as the HTTPS origin
and install the matching secret in the service outside Git. An explicitly submitted
branch can become public, but it is not merged or published on the reader. A local-only
result is labelled `PREPARED_LOCAL`. The legacy bearer/session service remains separate.
The bridge is not deployed and requires real-infrastructure testing before release.

Local validation: `node --test tests/scholar-auth.test.mjs tests/orcid-auth.test.mjs
tests/scholar-workspace.test.mjs`. These use SQLite and a mocked Qwen provider, not a
live D1, ORCID or DashScope account. Site gate and real browser smoke remain release
requirements; see `process/SCHOLAR-RECOVERY-2026-11-03.md`.

### Private editorial decisions

Apply migration `0008_scholar_decisions.sql` after 0002–0007. An author may
record a subject, before/after wording and optional rationale against an owned
saved translation or essay revision with `POST /api/scholar/decisions`. The
server derives the work, passage, layer and snapshot hash from that revision.
`GET` lists only the signed-in account's decisions; `DELETE /<id>` revokes one.
Deleting the source document also deletes its decisions. Decisions remain private.
For a model request, provide `decision_ids`, `use_style: true` and explicit
`consent_to_ai: true`; only selected, still-valid account-owned decisions are
sent. This is retrieval into the prompt, not model training or scholarly review.

### Revision-bound review annotations

Apply migration `0009_scholar_review_annotations.sql` after 0002–0008. The
review author and reviewer can select exact text from the immutable shared
snapshot and create/list private comments through
`GET/POST /api/scholar/reviews/<id>/annotations`. Offsets count JavaScript
UTF-16 code units and the server verifies the exact quote against the review
snapshot. `DELETE /api/scholar/review-annotations/<id>` is author-only.
Annotations are not included in model prompts or public submissions. A new
revision needs a new review; comments remain attached to the old snapshot.

### Evidence integrity

Before Qwen text or realtime voice receives a passage, the Worker verifies the
projection content hash, checks `withheld_songs`, and verifies the original
hashes of the passage layers it uses. A mismatch fails closed. The hash checks
internal consistency, not source authenticity or philological correctness; a
mutable upstream can publish a different internally consistent projection.
Production CPU and response-size limits must be tested on the deployed Worker,
especially for the largest works.

### Private source notebook

Apply migration `0010_scholar_source_notebook.sql` after 0002–0009.
`GET/POST /api/scholar/sources` lists or saves an owned passage reference with
an optional private note. The server verifies the source projection and stores
its hash. `DELETE /api/scholar/sources/<id>` removes a reference. An essay or
essay revision may include up to three explicitly selected `source_ids` with
`consent_to_ai: true`; sources are fetched again and compared to the saved
projection hash. If any changed or is withheld, drafting fails closed. This
records source references, not an independent verification or archival copy.
Notes and source contents are sent to the provider only when selected.

### Cross-repository MCP integration test

With the matching svread Scholar branch checked out locally, run:

```sh
SCHOLAR_MCP_SERVER=/absolute/path/to/svread/mcp/scholar_server.py node --test tests/scholar-mcp-e2e.test.mjs
```

The test launches a real MCP stdio process and a local HTTP adapter around the
Worker with SQLite: it authenticates two accounts, reads a real bundled Sanskrit
passage, saves a private essay, decision and source, requests review, reads an
anchored reviewer comment, drafts with explicitly selected evidence, and signs
off. The Qwen provider and Worker source response are mocked. A separate
`tests/scholar-publish-e2e.test.mjs` runs the publication bridge and validator
against a real temporary Git remote; neither test establishes production access.

### Preparing passage citations for an essay

`POST /api/scholar/citations/prepare` accepts selected private `source_ids`,
rechecks each projection and returns citation references containing work, passage,
T1 hash and projection hash. Private notes and notebook IDs are omitted. An essay
can save these in `content.citations`; the exact references are included in the
snapshot hash and become public on submission. The translation-work bridge must
be updated to its citation-validation checkpoint before this is enabled: it
checks T1 and proof against an exact committed Git tree. The projection digest
is client-reported to that bridge and is not an authenticated archive. Neither
check determines if a cited passage supports the essay's argument.

For the citation-inclusive publication integration test, point
`SCHOLAR_TRANSLATION_ROOT` at the matching translation-work citation branch:

```sh
SCHOLAR_TRANSLATION_ROOT=/absolute/path/to/translation-work node --test tests/scholar-publish-e2e.test.mjs
```

It uses a temporary Git remote and mocked Qwen/source responses. The cited T1
record is loaded from the canonical checkout, signed with the essay revision,
validated by the bridge, and checked in the submitted Git object. Private
notebook notes do not appear in that object.
