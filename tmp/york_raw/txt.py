import re,html,sys
t=open(sys.argv[1]).read()
t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
i=t.find('<main'); t=t[i:] if i>=0 else t
for stop in ['Lassonde School of Engineering Homepage','Keele Campus']:
    j=t.find(stop)
    if j>0: t=t[:j]
links=sorted(set(re.findall(r'href="(https?://[^"]+)"',t)))
s=re.sub(r'<[^>]+>','\n',t); s=html.unescape(s)
lines=[l.strip() for l in s.split('\n') if l.strip()]
print('\n'.join(lines))
print('LINKS:',[l for l in links if 'lassonde.yorku.ca/wp' not in l])
