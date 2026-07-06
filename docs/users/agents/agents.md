# Agents

Agents are RingCX users who can log in to handle inbound queues, outbound campaigns, or supervisor workflows. Agents must belong to an [agent group](agent-groups.md).

## Manage Agents

| Operation | Method and path |
| --- | --- |
| List agents in an agent group | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents` |
| Get agent | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}` |
| Create agent | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents` |
| Update agents in an agent group | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents` |
| Update one agent | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}` |
| Delete agent | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}` |

## Create an Agent

Create the agent under the agent group that should own the agent record.

```http
POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents
Authorization: Bearer <ringcxAccessToken>
Content-Type: application/json
```

```json
{
  "firstName": "Ada",
  "lastName": "Lovelace",
  "email": "ada@example.com",
  "username": "ada.lovelace",
  "password": "<temporaryPassword>",
  "agentType": "AGENT",
  "agentRank": 12,
  "allowInbound": true,
  "allowOutbound": true,
  "enableSoftphone": true,
  "maxChats": 0
}
```

### Common Fields

| Field | Required | Description |
| --- | --- | --- |
| `username` | Yes | Agent login username. |
| `password` | Yes | Initial password when creating a direct-login agent. |
| `firstName` / `lastName` | No | Agent name. |
| `email` | No | Agent email address. |
| `externalAgentId` | No | External identifier used by your user-management system. |
| `agentType` | No | `AGENT` or `SUPERVISOR`. |
| `agentRank` | No | Routing rank. Higher rank values can receive higher priority. |
| `allowInbound` | No | Whether the agent can receive inbound calls. |
| `allowOutbound` | No | Whether the agent can make outbound calls. |
| `enableSoftphone` | No | Whether softphone login is enabled. |
| `defaultLoginDest` | No | Default login destination. |
| `phoneLoginPin` | No | PIN for phone login workflows. |

## Retrieve Agents

```http
GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents
Authorization: Bearer <ringcxAccessToken>
Accept: application/json
```

Use the returned `agentId` when retrieving, updating, or deleting one agent.

```http
GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}
Authorization: Bearer <ringcxAccessToken>
Accept: application/json
```

## Update an Agent

Retrieve the agent first, update the fields you need to change, and submit the updated object with `PUT`.

```http
PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}
Authorization: Bearer <ringcxAccessToken>
Content-Type: application/json
```

```json
{
  "agentId": 1234567,
  "firstName": "Ada",
  "lastName": "Lovelace",
  "username": "ada.lovelace",
  "agentType": "SUPERVISOR",
  "allowInbound": true,
  "allowOutbound": true,
  "isActive": true
}
```

## Supporting Lookup APIs

Use these endpoints to find IDs referenced by agent configuration.

| Lookup | Method and path |
| --- | --- |
| Agent groups | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups` |
| Dial groups | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/withChildren` |
| Queue groups and queues | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/withChildren` |
| Agent access to a queue | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/gateGroups/{gateGroupId}/gates/{gateId}` |

## Delete an Agent

```http
DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}
Authorization: Bearer <ringcxAccessToken>
```

Delete an agent only after confirming that the agent is no longer needed for queues, campaigns, reports, or supervisor workflows.
