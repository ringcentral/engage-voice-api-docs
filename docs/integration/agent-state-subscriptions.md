# Agent State Subscription APIs

The Agent State Subscription APIs let WFM and real-time monitoring systems subscribe to agent-state updates for a RingCX sub-account. Use them when a downstream system needs event-style state updates instead of only polling real-time reports.

## Strategic Overview

Agent state subscriptions are designed for integrations that track availability, adherence, and live staffing. A subscription tells RingCX where to deliver agent-state updates for a sub-account, and the subscription can be listed, updated, or deleted as integration endpoints change.

### Key Use Cases

* **WFM Synchronization:** Feed live agent availability into workforce management tools.
* **Adherence Monitoring:** Compare actual agent states against scheduled activities.
* **Operational Dashboards:** Maintain a near-real-time view of agent presence without aggressive polling.
* **Endpoint Rotation:** Update subscription targets when middleware URLs or credentials change.

### Required Permissions & Scopes

#### 1. Configure OAuth Scopes

To authenticate, your application must be configured with the following permission in the [Developer Portal](https://developers.ringcentral.com/my-account.html#/applications):

* **`ReadAccounts`**: Required to validate account context and access RingCX integration APIs.

#### 2. Enable RingCX Admin Access

The authenticating user must have the `WFO_ACCESS` role for the target RingCX sub-account. The account must also be enabled for WFM/RTA subscription access.

!!! warning "Common Authorization Errors"
    If the user does not have the `WFO_ACCESS` role, the API returns an authorization error similar to:
    ```json
    {
      "errorCode": "access.denied.exception",
      "generalMessage": "You do not have permission to access this resource",
      "timestamp": 1611847650696
    }
    ```

!!! important "Rate Limiting & Stability"
    Subscription management calls are configuration operations. Avoid repeatedly creating and deleting subscriptions in a tight loop; list existing subscriptions first, then update the existing subscription when possible.

## Subscription Lifecycle

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List subscriptions | `GET https://ringcx.ringcentral.com/voice/api/cx/integration/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/agent-states/subscriptions` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Agent-State-Subscriptions/getAllSubscriptions) |
| Create subscription | `POST https://ringcx.ringcentral.com/voice/api/cx/integration/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/agent-states/subscriptions` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Agent-State-Subscriptions/subscribe) |
| Update subscription | `PUT https://ringcx.ringcentral.com/voice/api/cx/integration/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/agent-states/subscriptions/{subscriptionId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Agent-State-Subscriptions/updateSubscription) |
| Delete subscription | `DELETE https://ringcx.ringcentral.com/voice/api/cx/integration/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/agent-states/subscriptions/{subscriptionId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Agent-State-Subscriptions/deleteSubscription) |

## Create a Subscription

`POST https://ringcx.ringcentral.com/voice/api/cx/integration/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/agent-states/subscriptions`

A subscription request identifies the target sub-account and the integration endpoint that should receive agent-state updates. Use a stable HTTPS endpoint and configure authentication or custom headers when the receiving system requires them.

### Path Parameters

| Parameter | Type | Requirement | Description |
| --- | --- | --- | --- |
| `rcAccountId` | String | **Required** | RingCentral account ID. |
| `subAccountId` | String | **Required** | RingCX sub-account ID. |

### Request Body

The request body matches the `RTASubscriptionRequest` schema.

| Parameter | Type | Requirement | Description |
| --- | --- | --- | --- |
| `subscriptionName` | String | **Required** | Unique active subscription name for the sub-account. |
| `description` | String | Optional | Human-readable description. |
| `retryCount` | Integer | Optional | Maximum delivery retry count. Defaults to `3` and cannot exceed `10`. |
| `notificationUrl` | String | **Required** | HTTP or HTTPS endpoint that receives agent-state notifications. |
| `authConfigId` | UUID | Optional | Auth configuration ID used when RingCX sends notification requests to the receiver. |
| `active` | Boolean | Optional | Whether the subscription is created in an active state. Defaults to active. |
| `customHeaders` | Object | Optional | Additional headers to send with notification requests. Values are arbitrary JSON (`additionalProperties: object`); strings are the safest choice. |
| `expiresAt` | Integer | Optional | Future epoch timestamp (`int64`) after which the subscription expires. Use `0` or omit for no configured expiration. |

