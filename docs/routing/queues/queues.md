# Queues

Queues are the inbound voice destinations that callers wait in until RingCX routes the call to an available agent. A queue belongs to a [queue group](queue-groups.md), and the API path uses the historical `gates` resource name for queues.

## Core Concepts

Create a queue group before creating queues. Then configure skills, queue events, schedules, dispositions, phone book entries, special ANI rules, and DNIS assignments as needed for the routing experience.

A queue must be active before RingCX routes callers to it. If a caller reaches an inactive or incorrectly configured queue, the caller may hear a disconnected or unavailable message instead of waiting for an agent.

Before testing inbound routing, make sure at least one agent has access to the queue, has permission to receive inbound calls, and has a high enough priority to receive the test call.

## Manage Queues

Use the following endpoints to create, list, retrieve, update, and delete queues.

| Operation | Method and path |
| --- | --- |
| List queues in a queue group | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates` |
| Get queue details | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}` |
| Create queue | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates` |
| Update queue | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}` |
| Delete queue | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}` |
| Set active state | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/setIsActive` |

## Create a Queue

Only `gateName` is required to create a queue. Most other queue settings can be added during create or updated later.

=== "HTTP"

    ```http
    POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "isActive": true,
      "gateName": "Support Queue",
      "gateDesc": "Inbound support calls",
      "gatePriority": 0,
      "outboundCallerId": "ani"
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    gate_group_id = "<gateGroupId>"
    access_token = "<ringcxAccessToken>"
    payload = {
        "isActive": True,
        "gateName": "Support Queue",
        "gateDesc": "Inbound support calls",
        "gatePriority": 0,
        "outboundCallerId": "ani",
    }

    response = requests.post(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/gateGroups/{gate_group_id}/gates",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        json=payload,
    )
    response.raise_for_status()
    print(response.json())
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const gateGroupId = "<gateGroupId>";
    const accessToken = "<ringcxAccessToken>";
    const payload = {
      isActive: true,
      gateName: "Support Queue",
      gateDesc: "Inbound support calls",
      gatePriority: 0,
      outboundCallerId: "ani"
    };

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/gateGroups/${gateGroupId}/gates`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      }
    );

    if (!response.ok) throw new Error(await response.text());
    console.log(await response.json());
    ```

### Common Fields

| Field | Required | Description |
| --- | --- | --- |
| `gateName` | Yes | Queue name shown in RingCX Admin. |
| `gateDesc` | No | Short description of the queue. |
| `isActive` | No | Whether RingCX can route callers to the queue. |
| `gatePriority` | No | Queue priority. Higher values receive routing priority over lower values. |
| `outboundCallerId` | No | Caller ID behavior for calls presented from the queue. |
| `recordCall` | No | Recording behavior for calls handled by the queue. |
| `shortAbandonTime` | No | Seconds before an abandoned call is treated as a short abandon. |
| `slaTime` | No | Service-level target in seconds. |
| `wrapTime` | No | Seconds before an agent becomes available after call completion. |
| `acceptTime` | No | Seconds an off-hook-disabled agent has to accept a queued call. |

## Retrieve Queues

Use the list response to discover queue IDs before retrieving or updating a specific queue.

=== "HTTP"

    ```http
    GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates
    Authorization: Bearer <ringcxAccessToken>
    Accept: application/json
    ```

    ```http
    GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}
    Authorization: Bearer <ringcxAccessToken>
    Accept: application/json
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    gate_group_id = "<gateGroupId>"
    gate_id = "<gateId>"
    access_token = "<ringcxAccessToken>"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }

    queues = requests.get(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/gateGroups/{gate_group_id}/gates",
        headers=headers,
    )
    queues.raise_for_status()

    queue = requests.get(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/gateGroups/{gate_group_id}/gates/{gate_id}",
        headers=headers,
    )
    queue.raise_for_status()

    print(queues.json())
    print(queue.json())
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const gateGroupId = "<gateGroupId>";
    const gateId = "<gateId>";
    const accessToken = "<ringcxAccessToken>";
    const headers = {
      Authorization: `Bearer ${accessToken}`,
      Accept: "application/json"
    };

    const queues = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/gateGroups/${gateGroupId}/gates`,
      { headers }
    );
    if (!queues.ok) throw new Error(await queues.text());

    const queue = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/gateGroups/${gateGroupId}/gates/${gateId}`,
      { headers }
    );
    if (!queue.ok) throw new Error(await queue.text());

    console.log(await queues.json());
    console.log(await queue.json());
    ```

## Update a Queue

Retrieve the queue first, update the fields you need to change, and submit the updated object with `PUT`.

=== "HTTP"

    ```http
    PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "gateId": 72992,
      "gateName": "Support Queue",
      "gateDesc": "Inbound support and account questions",
      "isActive": true,
      "gatePriority": 0
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    gate_group_id = "<gateGroupId>"
    gate_id = "<gateId>"
    access_token = "<ringcxAccessToken>"
    payload = {
        "gateId": 72992,
        "gateName": "Support Queue",
        "gateDesc": "Inbound support and account questions",
        "isActive": True,
        "gatePriority": 0,
    }

    response = requests.put(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/gateGroups/{gate_group_id}/gates/{gate_id}",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        json=payload,
    )
    response.raise_for_status()
    print(response.json())
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const gateGroupId = "<gateGroupId>";
    const gateId = "<gateId>";
    const accessToken = "<ringcxAccessToken>";
    const payload = {
      gateId: 72992,
      gateName: "Support Queue",
      gateDesc: "Inbound support and account questions",
      isActive: true,
      gatePriority: 0
    };

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/gateGroups/${gateGroupId}/gates/${gateId}`,
      {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      }
    );

    if (!response.ok) throw new Error(await response.text());
    console.log(await response.json());
    ```

## Related Queue Configuration

Queues are often configured with supporting resources:

| Resource | Use for |
| --- | --- |
| [Queue events](queue-events.md) | Hold music, wait behavior, DTMF options, and priority event handling. |
| [Group skills](group-skills.md) | Skills that can be assigned to agents and referenced by queue routing. |
| Queue dispositions | Outcomes agents can select after handling a queue call. |
| Phone book entries | Transfer destinations available from the queue. |
| Requeue shortcuts | Agent-facing shortcuts for transferring a call to another queue or skill. |
| Schedule overrides | Temporary open or closed behavior for the queue. |
| Special ANI rules | Caller-specific priority handling. |

## Supporting Lookup APIs

Use these endpoints when configuring queue fields that reference other resources.

| Lookup | Method and path |
| --- | --- |
| Dial groups and campaigns | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/withChildren` |
| Queue groups and queues | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/withChildren` |

## Delete a Queue

=== "HTTP"

    ```http
    DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}
    Authorization: Bearer <ringcxAccessToken>
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    gate_group_id = "<gateGroupId>"
    gate_id = "<gateId>"
    access_token = "<ringcxAccessToken>"

    response = requests.delete(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/gateGroups/{gate_group_id}/gates/{gate_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response.raise_for_status()
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const gateGroupId = "<gateGroupId>";
    const gateId = "<gateId>";
    const accessToken = "<ringcxAccessToken>";

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/gateGroups/${gateGroupId}/gates/${gateId}`,
      {
        method: "DELETE",
        headers: { Authorization: `Bearer ${accessToken}` }
      }
    );

    if (!response.ok) throw new Error(await response.text());
    ```

Delete a queue only after confirming that DNIS assignments, schedules, events, and agent access rules no longer depend on it.
