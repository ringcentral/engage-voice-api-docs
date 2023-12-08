/****** Install Node JS SDK wrapper *******
$ npm install ringcentral-engage-voice-client
*******************************************/

const RunRequest = async function () {
    const EngageVoice = require('ringcentral-engage-voice-client').default

    // Instantiate the SDK wrapper object with your RingCentral app credentials
    const ev = new EngageVoice({
        clientId: "RINGCENTRAL_CLIENTID",
        clientSecret: "RINGCENTRAL_CLIENTSECRET"
    })

    try {
        // Authorize with your RingCentral Office user credentials
        await ev.authorize({
            username: "RINGCENTRAL_USERNAME",
            extension: "RINGCENTRAL_EXTENSION",
            password: "RINGCENTRAL_PASSWORD"
        })

        // Get Queue Groups data
        const groupsEndpoint = "/api/v1/admin/accounts/{accountId}/gateGroups"
        const groupsResponse = await ev.get(groupsEndpoint)
        for (var group of groupsResponse.data) {
            // Create a new Queue under your Queue Group
            if (group.groupName == "My New Queue Group") {
                const queueEndpoint = groupsEndpoint + "/" + group.gateGroupId + "/gates"
                const postBody = {
                    "isActive": true,
                    "gateName": "My Node Queue",
                    "gateDesc": "An initial queue for this Queue Group"
                }
                const queueResponse = await ev.post(queueEndpoint, postBody)
                console.log(queueResponse.data);
            }
        }
    }
    catch (err) {
        console.log(err.message)
    }
}

RunRequest();
