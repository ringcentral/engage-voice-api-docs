# Engage Voice Active Call APIs
Active Call APIs allow you to manage agents' active calls. One of the essential features in call centers is a call supervision capability which enables a supervisor to monitor or to assist an agent when needed. Using the Active Calls APIs set, you can dynamically add or remove a supervision session to an active call, toggle a call recording, terminate or finalize a call etc.


### Get a list of active calls
You can list agents' active calls with useful call's metadata. This API is essential as it returns the unique call id `uii` of each active call, so that you can use the `uii` to manage that particular call with other APIs.

<a href="list-activecalls" class="btn btn-light qs-link">See details &raquo;</a>

### Create a manual agent call
Instead of manually dialing from a phone dial pad, an outbound call from an agent's phone number can be made programmatically using this API. This requires the agent to be online and available so that the call can be initiated from the associated phone (e.g. the Integrated softphone) that the agent selects when logging in his Agent dashboard.

To initiate an outbound call, make an HTTP POST request to the `activeCall/createManualAgentCall` endpoint with the request body parameters shown in the following table:

| Parameter | Description |
|-|-|
| **username** | The username of an agent who makes the call |
| **destination** | The phone number of a callee. |
| **ringDuration** | The number of seconds a call should ring. |
| **callerId** | The phone number of the caller which can be seen by a callee. |


```http
`POST {baseURL}/api/v1/admin/accounts/{accountId}/activeCalls/createManualAgentCall`

{
  username: "some.name@abc.com",
  destination: "6501234567",
  ringDuration: 5,
  callerId: "1234567890"
}
```

### Add sessions to an active call.
You can add a third party to an active call. Typically, a third party is a supervisor who can join a call to monitor or to assist an agent. A supervisor can join a call in 3 different modes:

| Mode | Purpose |
|-|-|
| **MONITOR** | A supervisor can only listen to the agent/customer conversation. |
| **BARGEIN** | A supervisor can join the agent/customer call and be able to listen and talk to all. |
| **COACHING** | A supervisor can listen to the agent/customer conversation, and be able to talk (whisper) to an agent only. |

To add a session to an active call, make an HTTP POST request to the `activeCall/{uii}/addSessionToCall` endpoint with the request body parameters shown in the following table:

| Parameter | Description |
|-|-|
| **destination** | The phone number of a supervisor |
| **sessionType** | The purpose of a new session "MONITOR", "BARGEIN" or "COACHING" |


```http
`POST {baseURL}/api/v1/admin/accounts/{accountId}/activeCalls/{uii}/addSessionToCall`

{
  destination: "6501234567",
  sessionType: "MONITOR"
}
```

### Call disposition
Sets the call disposition for either INBOUND or OUTBOUND calls and releases the agent from PD state.

To finalize an active call with disposition, make an HTTP POST request to the `activeCall/{uii}/dispositionCall` endpoint with the request body parameters shown in the following table:

| Parameter | Description |
|-|-|
| **disposition** | The name of a preconfigured disposition |
| **callback** | true or false to specify the callback request |
| **callBackDTS** | Callback date and time |
| **notes** | Notes of this call disposition |


```http
`POST {baseURL}/api/v1/admin/accounts/{accountId}/activeCalls/{uii}/dispositionCall`

{
  phone: "6501234567"
}
```

### Terminate an active call
As the name implies, an active call can be terminated using this API.

To hang up an active call, make an HTTP POST request to the `activeCall/{uii}/hangupCall` as shown below:

```http
`POST {baseURL}/api/v1/admin/accounts/{accountId}/activeCalls/{uii}/hangupCall`

{
  phone: "6501234567"
}
```

### Terminate an active session
Remove a third party from a call. This will not terminate an active call.

To remove a supervision session from an active call, make an HTTP POST request to the `activeCall/{uii}/hangupSession` endpoint with the request body parameters shown in the following table:

| Parameter | Description |
|-|-|
| **phone** | the phone number of a supervisor |

```http
`POST {baseURL}/api/v1/admin/accounts/{accountId}/activeCalls/{uii}/hangupSession`

{
  phone: "6501234567"
}
```

### Toggle call recording on/off for an active call
As the name implies, an active call recording can be easily toggled on or off using this API.

To turn on or off call recording for an active call, make an HTTP POST request to the `activeCall/{uii}/toggleCallRecording` as shown below:

| Parameter | Description |
|-|-|
| **record** | 'true' for start recording and 'false' for stop recording |


```http
`POST {baseURL}/api/v1/admin/accounts/{accountId}/activeCalls/{uii}/toggleCallRecording`

{
  record: true
}
```
