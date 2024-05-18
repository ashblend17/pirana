import requests

def download_webpage(url, filename):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        # Raise an exception for non-200 status codes
        response.raise_for_status()
        # Open a file in binary write mode and save the response content to it
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Webpage downloaded successfully: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading webpage: {e}")

# Example usage:
url = 'https://example.com'
filename = 'example.html'
download_webpage(url, filename)
