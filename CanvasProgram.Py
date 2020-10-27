from canvasapi import Canvas
from Secrets import url,apiKey
import json

canvas = Canvas(url,apiKey)

usr = canvas.get_current_user()

l = usr.get_courses()

#I put the courses and assignments into a dictionary
d = {}
for i in range(0,4):
  d[l[i].name] = []
  for n in l[i].get_assignments():
    d[l[i].name].append(n.name)

#Then put the dictionary into a json file
#with open('assignments.json', 'w') as fp:
#    json.dump(d, fp)

f = open('script.js', 'w')
f.write("var data = " +str(d)+ "\ndocument.getElementById('tst').innerText = data['CSC130 Data Structure+Algorithm Analy - SECTION 03, 04'];")