# Cloud Routing APIs

The Cloud Routing APIs let you configure destination-based routing for voice traffic in RingCX. Use them to maintain cloud route destination groups, routing profiles, DNIS overrides, and destination assignments from an external provisioning system.

## Strategic Overview

Cloud routing is used when inbound voice traffic should be distributed across external destinations or routing profiles instead of a standard queue-only flow. These APIs are configuration APIs: they change how future calls are routed, but they do not control calls already in progress.

### Key Use Cases

* **Routing Provisioning:** Create destination groups and profiles as part of a new sub-account rollout.
* **Traffic Distribution:** Maintain profile-to-destination assignments and percent allocation schedules.
* **DNIS-Specific Behavior:** Apply DNIS overrides when specific numbers need different destination behavior.
* **Operational Failover:** Activate, deactivate, clone, or adjust routing profiles during planned changes.

### Required Permissions & Scopes

#### 1. Configure OAuth Scopes

To authenticate, your application must be configured with **`ReadAccounts`** in the [Developer Portal](https://developers.ringcentral.com/my-account.html#/applications).

#### 2. Enable RingCX Admin Access

The authenticating RingCX user must have Admin portal permissions to read and update cloud route groups, destinations, profiles, assigned destinations, and DNIS overrides for the target account.

!!! warning "Common Authorization Errors"
    If the OAuth token is valid but the user cannot manage cloud routing, the API returns an error similar to:
    ```json
    {
      "errorCode": "access.denied.exception",
      "generalMessage": "You do not have permission to access this resource",
      "timestamp": 1611847650696
    }
    ```

## Discover Cloud Route Groups

Start by listing destination groups and profile groups for the account.

`GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteDestinationGroups`

**API Reference:** [List cloud route destination groups](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/getCloudRouteDestinationGroupList)

`GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteProfileGroups/{cloudRouteGroupId}/cloudRouteProfiles`

**API Reference:** [List cloud route profiles](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/getCloudRouteProfileList)

## Manage Destinations

Cloud route destinations define where calls can be sent. A destination belongs to a cloud route destination group.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List destinations | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteDestinationGroups/{cloudRouteGroupId}/cloudRouteDestinations` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/getCloudRouteDestinationList) |
| Create destination | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteDestinationGroups/{cloudRouteGroupId}/cloudRouteDestinations` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/createCloudRouteDestination) |
| Get destination | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteDestinationGroups/{cloudRouteGroupId}/cloudRouteDestinations/{cloudRouteDestinationId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/getCloudRouteDestination) |
| Update destination | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteDestinationGroups/{cloudRouteGroupId}/cloudRouteDestinations/{cloudRouteDestinationId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/updateCloudRouteDestination) |
| Clone destination | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteDestinationGroups/{cloudRouteGroupId}/cloudRouteDestinations/{cloudRouteDestinationId}/clone` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/cloneCloudRouteDestination) |
| Set active state | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteDestinationGroups/{cloudRouteGroupId}/cloudRouteDestinations/{cloudRouteDestinationId}/setIsActive` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/setCloudRouteDestinationIsActive) |

## Manage Profiles

Cloud route profiles control how traffic is distributed across assigned destinations.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| Create profile | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteProfileGroups/{cloudRouteGroupId}/cloudRouteProfiles` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/createCloudRouteProfile) |
| Get profile | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteProfileGroups/{cloudRouteGroupId}/cloudRouteProfiles/{cloudProfileId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/getCloudRouteProfile) |
| Update profile | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteProfileGroups/{cloudRouteGroupId}/cloudRouteProfiles/{cloudRouteProfileId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/updateCloudRouteProfile) |
| Clone profile | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteProfileGroups/{cloudRouteGroupId}/cloudRouteProfiles/{cloudRouteProfileId}/clone` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/cloneCloudRouteProfile) |
| Set active state | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteProfileGroups/{cloudRouteGroupId}/cloudRouteProfiles/{cloudRouteProfileId}/setIsActive` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/setCloudRouteProfileIsActive) |

## Assign Destinations to Profiles

Use assigned destinations to define the destinations a profile can route to. For percentage-based routing, export the allocation hours, modify them offline, and import the updated allocation file.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List assigned destinations | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteProfileGroups/{cloudRouteGroupId}/cloudRouteProfiles/{cloudRouteProfileId}/assignedDestinations` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/getCloudAssignedDestinationList) |
| Create assignment | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteProfileGroups/{cloudRouteGroupId}/cloudRouteProfiles/{cloudRouteProfileId}/assignedDestinations` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/createCloudAssignedDestination) |
| Update assignments in batch | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteProfileGroups/{cloudRouteGroupId}/cloudRouteProfiles/{cloudRouteProfileId}/assignedDestinations/batch` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/batchUpdateCloudAssignedDestinations) |
| Export allocation hours | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteProfileGroups/{cloudRouteGroupId}/cloudRouteProfiles/{cloudRouteProfileId}/assignedDestinations/percentAllocationHours/export` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/exportPercentAllocationHours) |
| Import allocation hours | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteProfileGroups/{cloudRouteGroupId}/cloudRouteProfiles/{cloudRouteProfileId}/assignedDestinations/percentAllocationHours/import` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/importPercentAllocationHours) |

