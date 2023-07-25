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

        // Get Active Calls
        const endpoint = "/api/v1/admin/accounts/{accountId}/activeCalls/list?product=ACCOUNT&productId={accountId}"
        const response = await ev.get(endpoint)
        console.log(response.data);
    }
    catch (err) {
        console.log(err.message)
    }
}

RunRequest();
