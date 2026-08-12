# Skill Profiles

Skill profiles assign queue-group skills to agents. Use them when calls should route to agents with specific capabilities, such as language, product specialization, or escalation training.

## Workflow

1. Identify the queue group, queue, agent group, and agent.
2. Confirm that the agent is assigned to the queue that will receive the call.
3. Create the group skill under the same queue group as the queue.
4. Find or create the queue's Route to Agent event.
5. Add the group skill to that Route to Agent event.
6. Create a skill profile for the agent.
7. Assign the same group skill to the agent's skill profile.
8. Place a test call to a DNIS assigned to the queue and confirm that the call routes to an available agent with the matching skill.

Skill routing only works when the queue event and the agent skill profile reference the same group skill. The agent must also have access to the queue where the skill is used.

## Before You Start

Before configuring skill routing, collect the following identifiers:

| Identifier | Description |
| --- | --- |
| `accountId` | RingCX account ID. |
| `gateGroupId` | Queue group ID. Group skills are created under this queue group. |
| `gateId` | Queue ID for the inbound queue that should use skill routing. |
| `agentGroupId` | Agent group ID for the target agent. |
| `agentId` | Agent ID for the user who should receive matching calls. |

Use these queue assignment endpoints to verify that the target agent can receive calls from the queue:

| Operation | Method and path |
| --- | --- |
| List agents assigned to a queue | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/assignedAgents` |
| Assign agents to a queue | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/assignAgents` |

## SDK Setup

SDK examples in this article use JWT authentication and load credentials from environment variables.

=== "JavaScript"

    ```bash
    npm install ringcentral-engage-voice-client dotenv
    ```

=== "Python"

    ```bash
    pip3 install ringcentral_engage_voice python-dotenv
    ```

Create a `.env` file in the directory where you run the sample:

```text
RC_CLIENT_ID=<clientId>
RC_CLIENT_SECRET=<clientSecret>
RC_JWT=<jwt>
```

The SDK wrapper reads these values, signs in with RingCentral, and exchanges the RingCentral access token for a RingCX access token before calling RingCX APIs.

## Queue Event Basics

Queue events define what happens after a call enters a queue. Each event has a `queueEvent` value that stores one or more semicolon-delimited event tokens.

For skill routing, update the queue's Route to Agent event:

| Token | Purpose |
| --- | --- |
| `ROUTE-TO-AGENT:TRUE;` | Routes the caller to an available agent. |
| `SKILL-ROUTE:{skillId};` | Limits that route to agents whose skill profile includes the specified group skill. |

Retrieve the queue events for the queue and look for the event whose `queueEvent` value contains `ROUTE-TO-AGENT`. When you update an existing event, preserve any existing event settings that are still needed for the queue and add the `SKILL-ROUTE:{skillId};` token.

## Create a Group Skill

Group skills are managed under queue groups.

