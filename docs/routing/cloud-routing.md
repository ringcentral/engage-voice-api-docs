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

Your application needs the `ReadAccounts` OAuth scope. The authenticating RingCX user also needs platform permissions to read and update cloud route groups, destinations, profiles, and assigned destinations.

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
| List destinations | `GET /voice/api/v1/admin/accounts/{accountId}/cloudRouteDestinationGroups/{cloudRouteGroupId}/cloudRouteDestinations` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/getCloudRouteDestinationList) |
| Create destination | `POST /voice/api/v1/admin/accounts/{accountId}/cloudRouteDestinationGroups/{cloudRouteGroupId}/cloudRouteDestinations` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/createCloudRouteDestination) |
| Get destination | `GET /voice/api/v1/admin/accounts/{accountId}/cloudRouteDestinationGroups/{cloudRouteGroupId}/cloudRouteDestinations/{cloudRouteDestinationId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/getCloudRouteDestination) |
| Update destination | `PUT /voice/api/v1/admin/accounts/{accountId}/cloudRouteDestinationGroups/{cloudRouteGroupId}/cloudRouteDestinations/{cloudRouteDestinationId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/updateCloudRouteDestination) |
| Clone destination | `POST /voice/api/v1/admin/accounts/{accountId}/cloudRouteDestinationGroups/{cloudRouteGroupId}/cloudRouteDestinations/{cloudRouteDestinationId}/clone` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/cloneCloudRouteDestination) |
| Set active state | `PUT /voice/api/v1/admin/accounts/{accountId}/cloudRouteDestinationGroups/{cloudRouteGroupId}/cloudRouteDestinations/{cloudRouteDestinationId}/setIsActive` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/setCloudRouteDestinationIsActive) |

## Manage Profiles

Cloud route profiles control how traffic is distributed across assigned destinations.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| Create profile | `POST /voice/api/v1/admin/accounts/{accountId}/cloudRouteProfileGroups/{cloudRouteGroupId}/cloudRouteProfiles` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/createCloudRouteProfile) |
| Get profile | `GET /voice/api/v1/admin/accounts/{accountId}/cloudRouteProfileGroups/{cloudRouteGroupId}/cloudRouteProfiles/{cloudProfileId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/getCloudRouteProfile) |
| Update profile | `PUT /voice/api/v1/admin/accounts/{accountId}/cloudRouteProfileGroups/{cloudRouteGroupId}/cloudRouteProfiles/{cloudRouteProfileId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/updateCloudRouteProfile) |
| Clone profile | `POST /voice/api/v1/admin/accounts/{accountId}/cloudRouteProfileGroups/{cloudRouteGroupId}/cloudRouteProfiles/{cloudRouteProfileId}/clone` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/cloneCloudRouteProfile) |
| Set active state | `PUT /voice/api/v1/admin/accounts/{accountId}/cloudRouteProfileGroups/{cloudRouteGroupId}/cloudRouteProfiles/{cloudRouteProfileId}/setIsActive` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/setCloudRouteProfileIsActive) |

## Assign Destinations to Profiles

Use assigned destinations to define the destinations a profile can route to. For percentage-based routing, export the allocation hours, modify them offline, and import the updated allocation file.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List assigned destinations | `GET /voice/api/v1/admin/accounts/{accountId}/cloudRouteProfileGroups/{cloudRouteGroupId}/cloudRouteProfiles/{cloudRouteProfileId}/assignedDestinations` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/getCloudAssignedDestinationList) |
| Create assignment | `POST /voice/api/v1/admin/accounts/{accountId}/cloudRouteProfileGroups/{cloudRouteGroupId}/cloudRouteProfiles/{cloudRouteProfileId}/assignedDestinations` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/createCloudAssignedDestination) |
| Update assignments in batch | `PUT /voice/api/v1/admin/accounts/{accountId}/cloudRouteProfileGroups/{cloudRouteGroupId}/cloudRouteProfiles/{cloudRouteProfileId}/assignedDestinations/batch` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/batchUpdateCloudAssignedDestinations) |
| Export allocation hours | `POST /voice/api/v1/admin/accounts/{accountId}/cloudRouteProfileGroups/{cloudRouteGroupId}/cloudRouteProfiles/{cloudRouteProfileId}/assignedDestinations/percentAllocationHours/export` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/exportPercentAllocationHours) |
| Import allocation hours | `POST /voice/api/v1/admin/accounts/{accountId}/cloudRouteProfileGroups/{cloudRouteGroupId}/cloudRouteProfiles/{cloudRouteProfileId}/assignedDestinations/percentAllocationHours/import` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/importPercentAllocationHours) |

## Configure DNIS Overrides

DNIS overrides let a cloud route destination apply number-specific routing behavior.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List overrides | `GET /voice/api/v1/admin/accounts/{accountId}/cloudRouteDestinationGroups/{cloudRouteGroupId}/cloudRouteDestinations/{cloudRouteDestinationId}/dnisOverrides` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/getDnisOverrideList) |
| Create override | `POST /voice/api/v1/admin/accounts/{accountId}/cloudRouteDestinationGroups/{cloudRouteGroupId}/cloudRouteDestinations/{cloudRouteDestinationId}/dnisOverrides` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/createDnisOverride) |
| Create overrides in batch | `POST /voice/api/v1/admin/accounts/{accountId}/cloudRouteDestinationGroups/{cloudRouteGroupId}/cloudRouteDestinations/{cloudRouteDestinationId}/dnisOverrides/batch` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Cloud-Routing/createDnisOverrideBatch) |

## Recommended Workflow

1. List route groups and choose the destination/profile group.
2. Create or update destinations.
3. Create or update the routing profile.
4. Assign destinations to the profile and configure allocation rules.
5. Add DNIS overrides only for numbers that require special behavior.
6. Activate the destination or profile after the configuration has been verified.

!!! important "Rate Limiting & Stability"
    Make provisioning changes in batches and use exponential backoff on `429 Too Many Requests` responses.
