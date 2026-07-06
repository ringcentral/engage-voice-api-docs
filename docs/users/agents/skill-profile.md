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

```http
POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills
Authorization: Bearer <ringcxAccessToken>
Content-Type: application/json
```

```json
[
  {
    "skillName": "Spanish Language",
    "skillDesc": "Spanish-language support",
    "active": true
  }
]
```

See [Group Skills](../../routing/queues/group-skills.md) for the full group-skill workflow.

## Add the Skill to Queue Routing

Queue events can reference a group skill with a `SKILL-ROUTE:{skillId}` token in the event behavior.

```http
PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents/{eventId}
Authorization: Bearer <ringcxAccessToken>
Content-Type: application/json
```

```json
{
  "eventId": 67882,
  "eventRank": 10,
  "queueEvent": "PLAY-AUDIO:holdmusic;SKILL-ROUTE:1455;",
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

```http
POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}/skillProfiles
Authorization: Bearer <ringcxAccessToken>
Content-Type: application/json
```

```json
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

### Common Fields

| Field | Required | Description |
| --- | --- | --- |
| `profileName` | Yes | Display name for the profile. |
| `profileDesc` | No | Short description of the profile. |
| `isDefault` | No | Whether this is the default skill profile for the agent. |
| `gateGroupSkills` | No | Queue group skills assigned to the profile. |
| `chatGroupSkills` | No | Digital chat group skills assigned to the profile, when applicable. |

## Assign Skills to an Existing Profile

```http
PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}/skillProfiles/{skillProfileId}/skills/{skillId}
Authorization: Bearer <ringcxAccessToken>
Content-Type: application/json
```

Retrieve the profile after assignment to verify that the expected skills are present.
