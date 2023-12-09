# Creating an Agent Skill Profile

## About agent skill profiles

Depending on your contact center, there may be times that you’d like the system to route certain types of calls to specific agents with special skills. If this is the case, you can assign these agents custom skills by creating skill profiles. Skill profiles are the custom skills that you can create for each agent to tell the system to route certain calls to the agents you’ve assigned these skills to.

You can create skill profiles using the [Agents](../agents/index.md) endpoint, defining the agent you wish to assign that skill to, and then creating the Skill Profile for that agent.

Skill profiles work in conjunction with [Group Skills](../../routing/queues/group-skills.md), which are created at the queue group level. Creating group skills is the first step in the process of assigning skills to your agents. After you create group skills, you’ll also need to add these skills (via [Queue Events](../../routing/queues/queue-events.md)) to any queue that you assign these agents to. Once you have completed these two steps, you can assign these skills to the desired agents.

Let’s say, for example, you have Spanish-speaking customers calling into your contact center, and you’d like to designate certain agents to take these calls. You can create a group skill that you add to the queues of your choice, and then assign those skills to any bilingual or Spanish-speaking agents assigned to those queues.

In the sections below, we’ll review each step you should take to create a skill profile, which includes creating a group skill, adding it to a queue, and then finally assigning the skill to an agent.

## Creating a group skill
As we discussed above, before you can create a skill profile, you must first create a group skill. In the example below, we’ll show you how to create a group skill; however, if you’d like to learn more about group skills and the settings you’ll find in that part of the platform, visit [Group Skills](../../routing/queues/group-skills.md).

### Request
Be sure to set the proper [BASE_URL](../../basics/uris.md#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral.md) for your deployment.

=== "HTTP"
    ```html
    POST {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills
    Content-Type: application/json

    [
      {
        "skillName":"Spanish Language",
        "skillDesc":"A test skill for Spanish",
        "active":true,
      },
      {
        "skillName":"French Language",
        "skillDesc":"A test skill for French",
        "active":true,
      }
    ]

    ```

### Response

```json
[
  {
    "skillId":1455,
    "skillName":"Spanish Language",
    "skillDesc":"A test skill for Spanish",
    "active":true,
    "whisperAudio":null,
    "createdOn":"2020-05-19T16:53:17.000+0000",
    "agentSkillProfiles":null,
    "requeueShortcut":null
  },
  {
    "skillId":1456,
    "skillName":"French Language",
    "skillDesc":"A test skill for French",
    "active":true,
    "whisperAudio":null,
    "createdOn":"2020-05-19T17:25:13.000+0000",
    "agentSkillProfiles":null,
    "requeueShortcut":null
  }
]
```

## Adding group skills to a queue event
Once you’ve created a group skill, you can assign that skill to a [Queue](../../routing/queues/queues.md), so long as the queue has been created under the queue group in which the group skill was created.

In the example below, we’ll show you how you can add this group skill to a queue via the Queue Events setting, but if you’d like to learn more about Queue Events, including how to create a queue event, please visit [Queue Events](../../routing/queues/queue-events.md).

!!! alert "Please Note"
    If you do not assign this skill to the "Route to Agent" event type, the system will be unable to successfully route the skill-specific calls

!!! Important
    To add the group skill to a queue event, modify the `queueEvent` field by inserting `SKILL-ROUTE:{gateGroup.skillId}` into the field.  See the highlight below.

### Supporting APIs
The following API is used to retrieve predefined values for the groups skills.

#### Skills

Gets a list of group skills for the Queue Group under this account.

  `GET {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills`

### Request
Be sure to set the proper [BASE_URL](../../basics/uris.md#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral.md) for your deployment.

=== "HTTP"
    ```html hl_lines="7"
    POST {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents/{eventId}
    Content-Type: application/json

    {
      "eventId":67882,
      "eventRank":10,
      "queueEvent":"PLAY-AUDIO:holdmusic;SKILL-ROUTE:1455;",
      "eventDuration":120,
      "enableDtmf":0
    }
    ```

### Response

```json
{
  "eventId":67882,
  "eventRank":10,
  "queueEvent":"PLAY-AUDIO:holdmusic;SKILL-ROUTE:1455;",
  "eventDuration":120,
  "enableDtmf":0,
  "gate":
    {
      "permissions":[],
      "gateId":73001,
      "gateName":"My Queue (Spanish)",
      "gateDesc":"A Spanish version of the My Queue Group",
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
```

## Creating a skill profile
Now that you’ve created a group skill and added that skill to a queue, you can now assign the skill to an agent.

!!! alert "Please Note"
    The agent you choose in the example below must also be assigned to the queue to which the group skill was added.

### Primary Parameters
Only `profileName` is a required parameter to create a skill profile. All other parameters are optional.

| API Property |  | UI Display | UI Default | Description |
|-|-|-|-|-|
| **`profileId`** | Optional | *hidden* | 0 | A unique identifier for this Skill Profile. |
| **`profileName`** | Required | Name | *empty* | Give this skill profile a name. |
| **`profileDesc`** | Optional | Description | *empty* | Set a short description for the new skill profile. |
| **`isDefault`** | Optional | Default Profile | *empty* | If this skill is set to default, then the system will route calls specific to this skill to the agent before other calls. |
| **`gateGroupSkills`** | Optional | Queue Group Skills | *empty* | List of Queue Group Skills to assign to this Skill Profile. |
| **`chatGroupSkills`** | Optional | Chat Group Skills | *empty* | List of Chat Group Skills to assign to this Skill Profile. |

### Request
Be sure to set the proper [BASE_URL](../../basics/uris.md#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral.md) for your deployment.

=== "HTTP"
    ```html
    POST {BASE_URL}/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}/    skillProfiles
    Content-Type: application/json

    {
      "profileId":0, /* a unique ID will be created for you */
      "profileName":"Spanish Speaker",
      "profileDesc":"Can speak limited Spanish",
      "isDefault":false,
      "gateGroupSkills":
        [
          {
            "skillId":1455,
            "skillName":"Spanish Language",
            "skillDesc":"A test skill for Spanish",
            "active":true,
            "whisperAudio":null,
          }
        ],
      "chatGroupSkills":[]
    }
    ```

### Response

```json
{
  "profileId":215271,
  "profileName":"Spanish Speaker",
  "profileDesc":"Can speak limited Spanish",
  "isDefault":false,
  "createdOn":"2020-05-20T19:00:30.132+0000",
  "gateGroupSkills":
    [
      {
        "skillId":1455,
        "skillName":"Spanish Language",
        "skillDesc":"A test skill for Spanish",
        "active":true,
        "whisperAudio":null,
        "createdOn":"2020-05-19T17:25:13.000+0000"
      }
    ],
  "chatGroupSkills":[]
}
```

And that’s it! The agents you’ve assigned these special skills to will now be able to receive those skill-specific calls.
