# Agent Groups

Agent groups organize agents into administrative groups. An agent must belong to an agent group before you can create or manage that agent through the Agents API.

## Manage Agent Groups

| Operation | Method and path |
| --- | --- |
| List agent groups | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups` |
| Get agent group | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}` |
| Create agent group | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups` |
| Update agent group | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}` |
| Delete agent group | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}` |

## Create an Agent Group

Only `groupName` is required when creating an agent group.

=== "HTTP"

    ```http
    POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "groupName": "Support Agents"
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    access_token = "<ringcxAccessToken>"

    response = requests.post(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/agentGroups",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        json={"groupName": "Support Agents"},
    )
    response.raise_for_status()
    print(response.json())
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const accessToken = "<ringcxAccessToken>";

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/agentGroups`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ groupName: "Support Agents" })
      }
    );

    if (!response.ok) throw new Error(await response.text());
    console.log(await response.json());
    ```

### Common Fields

| Field | Required | Description |
| --- | --- | --- |
| `groupName` | Yes | Display name for the agent group. |
| `agentGroupId` | No | Agent group ID. If omitted during create, RingCX assigns an ID. |
| `isDefault` | No | Whether the group is the default agent group. |

## Retrieve Agent Groups

=== "HTTP"

    ```http
    GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups
    Authorization: Bearer <ringcxAccessToken>
    Accept: application/json
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    access_token = "<ringcxAccessToken>"

    response = requests.get(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/agentGroups",
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
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/agentGroups`,
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

Use the returned `agentGroupId` when creating agents.

## Update an Agent Group

Retrieve the agent group first, update the fields you need to change, and submit the updated object with `PUT`.

=== "HTTP"

    ```http
    PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "agentGroupId": 1950,
      "groupName": "Support Agents - Updated",
      "isDefault": false
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    agent_group_id = "<agentGroupId>"
    access_token = "<ringcxAccessToken>"
    payload = {
        "agentGroupId": 1950,
        "groupName": "Support Agents - Updated",
        "isDefault": False,
    }

    response = requests.put(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/agentGroups/{agent_group_id}",
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
    const agentGroupId = "<agentGroupId>";
    const accessToken = "<ringcxAccessToken>";
    const payload = {
      agentGroupId: 1950,
      groupName: "Support Agents - Updated",
      isDefault: false
    };

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/agentGroups/${agentGroupId}`,
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

## Delete an Agent Group

=== "HTTP"

    ```http
    DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}
    Authorization: Bearer <ringcxAccessToken>
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    agent_group_id = "<agentGroupId>"
    access_token = "<ringcxAccessToken>"

    response = requests.delete(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/agentGroups/{agent_group_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response.raise_for_status()
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const agentGroupId = "<agentGroupId>";
    const accessToken = "<ringcxAccessToken>";

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/agentGroups/${agentGroupId}`,
      {
        method: "DELETE",
        headers: { Authorization: `Bearer ${accessToken}` }
      }
    );

    if (!response.ok) throw new Error(await response.text());
    ```

Delete an agent group only after moving or deleting the agents that belong to it.
