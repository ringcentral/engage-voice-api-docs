# Agent Groups

Agent groups organize agents into administrative groups. An agent must belong to an agent group before you can create or manage that agent through the Agents API.

## Manage Agent Groups

| Operation | Method and path |
| --- | --- |
| List agent groups | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups` |
| Get agent group | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}` |
| Create agent group | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups` |
| Update agent group | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}` |
| Delete agent group | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}` |

## Create an Agent Group

Only `groupName` is required when creating an agent group.

```http
POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups
Authorization: Bearer <ringcxAccessToken>
Content-Type: application/json
```

```json
{
  "groupName": "Support Agents"
}
```

### Common Fields

| Field | Required | Description |
| --- | --- | --- |
| `groupName` | Yes | Display name for the agent group. |
| `agentGroupId` | No | Agent group ID. If omitted during create, RingCX assigns an ID. |
| `isDefault` | No | Whether the group is the default agent group. |

## Retrieve Agent Groups

```http
GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups
Authorization: Bearer <ringcxAccessToken>
Accept: application/json
```

Use the returned `agentGroupId` when creating agents.

## Update an Agent Group

Retrieve the agent group first, update the fields you need to change, and submit the updated object with `PUT`.

```http
PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}
Authorization: Bearer <ringcxAccessToken>
Content-Type: application/json
```

```json
{
  "agentGroupId": 1950,
  "groupName": "Support Agents - Updated",
  "isDefault": false
}
```

## Delete an Agent Group

```http
DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}
Authorization: Bearer <ringcxAccessToken>
```

Delete an agent group only after moving or deleting the agents that belong to it.
