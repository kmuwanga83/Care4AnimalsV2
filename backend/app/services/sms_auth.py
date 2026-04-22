# SMS Authentication Handling for Africa's Talking Gateway

import requests

class SMSAuth:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.africastalking.com/version1/messaging'

    def send_sms(self, to, message):
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }
        payload = {
            'username': 'sandbox',
            'to': to,
            'message': message,
            'from': 'YourSenderID'
        }

        response = requests.post(self.base_url, json=payload, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to send SMS: {response.status_code} {response.text}")

# Example usage:
# sms_auth = SMSAuth('YOUR_API_KEY')
# sms_auth.send_sms('recipient_phone_number', 'Hello from Care4Animals!')
