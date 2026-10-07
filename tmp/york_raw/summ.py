import json,sys
d=json.load(open(sys.argv[1]))
for i,c in enumerate(d['candidates']):
    print(i,c['year'],'|',c['title'][:90],'|',c['journal'][:40],'|',c['prof_position'],'| AFF:',c['affiliation_matches'],'|',(c['identity_evidence'] or [''])[0][:110],'| ABS:',bool(c.get('abstract')) and c['abstract'] not in ('BLOCKED',None), c.get('doi'))
