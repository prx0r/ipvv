# Recitation app — standalone chant PWA

## Inputs
- 18 studio chants + karaoke timings (`site/data/audio-*.json`), 4-mode player.
- Synth fallback (all 555 pages carry recite hooks).
- kashaudio render order (short works first: Bhairavastava → Anuttarāṣṭikā → …).

## Behavior
- Playlists, offline mp3s, line-mode as the learning loop (Sanskrit line, repeat,
  English follows). Anuttarāṣṭikā's 8 chants = complete Day-1 pack.
- Player lifted from page-bound to app shell; same modes, same badges.

## Phases
1. Playlist view over existing `/recite/` pages (static).
2. PWA shell + offline (needs app packaging, no new data).
