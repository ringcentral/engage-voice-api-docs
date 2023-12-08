/****** Install Node JS SDK wrapper *******
$ npm install ringcentral-engage-voice-client
*******************************************/

const RunRequest = async function () {
    const EngageVoice = require('ringcentral-engage-voice-client').default

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
            // Get Queues under your Queue Group
            if (group.groupName == "My New Queue Group") {
                const queueEndpoint = groupsEndpoint + "/" + group.gateGroupId + "/gates"
                const queueResponse = await ev.get(queueEndpoint)
                console.log(queueResponse.data);
            }
        }
    }
    catch (err) {
        console.log(err.message)
    }
}

RunRequest();
