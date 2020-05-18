# Queues Basics

Queues are where calls are routed to. Be sure to make your queue active if you want calls to be routed properly, otherwise, callers to that queue will get a disconnected message.

## Core Concepts
Inbound **queues** are grouped within **queue groups** and act as the location to which calls are routed. Inbound queues can be configured to provide a specific experience you wish each customer to have while they’re waiting for an agent to take their call. You can configure settings like Queue Events to decide what customers will hear while waiting, including the hold music they’ll hear, their total wait time in queue, and more.

To reach the inbound queue, you need a number for callers to call.  This is referred to the DNIS number and must be configured in the DNIS Assignment.

## Prerequisite
Before using *Queues*, make sure to configure your test Agent (User) with the right priority and permissions.  Your Agent should have a high enough priority so the inbound call is routed to them first.  Also, the permission for the Agent should be "Allow inbound calls" to give the Agent the right to receive inbound calls.

You must first create a Queue Group before creating Queues. Start with a simple [Queue Groups](./queue-groups) and then create your first [Queues](./queues).

## Create Queue
Make sure you know which account and which queue group you are creating this new queue in before proceeding. Creating a new queue group initially requires very few parameters.

### Supporting APIs
The following APIs are used to retrieve predefined values for certain fields. Use these values to populate the correct parameter values of fields.

| Request | Description |
|-|-|
| `GET {BASE_URL}/api/v1/admin/accounts/{accountId}/dialGroups/withChildren` | Gets a list of dial groups for campaigns created under this account. |
| `GET {BASE_URL}/api/v1/admin/accounts/{accountId}/scriptGroups/withChildren` | Gets a list of script groups for agents to read and communicate to callers, created under this account. |
| `GET {BASE_URL}/api/v1/admin/accounts/{accountId}/auxStates/?activeOnly=true` | Gets a list of post call states for an agent. Some examples include "Available", "Away", "Lunch", etc. |

### Primary Parameters
Only `gateName` is a required parameter to create a Queue. All other parameters are optional.