## Configure DNIS Overrides

DNIS overrides let a cloud route destination apply number-specific routing behavior.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List overrides | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteDestinationGroups/{cloudRouteGroupId}/cloudRouteDestinations/{cloudRouteDestinationId}/dnisOverrides` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/getDnisOverrideList) |
| Create override | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteDestinationGroups/{cloudRouteGroupId}/cloudRouteDestinations/{cloudRouteDestinationId}/dnisOverrides` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/createDnisOverride) |
| Create overrides in batch | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteDestinationGroups/{cloudRouteGroupId}/cloudRouteDestinations/{cloudRouteDestinationId}/dnisOverrides/batch` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/createDnisOverrideBatch) |

## Recommended Workflow

1. List route groups and choose the destination/profile group.
2. Create or update destinations.
3. Create or update the routing profile.
4. Assign destinations to the profile and configure allocation rules.
5. Add DNIS overrides only for numbers that require special behavior.
6. Activate the destination or profile after the configuration has been verified.

!!! important "Rate Limiting & Stability"
    Make provisioning changes in batches and use exponential backoff on `429 Too Many Requests` responses.

## Request Examples

### Create a Destination

`POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteDestinationGroups/{cloudRouteGroupId}/cloudRouteDestinations`

The resource identifier on the response is `cloudDestinationId` and the description field is `destinationDesc`. `routeDestination` carries the destination address (DID, SIP URI, ACD queue, etc.) and `destinationType` controls how the platform treats it. `isActive` governs whether the destination receives traffic.

```json
{
  "destinationName": "Denver overflow",
  "destinationDesc": "Overflow destination for Denver support",
  "destinationType": "DID",
  "routeDestination": "13035551234",
  "ringDuration": 20,
  "isActive": false
}
```

### Create a Profile

`POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteProfileGroups/{cloudRouteGroupId}/cloudRouteProfiles`

The resource identifier is `cloudProfileId` and the description field is `profileDesc`. `routingType` and `percentAllocType` control how traffic is distributed across the profile's assigned destinations.

```json
{
  "profileName": "Support business hours",
  "profileDesc": "Primary and overflow destinations for support",
  "routingType": "PERCENT_ALLOCATION",
  "percentAllocType": "DAILY",
  "isActive": false
}
```

### Assign a Destination

`POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteProfileGroups/{cloudRouteGroupId}/cloudRouteProfiles/{cloudRouteProfileId}/assignedDestinations`

The assignment object references the underlying destination by embedding a `cloudDestination` object. Use `rank` for priority and `allocationPercent` for percent-allocation profiles.

```json
{
  "cloudDestination": { "cloudDestinationId": 12345 },
  "destinationType": "STANDARD",
  "rank": 1,
  "allocationPercent": 100,
  "ringDuration": 20
}
```

### Create a DNIS Override

`POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteDestinationGroups/{cloudRouteGroupId}/cloudRouteDestinations/{cloudRouteDestinationId}/dnisOverrides`

A DNIS override (`CloudRouteDestinationOverride`) attaches an alternate `routeDestination` to a specific DNIS on the parent destination.

```json
{
  "dnis": "15551234567",
  "routeDestination": "13035556789",
  "countryId": "1"
}
```

### Example Destination Response

```json
{
  "cloudDestinationId": 12345,
  "cloudRouteGroup": { "cloudGroupId": 678, "groupName": "Denver routing" },
  "destinationName": "Denver overflow",
  "destinationDesc": "Overflow destination for Denver support",
  "destinationType": "DID",
  "routeDestination": "13035551234",
  "ringDuration": 20,
  "isActive": false,
  "isDeleted": false,
  "permissions": ["READ", "UPDATE"]
}
```

### Percent Allocation Import/Export

The export endpoint returns the current percent-allocation-hours file for the profile. Edit the returned file offline, then POST it back to the import endpoint as a `multipart/form-data` upload. The `extension` query parameter (`PIPE`, `COMMA`, or `TAB`) tells the platform how to parse the delimited file. Keep the export format intact; the file schema is controlled by the generator and should not be reconstructed from scratch.

```bash
curl -X POST \
  "https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/cloudRouteProfileGroups/{cloudRouteGroupId}/cloudRouteProfiles/{cloudRouteProfileId}/assignedDestinations/percentAllocationHours/import?extension=COMMA" \
  -H "Authorization: Bearer <token>" \
  -F "file=@allocation_hours.csv"
