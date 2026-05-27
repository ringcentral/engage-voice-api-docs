# Phone Number Management APIs

The Phone Number Management APIs let you manage DNIS pools, SMS DNIS assignments, product assignments, and tracking numbers used by RingCX routing. Use these APIs when phone-number inventory is managed outside the Admin portal or must be synchronized across environments.

## Strategic Overview

Phone numbers are shared by many RingCX features. Voice DNIS can be assigned to queues, IVRs, and cloud route profiles; SMS DNIS can be assigned to chat queues. Tracking numbers add another routing layer for campaigns or attribution workflows.

### Key Use Cases

* **Bulk Number Provisioning:** Upload or update large DNIS inventories without manual entry.
* **Routing Assignment:** Assign voice numbers to queues, IVRs, or cloud route profiles.
* **Digital Assignment:** Assign SMS-enabled numbers to chat queues.
* **Inventory Search:** Search pools and identify existing assignments before making changes.
* **Tracking Number Maintenance:** Maintain tracking-number groups and schedule overrides.

### Required Permissions & Scopes

Your application needs the `ReadAccounts` OAuth scope. In the RingCX Admin portal, the authenticating user must also have permission to read and update telephone-number inventory and the destination product being assigned.

## Manage DNIS Pools

DNIS pool endpoints create, update, search, upload, and delete phone-number inventory.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| Search DNIS | `POST /voice/api/v1/admin/utilities/tnManager/searchDnis` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/searchDnis) |
| Search pools | `POST /voice/api/v1/admin/utilities/tnManager/search` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/search) |
| Create DNIS pool records | `POST /voice/api/v1/admin/utilities/tnManager/dnisPool` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/createDnisPool) |
| Update a DNIS pool record | `PUT /voice/api/v1/admin/utilities/tnManager/dnisPool` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/updateDnisPool) |
| Upload DNIS pool records | `POST /voice/api/v1/admin/utilities/tnManager/uploadDnisPool` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/uploadDnisPool) |
| Bulk update DNIS pools | `PUT /voice/api/v1/admin/utilities/tnManager/updateBulkDnisPool` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/updateBulkDnisPool) |

## Assign Voice DNIS

Use assigned DNIS endpoints to connect numbers to voice routing products.

| Destination | Method and Path | API Reference |
| --- | --- | --- |
| Queue | `PUT /voice/api/v1/admin/utilities/tnManager/assignedDnis/gates/{gateId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/updateAssignedDnisForGate) |
| Visual IVR | `PUT /voice/api/v1/admin/utilities/tnManager/assignedDnis/visualIvrs/{visualIvrId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/updateAssignedDnisForVisualIvr) |
| Cloud route profile | `PUT /voice/api/v1/admin/utilities/tnManager/assignedDnis/cloudRouteProfiles/{cloudRouteProfileId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/updateAssignedDnisForCloudRouteProfile) |
| Existing assignment | `GET /voice/api/v1/admin/utilities/tnManager/assignedDnis/{dnis}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/getAssignedDnis) |
| Remove assignment | `DELETE /voice/api/v1/admin/utilities/tnManager/assignedDnis/{dnis}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/deleteAssignedDnis) |

## Assign SMS DNIS

SMS DNIS assignments connect digital numbers to chat queues.

`PUT https://ringcx.ringcentral.com/voice/api/v1/admin/utilities/tnManager/assignedSmsDnis/chatQueues/{chatQueueId}`

**API Reference:** [Assign SMS DNIS to chat queue](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/updateAssignedSmsDnisForChatQueue)

Use `GET /voice/api/v1/admin/utilities/tnManager/assignedSmsDnis/{dnis}` to inspect an existing SMS assignment and `DELETE /voice/api/v1/admin/utilities/tnManager/assignedSmsDnis/{dnis}` to remove it.

## Tracking Numbers