| API Property |  | UI Display | UI Default | Description |
|-|-|-|-|-|
| **`isActive`** | Optional | Active | *unchecked* | Make the Queue active or inactive. |
| **`gateName`** | Required | Name | *empty* | Give this queue a name. |
| **`gateDesc`** | Optional | Description | *empty* | Set a short description for the new Queue. |
| **`gatePriority`** | Optional | Queue Priority | 0 [Normal] | Specify the priority for this Queue. The higher the number, the higher the priority. 6 is the highest priority allowed from this setting. |
| **`outboundCallerId`** | Optional | Outbound Caller ID | Inbound Callers ANI | This Automatic Number Identification (ANI) of the inbound caller's number is shown to the agent receiving the call from the Queue. |
| **`callbackCampaign`** | Optional | Campaign Callback Mapping | *empty* | If a customer is marked as a callback in the system, pick a outbound (dial group) campaign to assign them to. Retrieve a list of campaigns using `GET {BASE_URL}/api/v1/admin/accounts/{accountId}/dialGroups/withChildren` |
| **`abandonCampaign`** | Optional | Abandon Campaign Mapping | *empty* | If a caller hangs up in the queue before reaching an agent, the caller’s number will be moved to a campaign lead list (dial group) so they can be called back via the campaign. Retrieve a list of campaigns using `GET {BASE_URL}/api/v1/admin/accounts/{accountId}/dialGroups/withChildren` |
| **Call Recording Settings** | | | | |
| **`recordCall`** | Optional | Call Recordings | Yes - Record Full Call| Values are numeric and include `0`: No-Don't Record Call, `1`: Yes-Record Full Call. |
| **`stopRecordingOnTransfer`** | Optional | Recording on Transfer | Yes - Record on Transfer | Values are boolean and include `true`: No-Don't Record on Transfer, `false`: Yes-Record on Transfer. |
| **`recordingInConference`** | Optional | Recording Perspective | Inbound Caller | Values are boolean and include `true`: record from the Agent's perspective, `false`: record from the Inbound Caller's perspective. |
| **Metric Settings** | | | | |
| **`shortAbandonTime`** | Optional | Short Abandon Time | 30 | The system counts the number of callers who abandon the queue before x seconds elapse (using default, x=30 seconds). |
| **`slaTime`** | Optional | SLA Time | 30 | Use this field to monitor your call center’s service level times, as measured by the percent of calls answered within your SLA (Service Level Agreement) time. For example, type 30 in this fiedl to monitor the percentage of calls answered within 30 seconds. |
| **`shortCallTime`** | Optional | Short Call Time | 30 | Enter a time (in seconds) to identify any call duration you wish to mark as a short call time. For example, if you enter 30, the system will mark calls of 30 seconds or less as a ‘short call time’. |
| **`longCallTime`** | Optional | Long Call Time | 300 | Enter a time (in seconds) to identify any call duration you wish to mark as a long call time. For example, if you enter 300, the system will mark calls of greater than 300 seconds as a ‘long call time’. |
| **Agent Settings** | | | | |
| **`surveyPopType`** | Optional | Disable Dispositions and Agent Notes | *unchecked* | Check (set value to `SUPPRESS`) this box to prevent dispositions and the Agent Notes field from appearing within the agent interface for this queue. Enable this setting (set value to `FLASH`) when you wish to provide those options within an integrated agent script or an external app instead. |
| **`script`** | Optional | Integrated Script | None | Select an agent script for this queue. The script you choose here will be presented by default to all agents taking calls in this queue. Retrieve a list of scripts using `GET {BASE_URL}/api/v1/admin/accounts/{accountId}/scriptGroups/withChildren` |
| **`ttAccept`** | Optional | TT Accept | *unchecked* | Touch Tone Accept. Check this box if you'd like to require your agents to press a key when they’re ready to accept a call. |
| **`hangupOnDisposition`** | Optional | Hangup on Disposition | *unchecked* | Select this option to ensure agent calls are terminated immediately following disposition. This can be useful if you wish to ensure that a call is dispositioned only when the agent is ready to end the call (rather than at any other time during the call). |
| **`enableGlobalPhoneBook`** | Optional | Enable Global Phone Book | *unchecked* | Check this box to allow agents to access your global phone book when making transfers. |
| **`enableIvrTokens`** | Optional | Enable IVR Tokens | *unchecked* | This advanced feature allows you to pass tokens from IVR Studio (created via the scripting node) to an external app URL on the queue. |
| **`wrapTime`** | Optional | Wrap Time | 8 | Give agent 8 seconds after caller hangs up before making agent available to receive calls again. |
| **`acceptTime`** | Optional | Max Accept Time | 30 | For agents not in an **offhook** session, this setting specifies the amount of time in seconds the queue will ring the agent’s phone before requeueing the call to attempt another agent. |
| **`dispositionTimeout`** | Optional | Disposition Alert Timer (sec.) | 60 | This setting allows you to choose a time (in seconds) after which agents will receive a reminder to disposition their call. The timer starts when a call ends. |

One of the **Agent Settings** is available in a nested object. This setting includes the Agent's Post Call State a. See the example nested JSON object below:

```json hl_lines="4"
"afterCallState":
  {
    "id":11789,
    "description":"Available"
  }
},
```

| API Property |  | UI Display | UI Default | Description |
|-|-|-|-|-|
| **`afterCallState.description`** | Optional | Post Call State | *empty* | Choose the agent state you would like to place agents in once they finish a call. Options in this dropdown menu will populate according to the agent states you configure via the Agent States at the account level. Retrieve a list of states using `GET {BASE_URL}/api/v1/admin/accounts/{accountId}/auxStates/?activeOnly=true` |

### Request
=== "HTTP"
    ```html
    POST {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates
    Content-Type: application/json

    {
        "isActive":true,
        "gateName":"My Queue",
        "gateDesc":"An initial queue for this Queue Group",
        "gatePriority":"0", /* 0 is normal priority out of 6 priorities. Please see list below of priority values */
        "outboundCallerId":"ani", /* ani is the default inbound caller's ID. Please see list below of caller IDs */
    }
    ```
