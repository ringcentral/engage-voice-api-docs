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

A subscription request identifies the target sub-account and the integration endpoint that should receive agent-state updates. Use a durable middleware endpoint that can authenticate incoming requests, retry safely, and tolerate duplicate delivery.

### Path Parameters

| Parameter | Type | Requirement | Description |
| --- | --- | --- | --- |
| `rcAccountId` | String | **Required** | RingCentral account ID. |
| `subAccountId` | String | **Required** | RingCX sub-account ID. |

### Request Body

| Parameter | Type | Requirement | Description |
| --- | --- | --- | --- |
| `subscriptionName` | String | **Required** | Unique active subscription name for the sub-account. |
| `description` | String | Optional | Human-readable description. |
| `retryCount` | Integer | Optional | Maximum retry count. Defaults to `3` and cannot exceed `10`. |
| `notificationUrl` | String | **Required** | HTTP or HTTPS endpoint that receives agent-state notifications. |
| `authConfigId` | UUID | Optional | External auth configuration ID used when RingCX calls the receiver. |
| `customHeaders` | Object | Optional | Additional headers to send to the receiver. |
| `expiresAt` | Integer | Optional | Future epoch timestamp after which the subscription expires. Use `0` or omit for no configured expiration. |

**Example Request:**

```json
{
  "subscriptionName": "WFM agent state feed",
  "description": "Agent state events for workforce management",
  "retryCount": 3,
  "notificationUrl": "https://example.com/ringcx/agent-states",
  "authConfigId": "2f8f8b6e-2a5c-4d8c-bd44-31db90a77b2a",
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

| Field | Type | Description |
| --- | --- | --- |
| `subscriptionId` | UUID | Unique subscription identifier. |
| `mainAccountId` | String | Main account that owns the sub-account. |
| `subAccountId` | String | RingCX sub-account receiving subscription events. |
| `subscriptionName` | String | Subscription display name. |
| `notificationUrl` | String | Receiver endpoint. |
| `authConfigId` | UUID | External auth configuration used for outbound notification authentication. |
| `active` | Boolean | Whether the subscription is active. |
| `maxRetryCount` | Integer | Maximum delivery retry count. |
| `customHeaders` | Object | Custom headers sent to the receiver. |
| `expiresAt` | Integer | Expiration epoch timestamp. |

## Receiver Payload

The subscription resource defines where RingCX sends agent-state events, but the event payload shape, signing/auth header behavior, retry backoff timing, and expected receiver response semantics were not discoverable in the public swagger or the accessible controller/service code. Confirm these details with RingCX engineering before publishing a receiver contract.

!!! info "Needs Engineering Confirmation"
    Before using this article as a public receiver implementation guide, confirm:

    * The HTTP method RingCX uses when calling `notificationUrl`.
    * The exact JSON payload for an agent-state change event.
    * Whether `authConfigId` controls outbound authentication, and how it is applied.
    * Whether `customHeaders` are sent with each event.
    * Which receiver status codes are treated as success.
    * Retry backoff timing and duplicate-delivery behavior.

Until those details are confirmed, design receivers to accept duplicate events and to log unknown fields rather than failing the whole request.

## Common Errors

| Status | Cause | Resolution |
| --- | --- | --- |
| `400 Bad Request` | Missing `subscriptionName`, invalid `notificationUrl`, retry count above `10`, or expired `expiresAt`. | Validate the request body before calling the API. |
| `403 Forbidden` | User lacks `WFO_ACCESS`. | Enable WFM/RTA access for the user. |
| `404 Not Found` | Invalid `authConfigId` or subscription ID. | Confirm the external auth configuration and subscription belong to the same sub-account. |
| `409 Conflict` | Active subscription name already exists for the sub-account. | List subscriptions first and update the existing subscription. |

## Sample Receiver (Python)

```python
from flask import Flask, request

app = Flask(__name__)
seen_events = set()

@app.post("/ringcx/agent-states")
def receive_agent_state():
    payload = request.get_json(force=True)
    event_id = payload.get("eventId") or payload.get("id")

    if event_id and event_id in seen_events:
        return ("", 204)
    if event_id:
        seen_events.add(event_id)

    # Store the raw event until the confirmed payload contract is published.
    print("received agent-state event", payload)
    return ("", 204)
```

## Operational Guidance

1. List subscriptions before creating a new one to avoid duplicate feeds.
2. Create one subscription per downstream integration endpoint.
3. Update the subscription when the receiver URL, credentials, or enabled state changes.
4. Delete subscriptions that are no longer monitored.
5. Monitor receiver health and compare delivery against [Real-Time Supervisor View](../analytics/reports/realtime-supervisor-view.md) snapshots when troubleshooting.

!!! important "Reliability"
    Design the receiving service to be idempotent. Network retries or downstream recovery can result in repeated state updates for the same agent transition.
