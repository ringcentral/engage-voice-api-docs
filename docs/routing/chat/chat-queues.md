# Chat Queue APIs

The Chat Queue APIs let you configure and maintain digital queues in RingCX. Use them to provision chat queues, assign agents, configure queue-level dispositions and events, and connect queues to web chat widgets from an external system.

## Strategic Overview

Chat queues are the digital equivalent of voice queues. They control where inbound digital interactions wait, which agents can receive them, what outcomes agents can apply, and which widget routes traffic into the queue.

### Key Use Cases

* **Queue Provisioning:** Create and update chat queues as part of a repeatable rollout process across sub-accounts.
* **Agent Assignment Sync:** Keep queue membership aligned with an external workforce, identity, or scheduling system.
* **Digital Routing Configuration:** Configure dispositions, queue events, and schedules without manually editing every queue in the Admin portal.
* **Widget Routing:** Connect web chat widgets to the queues that should receive inbound digital conversations.

### Real-Time vs. Configuration APIs

These APIs update configuration, not active chat sessions. Changes such as assigning an agent or activating a queue are reflected in routing behavior after the platform processes the configuration update. For live queue and agent state, use the [Real-Time Supervisor View API](../../analytics/reports/realtime-supervisor-view.md).

### Required Permissions & Scopes

#### 1. Configure OAuth Scopes

To authenticate, your application must be configured with the following permission in the [Developer Portal](https://developers.ringcentral.com/my-account.html#/applications):

* **`ReadAccounts`**: Required to validate account context and authorize RingCX API calls.

!!! warning "Warning"
    `ReadAccounts` is the only OAuth scope that materially affects RingCX APIs. Platform permissions are managed through the RingCX Admin portal.

#### 2. Enable RingCX Admin Permissions

The authenticating user must have the relevant chat group, chat queue, and agent permissions in RingCX Admin. Common permission requirements include:

* `READ` on Chat Group or Chat Queue for list and get operations.
* `CREATE` on Chat Group for creating chat queues.
* `UPDATE` on Chat Queue for queue updates, assignments, dispositions, events, schedule overrides, and active-state changes.
* `READ` on Agents when assigning or listing queue agents.

## API Discovery

Chat queues belong to chat groups. Start by listing chat groups, then choose the `chatGroupId` that owns the queue.

`GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/chatGroups/withChildren`

**API Reference:** [List chat groups with children](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/getChatGroupListWithChildren)

### Query Parameters

| Parameter | Type | Requirement | Description |
| --- | --- | --- | --- |
| `accountId` | String | **Required** | RingCX sub-account ID. |
| `includePermissions` | Boolean | Optional | Include permission metadata when available. |
| `page` | Integer | Optional | Zero-indexed page number. |
| `maxRows` | Integer | Optional | Maximum records to return per page. |

The response returns chat groups with their related queues and skills. Use the group's `chatGroupId` in subsequent queue calls.

## Manage Chat Queues

### List Chat Queues

Returns the chat queues in a chat group.

`GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/chatGroups/{chatGroupId}/chatQueues`

**API Reference:** [List chat queues](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/listChatQueues)

| Parameter | Type | Requirement | Description |
| --- | --- | --- | --- |
| `accountId` | String | **Required** | RingCX sub-account ID. |
| `chatGroupId` | Integer | **Required** | Chat group ID. |
| `page` | Integer | Optional | Zero-indexed page number. |
| `maxRows` | Integer | Optional | Maximum records to return per page. |

### Create Chat Queue

Creates a new chat queue within a chat group.

`POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/chatGroups/{chatGroupId}/chatQueues`

**API Reference:** [Create chat queue](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/createChatQueue)

At minimum, provide a queue name and the settings required by your routing model. The full `ChatQueue` object includes many optional configuration fields because it mirrors Admin portal settings.

**Example Request:**

```json
{
  "chatQueueName": "Support Chat",
  "chatQueueDescription": "General support digital queue",
  "isActive": true,
  "queuePriority": 5,
  "maxQueueLimit": 50,
  "slaTime": 30,
  "agentWrapTime": 15
}
```

!!! note
    Per-agent concurrent chat capacity is set on the **Agent** record (`maxChats`), not on the queue. Use the [Agent API](https://developers.ringcentral.com/engage/voice/api-reference) to control how many chats a given agent can handle simultaneously.

### Get or Update a Chat Queue

Use the queue-specific endpoint when you need to read the full configuration for one queue or update queue settings.

`GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/chatGroups/{chatGroupId}/chatQueues/{chatQueueId}`

**API Reference:** [Get chat queue](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/getChatQueue)

`PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/chatGroups/{chatGroupId}/chatQueues/{chatQueueId}`

**API Reference:** [Update chat queue](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/updateChatQueue)

!!! important
    Treat update operations as full-object updates unless the API reference for a specific endpoint states otherwise. Read the current queue first, modify the fields you own, and send the updated object back.

### Activate or Deactivate a Queue

Use the active-state endpoint when you only need to change whether the queue can receive routed interactions.

`PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/chatGroups/{chatGroupId}/chatQueues/{chatQueueId}/setIsActive`

**API Reference:** [Set chat queue active state](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/setChatQueueIsActive)

## Assign Agents

Agent assignment determines which agents can receive interactions from the chat queue.

### Assign Agents to a Queue

`PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/chatGroups/{chatGroupId}/chatQueues/{chatQueueId}/assignAgents`

**API Reference:** [Assign agents to chat queue](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/assignAgentsToChatQueues)

**Example Request:**

```json
[
  {
    "agentId": 12345
  },
  {
    "agentId": 67890
  }
]
```

### List Assigned Agents

`GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/chatGroups/{chatGroupId}/chatQueues/{chatQueueId}/assignedAgents`

**API Reference:** [List assigned chat queue agents](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/getAgentsFromChatQueue)

### Unassign an Agent

`DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/chatGroups/{chatGroupId}/chatQueues/{chatQueueId}/unassignAgents/{agentId}`

**API Reference:** [Unassign agent from chat queue](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/unassignAgentFromChatQueue)

## Configure Dispositions

Dispositions let agents mark the outcome of a digital interaction. Use these endpoints when you need to keep chat outcomes synchronized with CRM or reporting taxonomies.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List dispositions | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/chatGroups/{chatGroupId}/chatQueues/{chatQueueId}/dispositions` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/getChatQueueDispositionList) |
| Create disposition | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/chatGroups/{chatGroupId}/chatQueues/{chatQueueId}/dispositions` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/createChatQueueDisposition) |
| Get disposition | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/chatGroups/{chatGroupId}/chatQueues/{chatQueueId}/dispositions/{dispositionId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/getChatQueueDisposition) |
| Update disposition | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/chatGroups/{chatGroupId}/chatQueues/{chatQueueId}/dispositions/{dispositionId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/updateChatQueueDisposition) |
| Delete disposition | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/chatGroups/{chatGroupId}/chatQueues/{chatQueueId}/dispositions/{dispositionId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/deleteChatQueueDisposition) |

## Configure Queue Events

Queue events define behavior that occurs while a digital interaction is waiting or being routed. Use these endpoints for repeatable event configuration across multiple queues.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List events | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/chatGroups/{chatGroupId}/chatQueues/{chatQueueId}/events` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/getChatQueueEventList) |
| Create event | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/chatGroups/{chatGroupId}/chatQueues/{chatQueueId}/events` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/createChatQueueEvent) |
| Get event | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/chatGroups/{chatGroupId}/chatQueues/{chatQueueId}/events/{eventId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/getChatQueueEvents) |
| Update event | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/chatGroups/{chatGroupId}/chatQueues/{chatQueueId}/events/{eventId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/updateChatQueueEvent) |
| Delete event | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/chatGroups/{chatGroupId}/chatQueues/{chatQueueId}/events/{eventId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/deleteChatQueueEvent) |

