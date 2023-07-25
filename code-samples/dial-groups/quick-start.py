import os, sys, time
from dotenv import load_dotenv
from ringcentral_engage_voice import RingCentralEngageVoice

load_dotenv()

def create_dial_group():
    try:
        postBody = {
            "dialGroupName": "My New Dial Group",
            "dialGroupDesc": "A test dial group with predictive dial mode",
            "dialMode": "PREDICTIVE",
            "isActive": True
        }
        response = ev.post("/api/v1/admin/accounts/{accountId}/dialGroups", postBody).json()
        print(response)
    except Exception as e:
        print(e)

# Instantiate the SDK wrapper object with your RingCentral app credentials
ev = RingCentralEngageVoice(
    os.environ.get('RC_CLIENT_ID'),
    os.environ.get('RC_CLIENT_SECRET')
)

try:
    # Authorize with your RingCentral Office user credentials
    ev.authorize(
        jwt=os.environ.get('RC_JWT')
    )

    create_dial_group()
except Exception as e:
    print(e)
