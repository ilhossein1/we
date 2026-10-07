#!/usr/bin/env python3
"""Find 2024-2026 journal articles for a professor and try to fetch abstracts.
Usage: python3 tools/papers.py "First Last" "University of X" [--orcid 0000-...] [--rows 40]
Prints JSON candidates: title, year, journal, vol/issue/pages, doi, authors (with affiliations),
prof_position, identity evidence, abstract + source. Verify identity yourself before accepting."""
import json, re, sys, time, html, urllib.parse, urllib.request, unicodedata, argparse
UA = "Mozilla/5.0 (academic-research script; mailto=research-outreach@example.org)"
MAILTO = "research-outreach@example.org"
_last = {}
def get(url, tries=4, accept="application/json"):
    host = urllib.parse.urlparse(url).netloc
    for i in range(tries):
        wait = 1.05 - (time.time() - _last.get(host, 0))
        if wait > 0: time.sleep(wait)
        _last[host] = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                time.sleep(2 ** (i + 1)); continue
            return None
        except Exception:
            time.sleep(2 ** i)
    return None
def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z ]", " ", s)
def clean_jats(a):
    a = re.sub(r"<jats:title>.*?</jats:title>", "", a or "", flags=re.S)
    a = re.sub(r"<[^>]+>", " ", a)
    return re.sub(r"\s+", " ", html.unescape(a)).strip()
def name_match(author, first, last):
    fam = norm(author.get("family", "")); giv = norm(author.get("given", ""))
    if not fam and author.get("name"):
        parts = norm(author["name"]).split(); fam = parts[-1] if parts else ""; giv = " ".join(parts[:-1])
    lastn = norm(last).split(); firstn = norm(first).split()
    if not lastn or lastn[-1] not in fam.split() and norm(last).replace(" ", "") != fam.replace(" ", ""):
        return False
    return (not firstn) or (giv[:1] == firstn[0][:1])
def europepmc_abstract(doi):
    t = get("https://www.ebi.ac.uk/europepmc/webservices/rest/search?format=json&resultType=core&query=DOI:%22" + urllib.parse.quote(doi) + "%22")
    try:
        r = json.loads(t)["resultList"]["result"]
        if r and r[0].get("abstractText"):
            return clean_jats(r[0]["abstractText"]), "https://europepmc.org/article/%s/%s" % (r[0].get("source"), r[0].get("id"))
    except Exception: pass
    return None, None
def s2_abstract(doi):
    t = get("https://api.semanticscholar.org/graph/v1/paper/DOI:" + urllib.parse.quote(doi) + "?fields=abstract,externalIds", tries=3)
    try:
        a = json.loads(t).get("abstract")
        if a: return a.strip(), "https://api.semanticscholar.org/graph/v1/paper/DOI:" + doi + "?fields=abstract"
    except Exception: pass
    return None, None
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("name"); ap.add_argument("affil")
    ap.add_argument("--orcid"); ap.add_argument("--rows", type=int, default=60); ap.add_argument("--no-extra", action="store_true")
    a = ap.parse_args()
    parts = a.name.split(); first, last = " ".join(parts[:-1]), parts[-1]
    q = {"filter": "from-pub-date:2024-01-01,type:journal-article", "rows": str(a.rows), "mailto": MAILTO,
         "select": "DOI,title,author,published,container-title,volume,issue,page,article-number,abstract,type,URL"}
    if a.orcid:
        q["filter"] += ",orcid:" + a.orcid
    else:
        q["query.author"] = a.name
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(q)
    t = get(url); items = json.loads(t)["message"]["items"] if t else []
    out = []
    affkey = [w for w in norm(a.affil).split() if w not in ("university", "of", "the", "de", "d")]
    for it in items:
        auths = it.get("author", []); pos = None; ev = []
        for i, au in enumerate(auths):
            if name_match(au, first, last) or (a.orcid and a.orcid in (au.get("ORCID") or "")):
                pos = i; 
                if a.orcid and a.orcid in (au.get("ORCID") or ""): ev.append("orcid-in-metadata")
                affs = " ".join(x.get("name", "") for x in au.get("affiliation", []))
                if affs: ev.append("crossref-affiliation: " + affs[:200])
                break
        if pos is None: continue
        aff_ok = any(k in norm(" ".join(e for e in ev)) for k in affkey) if ev else False
        dp = (it.get("published") or {}).get("date-parts", [[None]])[0]
        doi = it.get("DOI")
        rec = {"title": " ".join(it.get("title") or []), "year": dp[0], "journal": " ".join(it.get("container-title") or []),
               "volume_issue_pages": ", ".join(x for x in [("vol " + it["volume"]) if it.get("volume") else "", ("issue " + it["issue"]) if it.get("issue") else "", ("pp " + it["page"]) if it.get("page") else "", ("art " + it["article-number"]) if it.get("article-number") else ""] if x),
               "doi": doi, "authors_in_order": [(" ".join(x for x in [au.get("given"), au.get("family")] if x) or au.get("name", "")) for au in auths],
               "prof_position": "%s (%d of %d)" % ("last" if pos == len(auths) - 1 else ("first" if pos == 0 else "middle"), pos + 1, len(auths)),
               "identity_evidence": ev, "affiliation_matches": aff_ok or ("orcid-in-metadata" in ev), "abstract": None, "abstract_source_url": None}
        if it.get("abstract"):
            rec["abstract"] = clean_jats(it["abstract"]); rec["abstract_source_url"] = "https://api.crossref.org/works/" + doi
        out.append(rec)
    out.sort(key=lambda r: (not r["affiliation_matches"], -(r["year"] or 0)))
    if not a.no_extra:
        n = 0
        for rec in out:
            if rec["abstract"] or not rec["affiliation_matches"]: continue
            if n >= 6: break
            n += 1
            ab, src = europepmc_abstract(rec["doi"])
            if not ab: ab, src = s2_abstract(rec["doi"])
            if ab: rec["abstract"], rec["abstract_source_url"] = ab, src
    print(json.dumps({"query_url": url, "n": len(out), "candidates": out}, ensure_ascii=False, indent=1))
main()
