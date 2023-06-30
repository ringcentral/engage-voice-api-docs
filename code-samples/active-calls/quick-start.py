import os, sys, time
from dotenv import load_dotenv
from ringcentral_engage_voice import RingCentralEngageVoice

load_dotenv()

def list_active_calls():
    try:
        params = "product=ACCOUNT&productId={accountId}"
        response = ev.get("/api/v1/admin/accounts/{accountId}/activeCalls/list", params).json()
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
    list_active_calls()
except Exception as e:
    print(e)