Tracking numbers are managed under tracking-number groups.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List groups with numbers | `GET /voice/api/v1/admin/accounts/{accountId}/tracGroups/withChildren` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/getTracGroupListWithChildren) |
| Get group | `GET /voice/api/v1/admin/accounts/{accountId}/tracGroups/{tracGroupId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/getTracGroup) |
| Update group | `PUT /voice/api/v1/admin/accounts/{accountId}/tracGroups/{tracGroupId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/updateTracGroup) |
| List numbers | `GET /voice/api/v1/admin/accounts/{accountId}/tracGroups/{tracGroupId}/tracNumbers` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/getTracNumberList) |
| Create number | `POST /voice/api/v1/admin/accounts/{accountId}/tracGroups/{tracGroupId}/tracNumbers` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/createTracNumber) |
| Update number | `PUT /voice/api/v1/admin/accounts/{accountId}/tracGroups/{tracGroupId}/tracNumbers/{tracId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/updateTracNumber) |

## Recommended Workflow

1. Search existing DNIS inventory before adding new records.
2. Create or upload missing DNIS pool records.
3. Assign voice DNIS to the correct queue, IVR, or cloud route profile.
4. Assign SMS DNIS to chat queues when digital routing is needed.
5. For tracking-number workflows, update tracking groups and schedule overrides separately.
6. Verify assignments before deleting or reassigning numbers.

!!! warning
    Reassigning or deleting a phone number can immediately affect customer routing. Confirm the target product and maintenance window before applying bulk changes.

!!! important "Rate Limiting & Stability"
    Treat number inventory changes as provisioning operations. Search first, update only changed records, and batch bulk uploads so retries do not duplicate or reassign numbers unexpectedly.

## Primary Parameters

| Parameter | Type | Requirement | Description |
| --- | --- | --- | --- |
| `dnis` | String | **Required** | Phone number in DNIS inventory. Use a normalized E.164-style value when possible. |
| `gateId` | Integer | Required for queue assignment | Voice queue identifier. |
| `visualIvrId` | Integer | Required for Visual IVR assignment | Visual IVR identifier. |
| `cloudRouteProfileId` | Integer | Required for cloud routing assignment | Cloud route profile identifier. |
| `chatQueueId` | Integer | Required for SMS assignment | Chat queue that should receive SMS traffic for the number. |
| `page`, `size`, `sort` | Integer/String | Optional | Search controls for paginated inventory lookups. |
| `file` | File | Required for upload endpoints | Bulk DNIS pool upload payload. |

## Request and Response Examples

### Create DNIS Pool Records

`POST https://ringcx.ringcentral.com/voice/api/v1/admin/utilities/tnManager/dnisPool`

```json
{
  "dnis": "15551234567",
  "description": "Main support line",
  "accountId": 123456,
  "active": true
}
```

### Assign Voice DNIS to a Queue

`PUT https://ringcx.ringcentral.com/voice/api/v1/admin/utilities/tnManager/assignedDnis/gates/{gateId}`

```json
{
  "dnis": "15551234567"
}
```

### Assign SMS DNIS to a Chat Queue

`PUT https://ringcx.ringcentral.com/voice/api/v1/admin/utilities/tnManager/assignedSmsDnis/chatQueues/{chatQueueId}`

```json
{
  "dnis": "15557654321"
}
```

### Search Result

```json
{
  "records": [
    {
      "dnis": "15551234567",
      "assignedProduct": "GATE",
      "destinationId": 4567,
      "active": true
    }
  ],
  "page": 0,
  "size": 25,
  "totalElements": 1
}
```

### Assignment Lookup

```json
{
  "dnis": "15551234567",
  "product": "GATE",
  "destinationId": 4567,
  "destinationName": "Support queue"
}
```

## Common Errors

| Status | Cause | Resolution |
| --- | --- | --- |
| `400 Bad Request` | DNIS format is invalid or the target destination ID is missing. | Normalize numbers and validate target IDs before assignment. |
| `403 Forbidden` | Caller lacks telephone-number or destination-product permissions. | Grant inventory and target product permissions in the Admin portal. |
| `404 Not Found` | DNIS or destination product does not exist. | Search inventory and list the destination product before assigning. |
| `409 Conflict` | DNIS is already assigned or duplicated in a bulk upload. | Inspect the current assignment and remove or update it intentionally. |

## Sample Implementation (Python)

```python
import requests

BASE_URL = "https://ringcx.ringcentral.com/voice/api"

def search_then_assign_voice_dnis(token, dnis, gate_id):
    headers = {"Authorization": f"Bearer {token}"}
    search = requests.post(
        f"{BASE_URL}/v1/admin/utilities/tnManager/searchDnis",
        headers=headers,
        json={"dnis": dnis},
    )
    search.raise_for_status()

    assignment = requests.put(
        f"{BASE_URL}/v1/admin/utilities/tnManager/assignedDnis/gates/{gate_id}",
        headers=headers,
        json={"dnis": dnis},
    )
    assignment.raise_for_status()
    return assignment.json() if assignment.content else None
```
