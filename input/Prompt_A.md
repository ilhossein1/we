# Research task A: every Mechanical Engineering professor at 14 Canadian universities

You are doing research only, for a graduate-school outreach project. A student with a B.Sc. in Mechanical Engineering will later write a personal email to each eligible professor. Your job is to collect verified facts so those emails can be written. Another Claude session will read your output files and write the emails, so precision and source URLs matter more than prose.

## Hard rules

1. Research only. Never send an email, never fill a form, never log into any account, never contact anyone.
2. No guessing, ever. Do not infer an email from a pattern (first.last@...), do not guess a title, a status or a paper. Every fact must come from a page or API response you actually opened, and you must record that URL. If you cannot verify something, write `NOT FOUND` and move on.
3. Copy verbatim. Titles, quotes and abstracts are copied exactly as published, never paraphrased or shortened.
4. Do not defeat access controls. No fake browser fingerprints, no CAPTCHA solving, no paywall bypass. If a page blocks you, use another official page of the same university (department directory, graduate-studies supervisor list, faculty search, research centre page) or an archived copy of the official page on web.archive.org dated 2025 or 2026 (mark the source `ARCHIVE` and give the archive URL). Search-engine snippets are not sources.
5. Be polite to APIs: about 1 request per second per host, add `mailto=` (any contact string you are allowed to use) on Crossref and OpenAlex calls, back off on HTTP 429.
6. Save your work after every department (append to the output files below). If you are about to run out of context or usage, stop researching, make sure the files are saved, and update the PROGRESS file so a later session can continue exactly where you stopped.
7. You may write Python scripts and use subagents to work in parallel (for example one subagent per university). Every subagent follows these same rules and writes to its own temp file, which you merge into the final files.

## Scope (who to collect)

For each department below, open the official faculty roster and list every faculty member: tenure-track, tenured, research chairs, and also teaching-stream, adjunct, emeritus and cross-appointed people (they get a status flag, not a full research workup).

Do the full workup (email, status check, papers) only for people whose status is ACTIVE (tenure-track or tenured, any rank, including department chairs and research chairs). For EMERITUS, RETIRED, ADJUNCT (adjunct-only), TEACHING_STREAM / LECTURER / INSTRUCTOR / SESSIONAL, list them in the roster with the flag and stop there.

Label each ACTIVE person with a field group:
- `MECH`: any mechanical-type research (thermal/fluids/energy, materials/manufacturing, solid mechanics/design, biomechanics/biomedical devices, robotics/control/mechatronics, aerospace, acoustics/vibration, and similar).
- `ENG_MGMT`: operations research, supply chain, logistics, engineering management, quality/reliability management, production planning, healthcare systems engineering, human factors/ergonomics, systems engineering with a management focus. These people are in scope too (they will get a different CV), so give them the full workup.
- `OTHER`: clearly outside both (for example pure electrical engineering or pure computer science). Roster only, no workup.

Skip the workup (but still list them in the roster with `Already_In_List=YES`) for the people in the SKIP LIST at the end of this prompt; they were already contacted.

## The full workup for each ACTIVE MECH or ENG_MGMT person

1. Title exactly as shown on the official page, and flags for Emeritus / Adjunct / Retired / On leave / Professor of Practice if shown.
2. Official email exactly as written on an official university page, plus that page's URL. If the page shows `name [at] uni [dot] ca`, normalise it and note `obfuscated`. If two official pages show different addresses, record both with both URLs.
3. Profile URL, lab or personal website URL (if linked), ORCID and/or Google Scholar URL (if found).
4. Research keywords as stated on the official page (English, short).
5. Any explicit statement that they are NOT taking new graduate students (exact quote + URL). Also record any explicit positive statement ("accepting students", "open positions") as a quote + URL, but do not spend extra effort hunting for it.
6. Any statement about not accepting applicants from Iran or visa-related refusals (exact quote + URL).
7. Papers: find their most recent peer-reviewed JOURNAL articles published in 2024, 2025 or 2026 (not conference proceedings, not theses, not preprints unless also published in a journal). Prefer 2025-2026, prefer papers where the professor is last author. Collect up to 2 papers that have a retrievable abstract. If the newest paper's abstract cannot be retrieved, keep looking through up to 5 candidates. For each paper record: title, year, journal (volume/issue/pages if available), DOI, full author list in order, the professor's position in that list, how you verified it is the same person (affiliation in metadata, ORCID match, or listed on their own page), the abstract VERBATIM, and the URL the abstract came from.
   - Good abstract sources, in rough order of efficiency: OpenAlex (`https://api.openalex.org/authors?search=` filtered by institution, then works since 2024 with `abstract_inverted_index`; reconstruct the text and mark the source `OpenAlex (reconstructed)`), Crossref (`api.crossref.org/works?query.author=...&filter=from-pub-date:2024-01-01`, the `abstract` field), Semantic Scholar Graph API, Europe PMC, arXiv, open-access publisher pages (MDPI, Frontiers, PLOS, Nature Communications, Scientific Reports, IEEE Access and other OA journals), CORE, Unpaywall, institutional repositories, and the professor's own publications page.
   - Beware of common names (for example "Yi Liu", "Wei Wang"). Only accept a paper if the affiliation or ORCID or the professor's own page ties it to this person.
   - If no 2024-2026 journal paper exists, write `NOT_FOUND`. If papers exist but every abstract is blocked, list up to 3 titles + DOIs and write `ALL_BLOCKED`.

