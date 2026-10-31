# Grievances — user's site complaints, word for word (2026-10-31 session)

*Every UI/UX complaint from this session, verbatim. Fixed status noted. Source: conversation transcript.*

## 1. Ask button dead
> "i click ask nothing"

**Cause:** `works.join(', ')` ran before `var works` existed → TypeError killed the entire chat script → `btn.onclick` never assigned.
**Fixed:** moved declarations above usage. Verified live: panel opens, Qwen answers with citations.

## 2. Collapse masters + sort by works
> "ok why dont we clean up the site a little bit like i need to be able to collapse the masters on the left and please arrange them by number of works we have"

**Done:** collapsible `<details>` (persisted per-dropdown via localStorage), sorted desc by work count with counts shown (Abhinavagupta 43 → tail of 1s).

## 3. Full-page reloads on every click
> "god its a shitty fucking site? i click concepts and the whole page changes and masters becomes expanded? jesus christ webs earch what a good fucking website creation hygeine check out our nibbanahelp site thats a little bit smoother at least"

**Done:** hand-rolled swap-nav (same-origin clicks fetch + swap `<main>` only; sidenav/chat/search persist; TOC rebuilds; back button works; inline scripts re-run; recite re-collects). Collapse + scroll position persist across swaps. No framework (Turbo/Swup evaluated, hand-rolled chosen: uniform shell, zero dependency).

## 4. Feels like 5 sites in one
> "it feels like 5 sites in one"

**Cause:** every generic page (translations, concepts, essays, practices, recite, assets — 35 pages) hardcoded Abhinavagupta's personal 43-work sidebar; masters index used timeline rows while modern used compact cards; 15-item topnav with no active state.
**Fixed:** neutral sidebar on all generic pages; masters index matches modern cards; topnav grouped to 6 + Library dropdown with active-section highlight.

## 5. Masters font inconsistency
> "so many mistakes like why when i open masters are they all a different font? stop wasting my time and make this production quality peer reivew it all webs earch what a good eautiful site looks like"

**Cause:** full display names with parenthetical epithets ("Ksemaraja (Rajanaka Ksemaraja)") + `▾` glyph falling back to system font + unstyled count spans.
**Fixed:** short names (parentheticals stripped), CSS chevron (no glyph fallback), counts in faint sans. Web-searched Stripe/Linear/Vercel/Docs standards; applied: one emphasis system, 600 not 700, accent sparingly, tight type scale.

## 6. Collapsed masters but Abhinavagupta still everywhere
> "ok i collapse the masters. so why teh fuck do i still see abhinavagupta? and works"

**Cause:** collapsing the sidebar Masters hid the nav list, but every generic page's sidebar WAS Abhinavagupta's works list (separate problem from the collapsible). Fixed as #4.

## 7. Masters/Scholars headers too big, Modern useless
> "painful. WHY ARE THE MASTERS FONT BIGGER .. WHY DO U HAVE 'MODERN' WHICH IS LITERALLY USELESS WHY NOT JUST HAVE SHCOLARS AS A DROPDOWN TEH SAME A S MASTERS WHY WOULD U MAKE MASTERS ANDS CHOLARS FONT BIGGER INSTEAD OF SMALELR.. FUCKING PAINFUL ABYSMAL WORK WEBSARCH DEISGN TEMPLATES"

**Fixed:** flat 36-scholar "Modern" list replaced with Scholars dropdown (same collapsible pattern, separately persisted). Section headers quieted (faint, smaller, tighter, weight 400). All bolds capped at 600 site-wide.

## 8. Dropdown fonts still too big, need shared style CSS, duplicate lists
> "OH MY GOD PLEASE PLEASE TAKE SOME INITIATIVE HERE ? THIS IS THE THIRD TIME IM TELLING YOU THE FONT FOR THE AMTERS IN THE DROP DOWN IS TOOO BIG SAME FOR SHCOLARS I WANT IT LIKE THE FONT WE CURRENTLY HAVE FOR 'CONCEPTS BELOW IT.. ALSO WE NEED SOME STYLE CSS SO ANY CHANGES MADE ARE INHERITED ACROSS THESITE ALSO SO ITS ALL COHESIVE.. LIKE UR SITE JUST DOESNT MAKE SENSE I HAVE A LIS OF SHCOLARS ON THE LEFT WHY WOULD I WANT TO SEE IT IN HE MIDDLE OF THE SCREEN AGAIN? WRITE A REPORT ON ALL MY GRVIANCES THE APAST SESSION WORD FOR WROD"

**Fixed:** centralized nav tokens (`--nav-link`, `--nav-hd`, `--nav-count` in `:root` — one change propagates). All sidebar links explicitly same small size. Matching dropdown auto-collapses on its index page (on /masters/, Masters starts collapsed since the list is in front of you; same for /scholars/).

## 9. Random links + branding + homepage link dump
> "THEN WORK AUTONMOSULY ACTUALLY RESOLVING ALL TAKE RESPONSILBIT YREDESIGN THE SITE.. IDK WHY U GOT 12 OR SO FUCKING RANDOM LINKS HOW IS THAT PROFESSIONAL? REMOVE 'TRIKA LIRARY'"

**Fixed:** "Trika Library" removed from titles, header tagline, footer, homepage H1, llms.txt header. Homepage link-dump (95 links: every master + every work + every section) replaced with 5 entry cards (read / recite / practice / pushing / essays) + Latest. Neutral sidenav on homepage.

## Standing pattern (so this stops happening)

Every generic page gets the neutral sidebar. No author sidebar except on that author's own pages. One emphasis system (600, never 700). One card pattern for index pages. Headers recede, links lead. Changes go in CSS variables + shared builders so they inherit. Verify with `bash tools/verify.sh` + click through home → masters → a work → a translation → chat before every ship.