=== "Python"
    ```python
        from engagevoice.sdk_wrapper import *

        # Use your Developer Client App credentials
        RC_APP_CLIENT_ID = ""
        RC_APP_CLIENT_SECRET = ""

        # Enter your credentials here.  Usually consists of Main Number and Extension number. Main number includes international codes including '+'
        RC_USERNAME = ""
        RC_PASSWORD = ""
        RC_EXTENSION_NUMBER = ""

        # Login with RingCentral Office user credentials.
        ev = RestClient(RC_APP_CLIENT_ID, RC_APP_CLIENT_SECRET)

        # When you login, the account information is returned in the response
        try:
            resp = ev.login(RC_USERNAME, RC_PASSWORD, RC_EXTENSION_NUMBER)
            print (resp)
        except Exception as e:
            print (e)

        # Now that we are logged in, get a list of Queue Groups and find the Platform queue group for this user
        endpoint = 'admin/accounts/'+acctId+'/gateGroups'

        try:
            response = ev.get(endpoint)
            for group in response:
                if group["groupName"] == "Platform":
                    queueGroup = str(group["gateGroupId"])
                    print ("My Platform Group ID: " + queueGroup)
        except Exception as e:
            print (e)

        # Create a payload to POST to a new Queue
        data = {
            "isActive":True,
            "gateName":"My Queue",
            "gateDesc":"An initial queue for this Queue Group",
            }

        # And define the endpoint to create a Queue
        endpoint = 'admin/accounts/'+acctId+'/gateGroups/'+gateGrpId+'/gates'
        try:
            response = ev.post(endpoint, data)
            print ("Creating new Queue")
            print (json.dumps(response))
        except Exception as e:
            print (e)
    ```

Where key parameters are:

-   **isActive**

    Activates this new queue so agents can begin taking calls. If this is unchecked, callers attempting to reach this queue will receive a disconnected message.

-   **gateName**

    **Refers** to the name of this new queue. This is the only required field you need to present to create a queue.

-   **gateDesc**

    Refers to a short description for the queue. Describe the purpose of the queue here.

-   **gatePriority**

    If you wish for certain queues within a queue group to receive more calls than others, you can use this setting to specify a higher priority for this queue compared to other queues.

-   **outboundCallerId**

    This setting is the Caller ID that displays to either the agent or a third party (if there is a transfer event set up in the queue) receiving an inbound call.  Typically, this should be the caller's ID so Inbound Caller's ANI is the default.

The response will auto fill any undefined settings with default settings.

### Response
```json tab="Response"
{
  "isActive": true,
  "gateName": "My Queue",
  "gateDesc": "An initial queue for this Queue Group",
  "gatePriority": 0,
  "billingCode": null,
  "outboundCallerId": "ani",
  "manualCallerId": null,
  "transferCallerId": null,
  "callbackCampaign": null,
  "abandonCampaign": null,
  "recordCall": 1,
  "stopRecordingOnTransfer": false,
  "recordingInConference": false,
  "shortAbandonTime": 30,
  "slaTime": 30,
  "shortCallTime": 30,
  "longCallTime": 300,
  "whisperMessage": null,
  "blockedAniMessage": null,
  "onHoldMessage": null,
  "endCallMessage": null,
  "script": null,
  "appUrl": null,
  "backupAppUrl": null,
  "ttAccept": false,
  "hangupOnDisposition": false,
  "enableGlobalPhoneBook": false,
  "enableIvrTokens": false,
  "afterCallState":
  {
    "id":11789,
    "description":"Available"
  },
  "wrapTime": 8,
  "acceptTime": 30,
  "dispositionTimeout": 60,
  "dequeueSoapService": null,
  "resultFileDestination": null,
  "agentConnSoapService": null,
  "agentTermSoapService": null,
  "postCallSoapService": null,
  "postDispSoapService": null,
  "transferTermSoapService": null,
  "sunSched":"00000000",
  "monSched": "08002100",
  "tueSched":"08002100",
  "wedSched": "08002100",
  "thuSched":"08002100",
  "friSched": "08002100",
  "satSched":"00000000",  
  "throttlingAniEvent": null,
  "afterCallState": null,
  "maxQueueEvent": null,
  "fifoDisabled": true,
  "observeDst": true,
  "specialAniEvent": null,
  "throttleDays": 0,
  "surveyPopType":"FLASH",
  "dequeueDelay": 0,
  "agentPopMessage": null,
  "noAgentEvent": null,
  "requeueType": "ADVANCED",
  "throttleCalls": 0,
  "afterCallBaseState": null,
  "syncQueueWait": 10,
  "maxQueueLimit": -1,
  "gateGroup":
    {"id": 52653,
     "description": "Platform"
    },
  "gateId": 72976,
  "gateClosedEvent": null,
  "permissions": [],
  "pauseRecordingSec": 30,
  "survey": null,
  "createdOn": "2020-05-15T20:38:13.686+0000",
  "revMatch": false,
  "agentGateAccess": []
}
```

