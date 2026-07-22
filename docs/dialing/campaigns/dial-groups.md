# Dial Groups

Dial groups are outbound campaign containers. Agents assigned to a dial group can work campaigns that belong to that group. A dial group also defines dialing behavior such as preview or predictive dialing.

## Dial Modes

Use `PREVIEW` when agents should review lead information before placing a call. Use `PREDICTIVE` when RingCX should place outbound calls automatically and connect answered calls to available agents.

Agents can be assigned to multiple dial groups, but they actively dial from one dial group at a time.

## Manage Dial Groups

| Operation | Method and path |
| --- | --- |
| List dial groups | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups` |
| List dial groups with campaigns | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/withChildren` |
| Get dial group | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}` |
| Create dial group | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups` |
| Update dial group | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}` |
| Delete dial group | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}` |
| List assigned agents | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/assignedAgents` |
| Assign agents | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/assignAgents` |

SDK examples in this article use JWT authentication. Set `RC_CLIENT_ID`, `RC_CLIENT_SECRET`, and `RC_JWT` in your environment; the SDK wrapper handles the RingCentral login and RingCX token exchange. For JavaScript, install `ringcentral-engage-voice-client` and `dotenv`. For Python, install `ringcentral_engage_voice` and `python-dotenv`.

## Create a Dial Group

Only `dialGroupName` is required, but most integrations also set `dialMode` and `isActive`.

