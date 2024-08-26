from django.utils import timezone
import requests

def send_opt(code, phone_number):
    api_key = "your_api_key"
    sender = "your_sender"
    recipient = "recipient_phone_number"

    url = f"https://api.sms-webservice.com/api/V3/Send?ApiKey={api_key}&Text={code}&Sender={sender}&Recipients={phone_number}"

    payload = {}
    headers = {}
    print("*\n" * 10, code, "*\n" * 10)

    # try:
    #     response = requests.get(url, headers=headers, data=payload)
    #     response.raise_for_status()
    #     print(response.text)
    # except requests.exceptions.HTTPError as err:
    #     print(err)
