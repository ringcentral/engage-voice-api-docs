#### Install Python SDK wrapper ####
# $ pip3 install ringcentral_engage_voice
#  or
# $ pip install ringcentral_engage_voice
#####################################

from ringcentral_engage_voice import RingCentralEngageVoice

def retrieve_single_queue_group():
    try:
        groupsEndpoint = "/api/v1/admin/accounts/{account}/gateGroups"
        groupsResponse = ev.get(groupsEndpoint).json()
        # Get every single Queue Group
        for group in groupsResponse:
            singleGroupEndpoint = f"{groupsEndpoint}/{group['gateGroupId']}"    # f string:https://     www.python.org/dev/peps/pep-0498/
            singleGroupResponse = ev.get(singleGroupEndpoint).json()
            print(singleGroupResponse)
            print("========")
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

    retrieve_single_queue_group()
except Exception as e:
    print(e)
