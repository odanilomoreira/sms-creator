import json

with open('credentials.json') as json_file:
    config = json.load(json_file)
    SMTP_EMAIL = config.get('SMTP_EMAIL')
    SMTP_PASSWORD = config.get('SMTP_PASSWORD')
    TWILIO_ACCOUNT_SID = config.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = config.get('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = config.get('TWILIO_PHONE_NUMBER')
    TWILIO_API_KEY = config.get('TWILIO_API_KEY')
    RESTAURANT_ID = config.get('RESTAURANT_ID')

