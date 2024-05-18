import requests

# URL of the PHP page that generates the PDF
pdf_url = 'https://erp.iiitkottayam.ac.in/php/id-card.php'

# Headers to mimic the browser request
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-GB,en;q=0.5',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'PHPSESSID=i5mbtienl3o9sjsjg44qiceual',  # Make sure this is a valid session ID
    'Host': 'erp.iiitkottayam.ac.in',
    'Referer': 'https://erp.iiitkottayam.ac.in/php/dash.php',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Sec-GPC': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Brave";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}

# Create a session to persist cookies
session = requests.Session()

# Update session headers
session.headers.update(headers)

# Send the GET request to fetch the PDF
response = session.get(pdf_url)

# Check if the request was successful
if response.status_code == 200:
    # Check if the response contains an error message or HTML instead of PDF content
    if 'application/pdf' in response.headers.get('Content-Type', ''):
        # Define the local filename to save the PDF
        pdf_filename = 'downloaded_id_card.pdf'
        
        # Write the PDF content to a file
        with open(pdf_filename, 'wb') as file:
            file.write(response.content)
        
        print(f"PDF file successfully downloaded as {pdf_filename}")
    else:
        print("The response does not contain PDF content. Please check the response details.")
        print(response.text)
else:
    print(f"Failed to download PDF file. Status code: {response.status_code}")
    print("Response content:")
    print(response.text)
