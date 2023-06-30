import os, sys, time
from dotenv import load_dotenv
from ringcentral_engage_voice import RingCentralEngageVoice

load_dotenv()

def retrieve_agent_groups():
    try:
        response = ev.get("/api/v1/admin/accounts/{accountId}/agentGroups").json()
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
    retrieve_agent_groups()
except Exception as e:
    print(e)
