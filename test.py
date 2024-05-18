import os
import requests

# Function to log in and get the session
def login_and_get_session():
    login_url = "https://erp.iiitkottayam.ac.in/php/functions.php"
    dob = "2004-01-28"
    rollno = "2022BCY0026"
    
    session = requests.Session()

    # Login payload
    payload = {
        'rollno': rollno,
        'dob': dob,
        'log': "submit"
    }

    # Attempt to login
    login_response = session.post(login_url, data=payload)

    # Check if login was successful by verifying the presence of the session cookie
    phpsessid = session.cookies.get('PHPSESSID')
    if phpsessid:
        print("Login successful. PHPSESSID:", phpsessid)
        return session
    else:
        print("Login failed. Please check your credentials.")
        exit()

# Function to download the PDF
def download_pdf(response, folder_name, filename):
    # Check if the request was successful
    if response.status_code == 200:
        # Save the PDF content to a file
        file_path = os.path.join(folder_name, filename)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"PDF file successfully downloaded as {file_path}")
    else:
        print(f"Failed to download PDF file. Status code: {response.status_code}")

def main():
    # Folder to save the PDF
    rollno = "2022BCY0044"
    folder_name = "data/" + rollno + "/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Log in and get the session
    session = login_and_get_session()

    # Manually provide the PDF request URL
    pdf_request_url = "https://erp.iiitkottayam.ac.in/php/id-card.php"

    # Download the PDF
    response = session.get(pdf_request_url)

    # Extract the filename from the content disposition header
    content_disposition = response.headers.get('Content-Disposition')
    filename = content_disposition.split("filename=")[1].strip('\"') if content_disposition else "doc.pdf"

    # Save the PDF content to a file
    download_pdf(response, folder_name, filename)

if __name__ == "__main__":
    main()
