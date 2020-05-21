# About Queue Events

In Creating an inbound [Queue](./queue), we discussed that inbound queues can be configured to provide the specific experience you want each caller to have while waiting for an agent to take their call. This experience can be configured by creating [Queue Events](./queue-events), a series of sequential events that the customer will experience once they are routed to the queue.

You can configure queue events to be as simple or complex as you like, from providing hold music for the caller while they wait to providing DTMF input options that the caller can choose from to determine the destination they’d like to route to.

## Core Concepts

### Priority Queue Events

You can create queue events that will typically occur in this queue, but you can also create special queue events — that is, priority queue events — that will occur when specific conditions exist, such as when your queue is closed or when the queue has reached the maximum number of calls.

### Speical ANI and Velocity ANI

You can also configure a priority queue event for specific ANIs (Automatic Number Identification) — that is, the phone number of the incoming caller. These priority events allow you to create special queue events for callers that you would like to give special routing priority.

You can create a priority queue event for two different types of ANIs: Special ANI and Velocity ANI. Special ANI priority events can be used for callers you would like to prioritize, such as your VIP customers. Velocity ANI priority events can be used to flag certain ANIs that call a specific amount of times in a certain amount of days. Once a caller has been flagged, the system will send them through the Velocity ANI queue event.

## Create Queue Events

Queue Events are actually a component of Queues and therefore do not need a `POST` method.  Create the [Queue](./queues) first and then update the Queue Events details using `PUT` below.

## Retrieve Queue Events

Retrieve a list of Queue Events set on this [Queue](./queues).

### Request

=== "HTTP"
    ```html
    GET {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents
    ```

### Response

=== "Response"
    ```json
    [
      {
        "eventId":67882,
        "eventRank":0,
        "queueEvent":"PLAY-AUDIO-LOOP:holdmusic",
        "eventDuration":120,
        "enableDtmf":0,
        "gate":
          {
            "permissions":[],
            "gateId":73001,
            "gateName":"My Queue (Spanish)",
            "gateDesc":"An *edited* queue for this Queue Group",
            "billingCode":null,
            "dequeueDelay":0,
            "maxQueueLimit":-1,
            "maxQueueEvent":null,
            "noAgentEvent":null,
            "specialAniEvent":null,
            "gateClosedEvent":null,
            "throttlingAniEvent":null,
            "throttleCalls":0,
            "throttleDays":0,
            "monSched":"08002100",
            "tueSched":"08002100",
            "wedSched":"08002100",
            "thuSched":"08002100",
            "friSched":"08002100",
            "satSched":"00000000",
            "sunSched":"00000000",
            "agentPopMessage":null,
            "whisperMessage":null,
            "onHoldMessage":null,
            "blockedAniMessage":null,
            "gatePriority":0,
            "recordCall":1,
            "stopRecordingOnTransfer":false,
            "recordingInConference":false,
            "revMatch":false,
            "appUrl":null,
            "backupAppUrl":null,
            "surveyPopType":"FLASH",
            "createdOn":"2020-05-18T19:22:12.000+0000",
            "shortAbandonTime":30,
            "shortCallTime":30,
            "longCallTime":300,
            "acceptTime":30,
            "ttAccept":false,
            "requeueType":"ADVANCED",
            "slaTime":30,
            "afterCallBaseState":null,
            "hangupOnDisposition":false,
            "wrapTime":8,
            "endCallMessage":null,
            "outboundCallerId":"ani",
            "transferCallerId":null,
            "manualCallerId":null,
            "syncQueueWait":10,
            "enableGlobalPhoneBook":false,
            "fifoDisabled":true,
            "pauseRecordingSec":30,
            "isActive":true,
            "observeDst":true,
            "enableIvrTokens":false,
            "dispositionTimeout":60,
            "gateGroup":
              {
                "id":52676,
                "description":"My Queue Group"
              },
            "afterCallState":null,
            "postCallSoapService":null,
            "dequeueSoapService":null,
            "agentConnSoapService":null,
            "postDispSoapService":null,
            "transferTermSoapService":null,
            "agentTermSoapService":null,
            "callbackCampaign":null,
            "abandonCampaign":null,
            "resultFileDestination":null,
            "survey":null,
            "gatePriorityGroup":null,
            "script":null,
            "gateQueueEvents":null,
            "agentGateAccess":null,
            "gateOpen":true
          }
      },
      {
        "eventId":67883,
        "eventRank":1,
        "queueEvent":"END-CALL:true",
        "eventDuration":0,
        "enableDtmf":0,
        "gate":
          {
            "permissions":[],
            "gateId":73001,
            "gateName":"My Queue (Spanish)",
            "gateDesc":"An *edited* queue for this Queue Group",
            "billingCode":null,
            "dequeueDelay":0,
            "maxQueueLimit":-1,
            "maxQueueEvent":null,
            "noAgentEvent":null,
            "specialAniEvent":null,
            "gateClosedEvent":null,
            "throttlingAniEvent":null,
            "throttleCalls":0,
            "throttleDays":0,
            "monSched":"08002100",
            "tueSched":"08002100",
            "wedSched":"08002100",
            "thuSched":"08002100",
            "friSched":"08002100",
            "satSched":"00000000",
            "sunSched":"00000000",
            "agentPopMessage":null,
            "whisperMessage":null,
            "onHoldMessage":null,
            "blockedAniMessage":null,
            "gatePriority":0,
            "recordCall":1,
            "stopRecordingOnTransfer":false,
            "recordingInConference":false,
            "revMatch":false,
            "appUrl":null,
            "backupAppUrl":null,
            "surveyPopType":"FLASH",
            "createdOn":"2020-05-18T19:22:12.000+0000",
            "shortAbandonTime":30,
            "shortCallTime":30,
            "longCallTime":300,
            "acceptTime":30,
            "ttAccept":false,
            "requeueType":"ADVANCED",
            "slaTime":30,
            "afterCallBaseState":null,
            "hangupOnDisposition":false,
            "wrapTime":8,
            "endCallMessage":null,
            "outboundCallerId":"ani",
            "transferCallerId":null,
            "manualCallerId":null,
            "syncQueueWait":10,
            "enableGlobalPhoneBook":false,
            "fifoDisabled":true,
            "pauseRecordingSec":30,
            "isActive":true,
            "observeDst":true,
            "enableIvrTokens":false,
            "dispositionTimeout":60,
            "gateGroup":
              {
                "id":52676,
                "description":"My Queue Group"
              },
            "afterCallState":null,
            "postCallSoapService":null,
            "dequeueSoapService":null,
            "agentConnSoapService":null,
            "postDispSoapService":null,
            "transferTermSoapService":null,
            "agentTermSoapService":null,
            "callbackCampaign":null,
            "abandonCampaign":null,
            "resultFileDestination":null,
            "survey":null,
            "gatePriorityGroup":null,
            "script":null,
            "gateQueueEvents":null,
            "agentGateAccess":null,
            "gateOpen":true
          }
      }
    ]    
    ```

