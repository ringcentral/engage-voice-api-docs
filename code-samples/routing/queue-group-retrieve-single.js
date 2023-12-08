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
            // Get every single Queue under your Queue Group
            if (group.groupName == "My New Queue Group") {
                const queuesEndpoint = groupsEndpoint + "/" + group.gateGroupId + "/gates"
                const queuesResponse = await ev.get(queuesEndpoint)
                for (var queue of queuesResponse.data) {
                    const singleQueueEndpoint = queuesEndpoint + "/" + queue.gateId
                    const singleQueueResponse = await ev.get(singleQueueEndpoint)
                    console.log(singleQueueResponse.data);
                    console.log("=========")
                }
            }
        }
    }
    catch (err) {
        console.log(err.message)
    }
}

RunRequest();  
