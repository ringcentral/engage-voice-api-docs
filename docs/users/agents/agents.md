# Agents

Agents are RingCX users who can log in to handle inbound queues, outbound campaigns, or supervisor workflows. Agents must belong to an [agent group](agent-groups.md).

## Manage Agents

| Operation | Method and path |
| --- | --- |
| List agents in an agent group | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents` |
| Get agent | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}` |
| Create agent | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents` |
| Update agents in an agent group | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents` |
| Update one agent | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}` |
| Delete agent | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}` |

## Create an Agent

Create the agent under the agent group that should own the agent record.

=== "HTTP"

    ```http
    POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "firstName": "Ada",
      "lastName": "Lovelace",
      "email": "ada@example.com",
      "username": "ada.lovelace",
      "password": "<temporaryPassword>",
      "agentType": "AGENT",
      "agentRank": 12,
      "allowInbound": true,
      "allowOutbound": true,
      "enableSoftphone": true,
      "maxChats": 0
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    agent_group_id = "<agentGroupId>"
    access_token = "<ringcxAccessToken>"
    payload = {
        "firstName": "Ada",
        "lastName": "Lovelace",
        "email": "ada@example.com",
        "username": "ada.lovelace",
        "password": "<temporaryPassword>",
        "agentType": "AGENT",
        "agentRank": 12,
        "allowInbound": True,
        "allowOutbound": True,
        "enableSoftphone": True,
        "maxChats": 0,
    }

    response = requests.post(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/agentGroups/{agent_group_id}/agents",
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
      firstName: "Ada",
      lastName: "Lovelace",
      email: "ada@example.com",
      username: "ada.lovelace",
      password: "<temporaryPassword>",
      agentType: "AGENT",
      agentRank: 12,
      allowInbound: true,
      allowOutbound: true,
      enableSoftphone: true,
      maxChats: 0
    };

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/agentGroups/${agentGroupId}/agents`,
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
| `username` | Yes | Agent login username. |
| `password` | Yes | Initial password when creating a direct-login agent. |
| `firstName` / `lastName` | No | Agent name. |
| `email` | No | Agent email address. |
| `externalAgentId` | No | External identifier used by your user-management system. |
| `agentType` | No | `AGENT` or `SUPERVISOR`. |
| `agentRank` | No | Routing rank. Higher rank values can receive higher priority. |
| `allowInbound` | No | Whether the agent can receive inbound calls. |
| `allowOutbound` | No | Whether the agent can make outbound calls. |
| `enableSoftphone` | No | Whether softphone login is enabled. |
| `defaultLoginDest` | No | Default login destination. |
| `phoneLoginPin` | No | PIN for phone login workflows. |

## Retrieve Agents

=== "HTTP"

    ```http
    GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents
    Authorization: Bearer <ringcxAccessToken>
    Accept: application/json
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    agent_group_id = "<agentGroupId>"
    access_token = "<ringcxAccessToken>"

    response = requests.get(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/agentGroups/{agent_group_id}/agents",
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
    const agentGroupId = "<agentGroupId>";
    const accessToken = "<ringcxAccessToken>";

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/agentGroups/${agentGroupId}/agents`,
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

Use the returned `agentId` when retrieving, updating, or deleting one agent.

=== "HTTP"

    ```http
    GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}
    Authorization: Bearer <ringcxAccessToken>
    Accept: application/json
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    agent_group_id = "<agentGroupId>"
    agent_id = "<agentId>"
    access_token = "<ringcxAccessToken>"

    response = requests.get(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/agentGroups/{agent_group_id}/agents/{agent_id}",
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
    const agentGroupId = "<agentGroupId>";
    const agentId = "<agentId>";
    const accessToken = "<ringcxAccessToken>";

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/agentGroups/${agentGroupId}/agents/${agentId}`,
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

## Update an Agent

Retrieve the agent first, update the fields you need to change, and submit the updated object with `PUT`.

=== "HTTP"

    ```http
    PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "agentId": 1234567,
      "firstName": "Ada",
      "lastName": "Lovelace",
      "username": "ada.lovelace",
      "agentType": "SUPERVISOR",
      "allowInbound": true,
      "allowOutbound": true,
      "isActive": true
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    agent_group_id = "<agentGroupId>"
    agent_id = "<agentId>"
    access_token = "<ringcxAccessToken>"
    payload = {
        "agentId": 1234567,
        "firstName": "Ada",
        "lastName": "Lovelace",
        "username": "ada.lovelace",
        "agentType": "SUPERVISOR",
        "allowInbound": True,
        "allowOutbound": True,
        "isActive": True,
    }

    response = requests.put(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/agentGroups/{agent_group_id}/agents/{agent_id}",
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
    const agentId = "<agentId>";
    const accessToken = "<ringcxAccessToken>";
    const payload = {
      agentId: 1234567,
      firstName: "Ada",
      lastName: "Lovelace",
      username: "ada.lovelace",
      agentType: "SUPERVISOR",
      allowInbound: true,
      allowOutbound: true,
      isActive: true
    };

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/agentGroups/${agentGroupId}/agents/${agentId}`,
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

## Supporting Lookup APIs

Use these endpoints to find IDs referenced by agent configuration.

| Lookup | Method and path |
| --- | --- |
| Agent groups | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups` |
| Dial groups | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/withChildren` |
| Queue groups and queues | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/withChildren` |
| Agent access to a queue | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/gateGroups/{gateGroupId}/gates/{gateId}` |

## Delete an Agent

=== "HTTP"

    ```http
    DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}
    Authorization: Bearer <ringcxAccessToken>
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    agent_group_id = "<agentGroupId>"
    agent_id = "<agentId>"
    access_token = "<ringcxAccessToken>"

    response = requests.delete(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/agentGroups/{agent_group_id}/agents/{agent_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response.raise_for_status()
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const agentGroupId = "<agentGroupId>";
    const agentId = "<agentId>";
    const accessToken = "<ringcxAccessToken>";

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/agentGroups/${agentGroupId}/agents/${agentId}`,
      {
        method: "DELETE",
        headers: { Authorization: `Bearer ${accessToken}` }
      }
    );

    if (!response.ok) throw new Error(await response.text());
    ```

Delete an agent only after confirming that the agent is no longer needed for queues, campaigns, reports, or supervisor workflows.
