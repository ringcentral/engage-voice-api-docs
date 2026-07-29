# About Agent Scripting

Agent scripting is a powerful tool for both your agents and your business that functions similarly to a script in a movie or play. It’s a prompt that helps agents to move smoothly through their interactions with leads and customers. You can learn a lot more from the [Script Designer](https://support.ringcentral.com/engagevoice/admin/voice-admin-intro-agent-scripting.html) and the corresponding [Script Studio](https://support.ringcentral.com/engagevoice/admin/voice-admin-script-studio-overview.html).

As you get deeper into Agent Scripting, you'll want to customize the agent experience to go beyond just an agent script and the best way to do that is through the [WWW tool](https://support.ringcentral.com/engagevoice/admin/voice-admin-use-www-tool.html) and [JavaScript tool](https://support.ringcentral.com/engagevoice/admin/voice-admin-use-javascript-tool.html). This guide will walk you through some examples of using the WWW tool to invoke external APIs and the [JavaScript tool](https://support.ringcentral.com/engagevoice/admin/voice-admin-use-javascript-tool.html) for processing the response and using the data you gather from the [WWW tool](https://support.ringcentral.com/engagevoice/admin/voice-admin-use-www-tool.html).

## Example

In this example we are going to look up the caller in HubSpot and bring up their HubSpot contact record in the agent script area within an iframe element. This way, the agent doesn't have to leave the page to view information or update the contact record.

<img class="img-fluid" width="110" src="../../../images/agent-scripting-workflow.png">

As you can see from the workflow, our steps are:

* Retrieve Contact - Lookup the contact by telephone number (ANI)
* Process Response - Build the HubSpot embed URL from the response body
* Display HubSpot Page - Use the embed URL in an iframe to load the contact page.

Let's go through them one-by-one.

### Retrieve Contact

The first step is to lookup the contact by telephone number. In this case, we record the incoming number as the ANI (Automatic Number Identification). We will retrieve this contact using the HubSpot API, but we are going to use a server-side middleware endpoint, such as an AWS Lambda function, to communicate with HubSpot.

!!! Note
    Third-party APIs must allow browser-based cross-origin requests before they can be called directly from an agent script. For APIs that do not support the required CORS headers, or for APIs that require private credentials, call customer-controlled middleware from the WWW tool. The middleware can store credentials securely, call the third-party API server-side, and return only the fields the script needs.

To make this request, make a GET request to your middleware endpoint. It should look something like this.

`https://{apiGatewayHost}/{stage}/hubspot-contact?q=:phone`

!!! Note
    The URL above is a placeholder. Use the HTTPS endpoint for the middleware service you create.

Notice the `q=:phone`. We are defining `phone` as a URL Parameter and this is how we put it into the query string. The caller's phone is automatically discovered by RingCX and put into the tool's [model object](https://support.ringcentral.com/engagevoice/admin/voice-admin-use-javascript-tool.html#modelobject). To retrieve it, we access the model like so:

`{{model.lead.leadPhone}}`

Configure the WWW tool to call your middleware endpoint with a `phone` URL parameter. Set the `phone` value to `{{model.lead.leadPhone}}`.

#### AWS Lambda Middleware

The GET request goes to an AWS Lambda function that looks up the contact in HubSpot. This example focuses on the RingCX workflow, but the Lambda configuration below shows the supporting middleware setup. Set the required environment variables in AWS Lambda before testing the workflow.

| Key | Value|
|-|-|
| ACCESS_CONTROL_ALLOW_ORIGIN | Your RingCX origin, or `*` for initial testing |
| ACCESS_CONTROL_ALLOW_HEADERS | Content-Type |
| HUBSPOT_ACCESS_TOKEN | Your HubSpot private app or OAuth access token |
| HUBSPOT_HUB_ID | Your HubSpot account Hub ID |

```javascript
const https = require('https');

/* ========Config Section======== */
const accessControlAllowOriginValue = process.env.ACCESS_CONTROL_ALLOW_ORIGIN;
const accessControlAllowHeadersValue = process.env.ACCESS_CONTROL_ALLOW_HEADERS;
const hubspotAccessToken = process.env.HUBSPOT_ACCESS_TOKEN;
const hubspotHubId = process.env.HUBSPOT_HUB_ID;
/* ========Config Section======== */

const searchContacts = (phone) => {
    const body = JSON.stringify({
        filterGroups: [
            {
                filters: [
                    {
                        propertyName: 'phone',
                        operator: 'EQ',
                        value: phone
                    }
                ]
            }
        ],
        properties: [
            'firstname',
            'lastname',
            'jobtitle',
            'phone',
            'email',
            'notes_last_contacted'
        ],
        limit: 1
    });

    const requestOptions = {
       host: 'api.hubapi.com',
       path: '/crm/v3/objects/contacts/search',
       port: 443,
       method: 'POST',
       headers: {
           'Authorization': `Bearer ${hubspotAccessToken}`,
           'Content-Type': 'application/json',
           'Content-Length': Buffer.byteLength(body)
       }
    };

    return new Promise((resolve, reject) => {
        const req = https.request(requestOptions, response => {
            let data = '';
            response.on('data', chunk => {
                data += chunk;
            });
            response.on('end', () => {
                try {
                    resolve({
                        statusCode: response.statusCode,
                        body: data ? JSON.parse(data) : {}
                    });
                } catch (error) {
                    reject(error);
                }
            });
        })
            .on('error', error => {
                reject(error);
            });

        req.write(body);
        req.end();
    });
};

exports.handler = (event, context, callback) => {

    const corsHeaders = {
        'Access-Control-Allow-Origin': accessControlAllowOriginValue || '*',
        'Access-Control-Allow-Headers': accessControlAllowHeadersValue || 'Content-Type',
        'Access-Control-Allow-Methods': 'OPTIONS,GET'
    };

    const sendResponse = (statusCode, body) => {
        callback(null, {
            statusCode,
            body: JSON.stringify(body),
            headers: corsHeaders
        });
    };

    const sendError = (error) => {
        sendResponse(400, {
            message: error.message
        });
    };

    const phone = event.queryStringParameters && event.queryStringParameters.q;

    switch (event.httpMethod) {
        case 'OPTIONS':
            sendResponse(204, {});
            break;
        case 'GET':
            if (!phone) {
                sendError(new Error('Missing q query parameter'));
                return;
            }

            searchContacts(phone)
                .then((hubspotResponse) => {
                    sendResponse(hubspotResponse.statusCode, {
                        contacts: hubspotResponse.body.results || [],
                        hubspotHubId: hubspotHubId
                    });
                })
                .catch(error => {
                    sendError(error);
                });
            break;
        default:
            sendError(new Error(`Unsupported method "${event.httpMethod}"`));
    }
};
```

### Process Response

At this point, HubSpot should have looked up the contact by our ANI. We now need to process this
response using our Scripting tool. The Scripting tool is just a part of the workflow that has JavaScript in it to perform more powerful actions like parsing the response and preparing the embed URL.

```javascript
var wwwResponse = getData('model.model.RetrieveContact');

// Find the first contact in the search results
var contacts = wwwResponse.contacts || [];
var firstContact = contacts[0];

if (!firstContact) {
    putData("lookupMessage", "No matching HubSpot contact found.");
    return;
}

// Capture the contact ID and returned properties
var contactId = firstContact.id;
var properties = firstContact.properties || {};

// Capture the HubSpot Hub ID returned by the middleware
var hubspotHubId = wwwResponse.hubspotHubId;

// Let's get details about this contact
// Store the first name
putData("firstName", properties.firstname || "");
// Store the last name
putData("lastName", properties.lastname || "");
// Store the job title
putData("jobTitle", properties.jobtitle || "");
// Store the phone
putData("phone", properties.phone || "");
// Store the email
putData("email", properties.email || "");
// Store last contacted date
if (properties.notes_last_contacted) {
    var rawLastContactDate = properties.notes_last_contacted;
    var lastContactedDate = new Date(rawLastContactDate*1);
    putData("lastContacted", lastContactedDate.toLocaleString("en-US", {timeZoneName: "short"}));
}

// Put together the host and path for the HubSpot contact timeline embed.
// The Page tool configuration supplies the https:// prefix.
var hubspotUrl = "app.hubspot.com/embed/"+hubspotHubId+"/0-1/"+contactId+"/timeline";
putData("hubspotURL", hubspotUrl);

return goTo("Hubspot_Page");
```

Now let's dissect each of those lines.

When you use the WWW tool, the response is stored in a local model object in the Script Studio. To retrieve this response, we need to reference the previous WWW tool by its name, `RetrieveContact`. Notice the way we do this is by using the method `getData`.

``` JavaScript
    var wwwResponse = getData('model.model.RetrieveContact');
```

What we just retrieved is a JSON object, which is exactly what we want. The middleware returns matching HubSpot contacts in the `contacts` array. For this example, we use the first returned contact.

``` JavaScript
    var contacts = wwwResponse.contacts || [];
    var firstContact = contacts[0];
```

With this contact, we want to construct a HubSpot contact timeline embed URL so the contact timeline can open inside the Page tool.

First we need the contact ID, which is returned as `id` in the HubSpot contact search response.

``` JavaScript
    var contactId = firstContact.id;
```

Then we capture the HubSpot Hub ID returned by the middleware.

``` JavaScript
    var hubspotHubId = wwwResponse.hubspotHubId;
```

We can then construct the embed host and path using the Hub ID, the HubSpot object type ID for contacts, and the contact ID. In this example, the Page tool supplies the `https://` prefix, so the model value does not include the protocol.

``` JavaScript
    var hubspotUrl = "app.hubspot.com/embed/"+hubspotHubId+"/0-1/"+contactId+"/timeline";
```

Now we can store that HubSpot URL into our model object so we can use it in the Page tool.

``` JavaScript
    putData("hubspotURL", hubspotUrl);
```

### Display HubSpot Page

Now we are ready to bring up the page to display to the agent. To do this we need to use the Page tool. When you edit the Page tool you can configure the URL the page should display by clicking on the gear icon. Here we'll add a tag to retrieve the URL we just put into the model object.

`{{model.model.hubspotURL}}`

<img class="img-fluid" width="964" src="../../../images/agent-scripting-page-config.png">

To test the workflow, use the "Render" option with a known contact phone number from the HubSpot instance. In the WWW tool from the first step, replace `{{model.lead.leadPhone}}` with a real 10-digit phone number.

The example also stores contact details in the model object, including first name, last name, email, and phone. These fields create a richer agent view of the contact record when a contact calls the agent. The [page tool](https://support.ringcentral.com/engagevoice/admin/voice-admin-page-tool-elements-overview.html) can display additional context from the model object as needed.

<img class="img-fluid" width="960" src="../../../images/agent-scripting-hubspot.png">
