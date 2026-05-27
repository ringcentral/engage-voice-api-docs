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

Your application needs the `ReadAccounts` OAuth scope. The authenticating user must also have RingCX platform permissions for the target sub-account and WFM/integration access enabled.

## Subscription Lifecycle

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List subscriptions | `GET /voice/api/cx/integration/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/agent-states/subscriptions` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Agent-State-Subscriptions/getAllSubscriptions) |
| Create subscription | `POST /voice/api/cx/integration/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/agent-states/subscriptions` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Agent-State-Subscriptions/subscribe) |
| Update subscription | `PUT /voice/api/cx/integration/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/agent-states/subscriptions/{subscriptionId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Agent-State-Subscriptions/updateSubscription) |
| Delete subscription | `DELETE /voice/api/cx/integration/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/agent-states/subscriptions/{subscriptionId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Agent-State-Subscriptions/deleteSubscription) |

## Create a Subscription

`POST https://ringcx.ringcentral.com/voice/api/cx/integration/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/agent-states/subscriptions`

A subscription request identifies the target sub-account and the integration endpoint that should receive agent-state updates. Use a durable middleware endpoint that can authenticate incoming requests, retry safely, and tolerate duplicate delivery.

**Example Request:**

```json
{
  "name": "WFM agent state feed",
  "url": "https://example.com/ringcx/agent-states",
  "enabled": true
}
```

## Operational Guidance

1. List subscriptions before creating a new one to avoid duplicate feeds.
2. Create one subscription per downstream integration endpoint.
3. Update the subscription when the receiver URL, credentials, or enabled state changes.
4. Delete subscriptions that are no longer monitored.
5. Monitor receiver health and compare delivery against [Real-Time Supervisor View](../analytics/reports/realtime-supervisor-view.md) snapshots when troubleshooting.

!!! important "Reliability"
    Design the receiving service to be idempotent. Network retries or downstream recovery can result in repeated state updates for the same agent transition.
