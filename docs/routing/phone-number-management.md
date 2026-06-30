# Phone Number Management APIs

The Phone Number Management APIs let you manage DNIS pools, product assignments, and tracking numbers used by RingCX routing. Use these APIs when phone-number inventory is managed outside the Admin portal or must be synchronized across environments.

## Strategic Overview

Phone numbers are shared by many RingCX features. Voice DNIS can be assigned to queues, IVRs, and cloud route profiles. Tracking numbers add another routing layer for campaigns or attribution workflows.

### Key Use Cases

* **Bulk Number Provisioning:** Upload or update large DNIS inventories without manual entry.
* **Routing Assignment:** Assign voice numbers to queues, IVRs, or cloud route profiles.
* **Inventory Search:** Search pools and identify existing assignments before making changes.
* **Tracking Number Maintenance:** Maintain tracking-number groups and schedule overrides.

### Required Permissions & Scopes

#### 1. Configure OAuth Scopes

To authenticate, your application must be configured with the following permission in the [Developer Portal](https://developers.ringcentral.com/my-account.html#/applications):

* **`ReadAccounts`**: Required to validate account context and access RingCX administrative APIs.

#### 2. Enable RingCX Admin Access

In the RingCX Admin portal, the authenticating user must have permission to read and update telephone-number inventory and the destination product being assigned, such as queues, Visual IVRs, or cloud route profiles.

!!! warning "Common Authorization Errors"
    If the user can authenticate but cannot manage the target number or destination product, the API returns an error similar to:
    ```json
    {
      "errorCode": "access.denied.exception",
      "generalMessage": "You do not have permission to access this resource",
      "timestamp": 1611847650696
    }
    ```

## Manage DNIS Pools

DNIS pool endpoints create, update, search, upload, and delete phone-number inventory.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| Search DNIS | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/utilities/tnManager/searchDnis` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/searchDnis) |
| Search pools | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/utilities/tnManager/search` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/search) |
| Create DNIS pool records | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/utilities/tnManager/dnisPool` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/createDnisPool) |
| Update a DNIS pool record | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/utilities/tnManager/dnisPool` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/updateDnisPool) |
| Upload DNIS pool records | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/utilities/tnManager/uploadDnisPool` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/uploadDnisPool) |
| Bulk update DNIS pools | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/utilities/tnManager/updateBulkDnisPool` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/updateBulkDnisPool) |

## Assign Voice DNIS

Use assigned DNIS endpoints to connect numbers to voice routing products.

| Destination | Method and Path | API Reference |
| --- | --- | --- |
| Queue | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/utilities/tnManager/assignedDnis/gates/{gateId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/updateAssignedDnisForGate) |
| Visual IVR | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/utilities/tnManager/assignedDnis/visualIvrs/{visualIvrId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/updateAssignedDnisForVisualIvr) |
| Cloud route profile | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/utilities/tnManager/assignedDnis/cloudRouteProfiles/{cloudRouteProfileId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/updateAssignedDnisForCloudRouteProfile) |
| Existing assignment | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/utilities/tnManager/assignedDnis/{dnis}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/getAssignedDnis) |
| Remove assignment | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/utilities/tnManager/assignedDnis/{dnis}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/deleteAssignedDnis) |

## Tracking Numbers

Tracking numbers are managed under tracking-number groups.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List groups with numbers | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/tracGroups/withChildren` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/getTracGroupListWithChildren) |
| Get group | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/tracGroups/{tracGroupId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/getTracGroup) |
| Update group | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/tracGroups/{tracGroupId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/updateTracGroup) |
| List numbers | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/tracGroups/{tracGroupId}/tracNumbers` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/getTracNumberList) |
| Create number | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/tracGroups/{tracGroupId}/tracNumbers` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/createTracNumber) |
| Update number | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/tracGroups/{tracGroupId}/tracNumbers/{tracId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Phone-Number-Management/updateTracNumber) |

## Recommended Workflow

1. Search existing DNIS inventory before adding new records.
2. Create or upload missing DNIS pool records.
3. Assign voice DNIS to the correct queue, IVR, or cloud route profile.
4. For tracking-number workflows, update tracking groups and schedule overrides separately.
5. Verify assignments before deleting or reassigning numbers.

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
| `page`, `size`, `sort` | Integer/String | Optional | Search controls for paginated inventory lookups. |
| `file` | File | Required for `uploadDnisPool` | Bulk DNIS pool upload payload (sent as `multipart/form-data`, not a query string). |
| `fileType` | String enum | Required for `uploadDnisPool` | Delimiter format. Currently `COMMA`. |

## Request and Response Examples

### Create DNIS Pool Records

`POST https://ringcx.ringcentral.com/voice/api/v1/admin/utilities/tnManager/dnisPool`

