# AUTH-SETUP — scholar sign-in (phase 1 done) + ORCID/Zenodo legs (human steps)

Owner: **ORCID 0009-0008-1635-5355** (https://orcid.org/0009-0008-1635-5355)

## Phase 1 — LIVE (local signup/login, free, zero deps)
- Endpoints: `POST /api/auth/access` {email, name, password ≥8} (join or sign in; also claims
  old email-only rows), `GET /api/auth/me`, `POST /api/auth/logout`.
- Session = HMAC-SHA256 signed HttpOnly cookie `svsess` (7d), secret = wrangler
  `SESSION_SECRET` (rotate: `wrangler secret put SESSION_SECRET`). Passwords =
  PBKDF2-SHA256 100k (worker WebCrypto hard-caps >100k), per-user hex salt, 120k→100k NOTE.
- UI: svread Scholar hub → "Scholar account" widget (credentials:'include'; worker CORS
  echoes svread origin + Allow-Credentials).
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
