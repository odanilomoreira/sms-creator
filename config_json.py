import json

with open('credentials.json') as json_file:
    config = json.load(json_file)
    SMTP_EMAIL = config.get('SMTP_EMAIL')
    SMTP_PASSWORD = config.get('SMTP_PASSWORD')
