# Scholar recovery and release review — 2026-11-03

The previous Scholar suite commits `translation-work:c01e519`, `ipvv:ce6b80ec`,
and `svread:50e658b` existed only in a temporary workspace. That workspace was
cleared before the commits reached GitHub; GitHub has no matching objects. The
hashes do not recover their contents. Do not treat those features as deployed.

Reviewed upstream through translation-work `cc8d685`, ipvv `26c0558f`, and
svread `29990fd`. Upstream contains the ORCID skeleton, approved C2 display, and
the updated reader. Account-scoped private Scholar drafts, grounded Qwen Scholar
assistance, realtime voice, revision-specific peer review, and explicit rights-aware
publication are still outstanding. The existing service creates review branches;
it is not the lost suite's account publication bridge.

This branch hardens the new ORCID skeleton: bind OAuth state to the initiating
browser, constrain redirects to reader-relative paths, use the authenticated iD
returned by the `/authenticate` token exchange, and suppress internal error details.
Tests cover state and redirect rejection and a mocked token exchange. Credentials
are not configured here; a real ORCID sandbox test and deployment remain required.

The former `/api/variants/:id/accept` set `accepted=1` for anyone who knew an ID,
without authenticating, validating the content, or recording a human decision. It
now fails closed pending an actual review workflow. This intentionally disables the
legacy accept button. Other legacy endpoints still need a separate security and
compatibility migration: `/api/profile` can reserve an email without verification;
variant creation accepts a caller-supplied user ID; and bookmark endpoints accept
or expose caller-supplied account IDs. Do not store private Scholar work in them.

Before release, complete the Scholar suite again against these upstream revisions.
Do not place private drafts or style samples in public Git. Gate evidence against
the existing PASS and human authority contracts; distinguish an author's approval
from independent peer review; bind approval to exact content; and mark AI assistance.
Validate the existing canonical hash schemes separately. Keep the Qwen voice relay
disabled until provider credentials and a quota preventing paid overage are available.
Never bypass the other agent's work with force pushes.

The full ipvv build needs the source-library volume and the site gate requires its
generated receipts. Browser, live provider, Cloudflare deployment, and Git credentials
must be verified on a host with the corresponding access. The local tests here do
not establish that a production deployment or the missing suite works.

The later commit on this branch adds a private account API for drafts, snapshot-bound
reviews, self-attested sign-offs and consented Qwen assistance. It is not a reader UI,
Git publication bridge, or voice relay. See `worker/SCHOLAR-WORKSPACE.md` for API,
migration, privacy and rollout details. It has not been deployed.
