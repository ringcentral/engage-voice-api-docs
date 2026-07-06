# Queue Groups

Queue groups are containers for inbound voice queues. Create a queue group before creating queues, queue skills, queue events, or queue-specific routing configuration.

## Queue Group and Gate Group Terminology

The API uses the historical `gateGroups` path name. In the RingCX Admin UI, these resources are commonly presented as queue groups. In these docs, **queue group** and **gate group** refer to the same resource.

## Manage Queue Groups

Use the following endpoints to create, list, retrieve, update, and delete queue groups.

| Operation | Method and path |
| --- | --- |
| List queue groups with child queues | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/withChildren` |
| Get queue group details | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}` |
| Create queue group | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups` |
| Update queue group | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}` |
| Delete queue group | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}` |

## Create a Queue Group

Only `groupName` is required when creating a queue group.

```http
POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups
Authorization: Bearer <ringcxAccessToken>
Content-Type: application/json
```

```json
{
  "groupName": "Support Queues"
}
```

### Common Fields

| Field | Required | Description |
| --- | --- | --- |
| `groupName` | Yes | Display name for the queue group. |
| `billingKey` | No | Optional external billing or reporting key. |
| `gateGroupId` | No | Queue group ID. If omitted during create, RingCX assigns the next available ID. |

## Retrieve Queue Groups

```http
GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/withChildren
Authorization: Bearer <ringcxAccessToken>
Accept: application/json
```

Use `withChildren` when you need the group and its queues in one response. Use `GET /gateGroups/{gateGroupId}` when you already know the queue group ID and only need one group.

## Update a Queue Group

Retrieve the queue group first, update the fields you need to change, and send the updated object back with `PUT`.

```http
PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}
Authorization: Bearer <ringcxAccessToken>
Content-Type: application/json
```

```json
{
  "gateGroupId": 12345,
  "groupName": "Support Queues - Updated",
  "billingKey": "support"
}
```

## Delete a Queue Group

```http
DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}
Authorization: Bearer <ringcxAccessToken>
```

Delete a queue group only after confirming that queues, skills, schedules, and other routing configuration under the group are no longer needed.
