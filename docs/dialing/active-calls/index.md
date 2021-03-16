# About Active Call APIs
Active Call APIs allow you to manage agents' active calls. One of the essential features in call centers is a call supervision capability which enables a supervisor to monitor or to assist an agent when needed. Using the Active Calls APIs set, you can dynamically add or remove a supervision session to an active call, toggle a call recording, terminate or finalize a call etc.

## Get a List of Active Calls
You can read agents' active calls to retrieve useful call's metadata. This API is essential as it returns the unique call id `uii` of each active call, and you can use the `uii` value in other APIs to manage that particular call.

Active calls can be listed based on a criteria called "Product". Each product must be identified by a product id. For example, to list all active calls under an account, you must obtain the account id and specify it in the request body.

### Primary Parameters

| API Property | Description |
|-|-|
| **`product`** | The name of a product, which can be one of the following criteria:</br>`"ACCOUNT"` - `"ACD"` - `"AGENT"` - `"CHAT_QUEUE"` - `"OUTBOUND"` - `"VISUAL_IVR"` - `"CLOUD_PROFILE"` - `"CLOUD_DESTINATION"` - `"TRAC_NUMBER"` - `"HTTP_SERVICES"` - `"SCRIPTING"` - `"TN_MANAGER"` - `"SURVEY"` - `"DNIS"` - `"TEAMS"` - `"KNOWLEDGE_BASE"` - `"UTILITIES"` |
| **`productId`** | The identifier of a selected product. E.g. if the **`product`** is `"ACCOUNT"`, the **productId** is the account id. |
| **`page`** | Number of page per request. |
| **`maxRows`** | Max number of items per page. |

### Request
Be sure to set the proper [BASE_URL](../../basics/uris/#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral) for your deployment.

```http
GET {BASE_URL}/api/v1/admin/accounts/{accountId}/activeCalls/list?product=ACCOUNT&productId=12440001
```

### Response
```json
[ { uii: "202005081040440132050000019657",
    accountId: "12440011",
    ani: "6501234567",
    dnis: "8661234567",
    enqueueTime: "2020-05-08T14:40:47.000+0000",
    dequeueTime: null,
    callState: "ACTIVE",
    archive: false,
    agentFirstName: "Paco",
    agentLastName: "Vu",
    destinationName: null } ]
```  


## Create a Manual Agent Call
Instead of manually dialing from a phone dial pad, an outbound call from an agent's phone number can be made programmatically using this API. This requires the agent to be online and available so that the call can be initiated from the associated phone (e.g. the Integrated softphone) that the agent selects when logging in his Agent dashboard.

### Primary Parameters

| API Property | Description |
|-|-|
| **`username`** | The username of an agent who makes the call |
| **`destination`** | The phone number of a callee. |
| **`ringDuration`** | The number of seconds a call should ring. |
| **`callerId`** | The phone number of the caller which can be seen by a callee. |

### Request
Be sure to set the proper [BASE_URL](../../basics/uris/#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral) for your deployment.

```http
POST {BASE_URL}/api/v1/admin/accounts/{accountId}/activeCalls/createManualAgentCall?username=some.name%40abc.com&destination=6501234567&ringDuration=5&callerId=1234567890
```

## Add Sessions to an Active Call.
You can add a third party to an active call. Typically, a third party is a supervisor who can join a call to monitor or to assist an agent. A supervisor can join a call in 3 different modes:

### Primary Parameters

| API Property | Description |
|-|-|
| **`destination`** | The phone number of a supervisor |
| **`sessionType`** | The purpose of a new session `MONITOR`, `BARGEIN` or `COACHING` |

### Supporting Values
The following value lists and APIs are used to retrieve predefined values for certain fields. Use these values to populate the correct parameter values of fields.

| Value | Description |
|-|-|
| **`MONITOR`** | A supervisor can only listen to the agent/customer conversation. |
| **`BARGEIN`** | A supervisor can join the agent/customer call and be able to listen and talk to all. |
| **`COACHING`** | A supervisor can listen to the agent/customer conversation, and be able to talk (whisper) to an agent only. |

### Request
Be sure to set the proper [BASE_URL](../../basics/uris/#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral) for your deployment.

```http
POST {BASE_URL}/api/v1/admin/accounts/{accountId}/activeCalls/{uii}/addSessionToCall?destination=+15554150123&sessionType=MONITOR
```

## Call Disposition
Sets the call disposition for either INBOUND or OUTBOUND calls and releases the agent from PD state.

### Primary Parameters

| API Property | Description |
|-|-|
| **`disposition`** | The name of a preconfigured disposition |
| **`callback`** | true or false to specify the callback request |
| **`callBackDTS`** | Callback date and time in the following format: yyyyMMddHHmmss |
| **`notes`** | Notes of this call disposition |

### Request
Be sure to set the proper [BASE_URL](../../basics/uris/#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral) for your deployment.

```http
POST {BASE_URL}/api/v1/admin/accounts/{accountId}/activeCalls/{uii}/dispositionCall

{
  phone: "6501234567"
}
```

## Terminate an Active Call
As the name implies, an active call can be terminated using this API.

### Request
Be sure to set the proper [BASE_URL](../../basics/uris/#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral) for your deployment.

```http
POST {BASE_URL}/api/v1/admin/accounts/{accountId}/activeCalls/{uii}/hangupCall
```

## Terminate an Active Session
Remove a third party from a call. This will not terminate an active call.

### Primary Parameters

| API Property | Description |
|-|-|
| **`phone`** | the phone number of a supervisor |

### Request
Be sure to set the proper [BASE_URL](../../basics/uris/#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral) for your deployment.

```http
POST {BASE_URL}/api/v1/admin/accounts/{accountId}/activeCalls/{uii}/hangupSession?phone=6501234567
```

### Toggle Call Recording On/Off for an Active Call
As the name implies, an active call recording can be easily toggled on or off using this API.

### Primary Parameters

| API Property | Description |
|-|-|
| **`record`** | 'true' for start recording and 'false' for stop recording |

### Request
Be sure to set the proper [BASE_URL](../../basics/uris/#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral) for your deployment.

```http
POST {BASE_URL}/api/v1/admin/accounts/{accountId}/activeCalls/{uii}/toggleCallRecording?record=true
```
