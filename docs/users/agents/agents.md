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

SDK examples in this article use JWT authentication. Set `RC_CLIENT_ID`, `RC_CLIENT_SECRET`, and `RC_JWT` in your environment; the SDK wrapper handles the RingCentral login and RingCX token exchange. For JavaScript, install `ringcentral-engage-voice-client` and `dotenv`. For Python, install `ringcentral_engage_voice` and `python-dotenv`.

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
      "initLoginBaseState": "AVAILABLE",
      "initLoginBaseStateId": 11786,
      "ghostRnaAction": "AVAILABLE",
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
        "initLoginBaseState": "AVAILABLE",
        "initLoginBaseStateId": 11786,
        "ghostRnaAction": "AVAILABLE",
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
      initLoginBaseState: "AVAILABLE",
      initLoginBaseStateId: 11786,
      ghostRnaAction: "AVAILABLE",
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

=== "JavaScript SDK"

    ```javascript
    const EngageVoice = require("ringcentral-engage-voice-client").default;
    require("dotenv").config();

    async function main() {
      const ev = new EngageVoice({
        clientId: process.env.RC_CLIENT_ID,
        clientSecret: process.env.RC_CLIENT_SECRET
      });

      await ev.authorize({ jwt: process.env.RC_JWT });

      const payload = {
        firstName: "Ada",
        lastName: "Lovelace",
        email: "ada@example.com",
        username: "ada.lovelace",
        password: "<temporaryPassword>",
        agentType: "AGENT",
        agentRank: 12,
        initLoginBaseState: "AVAILABLE",
        initLoginBaseStateId: 11786,
        ghostRnaAction: "AVAILABLE",
        allowInbound: true,
        allowOutbound: true,
        enableSoftphone: true,
        maxChats: 0
      };

      const response = await ev.post(
        "/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents",
        payload
      );
      console.log(response.data);
    }

    main().catch(console.error);
    ```

=== "Python SDK"

    ```python
    import os
    from dotenv import load_dotenv
    from ringcentral_engage_voice import RingCentralEngageVoice

    load_dotenv()

    ev = RingCentralEngageVoice(
        os.environ["RC_CLIENT_ID"],
        os.environ["RC_CLIENT_SECRET"],
    )
    ev.authorize(jwt=os.environ["RC_JWT"])

    payload = {
        "firstName": "Ada",
        "lastName": "Lovelace",
        "email": "ada@example.com",
        "username": "ada.lovelace",
        "password": "<temporaryPassword>",
        "agentType": "AGENT",
        "agentRank": 12,
        "initLoginBaseState": "AVAILABLE",
        "initLoginBaseStateId": 11786,
        "ghostRnaAction": "AVAILABLE",
        "allowInbound": True,
        "allowOutbound": True,
        "enableSoftphone": True,
        "maxChats": 0,
    }

    response = ev.post(
        "/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents",
        payload,
    ).json()
    print(response)
    ```

