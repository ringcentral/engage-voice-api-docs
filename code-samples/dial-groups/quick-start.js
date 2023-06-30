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
	
        // Create a new Dial Group
        const postBody = {
            "dialGroupName": "My New Dial Group",
            "dialGroupDesc": "A test dial group with predictive dial mode",
            "dialMode": "PREDICTIVE",
            "isActive": true
        }
        const response = await ev.post('/api/v1/admin/accounts/{accountId}/dialGroups', postBody)
        console.log(response);
    }
    catch (err) {
        console.log(err.message)
    }
}

RunRequest();
