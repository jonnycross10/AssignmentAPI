#!flask/bin/python
from flask import Flask
from canvasapi import Canvas
from Secrets import url,apiKey
import json
from datetime import datetime
import requests


app = Flask(__name__)

canvas = Canvas(url,apiKey)

usr = canvas.get_current_user()

l = usr.get_courses()



e={}

for i in range(0,4):
  headers = {"Authorization":"Bearer "+apiKey+"", "Content-Type": "json"
  }

  r = requests.get("https://csus.instructure.com/api/v1/courses/"+str(l[i].id)+"/users/99221?include[]=enrollments", headers = headers)

  jsn = r.json()
  e[l[i].course_code] = jsn['enrollments'][0]['grades']['current_score']



#have to cut off trailing z to convert correctly
#date = datetime.fromisoformat(ddate[0:19])
t = datetime.now()

upcoming_assignments = []

def isAssDue(assDate):
  if(assDate == None):
    return False
  if(datetime.fromisoformat(assDate[0:19])>t):
    return True
  return False


for i in range(0,4):
  course_ass = l[i].get_assignments(order_by = "due_at")
  for j in course_ass:
    if(isAssDue(j.due_at)):
      upcoming_assignments.append([l[i].name,j.name])

cs130Assignments = []
cs131Assignments = []
phil103Assignments = []
pubh50Assignments = []
#print(upcoming_assignments)
#print("\n")

for i in upcoming_assignments:
  if(i[0] == "CSC130 Data Structure+Algorithm Analy - SECTION 03, 04"):
    cs130Assignments.append(i[1])
  if(i[0] == "CSC131 Computer Software Engr - SECTIONS 03, 07"):
    cs131Assignments.append(i[1])
  if(i[0] == "PHIL103 Business+Computer Ethics - SECTIONS 02, 03, 04, 05, 60"):
    phil103Assignments.append(i[1])
  if(i[0] == "PUBH50 Healthy Lifestyles - SECTIONS 01, 05"):
    pubh50Assignments.append(i[1])

flaskApiDict = {}
cs130d = {}
cs130d["assignments"] = cs130Assignments
cs130d["grades"] = e[l[0].course_code] 

cs131d = {}
cs131d["assignments"] = cs131Assignments
cs131d["grades"] = e[l[1].course_code] 

phil103d = {}
phil103d["assignments"] = phil103Assignments
phil103d["grades"] = e[l[2].course_code] 

pubh50d = {}
pubh50d["assignments"] = pubh50Assignments
pubh50d["grades"] = e[l[3].course_code] 


flaskApiDict["cs 130"] = cs130d
flaskApiDict["cs 131"] = cs131d
flaskApiDict["phil 103"] = phil103d
flaskApiDict["pubh 50"] = pubh50d


@app.route('/cs130')
def cs130():
	return flaskApiDict["cs 130"]

@app.route('/cs131')
def cs131():
	return flaskApiDict["cs 131"]

if __name__ == '__main__':
    app.run(debug=True)
