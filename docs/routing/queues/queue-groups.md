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

## SDK Setup

SDK examples in this article use JWT authentication and load credentials from environment variables.

=== "JavaScript"

    ```bash
    npm install ringcentral-engage-voice-client dotenv
    ```

=== "Python"

    ```bash
    pip3 install ringcentral_engage_voice python-dotenv
    ```

Create a `.env` file in the directory where you run the sample:

```text
RC_CLIENT_ID=<clientId>
RC_CLIENT_SECRET=<clientSecret>
RC_JWT=<jwt>
```

The SDK wrapper reads these values, signs in with RingCentral, and exchanges the RingCentral access token for a RingCX access token before calling RingCX APIs.

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
        "/api/v1/admin/accounts/{accountId}/gateGroups",
        { groupName: "Support Queues" }
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
        "/api/v1/admin/accounts/{accountId}/gateGroups",
        {"groupName": "Support Queues"},
    ).json()
    print(response)
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

      const response = await ev.get("/api/v1/admin/accounts/{accountId}/gateGroups/withChildren");
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

    response = ev.get("/api/v1/admin/accounts/{accountId}/gateGroups/withChildren").json()
    print(response)
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
        gateGroupId: 12345,
        groupName: "Support Queues - Updated",
        billingKey: "support"
      };

      const response = await ev.put(
        "/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}",
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
        "gateGroupId": 12345,
        "groupName": "Support Queues - Updated",
        "billingKey": "support",
    }

    response = ev.put(
        "/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}",
        payload,
    ).json()
    print(response)
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

      await ev.delete(
        "/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}"
      );
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

    ev.delete(
        "/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}"
    )
    ```

Delete a queue group only after confirming that queues, skills, schedules, and other routing configuration under the group are no longer needed.