=== "HTTP"

    ```http
    POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "skillName": "Spanish Language",
      "skillDesc": "Spanish-language support",
      "active": true
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    gate_group_id = "<gateGroupId>"
    access_token = "<ringcxAccessToken>"
    payload = {
        "skillName": "Spanish Language",
        "skillDesc": "Spanish-language support",
        "active": True,
    }

    response = requests.post(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/gateGroups/{gate_group_id}/skills",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        json=payload,
    )
    response.raise_for_status()
    print(response.json())
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const gateGroupId = "<gateGroupId>";
    const accessToken = "<ringcxAccessToken>";
    const payload = {
      skillName: "Spanish Language",
      skillDesc: "Spanish-language support",
      active: true
    };

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/gateGroups/${gateGroupId}/skills`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      }
    );

    if (!response.ok) throw new Error(await response.text());
    console.log(await response.json());
    ```

=== "JavaScript SDK"

    ```javascript
    const EngageVoice = require("ringcentral-engage-voice-client").default;
    require("dotenv").config();

    async function main() {
      const ev = new EngageVoice({
        clientId: process.env.RC_CLIENT_ID,
        clientSecret: process.env.RC_CLIENT_SECRET
      });

      await ev.authorize({ jwt: process.env.RC_JWT });

      const payload = {
        skillName: "Spanish Language",
        skillDesc: "Spanish-language support",
        active: true
      };

      const response = await ev.post(
        "/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills",
        payload
      );
      console.log(response.data);
    }

    main().catch(console.error);
    ```

=== "Python SDK"

    ```python
    import os
    from dotenv import load_dotenv
    from ringcentral_engage_voice import RingCentralEngageVoice

    load_dotenv()

    ev = RingCentralEngageVoice(
        os.environ["RC_CLIENT_ID"],
        os.environ["RC_CLIENT_SECRET"],
    )
    ev.authorize(jwt=os.environ["RC_JWT"])

    payload = {
        "skillName": "Spanish Language",
        "skillDesc": "Spanish-language support",
        "active": True,
    }

    response = ev.post(
        "/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills",
        payload,
    ).json()
    print(response)
    ```

??? example "Response example"

    ```json
    {
      "skillId": 1455,
      "skillName": "Spanish Language",
      "skillDesc": "Spanish-language support",
      "active": true
    }
    ```

See [Group Skills](../../routing/queues/group-skills.md) for the full group-skill workflow.

## Add the Skill to Queue Routing

First, retrieve the queue events for the queue:

```http
GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents
Authorization: Bearer <ringcxAccessToken>
```

Find the Route to Agent event, then update that event so its `queueEvent` value includes both `ROUTE-TO-AGENT:TRUE;` and `SKILL-ROUTE:{skillId};`.

=== "HTTP"

    ```http
    PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents/{eventId}
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "eventId": 67882,
      "eventRank": 10,
      "queueEvent": "ROUTE-TO-AGENT:TRUE;SKILL-ROUTE:1455;",
      "eventDuration": 120,
      "enableDtmf": 0
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    gate_group_id = "<gateGroupId>"
    gate_id = "<gateId>"
    event_id = "<eventId>"
    access_token = "<ringcxAccessToken>"
    payload = {
        "eventId": 67882,
        "eventRank": 10,
        "queueEvent": "ROUTE-TO-AGENT:TRUE;SKILL-ROUTE:1455;",
        "eventDuration": 120,
        "enableDtmf": 0,
    }

    response = requests.put(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/gateGroups/{gate_group_id}/gates/{gate_id}/gateQueueEvents/{event_id}",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        json=payload,
    )
    response.raise_for_status()
    print(response.json())
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const gateGroupId = "<gateGroupId>";
    const gateId = "<gateId>";
    const eventId = "<eventId>";
    const accessToken = "<ringcxAccessToken>";
    const payload = {
      eventId: 67882,
      eventRank: 10,
      queueEvent: "ROUTE-TO-AGENT:TRUE;SKILL-ROUTE:1455;",
      eventDuration: 120,
      enableDtmf: 0
    };

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/gateGroups/${gateGroupId}/gates/${gateId}/gateQueueEvents/${eventId}`,
      {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      }
    );

    if (!response.ok) throw new Error(await response.text());
    console.log(await response.json());
    ```

=== "JavaScript SDK"

    ```javascript
    const EngageVoice = require("ringcentral-engage-voice-client").default;
    require("dotenv").config();

    async function main() {
      const ev = new EngageVoice({
        clientId: process.env.RC_CLIENT_ID,
        clientSecret: process.env.RC_CLIENT_SECRET
      });

      await ev.authorize({ jwt: process.env.RC_JWT });

      const payload = {
        eventId: 67882,
        eventRank: 10,
        queueEvent: "ROUTE-TO-AGENT:TRUE;SKILL-ROUTE:1455;",
        eventDuration: 120,
        enableDtmf: 0
      };

      const response = await ev.put(
        "/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents/{eventId}",
        payload
      );
      console.log(response.data);
    }

    main().catch(console.error);
    ```

=== "Python SDK"

    ```python
    import os
    from dotenv import load_dotenv
    from ringcentral_engage_voice import RingCentralEngageVoice

    load_dotenv()

    ev = RingCentralEngageVoice(
        os.environ["RC_CLIENT_ID"],
        os.environ["RC_CLIENT_SECRET"],
    )
    ev.authorize(jwt=os.environ["RC_JWT"])

    payload = {
        "eventId": 67882,
        "eventRank": 10,
        "queueEvent": "ROUTE-TO-AGENT:TRUE;SKILL-ROUTE:1455;",
        "eventDuration": 120,
        "enableDtmf": 0,
    }

    response = ev.put(
        "/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents/{eventId}",
        payload,
    ).json()
    print(response)
    ```

