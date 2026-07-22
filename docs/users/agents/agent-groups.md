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

SDK examples in this article use JWT authentication. Set `RC_CLIENT_ID`, `RC_CLIENT_SECRET`, and `RC_JWT` in your environment; the SDK wrapper handles the RingCentral login and RingCX token exchange. For JavaScript, install `ringcentral-engage-voice-client` and `dotenv`. For Python, install `ringcentral_engage_voice` and `python-dotenv`.

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

      const response = await ev.post(
        "/api/v1/admin/accounts/{accountId}/agentGroups",
        { groupName: "Support Agents" }
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

    response = ev.post(
        "/api/v1/admin/accounts/{accountId}/agentGroups",
        {"groupName": "Support Agents"},
    ).json()
    print(response)
    ```

??? example "Response example"

    ```json
    {
      "agentGroupId": 1950,
      "groupName": "Support Agents",
      "isDefault": false
    }
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

      const response = await ev.get("/api/v1/admin/accounts/{accountId}/agentGroups");
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

    response = ev.get("/api/v1/admin/accounts/{accountId}/agentGroups").json()
    print(response)
    ```

Use the returned `agentGroupId` when creating agents.

??? example "Response example"

    ```json
    [
      {
        "agentGroupId": 1950,
        "groupName": "Support Agents",
        "isDefault": false
      },
      {
        "agentGroupId": 1951,
        "groupName": "Supervisors",
        "isDefault": false
      }
    ]
    ```

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
        agentGroupId: 1950,
        groupName: "Support Agents - Updated",
        isDefault: false
      };

      const response = await ev.put(
        "/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}",
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
        "agentGroupId": 1950,
        "groupName": "Support Agents - Updated",
        "isDefault": False,
    }

    response = ev.put(
        "/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}",
        payload,
    ).json()
    print(response)
    ```

??? example "Response example"

    ```json
    {
      "agentGroupId": 1950,
      "groupName": "Support Agents - Updated",
      "isDefault": false
    }
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
