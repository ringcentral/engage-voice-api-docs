const EngageVoice = require('ringcentral-engage-voice-client').default
const path = require('path')
// Remember to modify the path to where you saved your .env file!
require('dotenv').config({ path: path.resolve(__dirname, '../.env') })

const RunRequest = async function () {
    // Instantiate the SDK wrapper object with your RingCentral app credentials
    const ev = new EngageVoice({
        clientId: process.env.RC_CLIENT_ID,
        clientSecret: process.env.RC_CLIENT_SECRET
    })

    try {
        // Authorize with your RingCentral Office user credentials
        await ev.authorize({ jwt: process.env.RC_JWT })

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
