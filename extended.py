import requests
import random
from bs4 import BeautifulSoup

def get_random_line(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        return random.choice(lines).strip()

def is_captcha_response(response_text):
    captcha_keywords = [
        'recaptcha', 'g-recaptcha', 'h-captcha', 'cf-turnstile', 'captcha', 'verify you are human'
    ]
    soup = BeautifulSoup(response_text, 'html.parser')
    # Check for common CAPTCHA-related elements
    captcha_indicators = [
        {'tag': 'div', 'class': 'g-recaptcha'},          # Google ReCaptcha
        {'tag': 'div', 'class': 'h-captcha'},            # hCaptcha
        {'tag': 'div', 'class': 'cf-turnstile'},         # Cloudflare Turnstile
        {'tag': 'div', 'class': 'captcha'},              # Generic
        {'tag': 'iframe', 'src': 'recaptcha'},           # ReCaptcha iframe
        {'tag': 'iframe', 'src': 'hcaptcha'},            # hCaptcha iframe
        {'tag': 'iframe', 'src': 'cf-turnstile'},        # Cloudflare Turnstile iframe
    ]
    for indicator in captcha_indicators:
        if soup.find(indicator['tag'], class_=indicator.get('class')) or soup.find(indicator['tag'], src=indicator.get('src')):
            return True
    # Fallback to keyword search if no specific elements are found
    return any(keyword in response_text.lower() for keyword in captcha_keywords)

def check_responses(urls, error_codes):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Cache-Control': 'no-cache'
    }
    
    for url in urls:
        try:
            with requests.Session() as session:
                session.headers.update(headers)
                response = session.get(url)
                if response.status_code in error_codes:
                    print(f"{url} = {response.status_code}, Message = \"{get_random_line('error_messages.txt')}\"")
                elif is_captcha_response(response.text):
                    print(f"{url} = CAPTCHA detected, please verify manually.")
                else:
                    print(f"{url} = {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"{url} = Error: {e}")

# List of URLs to test
urls = ['http://www.google.com', 'http://www.bing.com', 'https://chat.openai.com']

# List of error codes to handle
error_codes = [403, 406]  # Add more error codes as needed

check_responses(urls, error_codes)
