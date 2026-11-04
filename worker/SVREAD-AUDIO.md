# svread generated audio

`POST /api/read` accepts a work ID, passage ID, language and up to 4,000
characters of text. It returns a public R2 URL for a Fish Audio recording.
The provider request uses `s2.1-pro-free`; operators must verify and monitor the
provider's actual quota. The endpoint is unauthenticated and accepts caller-supplied
text: it does not by itself authenticate a source edition, enforce a translation
gate, or prevent request-volume abuse.

The v2 cache uses `read-v2/<work>/<passage>_<language>_<sha256>.mp3`. The SHA-256
is calculated by the Worker over compact JSON containing version 2, the exact
text sent to the provider, the voice reference and the model name. Work, passage
and language remain in the path. Changing text, voice, model or language therefore
uses a different object. This also prevents a different caller-supplied text from
occupying the key for a known reading. Old `read/` objects remain in R2 but are
not returned by the v2 endpoint; the first request for a v2 recording generates a
new object and consumes provider quota.

Local regression check: `node --test tests/reader-audio-cache.test.mjs`. The test
uses an in-memory R2 and mocked provider, so deployed R2, real audio and provider
quota still require verification before release. The site-wide gate remains
`python3 tools/verify_site.py` and must pass in the deployment environment.
