#### Install Python SDK wrapper ####
# $ pip3 install ringcentral_engage_voice
#  or
# $ pip install ringcentral_engage_voice
#####################################

from ringcentral_engage_voice import RingCentralEngageVoice

def create_a_queue_group():
    try:
        postBody = {
            "groupName": "My New Queue Group"
        }
        response = ev.post("/api/v1/admin/accounts/{accountId}/gateGroups", postBody).json()
        print(response)
    except Exception as e:
        print(e)


# Instantiate the SDK wrapper object with your RingCentral app credentials
ev = RingCentralEngageVoice(
    "RINGCENTRAL_CLIENTID",
    "RINGCENTRAL_CLIENTSECRET")

try:
    # Authorize with your RingCentral Office user credentials
    ev.authorize(
        username="RINGCENTRAL_USERNAME",
        password="RINGCENTRAL_PASSWORD",
        extension="RINGCENTRAL_EXTENSION"
    )

    create_a_queue_group()
except Exception as e:
    print(e)
