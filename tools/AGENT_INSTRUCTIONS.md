# Instructions for every research subagent

Read `/home/user/we/input/Prompt_A.md` in full first. It is the master task. Every hard rule in it applies to you
(research only, no guessing, verbatim copying, no access-control bypass, polite API use, save after each step).
You handle ONE assigned unit (a department or university). Do only that unit.

## Your output files (all under /home/user/we/tmp/, prefix = your slug)
- `<slug>_roster.csv`: exact header from Prompt_A (A_roster.csv header). One row per person. Use Python's `csv` module to write it (proper quoting). Append as you go.
- `<slug>_papers.jsonl`: one JSON line per professor with Papers_Status DONE or ALL_BLOCKED, exact schema from Prompt_A.
- `<slug>_admissions.md`: only if your unit has an admissions block in Prompt_A (see your assignment).
- `<slug>_progress.md`: what is done, who is left, blocked sites + what you tried, doubts. Update it at least every ~10 people.
Never write to the final A_* files; the coordinator merges.

## Environment facts (already tested)
- Web pages: fetch with `curl -sL -A "Mozilla/5.0" URL` (then parse with python/grep), or with the WebFetch tool. University sites respond normally.
- Crossref works (use mailto=research-outreach@example.org). Europe PMC works. ORCID public API works (`https://pub.orcid.org/v3.0/...`, header `Accept: application/json`).
- OpenAlex is OUT OF BUDGET for this network today (429). Do not use it. Semantic Scholar often returns 429; the helper retries a little, don't hammer it.
- web.archive.org is NOT reachable from here.
- Search-engine results may only be used to discover URLs; never cite a snippet as a source.

## Paper helper
`python3 /home/user/we/tools/papers.py "First Last" "University Name" [--orcid 0000-0000-0000-0000]`
Returns Crossref journal-article candidates since 2024 with author order, professor position, Crossref affiliation evidence,
and abstracts from Crossref / Europe PMC / Semantic Scholar where available. It matches names loosely (surname + first initial):
YOU must confirm identity (affiliation in metadata naming the university, ORCID match, or the paper listed on their own page).
`affiliation_matches: true` only means the Crossref affiliation string contains the university's words; still glance at it.
If ORCID is known, run with `--orcid` (more precise). If no candidate has an abstract, try the publisher landing page
(open-access ones like MDPI, Frontiers, PLOS, Nature/Sci Rep, IEEE Access, Elsevier OA often expose the abstract in the HTML or
`citation_abstract`/`og:description`/`dc.description` meta tags) with curl or WebFetch. If WebFetch gives you a summarized abstract,
it is NOT verbatim; only use text you extracted exactly. Elsevier/ScienceDirect, Wiley, Springer often block or paraphrase: then mark
abstract BLOCKED and try the next candidate (up to 5). Abstract text must be copied verbatim (strip HTML tags only).

## Workup scope per Prompt_A
- Full workup only for ACTIVE MECH or ENG_MGMT people NOT on the SKIP LIST.
- SKIP LIST people: one roster row with Already_In_List=YES, Papers_Status=SKIPPED, other fields may stay minimal (name, title if easy, status).
- Non-active people (EMERITUS, RETIRED, ADJUNCT, TEACHING_STREAM, etc.) and OTHER: roster row with flag, Papers_Status=SKIPPED.
- Emails: only as written on an official university page; record URL; `obfuscated` note when needed; otherwise `NOT FOUND`.
- Quotes about not taking students / recruiting / Iran-visa: only if you see them on pages you opened (profile, lab site). Don't hunt hard for positive ones.

## Efficiency
- Get the roster first and save all rows with basic fields (name, title, status, profile URL) before doing workups, so partial
  progress is useful. Then fill emails/keywords/papers person by person and rewrite the CSV.
- Write small Python scripts to batch-fetch profile pages and extract emails/titles, but check the parse results by eye.
- When done, return a short report: counts (listed, full workups, NOT_FOUND, ALL_BLOCKED), blocked sites, doubts.
