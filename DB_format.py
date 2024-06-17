import os
from bs4 import BeautifulSoup
# Insert into MongoDB
from pymongo import MongoClient
import time
from bson.binary import Binary

root_dir = "data"

student_record = {
    "name": "Name",
    "rollno": "RollNo",
    "dob": "dob",
    "branch": "Branch",
    "cgpa": 0.0,
    "current_semester": 1,
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


student = {
    "student_id": "student_id",     #rollno
    "name": "Name",
    "dob": "dob",               #omit for now
    "branch": "Branch",
    "cgpa": 0.0,
    "semester_count_for_cgpa":0,
    "current_semester": 1
}


course = {
    "course_id": "course_id",       #rollno_coursecode
    "student_id": "student_id",
    "code": "CourseCode",
    "name": "CourseName",
    "grade": "Grade"
}


semester = {
    "semester_id": "semester_id",   #rollno_semester
    "student_id": "student_id",     #rollno
    "semester": 1,
    "sgpa": 0.0
}



###################################################################################################################
# Connect to MongoDB server
client = MongoClient('mongodb://localhost:27017')  # adjust as needed

# Select database and collection
db = client['idcard']
collection = db['id']
error_files = []

def extract_student_grades(folderpath):
    os.walk(folderpath)
    for root, dirs, files in os.walk(folderpath):


        for file in files:
            if file.endswith(".html"):
                try:
                    folder_new = folderpath + file[-18:-7]
                    file_path = os.path.join(folder_new, file)
                    with open(file_path, mode='r') as file:
                        soup = BeautifulSoup(file, 'html.parser')
                        tables = soup.find_all('table')
                        rollno = tables[1].find_all('tr')[1].find_all('th')[0].find_all('td')[1].text.split()[2]
                        semester = tables[0].find_all('tr')[1].get_text().strip()
                        courses = tables[2].find_all('tr')[1:-1]
                        grades=[]
                        for course in courses:
                            code = course.find_all('td')[0].text.strip()
                            name = course.find_all('td')[1].text.strip()
                            grade = course.find_all('td')[2].text.strip()
                            course_id = rollno + "_" + code
                            grades.append({
                                "course_id": course_id,
                                "student_id": rollno,
                                "code": code,
                                "name": name,
                                "grade": grade
                            })
                            # print(course.find_all('td')[1])

                        
                        collection.insert_many(grades)
                        # print(semester)
                except:
                    print(f"Error for {file}")
                    error_files.append(file)
                    continue
    print(error_files)

def store_id(folderpath):
    os.walk(folderpath)
    for root, dirs, files in os.walk(folderpath):
        for file in files:
            if file.endswith(".pdf"):
                try:
                    rollno = file[:11]
                    folder_new = folderpath + rollno
                    file_path = os.path.join(folder_new, file)
                    id = {}
                    with open(file_path, mode='rb') as file:
                        pdf_data = Binary(file.read())
                        id = {
                            "student_id": rollno,
                            "id_card": pdf_data
                        }
                    collection.insert_one(id)
                except:
                    print(f"Error with {file}")
                    continue
            

def create_personal_record(folderpath):
    os.walk(folderpath)
    for root, dirs, files in os.walk(folderpath):
        # print(files)

        flag = True
        for file in files:
            if file.endswith(".html") and flag:
                try:
                    rollno = file[-18:-7]
                    folder_new = folderpath + rollno
                    file_path = os.path.join(folder_new, file)
                    student = {}
                    with open(file_path, mode='r') as file:
                        soup = BeautifulSoup(file,'html.parser')
                        tables = soup.find_all('table')
                        name = tables[1].find_all('tr')[1].find_all('th')[0].find_all('td')[0].text.strip()[5:].strip()
                        branch = rollno[4:7]
                        current_semester = str((2026-int(rollno[0:4])))
                        flag = False
                        student = {
                            "student_id": rollno,
                            "name": name,
                            "branch": branch,
                            "current_semester": current_semester
                        }
                    collection.insert_one(student)
                except:
                    print("Error")
                    continue




def create_semester_record(student,semester,grades):
    semester = {
        "_id": "semester_id",
        "student_id": student["_id"],
        "semester": semester,
        "sgpa": 0.0
    }
    return semester

def create_grades_record(semester,grades):
    courses = []
    for grade in grades:
        course = {
            "_id": "course_id",
            "semester_id": semester["_id"],
            "code": grade["code"],
            "name": grade["name"],
            "grade": grade["grade"]
        }
        courses.append(course)
    return courses








f = "D:\VScodeFiles\python\Projects\Result Piracy\data\\2022\\"
store_id(f)






############################################################################################################################################################
# Insert the student record
# result = collection.insert_one(student_record)
# print(f"Inserted record with ID: {result.inserted_id}")


# def open_html():
#     with open("D:\VScodeFiles\python\Projects\Result Piracy\data\\2022\\2022BCY0044\\2022BCY0044_1.html",mode='r') as file:
#         soup = BeautifulSoup(file.read(), 'html.parser')
#         print(soup.prettify())
        