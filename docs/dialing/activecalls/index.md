# Engage Voice Active Call APIs

Active Call APIs allow you to programmatically manage agents' active calls. You can read agent's active calls and each call metadata, adding a supervision session to a call or terminating an active call etc. This includes a capability to make a new outbound call programatically.

### Get a list of active calls
Read agents' active call data and . Active calls can be read based on a category called "Product".



<a href="list-activecalls" class="btn btn-light qs-link">See details &raquo;</a>

### Create a manual agent call
Instead of dialing from a phone dial pad, You can can make an outbound call programmatically from an agent phone number.

To make an outbound call, make an HTTP POST request to the `activeCall/createManualAgentCall` endpoint with the body parameters shown in the following table:

`POST /api/v1/admin/accounts/{accountId}/activeCall/createManualAgentCall`

| Parameter | Description |
|-|-|
| **username** | The username of an agent who makes the call |
| **destination** | The phone number of a callee. |
| **ringDuration** | The number of seconds a call should ring. |
| **callerId** | The phone number of the caller which should be seen by a callee. |


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
You can add a third party to an active call. Typically, a third party is a supervisor who can join an active call to monitor or to assist an agent. A supervisor can join a call in 3 modes:

| Mode | Purpose |
|-|-|
| **MONITOR** | a supervisor can only listen to the agent/customer conversation. |
| **BARGEIN** | a supervisor can join the agent/customer call and be able to listen and talk to all. |
| **COACHING** | a supervisor can listen to the agent/customer conversation, and be able to talk (whisper) to an agent only. |

To add a session to an active call, make an HTTP POST request to the `activeCall/{uii}/addSessionToCall` endpoint with the request body parameters shown in the following table:

`POST /api/v1/admin/accounts/{accountId}/activeCall/{uii}/addSessionToCall`

| Parameter | Description |
|-|-|
| **destination** | The phone number of a supervisor |
| **sessionType** | The type of a new session "MONITOR", "BARGEIN" or "COACHING" |


```http
`POST {baseURL}/api/v1/admin/accounts/{accountId}/activeCalls/{uii}/addSessionToCall`

{
  destination: "6501234567",
  sessionType: "MONITOR"
}
```

### Call disposition
Sets the call disposition for either INBOUND or OUTBOUND calls and releases the agent from PD state.

`https://engage.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/activeCalls/{uii}/dispositionCall`

### Terminates an active call

`https://engage.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/activeCalls/{uii}/hangupCall`

### Terminates an active session

`https://engage.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/activeCalls/{uii}/hangupSession`

### Toggling call recording on/off for an active call

Provides support for toggling call recording on/off for an active call

| Parameter | Description |
|-|-|
| **record** | 'true' for start recording and 'false' for stop recording |


`https://engage.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/activeCalls/{uii}/toggleCallRecording`
