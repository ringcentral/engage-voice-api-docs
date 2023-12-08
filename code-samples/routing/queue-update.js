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

        // Get Queue Groups info
        const groupEndpoint = "/api/v1/admin/accounts/{accountId}/gateGroups"
        const groupResponse = await ev.get(groupEndpoint)
        for (var group of groupResponse.data) {
            // Update your Queue under your Queue Group
            if (group.groupName == "My New Queue Group") {
                const queueEndpoint = groupEndpoint + "/" + group.gateGroupId + "/gates"
                const queueResponse = await ev.get(queueEndpoint)
                for (var queue of queueResponse.data) {
                    if (queue.gateName == "My Node Queue") {
                        const singleQueueEndpoint = queueEndpoint + "/" + queue.gateId
                        queue.gateDesc = "An *edited* queue description for this Queue"
                        const singleQueueResponse = await ev.put(singleQueueEndpoint, queue)
                        console.log(singleQueueResponse.data);
                        break
                    }
                }
            }
        }
    }
    catch (err) {
        console.log(err.message)
    }
}

RunRequest();