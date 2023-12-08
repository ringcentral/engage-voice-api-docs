#### Install Python SDK wrapper ####
# $ pip3 install ringcentral_engage_voice
#  or
# $ pip install ringcentral_engage_voice
#####################################

from ringcentral_engage_voice import RingCentralEngageVoice

def update_single_queue_group():
    try:
        groupsEndpoint = "/api/v1/admin/accounts/{accountId}/gateGroups"
        groupsResponse = ev.get(groupsEndpoint).json()
        for group in groupsResponse:
            # Update Queue Group name
            if group['groupName'] == "Ma New Queue Group":
                singleGroupEndpoint = f"{groupsEndpoint}/{group['gateGroupId']}"    # f         string:https://www.python.org/dev/peps/pep-0498/
                group['groupName'] = f"{group['groupName']} - Updated"
                singleGroupResponse = ev.put(singleGroupEndpoint, group).json()
                print(singleGroupResponse)
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

    update_single_queue_group()
except Exception as e:
    print(e)
