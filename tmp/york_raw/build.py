import csv,json
H="University,Department,Name,Title,Status,Field_Group,Already_In_List,Official_Email,Email_Source_URL,Email_Note,Profile_URL,Lab_URL,ORCID_or_Scholar,Research_Keywords,No_Students_Quote,No_Students_URL,Recruiting_Quote,Recruiting_URL,Iran_Visa_Quote,Iran_Visa_URL,Papers_Status".split(',')
FAC="https://lassonde.yorku.ca/mech/faculty/"
GM="https://lassonde.yorku.ca/mech/academics/graduate/mech-graduate-program-membership/"
OP="https://lassonde.yorku.ca/mech/academics/graduate/open-graduate-positions/"
rows=json.load(open('/home/user/we/tmp/york_raw/rows.json'))
with open('/home/user/we/tmp/york_roster.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=H); w.writeheader()
    for r in rows:
        d={k:'' for k in H}; d.update({'University':'York University','Department':'Mechanical Engineering','Already_In_List':'NO','No_Students_Quote':'NONE','Recruiting_Quote':'NONE','Iran_Visa_Quote':'NONE','Official_Email':'NOT FOUND'})
        d.update(r); w.writerow(d)
print(len(rows))
