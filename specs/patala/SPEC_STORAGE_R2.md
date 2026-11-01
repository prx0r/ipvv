# STORAGE INFRA — Cloudflare R2 / S3 (the asset layer)

*2026-08-11. The repeatable translation factory's storage layer. R2/S3 holds the *assets* of the
factory: source scans, media (blog/video), and large generated artifacts. Code + specs live in git;
credentials NEVER go in the repo.*

> **SECURITY RULE:** credentials live only in the environment (`.env`, secret manager, or the
> platform's env). The repo contains `.env.example` with placeholders only. If a real token was ever
> pasted into a chat/log, it must be **rotated immediately**.

---

## 1. The accounts (placeholders — fill in your environment)

```env
# .env  (NOT committed)
R2_ACCOUNT_ID=               # Cloudflare Account ID
R2_ACCESS_KEY_ID=            # S3-compatible access key
R2_SECRET_ACCESS_KEY=        # S3-compatible secret
R2_BUCKET=blog-video-assets
R2_ENDPOINT=https://<account_id>.r2.cloudflarestorage.com
```

The R2 API is **S3-compatible** — use any S3 client (aws cli with endpoint, boto3, wrangler).

## 2. Bucket layout (proposed)

```
r2://blog-video-assets/
  sources/            scanned witnesses, manuscripts, large e-texts
  media/blog/         blog images
  media/video/        video/audio (education layer)
  exports/            deterministic publication bundles (interchange)
  assets/             generated artifacts (term packs, gold packs)
```

The buckets hold **assets**, not scholarship data structures (those live in the pāṭala
`data/corpus`). The API is the source of truth for structure; R2 is the blob store.

## 3. Access model

- **Public read** for published media/assets (R2 public bucket or a CDN).
- **Private** for source scans pending rights review.
- **Write** only from the factory pipeline (CI/workers), never from the browser.
- Every object carries a rights tag (see `SPEC_SOURCE.md` §6): open / public-domain / permission /
  restricted.

## 4. Verification (example)

```bash
# verify credentials (uses YOUR env, not committed values)
curl -X GET "https://api.cloudflare.com/client/v4/accounts/$R2_ACCOUNT_ID/tokens/verify" \
     -H "Authorization: Bearer $R2_API_TOKEN"
```

## 5. Where this connects

- `SPEC_SOURCE.md` — source scans/witnesses (stored assets + their rights).
- `SPEC_FACTORY_QA.md` — deterministic publication bundles (can be exported to R2).
- `SPEC_EDUCATION.md` — video/audio assets.
- pāṭala `data/atlas/resources.ts` — links to hosted media.
