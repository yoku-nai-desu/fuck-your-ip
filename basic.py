import requests

def check_response(url):
    print("this script checks if your ip is considered forbidden or as I like to call it [fucked]")
    try:
        response = requests.get(url)
        print("\n Response status code:", response.status_code)
        
    except requests.exceptions.RequestException as e:
        print("Error:", e)

# Replace 'http://www.google.com' with any URL you want to request
url = 'https://www.google.com'
check_response(url)
