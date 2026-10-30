# site — live display (same shell, every work)

Static HTML in `dist/` (208 pages). Deploy `dist/` to Cloudflare Pages, like shivastotravali.pages.dev.

## What it displays (only formally done)

- IPVV: 49 passages — ORIGINAL (Sanskrit) + READ (L2) + STUDY (C1) + CRITICAL. GUIDE greyed (planned). Plus themes (9 clusters, overlapping) + pushing stub.
- VBT: 145 verses — ORIGINAL + READ + STUDY (attention-seat) + CRITICAL. GUIDE greyed.
- Tantrasara: 6 essay-0 units — ORIGINAL (verbatim span) + READ (plain) + STUDY (question) + CRITICAL (alternates). GUIDE greyed.

Missing layers render "not yet formally done — never invented", never filled.

## Rebuild (any new work)

```bash
python3 site/build.py                 # all works
python3 site/build.py ipvv            # one work
```

Add a work = loader returning items with {id, sanskrit, read, study, meta} + themes + pushing stub. Same depth tabs, same CSS, same nav. No backend.

## Deploy

Point Pages at `site/dist/`. Rebuild + commit + push; Pages redeploys.