Where:

-   **gatePriority** (Queue Priority) can take on the following values:

    | Value | Description |
    |-|-|
    | **`0`** | [0] Normal - This is the default priority |
    | **`1`** | [1] Medium - This is medium priority |
    | **`2`** | [2] High - This is high priority |
    | **`3`** | [3] High Level 2 - This is high priority is 1 level higher |
    | **`4`** | [4] High Level 3 - This is high priority is 2 levels higher |
    | **`5`** | [5] High Level 4 - This is high priority is 3 levels higher |
    | **`6`** | [6] High Level 5 - This is high priority is 4 levels higher |
    | **`-1`** | [-1] Low - This is the lowest priority |

-   **outboundCallerId** (Outbound Caller ID) can take on the following values:

    | Value | Description |
    |-|-|
    | **`Inbound Callers ANI`** | This Automatic Number Identification (ANI) of the inbound caller's number is shown to the agent receiving the call from the Queue. |
    | **`DNIS`** | This setting refers to the destination number, which is usually (but not always) the inbound number your callers will dial to reach your call center. |
    | **`Originating DNIS`** | This setting refers to a phone number your callers can dial to reach your contact center, which is usually (but not always) the destination number that you would like to route calls through. |
    | **`Dynamic Unique ID`** | A unique ten-digit, system-generated ID for each call session. This setting is useful in identifying specific calls in cases in which a 30-digit unique ID is not an option (or if you keep your own records that don’t include the unique ID). |

## Retrieve Queues
Retrieve a list of Queues using the `gate` endpoint.

### Optional Parameters
The following parameters are optional.

| API Property | Type | UI Display | UI Default | Description |
|-|-|-|-|-|
| **`page`** | Integer | Hidden | 1 | A way to specify which page to show for a long number of Queues |
| **`maxRows`** | Integer | Hidden | ?? | You can specify the maximum number of Queues to return in a single call. |

### Request

=== "HTTP"
    ```html
    GET {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates
    ```
=== "Python"
    ```python
        from engagevoice.sdk_wrapper import *

        # Use your Developer Client App credentials
        RC_APP_CLIENT_ID = ""
        RC_APP_CLIENT_SECRET = ""

        # Enter your credentials here.  Usually consists of Main Number and Extension number. Main number includes international codes including '+'
        RC_USERNAME = ""
        RC_PASSWORD = ""
        RC_EXTENSION_NUMBER = ""

        # Login with RingCentral Office user credentials.
        ev = RestClient(RC_APP_CLIENT_ID, RC_APP_CLIENT_SECRET)

        # When you login, the account information is returned in the response
        try:
            resp = ev.login(RC_USERNAME, RC_PASSWORD, RC_EXTENSION_NUMBER)
            print (resp)
        except Exception as e:
            print (e)

        # Now that we are logged in, get a list of Queue Groups and find the Platform queue group for this user
        endpoint = 'admin/accounts/'+acctId+'/gateGroups'

        try:
            response = ev.get(endpoint)
            for group in response:
                if group["groupName"] == "Platform":
                    queueGroup = str(group["gateGroupId"])
                    print ("My Platform Group ID: " + queueGroup)
        except Exception as e:
            print (e)

        # Let's get a list of Queues from this Platform Queue Group
        endpoint = 'admin/accounts/'+acctId+'/gateGroups/'+queueGroup+'/gates'

        try:
            response = ev.get(endpoint)
            print (json.dumps(response))
        except Exception as e:
            print (e)
    ```

