import requests
from bs4 import BeautifulSoup
import json
import os

#url of da site
url = 'https://ucsc.smartcatalogiq.com/en/2020-2021/general-catalog/courses/cse-computer-science-and-engineering/'
html = requests.get(url)

#gather all course information
s = BeautifulSoup(html.content, 'html.parser')
courseResults = s.find(id='main')
courseTitle = courseResults.find_all('h2', class_='course-name')
courseCredits = courseResults.find_all('div', class_='credits')

print()
#currently has problem with lab descriptions, the co requisites
courseDesc = [desc for desc in courseResults.find_all('div', class_='desc') if desc.text.strip()]

#currently has problem with classes with no prerequisites
#second problem is putting shit in a list with the different p and a classes
coursePrereq = courseResults.find_all('div', class_='extraFields')
coursePrereqList = []
for prereq in coursePrereq:
    prereq_links = prereq.find_all('p')
    prereq_courses = [link.text.strip() for link in prereq_links if 'Yes' not in link.text.strip()]
    coursePrereqList.append(prereq_courses)

for i, prereqs in enumerate(coursePrereqList):
    print(f"Course {i + 1} prerequisites:")
    for prereq in prereqs:
        print(f"  - {prereq}")
    print()

print(len(coursePrereqList))

#parse all the info into a json file
courses = []
for title, credits, desc in zip(courseTitle, courseCredits, courseDesc):
    course_info = {
        'course_code': ' '.join(title.text.strip().split()[:2]),
        'title': ' '.join(title.text.strip().split()[2:]),
        'description': desc.text.strip(),
        'credits': credits.text.strip(),
    
    }
    courses.append(course_info)

#create json in current directory
current_directory = os.path.dirname(__file__)
file_path = os.path.join(current_directory, 'courses.json')

with open(file_path, 'w') as json_file:
    json.dump(courses, json_file, indent=4)