## Configure Schedule Overrides

Schedule overrides temporarily change queue availability without changing the queue's normal schedule. This is useful for holidays, emergency closures, or temporary staffing changes.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List overrides | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/chatGroups/{chatGroupId}/chatQueues/{chatQueueId}/scheduleOverrides` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/getChatQueueScheduleOverrides) |
| Create override | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/chatGroups/{chatGroupId}/chatQueues/{chatQueueId}/scheduleOverrides` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/createChatQueueScheduledOverride) |
| Save override list | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/chatGroups/{chatGroupId}/chatQueues/{chatQueueId}/scheduleOverrides` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/saveChatQueueScheduleOverrides) |
| Update override | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/chatGroups/{chatGroupId}/chatQueues/{chatQueueId}/scheduleOverrides/{scheduleOverrideId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/updateChatQueueScheduledOverride) |
| Delete override | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/chatGroups/{chatGroupId}/chatQueues/{chatQueueId}/scheduleOverrides/{scheduleOverrideId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/deleteChatQueueScheduledOverride) |

## Connect Chat Widgets

Chat widgets are configured under account utilities and can be assigned to queues. A common provisioning flow is:

1. List or create the widget.
2. List the queue that should receive widget traffic.
3. Create the widget-to-queue assignment.
4. Verify the assignment from either the widget or queue side.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List widgets | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/utilities/chatWidgets` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/listChatWidgets) |
| Create widget | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/utilities/chatWidgets` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/createChatWidget) |
| Get widget | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/utilities/chatWidgets/{widgetId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/getChatWidget) |
| Update widget | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/utilities/chatWidgets/{widgetId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/updateChatWidget) |
| Assign widget to queue | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/utilities/assignChatQueueChatWidget` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/createChatQueueWidgetAssignment) |
| List queue widgets | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/utilities/chatQueues/{chatQueueId}/chatWidgets` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Chat-Queues/listChatWidgetsForQueue) |

