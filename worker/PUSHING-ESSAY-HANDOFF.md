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