=== "HTTP"

    ```http
    POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "dialGroupName": "Outbound Renewals",
      "dialGroupDesc": "Renewal outreach campaigns",
      "dialMode": "PREVIEW",
      "isActive": true
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    access_token = "<ringcxAccessToken>"
    payload = {
        "dialGroupName": "Outbound Renewals",
        "dialGroupDesc": "Renewal outreach campaigns",
        "dialMode": "PREVIEW",
        "isActive": True,
    }

    response = requests.post(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/dialGroups",
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
    const accessToken = "<ringcxAccessToken>";
    const payload = {
      dialGroupName: "Outbound Renewals",
      dialGroupDesc: "Renewal outreach campaigns",
      dialMode: "PREVIEW",
      isActive: true
    };

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/dialGroups`,
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
        dialGroupName: "Outbound Renewals",
        dialGroupDesc: "Renewal outreach campaigns",
        dialMode: "PREVIEW",
        isActive: true
      };

      const response = await ev.post(
        "/api/v1/admin/accounts/{accountId}/dialGroups",
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
        "dialGroupName": "Outbound Renewals",
        "dialGroupDesc": "Renewal outreach campaigns",
        "dialMode": "PREVIEW",
        "isActive": True,
    }

    response = ev.post(
        "/api/v1/admin/accounts/{accountId}/dialGroups",
        payload,
    ).json()
    print(response)
    ```

??? example "Response example"

    ```json
    {
      "dialGroupId": 115793,
      "dialGroupName": "Outbound Renewals",
      "dialGroupDesc": "Renewal outreach campaigns",
      "dialMode": "PREVIEW",
      "isActive": true,
      "maxLeadsReturned": 1,
      "agentDialGroupMembers": [],
      "permissions": []
    }
    ```

### Common Fields

| Field | Required | Description |
| --- | --- | --- |
| `dialGroupName` | Yes | Display name for the dial group. |
| `dialGroupDesc` | No | Short description of the dial group. |
| `dialMode` | No | Dialing mode, such as `PREVIEW` or `PREDICTIVE`. |
| `isActive` | No | Whether agents can actively use the dial group. |
| `enableAgentFilter` | No | Allows leads reserved for a specific agent to be dialed by that agent. |
| `allowLeadSearch` | No | Allows agents to search campaign leads from the dialer. |
| `maxLeadsReturned` | No | Maximum number of preview leads returned to an agent. |

## Retrieve Dial Groups

=== "HTTP"

    ```http
    GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/withChildren
    Authorization: Bearer <ringcxAccessToken>
    Accept: application/json
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    access_token = "<ringcxAccessToken>"

    response = requests.get(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/dialGroups/withChildren",
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
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/dialGroups/withChildren`,
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

      const response = await ev.get("/api/v1/admin/accounts/{accountId}/dialGroups/withChildren");
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

    response = ev.get("/api/v1/admin/accounts/{accountId}/dialGroups/withChildren").json()
    print(response)
    ```

Use `withChildren` when you need campaign IDs along with the dial group. Use `GET /dialGroups/{dialGroupId}` when you already know the dial group ID.

??? example "Response example"

    ```json
    [
      {
        "dialGroupId": 115793,
        "dialGroupName": "Outbound Renewals",
        "dialGroupDesc": "Renewal outreach campaigns",
        "dialMode": "PREVIEW",
        "isActive": true,
        "campaigns": [
          {
            "campaignId": 136785,
            "campaignName": "Renewal Outreach",
            "isActive": 1
          }
        ],
        "permissions": []
      }
    ]
    ```

## Update a Dial Group

Retrieve the dial group first, update the fields you need to change, and submit the updated object with `PUT`.

=== "HTTP"

    ```http
    PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "dialGroupId": 12345,
      "dialGroupName": "Outbound Renewals",
      "dialGroupDesc": "Renewal and win-back campaigns",
      "dialMode": "PREVIEW",
      "isActive": true
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    dial_group_id = "<dialGroupId>"
    access_token = "<ringcxAccessToken>"
    payload = {
        "dialGroupId": 12345,
        "dialGroupName": "Outbound Renewals",
        "dialGroupDesc": "Renewal and win-back campaigns",
        "dialMode": "PREVIEW",
        "isActive": True,
    }

    response = requests.put(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/dialGroups/{dial_group_id}",
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
    const dialGroupId = "<dialGroupId>";
    const accessToken = "<ringcxAccessToken>";
    const payload = {
      dialGroupId: 12345,
      dialGroupName: "Outbound Renewals",
      dialGroupDesc: "Renewal and win-back campaigns",
      dialMode: "PREVIEW",
      isActive: true
    };

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/dialGroups/${dialGroupId}`,
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
        dialGroupId: 12345,
        dialGroupName: "Outbound Renewals",
        dialGroupDesc: "Renewal and win-back campaigns",
        dialMode: "PREVIEW",
        isActive: true
      };

      const response = await ev.put(
        "/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}",
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
        "dialGroupId": 12345,
        "dialGroupName": "Outbound Renewals",
        "dialGroupDesc": "Renewal and win-back campaigns",
        "dialMode": "PREVIEW",
        "isActive": True,
    }

    response = ev.put(
        "/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}",
        payload,
    ).json()
    print(response)
    ```

??? example "Response example"

    ```json
    {
      "dialGroupId": 115793,
      "dialGroupName": "Outbound Renewals",
      "dialGroupDesc": "Renewal and win-back campaigns",
      "dialMode": "PREVIEW",
      "isActive": true,
      "allowLeadSearch": "YES",
      "maxLeadsReturned": 1,
      "agentDialGroupMembers": [],
      "permissions": []
    }
    ```

## Assign Agents

Assign agents after creating the dial group and enabling outbound calling for those agents.

=== "HTTP"

    ```http
    PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/assignAgents
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    dial_group_id = "<dialGroupId>"
    access_token = "<ringcxAccessToken>"

    response = requests.put(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/dialGroups/{dial_group_id}/assignAgents",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
    )
    response.raise_for_status()
    print(response.json())
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const dialGroupId = "<dialGroupId>";
    const accessToken = "<ringcxAccessToken>";

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/dialGroups/${dialGroupId}/assignAgents`,
      {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json"
        }
      }
    );

    if (!response.ok) throw new Error(await response.text());
    console.log(await response.json());
    ```

The request body is the agent-assignment payload for the dial group. Use the assigned-agents endpoint to verify the result.

=== "HTTP"

    ```http
    GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/assignedAgents
    Authorization: Bearer <ringcxAccessToken>
    Accept: application/json
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    dial_group_id = "<dialGroupId>"
    access_token = "<ringcxAccessToken>"

    response = requests.get(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/dialGroups/{dial_group_id}/assignedAgents",
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
    const dialGroupId = "<dialGroupId>";
    const accessToken = "<ringcxAccessToken>";

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/dialGroups/${dialGroupId}/assignedAgents`,
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
