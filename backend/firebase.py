from django.conf import settings

import firebase_admin
from firebase_admin import credentials, messaging

import os

cred = credentials.Certificate(os.path.join(settings.BASE_DIR, "backend/serviceAccountKey.json"))
default_app = firebase_admin.initialize_app(cred)

def send_to_firebase_cloud_notification(clientToken, title):
    # This registration token comes from the client FCM SDKs.
    #registration_token = clientToken

    # See documentation on defining a message payload.
    message = messaging.Message(
        data={
            'title': title,
        },
        token=clientToken,
    )

    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)

def send_to_firebase_cloud_messaging(clientToken, title, msg):
    # This registration token comes from the client FCM SDKs.
    #registration_token = clientToken

    # See documentation on defining a message payload.
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=msg,
        ),
        android=messaging.AndroidConfig(
            priority='high'
        ),
        token=clientToken,
    )

    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
