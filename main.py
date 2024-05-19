import os
import requests
import csv
from bs4 import BeautifulSoup
from getpass import getpass


# dob = "2004-01-28"
# rollno = "2022BCY0026"
login_url = "https://erp.iiitkottayam.ac.in/php/functions.php"
result_url = "https://erp.iiitkottayam.ac.in/php/sem_result.php"
id_card_url = "https://erp.iiitkottayam.ac.in/php/id-card.php"

# semester = "4"





def login(rollno,dob):
     # Login payload
    payload = {
        'rollno': rollno,
        'dob': dob,
        'log': "submit"
    }
    session = requests.Session()
    # Attempt to login
    print("Attempting to log in...")
    login_response = session.post(login_url, data=payload)
    # login_response = session.post(login_url, data=payload)
    # print(login_response)

    # Check if login was successful by verifying the presence of the session cookie
    phpsessid = session.cookies.get('PHPSESSID')
    if phpsessid:
        print("Login successful. PHPSESSID:", phpsessid)
        return session
    else:
        print("Login failed. Please check your credentials.")
        exit()


def init(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def get_result(rollno,semester,session):

    # Access the result page
    print("Accessing the result page...")
    result_page_response = session.get(result_url)

    # Check if result page access was successful
    if result_page_response.status_code == 200:
        print("Accessed result page successfully.")
    else:
        print(f"Failed to access result page. Status code: {result_page_response.status_code}")
        exit()

    # Post request to get specific semester result
    
    print(f"Requesting results for semester {semester}...")

    # data = {
    #     'sem': semester
    # }
    # Headers


    # Payload
    data = {
        'sem': str(semester)  # Change this to the semester you want
    }

    # Post request to get specific semester result
    print(session.cookies)
    session.headers.update({"Cookie":"PHPSESSID="+session.cookies.get("PHPSESSID") , "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"})
    print(session.headers.items())
    result_response = session.post("https://erp.iiitkottayam.ac.in/php/result-pub.php", data=data)

    # Check if the result retrieval was successful
    if result_response.status_code == 200:
        print("Results retrieved successfully.")
    else:
        print(f"Failed to retrieve results. Status code: {result_response.status_code}")
        exit()

    # Parse HTML content
    soup = BeautifulSoup(result_response.text, 'html.parser').prettify()
    folder_name = "D:\VScodeFiles\python\Projects\Result Piracy\data\\" + "2022" +"\\" + rollno
    # Save HTML content
    filename = f"{rollno}_{semester}.html"
    file_path = os.path.join(folder_name, filename)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(str(soup))
        print(f"Results saved to {file_path}")

    # For debugging, print out a small portion of the result
    # print("Preview of retrieved results:")
    # print(soup.prettify()[:])  # Print the first 500 characters for a preview





def get_id_card(rollno,session):

    # Access the result page
    # print("Accessing the result page...")
    # session.get("https://erp.iiitkottayam.ac.in/php/dash.php")
    # result_page_response = session.get(id_card_url)

    # Check if result page access was successful

    # Post request to get specific semester result
    
    print(f"Requesting id card...")

    # data = {
    #     'sem': semester
    # }
    # Headers


    # Payload
    # data = {
    #     'sem': str(semester)  # Change this to the semester you want
    # }

    # Post request to get specific semester result
    # print(session.cookies)
    # session.headers.update({"Cookie":"PHPSESSID"+session.cookies.get("PHPSESSID") , "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"})
    # print(session.headers.items())
    result_response = session.get("https://erp.iiitkottayam.ac.in/php/id-card.php")

    # Check if the result retrieval was successful
    if result_response.status_code == 200:
        print("Results retrieved successfully.")
    else:
        print(f"Failed to retrieve results. Status code: {result_response.status_code}")
        exit()

    # Parse HTML content
    # soup = BeautifulSoup(result_response.text, 'html.parser')
    folder_name = "D:\VScodeFiles\python\Projects\Result Piracy\data\\" + "2022" +"\\" + rollno
    # Save HTML content
    filename = f"{rollno}" + "_id.pdf"
    file_path = os.path.join(folder_name, filename)
    with open(file_path, "wb") as file:
        file.write(result_response.content)
        print(f"Results saved to {file_path}")

    # For debugging, print out a small portion of the result
    # print("Preview of retrieved results:")
    # print(soup.prettify()[:])  # Print the first 500 characters for a preview




# sess = login("2022BCY0044","2003-01-17")
# init("D:\VScodeFiles\python\Projects\Result Piracy\data")
# get_id_card("2022BCY0044",sess)

dic = {
    "2022": 4,
    "2021": 6,
    "2020": 8,
    "2023": 2
}


with open("ccc.csv",mode='r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        rollno = row[3]
        dob = row[7]
        year = rollno[0:4]
        folder_name = "D:\VScodeFiles\python\Projects\Result Piracy\data\\" + "2022" +"\\" + rollno
        sess = login(rollno,dob)
        init(folder_name)
        get_id_card(rollno,sess)
        for i in range(1,dic[rollno[year]]+1):
            get_result(rollno,i,sess)