# Scholar account workspace: review branch

This branch adds an **account-private API**, not a deployed reader feature. Apply
`migrations/0002_scholar_workspace.sql` to the correct D1 database only as part of a
reviewed rollout and after a backup. The migration is additive and repeatable.
Authenticated calls use the existing `svsess` cookie, require a strong session
secret, enforce the reader-origin allowlist, and return `Cache-Control: no-store`.

| Endpoint | Behavior |
|---|---|
| `GET /api/scholar/documents?work=...&offset=...` | Account's private paginated documents |
| `PUT /api/scholar/documents/<id>` | Create/update a document using `expected_revision`; concurrent edits return 409 |
| `DELETE /api/scholar/documents/<id>` | Delete that account's specified revision; shared reviews remain |
| `GET/POST /api/scholar/reviews` | List or privately share an immutable saved snapshot with another account ID |
| `POST /api/scholar/reviews/<id>/decision` | Selected reviewer records one decision and reasoning |
| `POST /api/scholar/signoffs` | Author approves exact saved revision and declares rights; record remains private |
| `POST /api/scholar/submit` | Explicitly submit an unchanged signed revision to the authenticated Git bridge |
| `POST /api/scholar/assist` | With explicit consent, request a grounded Qwen draft; optionally use only the account's own examples |
| `GET /api/scholar/voice` | Authenticated WebSocket relay for grounded push-to-talk; disabled until separately configured |

Private records live in D1, not public Git. A review snapshot remains with its
participants even if the owner deletes the original private document. A sign-off is
self-attested, not a cryptographic signature or independent peer review. The SHA-256
snapshot hash uses compact sorted-key Scheme A; do not interchange it with the
ReviewEvent/PromotionEvent Scheme B in translation-work `SCHOLAR.md`. Rights are a
contributor declaration, not proof of ownership or legal copyright.
Private peer-review decisions remain in D1 and are not automatically exported into
Git; the bridge records the author's own approval only.

Qwen is disabled unless `SCHOLAR_QWEN_FREE_TIER_CONFIRMED=true` and the existing
server-side DashScope key is available. This flag is an **operator assertion**, not a
billing cap: enable it only after a provider-side quota preventing paid overage is in
place. Consent is required for each request. The source and gated layers are fetched
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
Before a public rollout, also enforce account-level request and concurrency limits
and verify that the provider cannot bill above the intended free quota.

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
