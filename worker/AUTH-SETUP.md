# AUTH-SETUP — scholar sign-in (phase 1 done) + ORCID/Zenodo legs (human steps)

Owner: **ORCID 0009-0008-1635-5355** (https://orcid.org/0009-0008-1635-5355)

## Phase 1 — LIVE (local signup/login, free, zero deps)
- Endpoints: `POST /api/auth/access` {email, name, password ≥8} (join or sign in),
  `GET /api/auth/me`, `POST /api/auth/logout`. Existing email-only rows cannot be
  claimed until an email-ownership verification flow is implemented.
- Session = HMAC-SHA256 signed HttpOnly cookie `svsess` (7d), secret = wrangler
  `SESSION_SECRET` (at least 32 characters; rotate: `wrangler secret put SESSION_SECRET`). Passwords =
  PBKDF2-SHA256 100k (worker WebCrypto hard-caps >100k), per-user hex salt, 120k→100k NOTE.
- UI: svread Scholar hub → "Scholar account" widget (credentials:'include'; worker CORS
  echoes svread origin + Allow-Credentials).
- Cookie = `SameSite=None; Secure` for the cross-site worker. Browsers that block
  third-party cookies may still need a same-site worker route. Account email and name
  are self-attested until verification exists; profile login is not an ORCID verification.
- D1 migration already applied: `ALTER TABLE profiles ADD password_hash,salt,display_name,orcid,provider`
  (schema.sql carries it for fresh installs).

## Phase 2 — ORCID sign-in (human: ~5 min, free)
1. orcid.org → Developer Tools → register Public API client:
   name `svread`, URL `https://svread.pages.dev`,
   **redirect URI: `https://ipvv-api.tradesprior.workers.dev/api/auth/orcid/callback`**
2. Put client id/secret in `.orcid-env` (600, never git): `ORCID_CLIENT_ID=…` / `ORCID_CLIENT_SECRET=…` (sandbox first if you like: sandbox.orcid.org).
3. Then I build: `/api/auth/orcid/start` → 3-leg OAuth → verified iD → autofill profile
   (name, affiliation, works) → link-or-create local account. iD field already exists (`profiles.orcid`).

## Phase 3 — Zenodo publishing (agent leg)
1. zenodo.org → Settings → Applications → token with `deposit:write` (+ `deposit:actions`).
2. Token → `.zenodo-env` (600, never git). Community = yours (created already).
3. Then: `tools/publish_zenodo.py` — essays + translation releases → DOI per deposit;
   set DataCite trusted party in ORCID so deposits auto-appear in your ORCID works.

Free throughout: ORCID Public API (non-commercial), Zenodo (CERN), our worker/CF free tier.

## Shared session secret (login = submission credential, 2026-11-03)

One credential now works for chat AND the scholar submission service
(`translation-work/tools/scholar_service.py`): the `svsess` HMAC cookie is verified
by BOTH. The secret lives in **two places that must be rotated together**:

1. worker: `wrangler secret put SESSION_SECRET`
2. service: `/root/.scholar/session_secret` (mode 600) — file wins over env

Rotate: generate hex32 → write the file (chmod 600) → pipe the same value to
`wrangler secret put SESSION_SECRET`. Old cookies die on rotation (by design).
The service resolves the display name from `GET /api/auth/me` (attribution comes
from the worker, never the client); its `GET /v1/scholar/whoami` returns the
unified identity for UIs. Legacy bearer tokens still work.

## Phase 2 — ORCID sign-in (endpoints LIVE, awaiting creds)

Deployed endpoints (`worker/src/index.js`):
- `GET /api/auth/orcid/start?redirect=/path` — 302 to ORCID authorize (`scope=/authenticate`), HMAC-signed short-lived state
- `GET /api/auth/orcid/callback?code&state` — token exchange → `oauth/userinfo` → link-or-create profile keyed by **verified ORCID iD** (`profiles.orcid`), sets `svsess`, redirects back
- Without `ORCID_CLIENT_ID` / `ORCID_CLIENT_SECRET` both return **503** ("not configured") — by design

To turn on (owner, Developer Tools at https://developer.orcid.org):
1. Register a client (sign-in API), redirect URI: `https://ipvv-api.tradesprior.workers.dev/api/auth/orcid/callback`
2. `wrangler secret put ORCID_CLIENT_ID` / `ORCID_CLIENT_SECRET` — then start/callback go live, no redeploy
3. Note: email is synthesized (`<iD>@orcid.svread`) until we request the email claim — ORCID best practice is to ask for it manually on first sign-in; a follow-up task
