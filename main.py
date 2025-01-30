import requests
from bs4 import BeautifulSoup
import json

#new url were using
url = "https://courses.engineering.ucsc.edu/courses/cse/2024"
response = requests.get(url)
s = BeautifulSoup(response.content, 'html.parser')


#find all the course cells
course_cells = s.find_all('td', class_='soe-classes-schedule-course-name')

#iterate through each course cell and extract the course code and title
for cell in course_cells:
    course_link = cell.find('a')
    if course_link:
        full_name = course_link.get_text(strip=True)

        courses = []

        for cell in course_cells:
            course_link = cell.find('a')
            if course_link:
                full_name = course_link.get_text(strip=True)
                
                if ":" in full_name:
                    code, title = full_name.split(":", 1)
                    course = {
                        "Course Code": code.strip(),
                        "Course Title": title.strip()
                    }
                courses.append(course)

#write courses to  json file
with open('courses.json', 'w') as json_file:
    json.dump(courses, json_file, indent=4)