# Pushing → Scholar essays — implementation checkpoint

This isolated branch extends the Scholar recovery branch for an enquiry-to-essay
prototype. It does not deploy the Worker or publish any scholarship. The matching
reader work is in [svread #5](https://github.com/prx0r/svread/pull/5).

The aim is to make it possible for an authenticated author to grant or revoke
specific AI uses of an exact, already-published essay object; a reader can then
choose eligible scholarship as evidence for a Qwen enquiry or essay draft.
Permission to answer questions and permission to use the work in drafts are
separate. Neither is inferred from a copyright statement. Private drafts and
review feedback are not eligible for this path. Generated prose and citations
remain proposals requiring review, not independent scholarship or proof.

Before committing this branch, the required tool help checks passed. The existing
`bash tools/verify.sh` fails in this checkout because generated
`site/dist/data/receipts.jsonl` is missing and kernel verification cannot open it.
Use the authorized source/build environment to reproduce the full gate before any
release; do not manufacture receipts.

## Backend contract (migration 0012)

- `GET /api/scholar/published-essays?work=...` lists only verified published
  essay objects from the hash-checked Scholar projection, with their current
  scoped grant and an `owned` flag. An essay's content address, self-attested
  sign-off and signed snapshot are rechecked; this is integrity and account
  attribution, not independent identity verification.
- `PUT /api/scholar/essay-permissions` accepts `work`, `essay_id`,
  `allow_answers`, `allow_drafts` and `confirmed: true`. Only the authenticated
  account recorded as that published object's author may set or revoke a grant.
  Permission is bound to the exact essay content address; a later version needs
  a fresh grant. Existing published works start with neither permission.
- `POST /api/scholar/assist` accepts up to three `scholar_essays` references
  (`{work, essay_id}`). `kind: enquiry` needs the answer permission; `essay` and
  `essay_revision` need the drafting permission. An enquiry may omit a root
  passage only when it selects a permitted essay or a saved source. Other tasks
  cannot use these essay grants. Existing explicit per-request Qwen consent and
  quota checks still apply.
- The Worker selects bounded, keyword-ranked paragraph excerpts and gives them
  stable labels such as `E1:p2`. It rejects invented labels and a response that
  cites none of the selected scholarship. The response records the exact essay
  ID, paragraph number, excerpt offsets/hash and current projection hash. The
  excerpts and labels aid checking; they do **not** establish that a claim is
  supported, that a passage is complete, or that a published work grants any
  other licence. The user must review the output and its sources.
- Revocation prevents future requests after the grant change is observed. It
  cannot recall excerpts already sent to a provider or in-flight requests.
  There is no private draft or reviewer-report access through this grant path.
  Account-backed grant history and a production retention policy remain future
  work; current attribution is self-attested by the account.

Apply `migrations/0012_scholar_essay_permissions.sql` after 0002–0011 only as part
of the reviewed deployment and after backing up the correct D1 database. See the
matching svread prototype for user controls and the essay-draft handoff.

The citation-preparation endpoint also accepts explicitly selected public
`passages: [{work, target}]` alongside private `source_ids`. It rechecks the
current projection and T1 hash, de-duplicates a passage also selected from the
notebook, and returns only the publishable reference fields. A caller should
compare these references with those used for the draft and recheck them before
saving. The bridge validates declared T1 links and the pinned source Git tree;
it does not validate whether each essay claim follows from those sources.

The local integration tests cover a signed essay written to an actual temporary
Git remote, projection of that exact object, author consent, and a second
account's cited enquiry. The projection and Qwen provider are mocked; no test
establishes public deployment, live D1 or a real provider response.
