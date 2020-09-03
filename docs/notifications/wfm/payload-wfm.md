# Understanding the Event Payload

Workforce Management events are sent for changes to agent states, login/logoff, or end of call. Understanding what is sent with this Generic HTTP event is detailed below so you can understand the payload and transform the event to your favorite workforce management application.

## Agent Login Events

Agent Login Events sends notifications every time an agent logs in or changes state.  

### Agent Login Information

The following payload is created and sent to the URL destination specified.

| API Property | Description |
|-|-|
| **`external_agent_id`** | A custom agent ID used for external mappings |
| **`duration`** | Amount of time to login |
| **`agent_login_id`** | An internal unique agent *login* identifier |
| **`account_id`** | The unique account this agent belongs to |
| **`event_type`** | The event type that occurred. In this case, this should always be `LOGIN` |
| **`agent_id`** | An internal unique identifier for the agent |
| **`date_time`** | The login time in ISO 8601 format |
| **`agent_phone`** | The agent's phone number. This can either be their direct number or main number plus extension. |
| **`username`** | The username provided for login. This is usually the given email address combined with the unique account ID |
| **`source_ip`** | IP Address where the agent is logging in from |

```html tab="Login Request Body"
{
  "external_agent_id":null,
  "duration":"0",
  "agent_login_id":"612730076",
  "account_id":"15300002",
  "event_type":"LOGIN",
  "agent_id":"1369310",
  "date_time":"2020-06-25 14:36:49",
  "agent_phone":"16505550100*1212@RC_SOFTPHONE",
  "username":"rc.guest+15300002_1791@gmail.com",
  "source_ip":"192.168.0.100"
}
```

## Agent Logoff Events

Agent Logoff Events sends notifications every time an agent logs out or leaves their agent session.  

### Agent Logoff Information

The following payload is created and sent to the URL destination specified.

| API Property | Description |
|-|-|
| **`external_agent_id`** | A custom agent ID used for external mappings |
| **`duration`** | Amount of time the agent was online before logging off |
| **`agent_login_id`** | An internal unique agent *login* identifier |
| **`account_id`** | The unique account this agent belongs to |
| **`event_type`** | The event type that occurred. In this case, this should always be `LOGOUT` |
| **`agent_id`** | An internal unique identifier for the agent |
| **`date_time`** | The logoff time in ISO 8601 format |
| **`agent_phone`** | The agent's phone number. This can either be their direct number or main number plus extension. |
| **`username`** | The username of the user logging off. This is usually the given email address combined with the unique account ID |
| **`source_ip`** | IP Address where the agent is logging off from |


```html tab="Logoff Request Body"
{
  "external_agent_id":null,
  "duration":"24",
  "agent_login_id":"612960320",
  "account_id":"15300002",
  "event_type":"LOGOUT",
  "agent_id":"1369310",
  "date_time":"2020-07-16 19:21:19",
  "agent_phone":"16505550100*1212@RC_SOFTPHONE",
  "username":"rc.guest+15300002_1791@gmail.com",
  "source_ip":"192.168.0.100"
}
```

## Agent State Events

Agent State Events sends notifications every time an agent changes their own state. Predefined states include AVAILABLE, LUNCH, ON BREAK, TRAINING, AWAY, TRANSITION, ENGAGED and WORKING. Even custom states can be created on an account and the agent can select those custom states, however, custom states must also be mapped to a base state and that base state is a fixed set of states. Custom state events only send when you select "Send All Agent States".

### Agent State Information

When an agent first logs in, the state events are unique. Two state events are fired with the initial state event transitioning from LOGIN state to AVAILABLE and then a subsequent event for transitioning to "Available" in the agent's aux state.

| API Property | Description |
|-|-|
| **`agent_id`** | An internal unique identifier for the agent |
| **`prev_state`** | The state the agent was in before this changed state |
| **`prev_aux_state`** | The aux state is the state name shown to the agent before this changed state |
| **`agent_phone`** | The agent's phone number for logging in. This can either be their direct number or main number plus extension. |
| **`source_ip`** | IP Address where the agent is logging in from |
| **`external_agent_id`** | A custom agent ID used for external mappings |
| **`duration`** | Amount of time to login |
| **`agent_login_id`** | An internal unique agent *login* identifier |
| **`account_id`** | The unique account this agent belongs to |
| **`event_type`** | The state the agent selected to be in or is automatically placed in |
| **`event_aux_type`** | Similar to the `event_type`, this is the state the agent chose to be in, but is the name the agent sees in the agent console |
| **`date_time`** | The login time in ISO 8601 format |
| **`pending_disp`** | [0] if call ended and disposition has not been completed yet. |
| **`username`** | The agent's unique username which is typically their email address. |
| **`call_id`** | Once the call is connected, a unique call ID is created to identify the call |
| **`call_source_id`** | The unique call identifier this call came from |
| **`call_source_name`** | The Queue name this call came from |
| **`dnis`** | The number called to be put in the queue and eventually routed to the agent. This applies to ACD calls only |
| **`call_type`** | The type of call this is, whether inbound dialed calls (`ACD`) or outbound lead calls (`VPD`) |

```html tab="Initial Request Body"
{
  "agent_id":"1369310",
  "prev_state":"LOGIN",
  "prev_aux_state":"",
  "agent_phone":"16505550100*1212@RC_SOFTPHONE",
  "source_ip":"192.168.0.100",
  "external_agent_id":null,
  "duration":"0",
  "agent_login_id":"612829048",
  "account_id":"15300002",
  "event_type":"AVAILABLE",
  "event_aux_type":"",
  "date_time":"2020-06-30 19:44:01",
  "pending_disp":"0",
  "username":"rc.guest+15300002_1791@gmail.com"
}
```

