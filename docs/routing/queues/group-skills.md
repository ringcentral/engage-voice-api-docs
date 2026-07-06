# Group Skills

Group skills are queue-group-level skills that can be assigned to agents and used by queue routing. Create the [queue group](queue-groups.md) first, then create the group skills that belong to that queue group.

## Manage Group Skills

The API path uses `gateGroups` because queue groups are represented as gate groups in the API.

| Operation | Method and path |
| --- | --- |
| List group skills | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills` |
| Get group skill | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills/{skillId}` |
| Create group skills | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills` |
| Update group skills | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills` |
| Update one group skill | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills/{skillId}` |
| Delete group skill | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills/{skillId}` |

## Create Group Skills

Create one or more group skills by sending an array of skill objects. To create a single skill, send an array with one object.

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
  },
  {
    "skillName": "French Language",
    "skillDesc": "French-language support",
    "active": true
  }
]
```

### Common Fields

| Field | Required | Description |
| --- | --- | --- |
| `skillName` | Yes | Display name for the skill. |
| `skillDesc` | No | Short description of the skill. |
| `active` | No | Whether the skill is available for routing. |
| `skillId` | No | Group skill ID. Omit it when creating a new skill. |
| `whisperAudio` | No | Optional audio prompt played to the agent. |
| `agentSkillProfiles` | No | Agent skill profile associations. |
| `requeueShortcut` | No | Requeue shortcut association. |

## Retrieve Group Skills

```http
GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills
Authorization: Bearer <ringcxAccessToken>
Accept: application/json
```

Use the returned `skillId` values when retrieving, updating, or deleting a single skill.

## Update Group Skills

Retrieve the current skill object first, update the fields that should change, and submit the updated object. Use the collection endpoint for batch updates or the `{skillId}` endpoint for one skill.

```http
PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills/{skillId}
Authorization: Bearer <ringcxAccessToken>
Content-Type: application/json
```

```json
{
  "skillId": 1455,
  "skillName": "Spanish Language",
  "skillDesc": "Spanish-language support and billing questions",
  "active": true
}
```

## Delete a Group Skill

```http
DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills/{skillId}
Authorization: Bearer <ringcxAccessToken>
```

Delete a group skill only after confirming it is no longer referenced by agent skill profiles or queue routing behavior.