??? example "Response example"

    ```json
    {
      "eventId": 67882,
      "eventRank": 10,
      "queueEvent": "ROUTE-TO-AGENT:TRUE;SKILL-ROUTE:1455;",
      "eventDuration": 120,
      "enableDtmf": 0
    }
    ```

## Manage Agent Skill Profiles

| Operation | Method and path |
| --- | --- |
| List skill profiles for an agent | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}/skillProfiles` |
| Get skill profile | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}/skillProfiles/{skillProfileId}` |
| Create skill profile | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}/skillProfiles` |
| Update skill profile | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}/skillProfiles/{skillProfileId}` |
| Delete skill profile | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}/skillProfiles/{skillProfileId}` |
| List assigned skills | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}/skillProfiles/{skillProfileId}/skills` |
| Assign skills to profile | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}/skillProfiles/{skillProfileId}/skills` |
| Assign one skill | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}/skillProfiles/{skillProfileId}/skills/{skillId}` |
| Remove one skill | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}/skillProfiles/{skillProfileId}/skills/{skillId}` |

## Create a Skill Profile

=== "HTTP"

    ```http
    POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}/skillProfiles
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "profileName": "Spanish Speaker",
      "profileDesc": "Routes Spanish-language calls to this agent",
      "isDefault": false,
      "gateGroupSkills": [
        {
          "skillId": 1455,
          "skillName": "Spanish Language",
          "active": true
        }
      ],
      "chatGroupSkills": []
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    agent_group_id = "<agentGroupId>"
    agent_id = "<agentId>"
    access_token = "<ringcxAccessToken>"
    payload = {
        "profileName": "Spanish Speaker",
        "profileDesc": "Routes Spanish-language calls to this agent",
        "isDefault": False,
        "gateGroupSkills": [
            {
                "skillId": 1455,
                "skillName": "Spanish Language",
                "active": True,
            }
        ],
        "chatGroupSkills": [],
    }

    response = requests.post(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/agentGroups/{agent_group_id}/agents/{agent_id}/skillProfiles",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        json=payload,
    )
    response.raise_for_status()
    print(response.json())
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const agentGroupId = "<agentGroupId>";
    const agentId = "<agentId>";
    const accessToken = "<ringcxAccessToken>";
    const payload = {
      profileName: "Spanish Speaker",
      profileDesc: "Routes Spanish-language calls to this agent",
      isDefault: false,
      gateGroupSkills: [
        {
          skillId: 1455,
          skillName: "Spanish Language",
          active: true
        }
      ],
      chatGroupSkills: []
    };

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/agentGroups/${agentGroupId}/agents/${agentId}/skillProfiles`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      }
    );

    if (!response.ok) throw new Error(await response.text());
    console.log(await response.json());
    ```

=== "JavaScript SDK"

    ```javascript
    const EngageVoice = require("ringcentral-engage-voice-client").default;
    require("dotenv").config();

    async function main() {
      const ev = new EngageVoice({
        clientId: process.env.RC_CLIENT_ID,
        clientSecret: process.env.RC_CLIENT_SECRET
      });

      await ev.authorize({ jwt: process.env.RC_JWT });

      const payload = {
        profileName: "Spanish Speaker",
        profileDesc: "Routes Spanish-language calls to this agent",
        isDefault: false,
        gateGroupSkills: [
          {
            skillId: 1455,
            skillName: "Spanish Language",
            active: true
          }
        ],
        chatGroupSkills: []
      };

      const response = await ev.post(
        "/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}/skillProfiles",
        payload
      );
      console.log(response.data);
    }

    main().catch(console.error);
    ```

=== "Python SDK"

    ```python
    import os
    from dotenv import load_dotenv
    from ringcentral_engage_voice import RingCentralEngageVoice

    load_dotenv()

    ev = RingCentralEngageVoice(
        os.environ["RC_CLIENT_ID"],
        os.environ["RC_CLIENT_SECRET"],
    )
    ev.authorize(jwt=os.environ["RC_JWT"])

    payload = {
        "profileName": "Spanish Speaker",
        "profileDesc": "Routes Spanish-language calls to this agent",
        "isDefault": False,
        "gateGroupSkills": [
            {
                "skillId": 1455,
                "skillName": "Spanish Language",
                "active": True,
            }
        ],
        "chatGroupSkills": [],
    }

    response = ev.post(
        "/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}/skillProfiles",
        payload,
    ).json()
    print(response)
    ```