## Recommended Implementation Pattern

1. **Discover chat groups:** Call `chatGroups/withChildren` and choose the chat group that should own the queue.
2. **Create or update the queue:** Create a new queue, or read and update the existing queue configuration.
3. **Assign agents:** Assign the agents who should receive digital interactions from the queue.
4. **Configure outcomes and events:** Synchronize dispositions, queue events, and schedule overrides.
5. **Connect widgets:** Assign web chat widgets to the queue so customer conversations route correctly.
6. **Verify routing:** Use real-time reporting to confirm agents are staffed and queue activity appears as expected.

!!! important "Rate Limiting & Stability"
    Standard RingCX API rate limiting applies. For bulk provisioning, make changes in batches and implement exponential backoff on `429 Too Many Requests` responses.

## ChatQueue Response Schema

The `ChatQueue` definition is large because it mirrors the Admin portal. The fields most commonly read or written through the API are:

| Group | Fields | Description |
| --- | --- | --- |
| Identity | `chatQueueId`, `chatQueueName`, `chatQueueDescription`, `chatGroup` | Stable identifiers and display name. The owning chat group is returned as an embedded `chatGroup` object. |
| Routing state | `isActive`, `queuePriority`, `requeueType`, `maxQueueLimit`, `agentMaxAcceptTime` | Controls whether the queue can receive work and how work is prioritised. |
| Schedule | `monSched`, `tueSched`, `wedSched`, `thuSched`, `friSched`, `satSched`, `sunSched`, `observeDst` | Day-of-week schedules controlling normal availability. |
| Behaviour timers | `slaTime`, `shortChatTime`, `longChatTime`, `agentWrapTime`, `idleTimeout`, `dispTimeout` | Queue timers used by routing, reporting, and wrap-up workflows. |
| Wired services | `newChatHttpService`, `dequeueHttpService`, `agentConnectHttpService`, `agentTermHttpService`, `postDispHttpService`, `postChatHttpService` | Embedded `RemoteHttpService` references invoked at lifecycle events. |
| Permissions | `permissions` | Per-resource CRUD permissions for the authenticated user. |

**Example Response:**

```json
{
  "chatQueueId": 4567,
  "chatQueueName": "Support Chat",
  "chatQueueDescription": "General support digital queue",
  "isActive": true,
  "queuePriority": 5,
  "maxQueueLimit": 50,
  "slaTime": 30,
  "agentWrapTime": 15,
  "chatGroup": {
    "chatGroupId": 1234,
    "groupName": "Support"
  },
  "permissions": ["READ", "UPDATE"]
}
```

## Platform Permission Error

If the caller has the OAuth scope but lacks access to the chat group, queue, or agent assignment operation, the API can return a permission error similar to:

```json
{
  "errorCode": "access.denied.exception",
  "generalMessage": "You do not have permission to access this resource",
  "timestamp": 1611847650696
}
```

## Common Errors

| Status | Cause | Resolution |
| --- | --- | --- |
| `400 Bad Request` | Full-object update is missing fields that are required by the queue model. | Read the queue first and merge your changes into the full object before sending `PUT`. |
| `403 Forbidden` | Caller lacks access to the chat group, queue, or agent assignment. | Confirm Admin portal permissions for digital routing and agent management. |
| `404 Not Found` | Queue, group, disposition, event, widget, or agent ID does not exist under the account. | Re-list the parent resource immediately before changing children. |
| `409 Conflict` | Queue is inactive, already assigned, or has conflicting widget/agent state. | Verify queue status and existing assignments before retrying. |

## Sample Implementation (Python)

```python
import requests

BASE_URL = "https://ringcx.ringcentral.com/voice/api"

def assign_agents_to_chat_queue(token, account_id, chat_group_id, chat_queue_id, agent_ids):
    headers = {"Authorization": f"Bearer {token}"}

    assign_url = (
        f"{BASE_URL}/v1/admin/accounts/{account_id}/chatGroups/{chat_group_id}"
        f"/chatQueues/{chat_queue_id}/assignAgents"
    )
    response = requests.put(
        assign_url,
        headers=headers,
        json=[{"agentId": agent_id} for agent_id in agent_ids],
    )
    response.raise_for_status()

    list_url = (
        f"{BASE_URL}/v1/admin/accounts/{account_id}/chatGroups/{chat_group_id}"
        f"/chatQueues/{chat_queue_id}/assignedAgents"
    )
    return requests.get(list_url, headers=headers).json()
```
