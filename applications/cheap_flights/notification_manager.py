from twilio.rest import Client
import os

account_sid = os.environ.get("PYTHON_SMS_SID")
auth_token = os.environ.get("PYTHON_SMS_AUTH")
phone = os.environ.get("PYTHON_PHONE_NUMBER")

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.

    def send_text(seld, msg):
        if msg:
            client = Client(account_sid, auth_token)
            message = client.messages \
                .create(
                body=msg,
                from_="+13436553073",
                to=phone
            )
            print(message.sid)