## Universities and departments for this task (work in this order)

If a file named task3_rosters.csv is attached, use its rows for Ottawa, Guelph, Memorial and Manitoba as a starting roster, but re-verify every email and status.

Priority 1 (finish all of these first):
1. University of Waterloo: Mechanical and Mechatronics Engineering (https://uwaterloo.ca/mechanical-mechatronics-engineering/) and Systems Design Engineering (https://uwaterloo.ca/systems-design-engineering/)
2. McMaster University: Mechanical Engineering (https://www.eng.mcmaster.ca/mech/)
3. Queen's University: Mechanical and Materials Engineering (https://smithengineering.queensu.ca/mme/)
4. University of Ottawa: Mechanical Engineering
5. York University (Lassonde): Mechanical Engineering
6. University of Guelph: School of Engineering
7. Ontario Tech University: Mechanical and Manufacturing Engineering
8. University of Windsor: Mechanical, Automotive and Materials Engineering
9. Lakehead University: Mechanical Engineering
10. Dalhousie University: Mechanical Engineering
11. Memorial University of Newfoundland: Mechanical Engineering, and Ocean and Naval Architectural Engineering
12. University of Manitoba: Mechanical Engineering
13. Laurentian University and University of Prince Edward Island (Faculty of Sustainable Design Engineering): first check whether a thesis-based research master's in a mechanical-type field exists (quote + URL). Only if it does, do the roster and workup.

Priority 2 (only after priority 1 is complete): University of Manitoba Biomedical Engineering; separate Industrial Engineering departments at the universities above, if any exist (for example Dalhousie Industrial Engineering).

## Admission facts (one block per department, only for these departments)

University of Ottawa Mechanical; University of Guelph School of Engineering; Memorial Ocean and Naval Architectural Engineering; University of Manitoba Biomedical Engineering; Laurentian and UPEI (if in scope). Also fill the gaps marked here: University of Windsor MAME (Fall 2027 international deadline, application fee, references, GRE); Lakehead Mechanical (fee, English requirement, references); Waterloo Systems Design Engineering (is a supervisor required before an offer, and is there guaranteed funding for MASc).

For each: exact name of the thesis master's degree; Fall 2027 (September 2027) application deadline for international applicants; application fee; English test minimum (IELTS overall and bands); GRE required or not; minimum GPA or average; number of references; whether a supervisor must agree before admission; whether funding is guaranteed or a minimum funding amount is stated; language of instruction and any French requirement. Give an exact quote and URL for every fact. Unknown: `To verify`.

## Output files (create these in the working directory and keep appending)

1. `A_roster.csv` with this exact header:
   `University,Department,Name,Title,Status,Field_Group,Already_In_List,Official_Email,Email_Source_URL,Email_Note,Profile_URL,Lab_URL,ORCID_or_Scholar,Research_Keywords,No_Students_Quote,No_Students_URL,Recruiting_Quote,Recruiting_URL,Iran_Visa_Quote,Iran_Visa_URL,Papers_Status`
   - Status: ACTIVE, EMERITUS, RETIRED, ADJUNCT, TEACHING_STREAM, ON_LEAVE, UNCLEAR
   - Field_Group: MECH, ENG_MGMT, OTHER (blank if not ACTIVE)
   - Papers_Status: DONE, NOT_FOUND, ALL_BLOCKED, SKIPPED (with reason in Email_Note if useful)
   - Use `NONE` for empty quote fields and `NOT FOUND` for unverified emails.
2. `A_papers.jsonl`, one JSON object per line, one line per professor with Papers_Status DONE or ALL_BLOCKED:
   `{"university":"","department":"","name":"","papers":[{"title":"","year":2026,"journal":"","volume_issue_pages":"","doi":"","authors_in_order":["",""],"prof_position":"last (4 of 4)","identity_check":"crossref-affiliation | orcid | own-page","abstract":"VERBATIM TEXT or BLOCKED","abstract_source_url":""}]}`
3. `A_admissions.md`: one section per department listed above, each fact with quote and URL.
4. `A_PROGRESS.md`: departments finished, departments partly done (which names are left), blocked sites and what you tried, any doubts (for example two different emails, unclear status). Update it after every department.

When you finish (or must stop), print a short summary: number of people listed, number with full workup, number NOT_FOUND / ALL_BLOCKED, and the file names.

## SKIP LIST (already contacted; list them in the roster with Already_In_List=YES and do nothing else)

- Waterloo: Adrian Gerlich; Arash Arami; Armaghan Salehian; Baris Fidan; Cecile Devaud; Clifford Butcher; Duane Cronin; Ehsan Toyserkani; Eihab Abdel-Rahman; Elise Laende; Elliot Biro; Fue-Sang Lien; Hamid Jahed; Hyock Ju Kwon; James Tung; Jean-Pierre Hickey; John Magliaro; John McPhee; Jonathan Kusins; Kyle Daun; Michael Mayer; Mihaela Vlasea; Nasser Lashgarian Azad; Naveen Chandrashekar; Nima Maftoon; Peng Peng; Robert Nishida; Roydon Fraser; Russell Buchanan; Sean Peterson; Soo Jeon; Stewart McLachlin; Teng Cui; Vinny Gupta; William Melek; Y. Norman Zhou; Yue Hu; Zhao Pan
- McMaster: Ali Emadi; Chan Y. Ching; Cheryl Quenneville; Christopher Morton; Eu-Gene Ng; Fengjun Yan; Gary M. Bone; Gregory R. Wohl; James S. Cotton; Keena Trowell; Maryam Aramesh; Mohamed S. Hamed; Mukesh K. Jain; P. Ravi Selvaganapathy; Peidong Wu; Philip Koshy; Ryan Ahmed; S. Andrew Gadsden; Saeid Habibi; Shakirudeen A. Salaudeen; Stephen C. Veldhuis; Stephen Tullis; Sumanth Shankar; Tohid F. Didar; Zahra Keshavarz-Motamed
- Queen's: Amy R. Wu; Barbara L. da Silva; Bradley J. Diak; Brian Surgenor; Diane Wowk; Francesco Ambrogi; Gaby Ciccarelli; Gene Zak; Heidi-Lynn Ploeg; Il Yong Kim; Jackson Crane; John W. Kurelek; Keith Pilkey; Kevin J. Deluzio; Laurent Karim Béland; Levente Balogh; Lidan You; Mahmoud Alzoubi; Mark R. Daymond; Matthew Robertson; Meng Li; Michael J. Rainbow; Qingguo Li; Roshni Rainbow; T. Claire Davies; Ugo Piomelli; Vahid Fallah; Xian Wang; Yanwen Zhang; Yong Jun Lai; Zhongwen Yao
- York: Aleksander Czekanski; Alidad Amirfazli; Ronald Hanson; Zheng Hong (George) Zhu
- Ontario Tech: Ali Hosseini; Tao Liu
- Windsor: Ahmet Alpas; Shahpour Alirezaee
- Lakehead: Junfei Li; Muhammad Saif Ullah Khalid; Wilson Wang
- Dalhousie: Adam Donaldson; Ahmed Saif; Ali Nasiri; Alireza Ghasemi; Alison J. Scott; Amyl Ghanem; Andrew Warkentin; Baafour Nyantekyi-Kwakye; Claver Diallo; Clifton Johnston; Darrel Doman; Derek Rutherford; Dominic Groulx; Fadi Oudah; Farid Taheri; Geoffrey Maksym; George Jarjoura; Ghada I. Koleilat; Gianfranco Mazzanti; Hamed H. Aly; Hamid Afshari; Ismet Ugursal; Janie Astephen Wilson; Jason Gu; Jeremy A. Brown; Kevin Plucknett; Kyle Tousignant; Laurent Kreplak; Lukas Swan; Mae Seto; Michael J. Dunbar; Michael J. Pegg; Michael Metzger; Michael S. Freund; Mita Dasog; Mohammad Saeedi; Nouman Ali; Paul Amyotte; Paul Bishop; Pedram Sadeghian; Peter Allen; Robert Bauer; Samuel P. Veres; Sarah Wells; Ted Hubbard; Tri Nguyen-Quang; Uday Venkatadri; Ya-Jun Pan; Yi Liu; Zoheir Farhat
- Memorial: Sima Alidokht; Ting Zou; Xili Duan
- Manitoba: Hassan Alkomy; Nan Wu; Olanrewaju (Lanre) Ojo; Philip Ferguson; Scott Ormiston; Xihui (Larry) Liang; Yuejian Chen; Yunhua Luo