### Response
```json tab="Response"
[
  {
    "script": null,
    "gateGroup":
      {
        "id": 52653,
        "description": "Platform"
      },
    "gateName": "Platform Inbound",
    "gateDesc": null,
    "gateId": 72874,
    "agentGateAccess": null,
    "isActive": true,
    "permissions": []
  },
  {
    "script": null,
    "gateGroup":
      {
        "id": 52653,
        "description": "Platform"
      },
    "gateName": "My Queue",
    "gateDesc": "An initial queue for this Queue Group",
    "gateId": 72979,
    "agentGateAccess": null,
    "isActive": true,
    "permissions": []
  }
]
```

## Retrieve a Single Queue

Retrieving details for a single Queue  using the `gates` endpoint.

### Request

=== "HTTP"
    ```html
    GET {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}
    ```
=== "Python"
    ```python
        from engagevoice.sdk_wrapper import *

        # Use your Developer Client App credentials
        RC_APP_CLIENT_ID = ""
        RC_APP_CLIENT_SECRET = ""

        # Enter your credentials here.  Usually consists of Main Number and Extension number. Main number includes international codes including '+'
        RC_USERNAME = ""
        RC_PASSWORD = ""
        RC_EXTENSION_NUMBER = ""

        # Login with RingCentral Office user credentials.
        ev = RestClient(RC_APP_CLIENT_ID, RC_APP_CLIENT_SECRET)

        # When you login, the account information is returned in the response
        try:
            resp = ev.login(RC_USERNAME, RC_PASSWORD, RC_EXTENSION_NUMBER)
            print (resp)
        except Exception as e:
            print (e)

        # Now that we are logged in, get a list of Queue Groups and find the Platform queue group for this user
        endpoint = 'admin/accounts/'+acctId+'/gateGroups'

        try:
            response = ev.get(endpoint)
            for group in response:
                if group["groupName"] == "Platform":
                    queueGroup = str(group["gateGroupId"])
                    print ("My Platform Group ID: " + queueGroup)
        except Exception as e:
            print (e)

        # Let's find the Queue we just created in this Platform Queue Group
        endpoint = 'admin/accounts/'+acctId+'/gateGroups/'+queueGroup+'/gates'

        try:
            response = ev.get(endpoint)
            for queue in response:
                if queue["gateName"] == "My Queue":
                    print (json.dumps(queue))
                    myQueue = queue
                    queueId = str(queue["gateId"])
                    print ("My Queue ID: " + queueId)
        except Exception as e:
            print (e)
    ```

### Response
```json tab="Response"
{
  "isActive": true,
  "gateName": "My Queue",
  "gateDesc": "An initial queue for this Queue Group",
  "gatePriority": 0,
  "billingCode": null,
  "outboundCallerId": "ani",
  "manualCallerId": null,
  "transferCallerId": null,
  "callbackCampaign": null,
  "abandonCampaign": null,
  "recordCall": 1,
  "stopRecordingOnTransfer": false,
  "recordingInConference": false,
  "shortAbandonTime": 30,
  "slaTime": 30,
  "shortCallTime": 30,
  "longCallTime": 300,
  "whisperMessage": null,
  "blockedAniMessage": null,
  "onHoldMessage": null,
  "endCallMessage": null,
  "script": null,
  "appUrl": null,
  "backupAppUrl": null,
  "ttAccept": false,
  "hangupOnDisposition": false,
  "enableGlobalPhoneBook": false,
  "enableIvrTokens": false,
  "afterCallState": null,
  "wrapTime": 8,
  "acceptTime": 30,
  "dispositionTimeout": 60,
  "dequeueSoapService": null,
  "resultFileDestination": null,
  "agentConnSoapService": null,
  "agentTermSoapService": null,
  "postCallSoapService": null,
  "postDispSoapService": null
  "transferTermSoapService": null,
  "satSched": "00000000",
  "sunSched": "00000000",
  "monSched": "08002100",
  "tueSched": "08002100",
  "wedSched": "08002100",
  "thuSched": "08002100",
  "friSched": "08002100",
  "throttlingAniEvent": null,
  "maxQueueEvent": null,
  "fifoDisabled": true,
  "observeDst": true,
  "specialAniEvent": null,
  "throttleDays": 0,
  "surveyPopType": "FLASH",
  "dequeueDelay": 0,
  "agentPopMessage": null,
  "noAgentEvent": null,
  "requeueType": "ADVANCED",
  "throttleCalls": 0,
  "afterCallBaseState": null,
  "blockedAniMessage": null,
  "syncQueueWait": 10,
  "maxQueueLimit": -1,
  "gateGroup":
    {
      "id": 52653,
      "description": "Platform"
    },
  "gateId": 72991,
  "gateClosedEvent": null,
  "permissions": [],
  "pauseRecordingSec": 30,
  "survey": null,
  "createdOn": "2020-05-18T15:41:44.000+0000",
  "revMatch": false,
  "agentGateAccess": null,
}
```

