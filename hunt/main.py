import os
import requests
import csv
from bs4 import BeautifulSoup
from getpass import getpass
import threading
from concurrent.futures import ThreadPoolExecutor,as_completed
import time

# For logging and info
fetch_failed = []
skipped = []

# Critical URLs
login_url = "https://erp.iiitkottayam.ac.in/php/functions.php"
result_page_URL = "https://erp.iiitkottayam.ac.in/php/sem_result.php"
result_url = "https://erp.iiitkottayam.ac.in/php/result-pub.php"
id_card_url = "https://erp.iiitkottayam.ac.in/php/id-card.php"


# Login script function for ERP
def login(rollno,dob):
    # Login payload
    payload = {
        'rollno': rollno,
        'dob': dob,
        'log': "submit"
    }
    session = requests.Session()
    print("Attempting to log into ",rollno)
    login_response = session.post(login_url, data=payload)

    # Check if login was successful by verifying the presence of the session cookie
    phpsessid = session.cookies.get('PHPSESSID')
    if phpsessid:
        print("Login successful. PHPSESSID:", phpsessid)
        return session
    else:
        fetch_failed.append(rollno)
        print("Login failed. Please check your credentials.")
        exit()

# initializing script for creating directories
def init(folder_name) -> bool:
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        return False
    else:
        return True

# fetch results for given semester in html
def get_result(rollno,semester,session,year):

    # Access the result page
    print("Accessing the result page...")
    result_page_response = session.get(result_page_URL)

    # Check if result page access was successful
    if result_page_response.status_code == 200:
        print("Accessed result page successfully.")
    else:
        fetch_failed.append(rollno)
        print(f"Failed to access result page. Status code: {result_page_response.status_code}")
        exit()

    print(f"Requesting results for semester {semester}...")

    # Payload
    data = {
        'sem': str(semester)
    }

    # Post request to get specific semester result
    print(session.cookies)
    session.headers.update({"Cookie":"PHPSESSID="+session.cookies.get("PHPSESSID") , "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"})
    print(session.headers.items())
    result_response = session.post(result_url, data=data)

    # Check if the result retrieval was successful
    if result_response.status_code == 200:
        print("Results retrieved successfully.")
    else:
        fetch_failed.append(rollno)
        print(f"Failed to retrieve results. Status code: {result_response.status_code}")
        exit()

    # Parse HTML content
    soup = BeautifulSoup(result_response.text, 'html.parser').prettify()

    # change this directory to the base directory where you want to store all data
    # data stored in folders named after roll number. Each folder contains all results and ID cards of students
    folder_name = "D:\VScodeFiles\python\Projects\Result Piracy\data\\" + year +"\\" + rollno

    # Save HTML content
    filename = f"{rollno}_{semester}.html"
    file_path = os.path.join(folder_name, filename)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(str(soup))
        print(f"Results saved to {file_path}")

# fetch ID card from URL
def get_id_card(rollno,session,year):
    print(f"Requesting id card...")
    result_response = session.get(id_card_url)

    # Check if the result fetch was successful
    if result_response.status_code == 200:
        print("Results retrieved successfully.")
    else:
        print(f"Failed to retrieve results. Status code: {result_response.status_code}")
        exit()

    folder_name = "D:\VScodeFiles\python\Projects\Result Piracy\data\\" + year +"\\" + rollno
    # Save id card in pdf format
    filename = f"{rollno}" + "_id.pdf"
    file_path = os.path.join(folder_name, filename)
    with open(file_path, "wb") as file:
        file.write(result_response.content)
        print(f"Results saved to {file_path}")

# driver function for the threading model
def controller(rollno,sem,dob,folder_name,year):
    sess = login(rollno,dob)
    init(folder_name)
    get_id_card(rollno,sess,year)
    for i in range(1,int(sem)+1):
        get_result(rollno,i,sess,year)

# dictionary for year-semester mapping. Used to iterate over available semesters for a year
dic = {
    "2022": 4,
    "2021": 6,
    "2020": 8,
    "2023": 2
}

#multi threading to speed up the fetching process
threads = []
with open("datasrc/2021.csv",mode='r') as file:
    csv_reader = csv.reader(file)
    # increase/ decrease workers threads. Recommended 5-10
    with ThreadPoolExecutor(max_workers=10) as exec:
        # Enter the col number of the roll number from csv file in arg 2 below (row[i]) and col number of the DOB in arg 4 below.
        futures = [exec.submit(controller , row[3] , dic[row[3][0:4]] , row[7] , str("D:\VScodeFiles\python\Projects\Result Piracy\data\\" + row[3][0:4] +"\\" + row[3]) ,row[3][0:4]) for row in csv_reader]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Task generated an exception: {e}")
    

print("\nFetch failed for : ",fetch_failed)
#skipping has been removed but it can be used to skip data fetch for students whose data already exists
print("\nSkipped for: ",skipped)