## Update Queue Events

Modify Queue Events using the `gateQueueEvents` endpoint.  You can modify multiple Queue Events with this command.  To modify only a single Queue Event, use the `gateQueueEvents` with your specific `eventId`.

### Primary Parameters
Only `gateName` is a required parameter to create a Queue. All other parameters are optional.

| API Property |  | UI Display | UI Default | Description |
|-|-|-|-|-|
| **`eventId`** | Optional | ID | *hidden* | A Queue Event unique ID. If not provided an available event ID will be created for you. |
| **`eventRank`** | Required | Rank | 0 | A priority ranking for the order in which Queue Events should be executed. |
| **`queueEvent`** | Optional | Single Play Audio | *empty* | Provide a short description of the skill. |
| **`active`** | Optional | Active | Yes | Set this skill to Active by setting it to `true`. |
| **`whisperAudio`** | Optional | **None** | *empty* | A link to the short audio file that plays a message to the agent as they connect with a customer. The audio may inform the agent about the incoming call, or prompt the agent to accept the call. |
| **`createOn`** | Optional | Created | *current date* | A date in Simple Date Format. |
| **`agentSkillProfiles`** | Optional | **None** | *empty* | Custom skills defined and bound to an Agent to redirect these queues to. |
| **`requeueShortcut`** | Optional | **None** | *empty* | Allow agents to manually send their current call to a specific inbound queue, or to another agent with a special skill. |

### Request

=== "HTTP"
    ```html
    POST {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents
    Content-Type: application/json

    [
      {
        "eventId":67882,
        "eventRank":0,
        "queueEvent":"PLAY-AUDIO-LOOP:holdmusic",
        "eventDuration":120,
        "enableDtmf":0
      },
      {
        "eventId":67883,
        "eventRank":1,
        "queueEvent":"END-CALL:true",
        "eventDuration":0,
        "enableDtmf":0
      }
    ]    
    ```

### Response