## Update a Single Queue

Update the details for a single Queue  using the `gates` endpoint. Several details need to be updated with a single `PUT` command so make sure to `GET` all details, modify the relevant fields, and then submit the entire object to update the Queue.

### Request

=== "HTTP"
    ```html hl_lines="7 25"
    # Retrieve the entire Queue JSON object
    GET {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}
    Content-Type: application/json
    {
      "isActive": true,
      "gateName": "My Queue",
      "gateDesc": "An initial queue for this Queue Group",
      "gateGroup":
        {
          "id": 52653,
          "description": "Platform"
        },
      "gateId": 72992,
      "script": null,
      "agentGateAccess": null,
      "permissions": []
    }

    # Modify the gateDesc and send the entire JSON response back
    PUT {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}
    Content-Type: application/json
    {
      "isActive": true,
      "gateName": "My Queue",
      "gateDesc": "An *edited* queue for this Queue Group",
      "gateGroup":
        {
          "id": 52653,
          "description": "Platform"
        },
      "gateId": 72992,
      "script": null,
      "agentGateAccess": null,
      "permissions": []
    }
    ```
=== "Python"
    ```python
        from engagevoice.sdk_wrapper import *

        # Use your Developer Client App credentials
        RC_APP_CLIENT_ID = ""
        RC_APP_CLIENT_SECRET = ""

        # Enter your credentials here.  Usually consists of Main Number and Extension number. Main number includes international codes including '+'
        RC_USERNAME = ""
        RC_PASSWORD = ""
        RC_EXTENSION_NUMBER = ""

        # Login with RingCentral Office user credentials.
        ev = RestClient(RC_APP_CLIENT_ID, RC_APP_CLIENT_SECRET)

        # When you login, the account information is returned in the response
        try:
            resp = ev.login(RC_USERNAME, RC_PASSWORD, RC_EXTENSION_NUMBER)
            print (resp)
        except Exception as e:
            print (e)

        # Now that we are logged in, get a list of Queue Groups and find the Platform queue group for this user
        endpoint = 'admin/accounts/'+acctId+'/gateGroups'

        try:
            response = ev.get(endpoint)
            for group in response:
                if group["groupName"] == "Platform":
                    queueGroup = str(group["gateGroupId"])
                    print ("My Platform Group ID: " + queueGroup)
        except Exception as e:
            print (e)

        # Let's find the Queue we just created in this Platform Queue Group
        endpoint = 'admin/accounts/'+acctId+'/gateGroups/'+queueGroup+'/gates'

        try:
            response = ev.get(endpoint)
            for queue in response:
                if queue["gateName"] == "My Queue":
                    print (json.dumps(queue))
                    myQueue = queue
                    queueId = str(queue["gateId"])
                    print ("My Queue ID: " + queueId)
        except Exception as e:
            print (e)

        # Update the queue description
        endpoint = 'admin/accounts/'+acctId+'/gateGroups/'+queueGroup+'/gates/'+queueId
        queue["gateDesc"] = "An *edited* queue for this Queue Group"

        try:
            response = ev.put(endpoint, queue)
            print (json.dumps(response))
        except Exception as e:
            print (e)
    ```

## Delete a Single Queue

Delete a single Queue Group using the `gates` endpoint.

### Request
```html tab="HTTP"
DELETE {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}
```
