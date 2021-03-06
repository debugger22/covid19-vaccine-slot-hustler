# Details

MOBILE_NUMBER = ""
PIN_CODE = ""
TIME_INTERVAL_IN_SECONDS = 20


import requests
import datetime
import hashlib
import time
from playsound import playsound

base_url = "https://cdn-api.co-vin.in/api"

generate_otp_url = "/v2/auth/public/generateOTP"
confirm_otp_url = "/v2/auth/public/confirmOTP"
find_by_pin_url = "/v2/appointment/sessions/public/findByPin"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def get_token():
    """
    Returns token post OTP verification
    """
    # Generate OTP
    r = requests.post(url=f"{base_url}{generate_otp_url}", json={"mobile": MOBILE_NUMBER}, headers=headers)

    if r.status_code == 200:
        txnId = r.json()['txnId']
        # Take OTP input from shell and convert it to SHA-256
        otp = hashlib.sha256(str(input("Enter OTP: ")).encode('utf-8')).hexdigest()

        # Validate OTP to get bearer token
        r = requests.post(url=f"{base_url}{confirm_otp_url}", json={"txnId": txnId, "otp": otp}, headers=headers)
        if r.status_code == 200:
            token = r.json()['token']
        return token
    else:
        print("Failed to verify OTP, please wait for 3 minutes and restart the script")
        print(r.text)
        return None


refresh_token = True

# Main loop
while True:
    if refresh_token:
        token = get_token()
    headers['Authorization'] = f'Bearer {token}'
    t = datetime.datetime.now().strftime("%d-%m-%Y")
    alert = False

    # Iterate over next 5 days including today to check for vaccination slots
    for i in range(5):
        date = (datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%d-%m-%Y")

        # Get vaccination sessions data using pincode and date
        r = requests.get(url=f"{base_url}{find_by_pin_url}", params={"pincode": PIN_CODE, "date": date}, headers=headers)

        if r.status_code == 200:
            refresh_token = False
            sessions = r.json()['sessions']
            print(f"{date}: {len(sessions)}")
            # TODO: Parse sessions to filter out user's age and dose preferences
            # The schema for sessions can be found here: https://apisetu.gov.in/public/marketplace/api/cowin/cowin-public-v2/
            if len(sessions) > 0:
                alert = True
        else:
            # Either token has expired or something unexpected happen
            refresh_token = True
            print(r.text)
    print("------------------------")

    if alert:
        # Alert the user by playing an audio file
        playsound("alarm.mp3")

    time.sleep(TIME_INTERVAL_IN_SECONDS)