??? example "Response example"

    ```json
    {
      "profileId": 215271,
      "profileName": "Spanish Speaker",
      "profileDesc": "Routes Spanish-language calls to this agent",
      "isDefault": false,
      "gateGroupSkills": [
        {
          "skillId": 1455,
          "skillName": "Spanish Language",
          "active": true
        }
      ],
      "chatGroupSkills": []
    }
    ```

### Common Fields

| Field | Required | Description |
| --- | --- | --- |
| `profileName` | Yes | Display name for the profile. |
| `profileDesc` | No | Short description of the profile. |
| `isDefault` | No | Whether this is the default skill profile for the agent. |
| `gateGroupSkills` | No | Queue group skills assigned to the profile. |
| `chatGroupSkills` | No | Digital chat group skills assigned to the profile, when applicable. |

## Assign Skills to an Existing Profile

=== "HTTP"

    ```http
    PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}/skillProfiles/{skillProfileId}/skills/{skillId}
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    agent_group_id = "<agentGroupId>"
    agent_id = "<agentId>"
    skill_profile_id = "<skillProfileId>"
    skill_id = "<skillId>"
    access_token = "<ringcxAccessToken>"

    response = requests.put(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/agentGroups/{agent_group_id}/agents/{agent_id}/skillProfiles/{skill_profile_id}/skills/{skill_id}",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
    )
    response.raise_for_status()
    print(response.json())
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const agentGroupId = "<agentGroupId>";
    const agentId = "<agentId>";
    const skillProfileId = "<skillProfileId>";
    const skillId = "<skillId>";
    const accessToken = "<ringcxAccessToken>";

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/agentGroups/${agentGroupId}/agents/${agentId}/skillProfiles/${skillProfileId}/skills/${skillId}`,
      {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json"
        }
      }
    );

    if (!response.ok) throw new Error(await response.text());
    console.log(await response.json());
    ```

=== "JavaScript SDK"

    ```javascript
    const EngageVoice = require("ringcentral-engage-voice-client").default;
    require("dotenv").config();

    async function main() {
      const ev = new EngageVoice({
        clientId: process.env.RC_CLIENT_ID,
        clientSecret: process.env.RC_CLIENT_SECRET
      });

      await ev.authorize({ jwt: process.env.RC_JWT });

      const response = await ev.put(
        "/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}/skillProfiles/{skillProfileId}/skills/{skillId}"
      );
      console.log(response.data);
    }

    main().catch(console.error);
    ```

=== "Python SDK"

    ```python
    import os
    from dotenv import load_dotenv
    from ringcentral_engage_voice import RingCentralEngageVoice

    load_dotenv()

    ev = RingCentralEngageVoice(
        os.environ["RC_CLIENT_ID"],
        os.environ["RC_CLIENT_SECRET"],
    )
    ev.authorize(jwt=os.environ["RC_JWT"])

    response = ev.put(
        "/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}/skillProfiles/{skillProfileId}/skills/{skillId}"
    ).json()
    print(response)
    ```

Retrieve the profile after assignment to verify that the expected skills are present.

??? example "Assigned profile response example"

    ```json
    {
      "profileId": 215271,
      "profileName": "Spanish Speaker",
      "gateGroupSkills": [
        {
          "skillId": 1455,
          "skillName": "Spanish Language",
          "active": true
        }
      ],
      "chatGroupSkills": []
    }
    ```

## Validate Skill Routing

Before sending production traffic to the queue, verify the complete route:

| Check | How to verify |
| --- | --- |
| Agent queue access | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/assignedAgents` includes the target `agentId`. |
| Queue routing event | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents/{eventId}` returns a Route to Agent event whose `queueEvent` includes `ROUTE-TO-AGENT:TRUE;SKILL-ROUTE:{skillId};`. |
| Agent skill profile | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}/skillProfiles/{skillProfileId}` includes the same `skillId` in `gateGroupSkills`. |
| Agent state | The agent is logged in, available, and able to receive inbound queue calls. |

Place a test call to a DNIS assigned to the queue. If the call does not route to the expected agent, review the queue event rank, the agent's queue assignment, the agent's skill profile, the agent's availability state, and any other available agents that share the same skill.
