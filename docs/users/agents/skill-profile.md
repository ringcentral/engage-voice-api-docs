# Skill Profiles

Skill profiles assign queue-group skills to agents. Use them when calls should route to agents with specific capabilities, such as language, product specialization, or escalation training.

## Workflow

1. Create the group skill under a queue group.
2. Reference the skill from a queue event, such as a route-to-agent event.
3. Create a skill profile for the agent.
4. Assign one or more group skills to the agent's skill profile.

The agent must also have access to the queue where the skill is used.

## Create a Group Skill

Group skills are managed under queue groups.

=== "HTTP"

    ```http
    POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    [
      {
        "skillName": "Spanish Language",
        "skillDesc": "Spanish-language support",
        "active": true
      }
    ]
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    gate_group_id = "<gateGroupId>"
    access_token = "<ringcxAccessToken>"
    payload = [
        {
            "skillName": "Spanish Language",
            "skillDesc": "Spanish-language support",
            "active": True,
        }
    ]

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
    const payload = [
      {
        skillName: "Spanish Language",
        skillDesc: "Spanish-language support",
        active: true
      }
    ];

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

See [Group Skills](../../routing/queues/group-skills.md) for the full group-skill workflow.

## Add the Skill to Queue Routing

Queue events can reference a group skill with a `SKILL-ROUTE:{skillId}` token in the event behavior.

=== "HTTP"

    ```http
    PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents/{eventId}
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "eventId": 67882,
      "eventRank": 10,
      "queueEvent": "PLAY-AUDIO:holdmusic;SKILL-ROUTE:1455;",
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
        "queueEvent": "PLAY-AUDIO:holdmusic;SKILL-ROUTE:1455;",
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
      queueEvent: "PLAY-AUDIO:holdmusic;SKILL-ROUTE:1455;",
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

Retrieve the profile after assignment to verify that the expected skills are present.
