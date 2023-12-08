#### Install Python SDK wrapper ####
# $ pip3 install ringcentral_engage_voice
#  or
# $ pip install ringcentral_engage_voice
#####################################

from ringcentral_engage_voice import RingCentralEngageVoice

def retrieve_queues():
    try:
        groupsEndpoint = "/api/v1/admin/accounts/{accountId}/gateGroups"
        groupsResponse = ev.get(groupsEndpoint).json()
        for group in groupsResponse:
            # Retrieve Queues under your Queue Group
            if (group['groupName'] == "My New Queue Group"):
                queueEndpoint = f"{groupsEndpoint}/{group['gateGroupId']}/gates"    # f         string:https://www.python.org/dev/peps/pep-0498/
                queueResponse = ev.get(queueEndpoint).json()
                print(queueResponse)
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

    retrieve_queues()
except Exception as e:
    print(e)