The body is an **array** of `DnisPool` objects; the endpoint creates the list atomically and returns the saved records. The description field on a DnisPool is `dnisDescription` and the owning account is `reservedAccountId` (string). Use `notes` for free-form internal notes.

```json
[
  {
    "dnis": "15551234567",
    "reservedAccountId": "123456",
    "dnisDescription": "Main support line",
    "dnisCategory": "VOICE",
    "active": true
  }
]
```

### Upload a DNIS Pool File

`POST https://ringcx.ringcentral.com/voice/api/v1/admin/utilities/tnManager/uploadDnisPool`

This endpoint accepts a delimited file as a `multipart/form-data` upload. The `fileType` query parameter declares the delimiter (`COMMA`). Use `quoteCharacter` when fields contain the delimiter.

```bash
curl -X POST \
  "https://ringcx.ringcentral.com/voice/api/v1/admin/utilities/tnManager/uploadDnisPool?fileType=COMMA" \
  -H "Authorization: Bearer <token>" \
  -F "file=@dnis_pool.csv"
```

### Assign Voice DNIS to a Queue

`PUT https://ringcx.ringcentral.com/voice/api/v1/admin/utilities/tnManager/assignedDnis/gates/{gateId}`

The body is an **array** of `AssignedDnis` objects. Each entry must use `dnisDescription` (not `description`) and `isActive`.

```json
[
  {
    "dnis": "15551234567",
    "isActive": true,
    "dnisDescription": "Primary support routing"
  }
]
```

### Search Result (`searchDnis`)

The shape returned by `getCustomerDnisPoolList` is `DnisSearchResultDTO`. Fields below are illustrative; refer to the API reference for the full set returned for a given account.

```json
{
  "records": [
    {
      "dnis": "15551234567",
      "dnisE164": "+15551234567",
      "reservedAccountId": "123456",
      "dnisCategory": "VOICE",
      "active": true
    }
  ],
  "totalElements": 1
}
```

### Assignment Lookup (`getDnisAssignment`)

Returns a single `AssignedDnis`. The product is signalled by which of `gate`, `visualIvr`, `cloudRouteProfile`, or `tracNumber` is populated.

```json
{
  "dnis": "15551234567",
  "isActive": true,
  "dnisDescription": "Primary support routing",
  "gate": {
    "gateId": 4567,
    "gateName": "Support queue"
  }
}
```

## Resource Schema Summary

| Resource | Key Fields | Notes |
| --- | --- | --- |
| DNIS pool record (`DnisPool`) | `dnis`, `dnisE164`, `reservedAccountId`, `dnisDescription`, `dnisCategory`, `notes`, `active` | Inventory record for a phone number before or after assignment. |
| Voice assignment (`AssignedDnis`) | `dnis`, `isActive`, `dnisDescription`, plus one of `gate` / `visualIvr` / `cloudRouteProfile` / `tracNumber` | The destination object embedded on the response tells you which product owns the assignment. |
| Tracking number (`TracNumber`) | `tracId`, `tracGroupId`, `dnis`, `dnisDescription`, `active` | Tracking-number configuration used for attribution or routing. |

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

def search_then_assign_voice_dnis(token, dnis, gate_id, description="Primary support routing"):
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
        json=[
            {
                "dnis": dnis,
                "isActive": True,
                "dnisDescription": description,
            }
        ],
    )
    assignment.raise_for_status()
    return assignment.json() if assignment.content else None


def upload_dnis_pool(token, file_path, file_type="COMMA"):
    headers = {"Authorization": f"Bearer {token}"}
    with open(file_path, "rb") as fh:
        response = requests.post(
            f"{BASE_URL}/v1/admin/utilities/tnManager/uploadDnisPool",
            headers=headers,
            params={"fileType": file_type},
            files={"file": fh},
        )
    response.raise_for_status()
    return response.json()
```