```html tab="Available Request Body" hl_lines="3 11 12"
{
  "agent_id":"1369310",
  "prev_state":"AVAILABLE",
  "prev_aux_state":"",
  "agent_phone":"16505550100*1212@RC_SOFTPHONE",
  "source_ip":"192.168.0.100",
  "external_agent_id":null,
  "duration":"1",
  "agent_login_id":"612829048",
  "account_id":"15300002",
  "event_type":"AVAILABLE",
  "event_aux_type":"Available",
  "date_time":"2020-06-30 19:44:02",
  "pending_disp":"0",
  "username":"rc.guest+15300002_1791@gmail.com"
}
```

```html tab="Transition Request Body" hl_lines="3 4 11 12"
{
  "agent_id":"1369310",
  "prev_state":"AVAILABLE",
  "prev_aux_state":"Available"
  "agent_phone":"16505550100*1212@RC_SOFTPHONE",
  "source_ip":"192.168.0.100",
  "external_agent_id":null,
  "duration":"17",
  "agent_login_id":"612829048",
  "account_id":"15300002",
  "event_type":"TRANSITION",
  "event_aux_type":"",
  "date_time":"2020-06-30 19:44:30",
  "pending_disp":"0",
  "username":"rc.guest+15300002_1791@gmail.com"
}
```

```html tab="Engaged Request Body" hl_lines="3 11 12"
{
  "agent_id":"1369310",
  "prev_state":"TRANSITION",
  "prev_aux_state":"",
  "agent_phone":"16505550100*1212@RC_SOFTPHONE",
  "source_ip":"192.168.0.100",
  "external_agent_id":null,
  "duration":"0",
  "agent_login_id":"612829048",
  "account_id":"15300002",
  "event_type":"ENGAGED",
  "event_aux_type":"",
  "date_time":"2020-06-30 19:44:30",
  "pending_disp":"0",
  "username":"rc.guest+15300002_1791@gmail.com",
  "call_id":"202008281319380132120000030797",
  "call_source_id":"72992",
  "call_source_name":"My Queue",
  "dnis":"2095550101",
  "call_type":"ACD"
}
```

After the initial state event, a subsequent state event fires to change the aux state to a state the agent will be able to read.  For example, the aux state today shows "Available" to the agent, but that can be customized to read "Ready for Calls".


## End Call Events

Call events can be from two types of calls: an inbound call or an outbound call. At the end of a call, details about the call are made available in the call event.  These details include the call recording, call duration, the DNIS which the caller dialed, the caller's ANI, and the call state.  Call state are the agent dispositions of the call and depend upon being an inbound call or outbound call.

!!! important
    While the recording URL is sent 1-3 seconds after a call is ended, the actual recording takes more time to encode. Depending on the length of the recording, the recording link may not be valid for up to 1-2 minutes after the end call event.

### End Call Information

| API Property | Description |
|-|-|
| **`recording_url`** | A link to the full audio call recording (WAV) |
| **`queue_duration`** | Amount of time the caller was in the queue |
| **`agent_disposition`** | Any notes that the agent took about the call |
| **`gate_name`** | The queue the caller came from |
| **`call_state`** | For inbound calls, the call was not answered (`DEFLECTED`), `ANSWERED`, or the caller decided to `ABANDON` the call. For outbound calls, the call was `ANSWERED`, `ABANDONED`, or sent to a `MACHINE` |
| **`call_duration`** | How long was the call for in seconds |
| **`call_id`** | A unique internal identifier for the call |
| **`account_id`** | The account the caller dialed the main number for |
| **`event_type`** | For inbound routed calls, this is noted as an Automatic Call Distribution (`ACD-CALL`). For outbound calls, this is noted as a dialed call (`VPD-CALL`) |
| **`gate_id`** | The unique queue identifier |
| **`call_start`** | The start time of the call in ISO 8601 format |
| **`dnis`** | Dialed Number Identification Service - this is the number the caller dialed |
| **`ani`** | Automatic Number Identification - this is the caller's number |

```html tab="Unanswered Request Body"
{
  "recording_url":"",
  "queue_duration":"0",
  "agent_disposition":"",
  "gate_name":"My Queue",
  "call_state":"DEFLECTED",
  "call_duration":"1",
  "call_id":"202006302131470132090000083238",
  "account_id":"15300002",
  "event_type":"ACD-CALL",
  "gate_id":"72992",
  "call_start":"2020-06-30 21:31:47",
  "dnis":"4155550110",
  "ani":"5105550111"
}
```

```html tab="Answered Request Body"
{
  "recording_url":"https://c02-recordings.virtualacd.biz/api/v1/calls/recordings/?v=1&accountId=15300002&bucket=c02-recordings&region=us-east-1&compliance=false&file=15300002/202007/30/202007302136360132130000036446-1.WAV",
  "agent_id":"1369310",
  "queue_duration":"3",
  "agent_disposition":"",
  "gate_name":"My Queue",
  "call_state":"ANSWERED",
  "call_duration":"18",
  "call_id":"202006302136360132130000036446",
  "external_agent_id":null,
  "account_id":"15300002",
  "event_type":"ACD-CALL",
  "gate_id":"72992",
  "call_start":"2020-06-30 21:36:37",
  "dnis":"4155550110",
  "ani":"5105550111",
  "username":"rc.guest+15300002_1791@gmail.com"
}
```