```

## Primary Resource Fields

| Resource | Fields | Notes |
| --- | --- | --- |
| Destination group (`CloudRouteGroup`) | `cloudGroupId`, `groupName`, `isDefault`, `cloudRouteDestinations`, `cloudRouteProfiles`, `permissions` | Groups destinations and profiles for an account. |
| Destination (`CloudRouteDestination`) | `cloudDestinationId`, `destinationName`, `destinationDesc`, `destinationType`, `routeDestination`, `ringDuration`, `isActive`, `isDeleted` | A target that can receive routed calls. Day-of-week schedule fields (`monSched`, `tueSched`, ...) define when the destination is eligible. |
| Profile (`CloudRouteProfile`) | `cloudProfileId`, `profileName`, `profileDesc`, `routingType`, `percentAllocType`, `routeExhaustedAction`, `isActive` | Routing policy that owns destination assignments. |
| Assigned destination (`CloudRouteAssignedDestination`) | `assignedDestinationId`, `cloudDestination`, `destinationType`, `rank`, `allocationPercent`, `allocationPercentHours`, `ringDuration` | Connects a destination to a profile. |
| DNIS override (`CloudRouteDestinationOverride`) | `destOverrideId`, `dnis`, `routeDestination`, `countryId`, `cloudDestination` | Applies number-specific routing behaviour on top of a destination. |

## Common Errors

| Status | Cause | Resolution |
| --- | --- | --- |
| `400 Bad Request` | Missing required destination/profile fields or malformed allocation import. | Validate request bodies and uploaded allocation files before calling the API. |
| `403 Forbidden` | User lacks cloud-routing Admin portal permissions. | Grant routing configuration permissions for the target account. |
| `404 Not Found` | Group, destination, profile, assignment, or DNIS override ID does not belong to the account. | Re-list the parent resource and use IDs from the same group. |
| `409 Conflict` | Active routing configuration would conflict with existing assignments or DNIS overrides. | Deactivate or update existing configuration before creating replacements. |

## Sample Implementation (Python)

```python
import requests

BASE_URL = "https://ringcx.ringcentral.com/voice/api"

def create_destination_and_assign(token, account_id, dest_group_id, profile_group_id, profile_id):
    headers = {"Authorization": f"Bearer {token}"}

    destination_url = (
        f"{BASE_URL}/v1/admin/accounts/{account_id}"
        f"/cloudRouteDestinationGroups/{dest_group_id}/cloudRouteDestinations"
    )
    destination = requests.post(
        destination_url,
        headers=headers,
        json={
            "destinationName": "Denver overflow",
            "destinationDesc": "Overflow destination for Denver support",
            "destinationType": "DID",
            "routeDestination": "13035551234",
            "ringDuration": 20,
            "isActive": False,
        },
    )
    destination.raise_for_status()
    destination_id = destination.json()["cloudDestinationId"]

    assign_url = (
        f"{BASE_URL}/v1/admin/accounts/{account_id}/cloudRouteProfileGroups/{profile_group_id}"
        f"/cloudRouteProfiles/{profile_id}/assignedDestinations"
    )
    assignment = requests.post(
        assign_url,
        headers=headers,
        json={
            "cloudDestination": {"cloudDestinationId": destination_id},
            "destinationType": "STANDARD",
            "rank": 1,
            "allocationPercent": 100,
            "ringDuration": 20,
        },
    )
    assignment.raise_for_status()
    return assignment.json()


def import_allocation_hours(token, account_id, profile_group_id, profile_id, file_path, extension="COMMA"):
    headers = {"Authorization": f"Bearer {token}"}
    url = (
        f"{BASE_URL}/v1/admin/accounts/{account_id}/cloudRouteProfileGroups/{profile_group_id}"
        f"/cloudRouteProfiles/{profile_id}/assignedDestinations/percentAllocationHours/import"
    )
    with open(file_path, "rb") as fh:
        response = requests.post(
            url,
            headers=headers,
            params={"extension": extension},
            files={"file": fh},
        )
    response.raise_for_status()
    return response.json()
```
