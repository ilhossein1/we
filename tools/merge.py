#!/usr/bin/env python3
"""Merge per-unit temp files in tmp/ into the final A_* files."""
import csv, glob, json, os, re
HDR = "University,Department,Name,Title,Status,Field_Group,Already_In_List,Official_Email,Email_Source_URL,Email_Note,Profile_URL,Lab_URL,ORCID_or_Scholar,Research_Keywords,No_Students_Quote,No_Students_URL,Recruiting_Quote,Recruiting_URL,Iran_Visa_Quote,Iran_Visa_URL,Papers_Status".split(",")
ORDER = ["waterloo_mme","waterloo_syde","mcmaster","queens","ottawa","york","guelph","ontariotech","windsor","lakehead","dalhousie","memorial","manitoba","laurentian_upei"]
os.chdir(os.path.join(os.path.dirname(__file__), ".."))
rows, problems = [], []
for s in ORDER:
    f = f"tmp/{s}_roster.csv"
    if not os.path.exists(f): problems.append(f"{s}: no roster yet"); continue
    with open(f, newline="", encoding="utf-8") as fh:
        r = csv.DictReader(fh)
        if r.fieldnames != HDR: problems.append(f"{s}: header differs: {r.fieldnames}")
        for row in r: rows.append({k: (row.get(k) or "").strip() for k in HDR})
with open("A_roster.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=HDR); w.writeheader(); w.writerows(rows)
papers = []
for s in ORDER:
    f = f"tmp/{s}_papers.jsonl"
    if not os.path.exists(f): continue
    for i, line in enumerate(open(f, encoding="utf-8")):
        if not line.strip(): continue
        try: papers.append(json.loads(line))
        except Exception as e: problems.append(f"{s} papers line {i+1}: {e}")
with open("A_papers.jsonl", "w", encoding="utf-8") as fh:
    for p in papers: fh.write(json.dumps(p, ensure_ascii=False) + "\n")
adm = ["# A_admissions\n"]
for s in ORDER:
    f = f"tmp/{s}_admissions.md"
    if os.path.exists(f): adm.append(f"\n<!-- source: {f} -->\n" + open(f, encoding="utf-8").read().strip() + "\n")
open("A_admissions.md", "w", encoding="utf-8").write("\n".join(adm))
# consistency checks
pnames = {(p.get("university"), p.get("name")) for p in papers}
for r in rows:
    if r["Papers_Status"] in ("DONE", "ALL_BLOCKED") and (r["University"], r["Name"]) not in pnames:
        problems.append(f"no papers line for {r['University']} / {r['Name']} ({r['Papers_Status']})")
from collections import Counter
st = Counter(r["Status"] for r in rows); ps = Counter(r["Papers_Status"] for r in rows)
fg = Counter(r["Field_Group"] for r in rows if r["Status"] == "ACTIVE")
print("rows", len(rows), "papers lines", len(papers)); print("status", dict(st)); print("field", dict(fg)); print("papers_status", dict(ps))
print("already_in_list", sum(r["Already_In_List"] == "YES" for r in rows))
print("by unit", dict(Counter((r["University"], r["Department"]) for r in rows)))
print("\n".join(problems[:80]))
