from ringcentral_engage_voice import RingCentralEngageVoice

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
    "RINGCENTRAL_CLIENTID",
    "RINGCENTRAL_CLIENTSECRET")

try:
    # Authorize with your RingCentral Office user credentials
    ev.authorize(
        username="RINGCENTRAL_USERNAME",
        password="RINGCENTRAL_PASSWORD",
        extension="RINGCENTRAL_EXTENSION"
    )

    create_dial_group()
except Exception as e:
    print(e)
