# Get a list of active calls
Active calls can be listed based on a category called "Product". Each product must be identified by a product id. For example, to list all active calls 

To get a list of active calls, make an HTTP GET request to the `activeCall/list` endpoint

`GET /api/v1/admin/accounts/{accountId}/activeCall/list`

| Parameter | Description |
|-|-|
| **product** | The name of a product, which can be one of the following criteria:</br>`"ACCOUNT"` - `"ACD"` - `"AGENT"` - `"CHAT_QUEUE"` - `"OUTBOUND"` - `"VISUAL_IVR"` - `"CLOUD_PROFILE"` - `"CLOUD_DESTINATION"` - `"TRAC_NUMBER"` - `"HTTP_SERVICES"` - `"SCRIPTING"` - `"TN_MANAGER"` - `"SURVEY"` - `"DNIS"` - `"TEAMS"` - `"KNOWLEDGE_BASE"` - `"UTILITIES"` |
| **productId** | The identifier of a selected product. E.g. if the **product** is `"ACCOUNT"`, the **productId** is the account id. |
| **page** | Number of page per request. |
| **maxRows** | Max number of items per page. |


```
`GET {baseURL}/api/v1/admin/accounts/{accountId}/activeCalls/list?product=ACCOUNT&productId=12440001`

[ { uii: '202005081040440132050000019657',
    accountId: '12440001',
    ani: '6501234567',
    dnis: '8661234567',
    enqueueTime: '2020-05-08T14:40:47.000+0000',
    dequeueTime: null,
    callState: 'ACTIVE',
    archive: false,
    agentFirstName: 'Paco',
    agentLastName: 'Vu',
    destinationName: null } ]
```