??? example "Response example"

    ```json
    {
      "agentId": 1234567,
      "firstName": "Ada",
      "lastName": "Lovelace",
      "username": "ada.lovelace",
      "agentType": "AGENT",
      "agentRank": 12,
      "initLoginBaseState": "AVAILABLE",
      "initLoginBaseStateId": 11786,
      "allowInbound": true,
      "allowOutbound": true,
      "enableSoftphone": true,
      "maxChats": 0,
      "isActive": true
    }
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
| `initLoginBaseState` | No | Initial base state used when the agent logs in, such as `AVAILABLE`. |
| `initLoginBaseStateId` | No | Account aux-state ID for the agent's initial login state. |
| `ghostRnaAction` | No | State action used after a ghost RNA event. |
| `allowInbound` | No | Whether the agent can receive inbound calls. |
| `allowOutbound` | No | Whether the agent can make outbound calls. |
| `enableSoftphone` | No | Whether softphone login is enabled. |
| `defaultLoginDest` | No | Default login destination. |
| `phoneLoginPin` | No | PIN for phone login workflows. |

Use the account aux-states endpoint to find valid initial-state values. The response includes `stateId` and `agentAuxState`; use those values for `initLoginBaseStateId` and `initLoginBaseState`.

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

=== "JavaScript SDK"

    ```javascript
    const EngageVoice = require("ringcentral-engage-voice-client").default;
    require("dotenv").config();

    async function main() {
      const ev = new EngageVoice({
        clientId: process.env.RC_CLIENT_ID,
        clientSecret: process.env.RC_CLIENT_SECRET
      });

      await ev.authorize({ jwt: process.env.RC_JWT });

      const response = await ev.get(
        "/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents"
      );
      console.log(response.data);
    }

    main().catch(console.error);
    ```

=== "Python SDK"

    ```python
    import os
    from dotenv import load_dotenv
    from ringcentral_engage_voice import RingCentralEngageVoice

    load_dotenv()

    ev = RingCentralEngageVoice(
        os.environ["RC_CLIENT_ID"],
        os.environ["RC_CLIENT_SECRET"],
    )
    ev.authorize(jwt=os.environ["RC_JWT"])

    response = ev.get(
        "/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents"
    ).json()
    print(response)
    ```

Use the returned `agentId` when retrieving, updating, or deleting one agent.

??? example "Response example"

    ```json
    [
      {
        "agentId": 1234567,
        "firstName": "Ada",
        "lastName": "Lovelace",
        "username": "ada.lovelace",
        "agentType": "AGENT",
        "initLoginBaseState": "AVAILABLE",
        "initLoginBaseStateId": 11786,
        "allowInbound": true,
        "allowOutbound": true,
        "isActive": true
      }
    ]
    ```

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

=== "JavaScript SDK"

    ```javascript
    const EngageVoice = require("ringcentral-engage-voice-client").default;
    require("dotenv").config();

    async function main() {
      const ev = new EngageVoice({
        clientId: process.env.RC_CLIENT_ID,
        clientSecret: process.env.RC_CLIENT_SECRET
      });

      await ev.authorize({ jwt: process.env.RC_JWT });

      const response = await ev.get(
        "/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}"
      );
      console.log(response.data);
    }

    main().catch(console.error);
    ```

=== "Python SDK"

    ```python
    import os
    from dotenv import load_dotenv
    from ringcentral_engage_voice import RingCentralEngageVoice

    load_dotenv()

    ev = RingCentralEngageVoice(
        os.environ["RC_CLIENT_ID"],
        os.environ["RC_CLIENT_SECRET"],
    )
    ev.authorize(jwt=os.environ["RC_JWT"])

    response = ev.get(
        "/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}"
    ).json()
    print(response)
    ```

??? example "Response example"

    ```json
    {
      "agentId": 1234567,
      "firstName": "Ada",
      "lastName": "Lovelace",
      "username": "ada.lovelace",
      "agentType": "AGENT",
      "agentRank": 12,
      "initLoginBaseState": "AVAILABLE",
      "initLoginBaseStateId": 11786,
      "allowInbound": true,
      "allowOutbound": true,
      "enableSoftphone": true,
      "maxChats": 0,
      "isActive": true
    }
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

=== "JavaScript SDK"

    ```javascript
    const EngageVoice = require("ringcentral-engage-voice-client").default;
    require("dotenv").config();

    async function main() {
      const ev = new EngageVoice({
        clientId: process.env.RC_CLIENT_ID,
        clientSecret: process.env.RC_CLIENT_SECRET
      });

      await ev.authorize({ jwt: process.env.RC_JWT });

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

      const response = await ev.put(
        "/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}",
        payload
      );
      console.log(response.data);
    }

    main().catch(console.error);
    ```

=== "Python SDK"

    ```python
    import os
    from dotenv import load_dotenv
    from ringcentral_engage_voice import RingCentralEngageVoice

    load_dotenv()

    ev = RingCentralEngageVoice(
        os.environ["RC_CLIENT_ID"],
        os.environ["RC_CLIENT_SECRET"],
    )
    ev.authorize(jwt=os.environ["RC_JWT"])

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

    response = ev.put(
        "/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}",
        payload,
    ).json()
    print(response)
    ```

??? example "Response example"

    ```json
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

## Supporting Lookup APIs

Use these endpoints to find IDs referenced by agent configuration.

| Lookup | Method and path |
| --- | --- |
| Agent groups | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups` |
| Initial state and aux-state IDs | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/auxStates?activeOnly=true` |
| Dial groups | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/withChildren` |
| Queue groups and queues | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/withChildren` |
| Agent access to a queue | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/gateGroups/{gateGroupId}/gates/{gateId}` |

??? example "Aux-state response example"

    ```json
    [
      {
        "stateId": 11786,
        "agentAuxState": "AVAILABLE",
        "baseAgentState": {
          "colKey": "AVAILABLE"
        },
        "isActive": true
      }
    ]
    ```

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
