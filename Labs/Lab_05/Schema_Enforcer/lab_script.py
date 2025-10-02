import csv
import json 
import pandas as pd

headers = ['student_id', 'major', 'GPA', 'is_cs_major', 'credits_taken']

data = [
    [1001, 'Computer Science', 3.8, 'Yes', '15.0'],     
    [1002, 'Mathematics', 3, 'No', '12.5'],             
    [1003, 'Biology', 2.7, 'Yes', '10'],                
    [1004, 'Computer Science', 4, 'No', '18.0'],        
    [1005, 'Engineering', 3.2, 'Yes', '14.5'],         
]

with open('raw_survey_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers) 
    writer.writerows(data)    

print("raw_survey_data.csv has been created with inconsistent types.") 


course_catalog = [
    {
        "course_id": "DS2002",
        "section": "001",
        "title": "Data Science Systems",
        "level": 200,
        "instructors": [
            {"name": "Austin Rivera", "role": "Primary"},
            {"name": "Heywood Williams-Tracy", "role": "TA"}
        ]
    },
    {
        "course_id": "PLPT3200",
        "section": "100",
        "title": "African American Political Theory",
        "level": 200,
        "instructors": [
            {"name": "Lawrie Balfour", "role": "Primary"}
        ]
    },
    {
        "course_id": "GSGS2610",
        "section": "001",
        "title": "Systems of Inequality",
        "level": 200,
        "instructors": [
            {"name": "Andreja Sillunas", "role": "Primary"},
        ]
    }
]

with open('raw_course_catalog.json', 'w') as json_file:
    json.dump(course_catalog, json_file, indent=4)

print("raw_course_catalog.json has been created with hierarchical course data.")


df = pd.read_csv('raw_survey_data.csv')

df['is_cs_major'] = df['is_cs_major'].replace({'Yes': True, 'No': False})

df = df.astype({'GPA': 'float64', 'credits_taken': 'float64'})

df.to_csv('clean_survey_data.csv', index=False)

print("clean_survey_data.csv has been created with cleaned data types.")


with open('raw_course_catalog.json', 'r') as json_file:
    course_data = json.load(json_file)

df_courses = pd.json_normalize(
    course_data,
    record_path=['instructors'],
    meta=['course_id', 'title', 'level']
)

df_courses.to_csv('clean_course_catalog.csv', index=False)

print("clean_course_catalog.csv has been created with normalized instructor data.")

