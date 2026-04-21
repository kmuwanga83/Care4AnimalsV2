import requests

class SmsGateway:
    def __init__(self, api_key, username):
        self.api_key = api_key
        self.username = username
        self.base_url = 'https://api.africastalking.com/v1/sms'

    def send_sms(self, to, message):
        headers = {'apikey': self.api_key}
        data = {
            'to': to,
            'message': message,
            'username': self.username
        }
        response = requests.post(self.base_url, headers=headers, data=data)
        return response.json()

    def receive_sms(self):
        # Endpoint for receiving SMS can be configured
        # The actual implementation will depend on how you set up your webhook
        pass

# Example usage:
# sms_gateway = SmsGateway(api_key='YOUR_API_KEY', username='YOUR_USERNAME')
# response = sms_gateway.send_sms(to='recipient_phone_number', message='Hello!')
# print(response)