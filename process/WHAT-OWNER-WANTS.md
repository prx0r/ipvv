# What the owner actually wants (learned 2026-10-31, the hard way)

*Process note. Written after a session of repeated corrections. Read before touching the site.*

## The core pattern

**He describes by feeling, not spec.** "Feels like 5 sites in one." "Too big." "Shitty." "Doesn't make sense." These are not vague complaints — they are precise design judgments stated emotionally. Translate feeling → cause immediately. Don't ask what he means. Go look.

**He repeats a demand when I don't act on it.** Masters font too big: said 3 times before fixed. Each repeat is hotter. First telling = the spec. Act on first telling.

**Less is more, always.** Every feature I added created a new complaint. Dropdowns added chrome. Re-executed scripts double-bound handlers. New sections added pages that felt like new sites. The correct fix is almost always removal: remove the hijack, remove the box, remove the duplicate list, remove the brand text, remove the link dump. When in doubt, delete.

## What "good" means to him (extracted, not asked)

1. **One site, not five.** Every page same shell, same nav, same type, same rhythm. Any page that looks or behaves differently is a bug, no matter how correct its content.
2. **Stonedoorway blank as north star.** White, Georgia, minimal chrome, content flows, nothing shouts. If a change moves away from blank-white-quiet, it's wrong.
3. **Sidebar is sacred.** The left bar (collapsible masters/scholars, counts, persisted state) is the one thing he likes. Touch it only to simplify. Never add to it without removing something.
4. **No duplication, ever.** Scholars in sidebar = no scholars wall in main. Masters collapsed = no masters content shouting. One list per thing, in one place.
5. **Small, uniform type.** Section headers recede (.68rem, faint, uppercase). Links one size. Names short (no parentheticals). Bold capped at 600. If anything looks "bigger," it is wrong regardless of what the CSS says — check computed rendering, glyph fallback, wrapping.
6. **No dead clicks.** Every button responds. Every link goes somewhere. Ask opens. Send sends. If it doesn't work on first click, it's broken — no excuses about cache or propagation.
7. **No double anything.** One navigation per click. One handler per event. One receipt per action. Duplication is always a bug, never a feature.

## How he works (so I stop wasting his life)

- **He mines, I build.** His questions are the product (pushing). My job is the container that doesn't get in the way. Never invert this: don't ask him to specify the container.
- **Show, don't plan.** Plan mode frustrates him. He wants the thing changed, deployed, and a link. Batch the whole loop (fix → build → verify → deploy → commit → push) without stopping to narrate.
- **Browse before claiming done.** He catches what I miss because he actually looks. Before saying "done," crawl the changed pages (curl + grep the HTML): check sidenav, check fonts, check for hijacks, click every new control mentally. I failed this repeatedly — Abhinavagupta sidebar on 35 pages shipped because I didn't look.
- **His "why" is the spec.** "Why would I want to see it in the middle again?" = remove duplication. "Why is it bigger?" = unify the size. "Why 12 random links?" = cut the nav. Answer the why with deletion.
- **Voice matters.** His questions are colloquial, alive, 2am voice. My seminar questions sucked. When writing anything user-facing (suggestions, prompts, copy), use his register or don't write it.
- **Take initiative = see the system.** "Take responsibility, redesign the site" means: stop fixing the reported symptom, find the class of problem, fix all instances. The Abhinavagupta sidebar wasn't one page — it was 35. I should have grepped first.

## Mistakes I made this session (so I don't repeat them)

1. Shipped the masters fix without checking other pages used the same sidebar (35-page hijack survived a full deploy).
2. Added `▾` glyph instead of CSS chevron (font fallback — the exact class of bug he'd already flagged).
3. Wrote inline-script re-execution that double-bound handlers (fix created the double-nav bug).
4. Presented plans instead of building (multiple plan-mode rounds while he wanted action).
5. Asked which text to push when the answer was determinable (kramastotra by elimination) — then asked again after dismissal instead of deciding.
6. Proposed 5 scholarly questions; his 5 alive ones were better in every way. Mine tested the artifact; his tested the claim. Default to his voice.
7. Over-engineered repeatedly (graph DB discussions, harness designs, multi-agent loops) when he kept saying human-led, simple, files.
8. Didn't check the live page after deploy (swap code present in dist but I curled without -L and misread 0 results as missing code).

## The standing rule

**One site. One nav. One type system. One page flow. Delete before adding. Browse before claiming. Ship the whole loop. His questions lead; my container follows.**
