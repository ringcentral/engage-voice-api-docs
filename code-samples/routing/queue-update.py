#### Install Python SDK wrapper ####
# $ pip3 install ringcentral_engage_voice
#  or
# $ pip install ringcentral_engage_voice
#####################################

from ringcentral_engage_voice import RingCentralEngageVoice

def update_single_queue():
    try:
        groupsEndpoint = "/api/v1/admin/accounts/{accountId}/gateGroups"
        groupsResponse = ev.get(groupsEndpoint).json()
        for group in groupsResponse:
            # Retrieve Queues under your Queue Group
            if (group['groupName'] == "My New Queue Group"):
                queuesEndpoint = f"{groupsEndpoint}/{group['gateGroupId']}/gates"    # f        string:https://www.python.org/dev/peps/pep-0498/
                queuesResponse = ev.get(queuesEndpoint).json()
                for queue in queuesResponse:
                    # Update your Queue
                    if queue['gateName'] == "My New Queue":
                        singleQueueEndpoint = f"{queuesEndpoint}/{queue['gateId']}"
                        queue['gateDesc'] = f"{queue['gateDesc']} - Updated"
                        singleQueueResponse = ev.put(singleQueueEndpoint, queue).json()
                        print(singleQueueResponse)
                        break
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

    update_single_queue()
except Exception as e:
    print(e)
