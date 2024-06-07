
import os
import bs4 as bs

student_record = {
    "name": "Name",
    "rollno": "RollNo",
    "dob": "dob",
    "branch": "Branch",
    "cgpa": 0.0,
    "current_semester": 1,  # renamed for clarity
    "grades": [
        {
            "semester": 1,
            "sgpa": 0.0,
            "courses": [
                {
                    "code": "CourseCode1",
                    "name": "CourseName1",
                    "grade": "Grade1",
                },
                {
                    "code": "CourseCode2",
                    "name": "CourseName2",
                    "grade": "Grade2",
                }
            ]
        }
    ],
}

# Insert into MongoDB
from pymongo import MongoClient

# Connect to MongoDB server
client = MongoClient('mongodb://localhost:27017/')  # adjust as needed

# Select database and collection
db = client['university']
collection = db['students']

# Insert the student record
result = collection.insert_one(student_record)
print(f"Inserted record with ID: {result.inserted_id}")


def open_html():
    with open("D:\VScodeFiles\python\Projects\Result Piracy\data\\2022\\2022BCY0044\\2022BCY0044_1.html",mode='r') as file:
        soup = bs.BeautifulSoup(file.read(), 'html.parser')
        print(soup.prettify())
        