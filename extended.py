import requests
import random

def get_random_line(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        return random.choice(lines).strip()

def check_responses(urls, error_codes):
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code in error_codes:
                print(f"{url} = {response.status_code}, Message = \"{get_random_line('error_messages.txt')}\"")
            else:
                print(f"{url} = {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"{url} = Error: {e}")

# List of URLs to test
urls = ['http://www.google.com', 'http://www.bing.com', 'https://chat.openai.com']

# List of error codes to handle
error_codes = [403, 406]  # Add more error codes as needed

check_responses(urls, error_codes)
