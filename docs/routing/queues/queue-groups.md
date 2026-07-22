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

=== "HTTP"

    ```http
    POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "groupName": "Support Queues"
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    access_token = "<ringcxAccessToken>"

    response = requests.post(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/gateGroups",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        json={"groupName": "Support Queues"},
    )
    response.raise_for_status()
    print(response.json())
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const accessToken = "<ringcxAccessToken>";

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/gateGroups`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ groupName: "Support Queues" })
      }
    );

    if (!response.ok) throw new Error(await response.text());
    console.log(await response.json());
    ```

??? example "Response example"

    ```json
    {
      "gateGroupId": 52653,
      "groupName": "Support Queues",
      "billingKey": null,
      "groupSkills": null,
      "permissions": []
    }
    ```

### Common Fields

| Field | Required | Description |
| --- | --- | --- |
| `groupName` | Yes | Display name for the queue group. |
| `billingKey` | No | Optional external billing or reporting key. |
| `gateGroupId` | No | Queue group ID. If omitted during create, RingCX assigns the next available ID. |

## Retrieve Queue Groups

=== "HTTP"

    ```http
    GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/withChildren
    Authorization: Bearer <ringcxAccessToken>
    Accept: application/json
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    access_token = "<ringcxAccessToken>"

    response = requests.get(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/gateGroups/withChildren",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        },
    )
    response.raise_for_status()
    print(response.json())
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const accessToken = "<ringcxAccessToken>";

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/gateGroups/withChildren`,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
          Accept: "application/json"
        }
      }
    );

    if (!response.ok) throw new Error(await response.text());
    console.log(await response.json());
    ```

Use `withChildren` when you need the group and its queues in one response. Use `GET /gateGroups/{gateGroupId}` when you already know the queue group ID and only need one group.

??? example "Response example"

    ```json
    [
      {
        "gateGroupId": 52653,
        "groupName": "Support Queues",
        "groupSkills": null,
        "permissions": []
      },
      {
        "gateGroupId": 52658,
        "groupName": "Escalation Queues",
        "groupSkills": null,
        "permissions": []
      }
    ]
    ```

## Update a Queue Group

Retrieve the queue group first, update the fields you need to change, and send the updated object back with `PUT`.

=== "HTTP"

    ```http
    PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "gateGroupId": 12345,
      "groupName": "Support Queues - Updated",
      "billingKey": "support"
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    gate_group_id = "<gateGroupId>"
    access_token = "<ringcxAccessToken>"
    payload = {
        "gateGroupId": 12345,
        "groupName": "Support Queues - Updated",
        "billingKey": "support",
    }

    response = requests.put(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/gateGroups/{gate_group_id}",
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
      gateGroupId: 12345,
      groupName: "Support Queues - Updated",
      billingKey: "support"
    };

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/gateGroups/${gateGroupId}`,
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

??? example "Response example"

    ```json
    {
      "gateGroupId": 52653,
      "groupName": "Support Queues - Updated",
      "billingKey": "support",
      "groupSkills": null,
      "permissions": []
    }
    ```

## Delete a Queue Group

=== "HTTP"

    ```http
    DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}
    Authorization: Bearer <ringcxAccessToken>
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    gate_group_id = "<gateGroupId>"
    access_token = "<ringcxAccessToken>"

    response = requests.delete(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/gateGroups/{gate_group_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response.raise_for_status()
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const gateGroupId = "<gateGroupId>";
    const accessToken = "<ringcxAccessToken>";

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/gateGroups/${gateGroupId}`,
      {
        method: "DELETE",
        headers: { Authorization: `Bearer ${accessToken}` }
      }
    );

    if (!response.ok) throw new Error(await response.text());
    ```

Delete a queue group only after confirming that queues, skills, schedules, and other routing configuration under the group are no longer needed.
