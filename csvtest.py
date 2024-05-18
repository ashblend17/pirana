import csv
import os
import requests
from bs4 import BeautifulSoup

with open("ccc.csv",mode='r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        rollno = row[3]
        dob = row[7]

        # print(rollno + "_" + dob)