=== "Response"
    ```json
    [
      {
        "eventId":67882,
        "eventRank":0,
        "queueEvent":"PLAY-AUDIO-LOOP:holdmusic",
        "eventDuration":120,
        "enableDtmf":0,
        "gate":
          {
            "permissions":[],
            "gateId":73001,
            "gateName":"My Queue (Spanish)",
            "gateDesc":"An *edited* queue for this Queue Group",
            "billingCode":null,
            "dequeueDelay":0,
            "maxQueueLimit":-1,
            "maxQueueEvent":null,
            "noAgentEvent":null,
            "specialAniEvent":null,
            "gateClosedEvent":null,
            "throttlingAniEvent":null,
            "throttleCalls":0,
            "throttleDays":0,
            "monSched":"08002100",
            "tueSched":"08002100",
            "wedSched":"08002100",
            "thuSched":"08002100",
            "friSched":"08002100",
            "satSched":"00000000",
            "sunSched":"00000000",
            "agentPopMessage":null,
            "whisperMessage":null,
            "onHoldMessage":null,
            "blockedAniMessage":null,
            "gatePriority":0,
            "recordCall":1,
            "stopRecordingOnTransfer":false,
            "recordingInConference":false,
            "revMatch":false,
            "appUrl":null,
            "backupAppUrl":null,
            "surveyPopType":"FLASH",
            "createdOn":"2020-05-18T19:22:12.000+0000",
            "shortAbandonTime":30,
            "shortCallTime":30,
            "longCallTime":300,
            "acceptTime":30,
            "ttAccept":false,
            "requeueType":"ADVANCED",
            "slaTime":30,
            "afterCallBaseState":null,
            "hangupOnDisposition":false,
            "wrapTime":8,
            "endCallMessage":null,
            "outboundCallerId":"ani",
            "transferCallerId":null,
            "manualCallerId":null,
            "syncQueueWait":10,
            "enableGlobalPhoneBook":false,
            "fifoDisabled":true,
            "pauseRecordingSec":30,
            "isActive":true,
            "observeDst":true,
            "enableIvrTokens":false,
            "dispositionTimeout":60,
            "gateGroup":
              {
                "id":52676,
                "description":"My Queue Group"
              },
            "afterCallState":null,
            "postCallSoapService":null,
            "dequeueSoapService":null,
            "agentConnSoapService":null,
            "postDispSoapService":null,
            "transferTermSoapService":null,
            "agentTermSoapService":null,
            "callbackCampaign":null,
            "abandonCampaign":null,
            "resultFileDestination":null,
            "survey":null,
            "gatePriorityGroup":null,
            "script":null,
            "gateQueueEvents":null,
            "agentGateAccess":null,
            "gateOpen":true
          }
      },
      {
        "eventId":67883,
        "eventRank":1,
        "queueEvent":"END-CALL:true",
        "eventDuration":0,
        "enableDtmf":0,
        "gate":
          {
            "permissions":[],
            "gateId":73001,
            "gateName":"My Queue (Spanish)",
            "gateDesc":"An *edited* queue for this Queue Group",
            "billingCode":null,
            "dequeueDelay":0,
            "maxQueueLimit":-1,
            "maxQueueEvent":null,
            "noAgentEvent":null,
            "specialAniEvent":null,
            "gateClosedEvent":null,
            "throttlingAniEvent":null,
            "throttleCalls":0,
            "throttleDays":0,
            "monSched":"08002100",
            "tueSched":"08002100",
            "wedSched":"08002100",
            "thuSched":"08002100",
            "friSched":"08002100",
            "satSched":"00000000",
            "sunSched":"00000000",
            "agentPopMessage":null,
            "whisperMessage":null,
            "onHoldMessage":null,
            "blockedAniMessage":null,
            "gatePriority":0,
            "recordCall":1,
            "stopRecordingOnTransfer":false,
            "recordingInConference":false,
            "revMatch":false,
            "appUrl":null,
            "backupAppUrl":null,
            "surveyPopType":"FLASH",
            "createdOn":"2020-05-18T19:22:12.000+0000",
            "shortAbandonTime":30,
            "shortCallTime":30,
            "longCallTime":300,
            "acceptTime":30,
            "ttAccept":false,
            "requeueType":"ADVANCED",
            "slaTime":30,
            "afterCallBaseState":null,
            "hangupOnDisposition":false,
            "wrapTime":8,
            "endCallMessage":null,
            "outboundCallerId":"ani",
            "transferCallerId":null,
            "manualCallerId":null,
            "syncQueueWait":10,
            "enableGlobalPhoneBook":false,
            "fifoDisabled":true,
            "pauseRecordingSec":30,
            "isActive":true,
            "observeDst":true,
            "enableIvrTokens":false,
            "dispositionTimeout":60,
            "gateGroup":
              {
                "id":52676,
                "description":"My Queue Group"
              },
            "afterCallState":null,
            "postCallSoapService":null,
            "dequeueSoapService":null,
            "agentConnSoapService":null,
            "postDispSoapService":null,
            "transferTermSoapService":null,
            "agentTermSoapService":null,
            "callbackCampaign":null,
            "abandonCampaign":null,
            "resultFileDestination":null,
            "survey":null,
            "gatePriorityGroup":null,
            "script":null,
            "gateQueueEvents":null,
            "agentGateAccess":null,
            "gateOpen":true
          }
        }
      ]
    ```