**Example Request:**

```json
{
  "subscriptionName": "WFM agent state feed",
  "description": "Agent state events for workforce management",
  "retryCount": 3,
  "notificationUrl": "https://example.com/ringcx/agent-states",
  "authConfigId": "2f8f8b6e-2a5c-4d8c-bd44-31db90a77b2a",
  "active": true,
  "customHeaders": {
    "X-Integration-Name": "wfm-sync"
  },
  "expiresAt": 1893456000
}
```

### Example Response

```json
{
  "subscriptionId": "5b0f5e9a-f3c2-45c4-9a4f-111111111111",
  "mainAccountId": "400000000",
  "subAccountId": "123456789",
  "subscriptionName": "WFM agent state feed",
  "description": "Agent state events for workforce management",
  "notificationUrl": "https://example.com/ringcx/agent-states",
  "authConfigId": "2f8f8b6e-2a5c-4d8c-bd44-31db90a77b2a",
  "active": true,
  "maxRetryCount": 3,
  "customHeaders": {
    "X-Integration-Name": "wfm-sync"
  },
  "expiresAt": 1893456000,
  "createdBy": "Admin User",
  "createdAt": "2026-05-27T18:00:00Z",
  "updatedBy": "Admin User",
  "updatedAt": "2026-05-27T18:00:00Z"
}
```

### Response Object

The response matches the `RTASubscriptionResponse` schema and includes audit fields that show who last changed the subscription.

| Field | Type | Description |
| --- | --- | --- |
| `subscriptionId` | UUID | Unique subscription identifier. |
| `mainAccountId` | String | Main account that owns the sub-account. |
| `subAccountId` | String | RingCX sub-account receiving subscription events. |
| `subscriptionName` | String | Subscription display name. |
| `description` | String | Human-readable description. |
| `notificationUrl` | String | Receiver endpoint. |
| `authConfigId` | UUID | Auth configuration used for notification authentication, if configured. |
| `authConfig` | Object | Resolved auth configuration metadata, when returned. |
| `active` | Boolean | Whether the subscription is active. |
| `maxRetryCount` | Integer | Maximum delivery retry count. The request field is `retryCount`; the response field is `maxRetryCount`. |
| `customHeaders` | Object | Custom headers sent to the receiver. |
| `expiresAt` | Integer | Expiration epoch timestamp. |
| `createdBy`, `createdAt`, `updatedBy`, `updatedAt` | String / DateTime | Audit fields tracking who last changed the subscription. |

## Receiver Endpoint

The `notificationUrl` is the destination for the agent-state notification feed. This page covers how to manage the subscription resource. For examples of Workforce Management agent-state notification fields, see [Understanding the Event Payload](../notifications/wfm/payload-wfm.md#agent-state-events).

When implementing a receiver, validate the authentication method and custom headers configured for the subscription, respond quickly after accepting the notification, and process events idempotently. The `retryCount` setting controls how many delivery retries RingCX can attempt after a delivery failure.

## Common Errors

| Status | Cause | Resolution |
| --- | --- | --- |
| `400 Bad Request` | Missing `subscriptionName`, invalid `notificationUrl`, retry count above `10`, or expired `expiresAt`. | Validate the request body before calling the API. |
| `403 Forbidden` | User lacks `WFO_ACCESS`. | Enable WFM/RTA access for the user. |
| `404 Not Found` | Invalid `authConfigId` or subscription ID. | Confirm the external auth configuration and subscription belong to the same sub-account. |
| `409 Conflict` | Active subscription name already exists for the sub-account. | List subscriptions first and update the existing subscription. |

## Operational Guidance

1. List subscriptions before creating a new one to avoid duplicate feeds.
2. Create one subscription per downstream integration endpoint.
3. Update the subscription when the receiver URL, credentials, or enabled state changes.
4. Delete subscriptions that are no longer monitored.
5. Monitor receiver health and compare delivery against [Real-Time Supervisor View](../analytics/reports/realtime-supervisor-view.md) snapshots when troubleshooting.

!!! important "Reliability"
    Design the receiving service to be idempotent. Delivery retries can occur after receiver or network failures.
