# Group Skills

Group skills are queue-group-level skills that can be assigned to agents and used by queue routing. Create the [queue group](queue-groups.md) first, then create the group skills that belong to that queue group.

## Manage Group Skills

The API path uses `gateGroups` because queue groups are represented as gate groups in the API.

| Operation | Method and path |
| --- | --- |
| List group skills | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills` |
| Get group skill | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills/{skillId}` |
| Create group skill | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills` |
| Update group skills | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills` |
| Update one group skill | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills/{skillId}` |
| Delete group skill | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills/{skillId}` |

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

## Create a Group Skill

Create one group skill by sending a skill object.

=== "HTTP"

    ```http
    POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "skillName": "Spanish Language",
      "skillDesc": "Spanish-language support",
      "active": true
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    gate_group_id = "<gateGroupId>"
    access_token = "<ringcxAccessToken>"
    payload = {
        "skillName": "Spanish Language",
        "skillDesc": "Spanish-language support",
        "active": True,
    }

    response = requests.post(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/gateGroups/{gate_group_id}/skills",
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
      skillName: "Spanish Language",
      skillDesc: "Spanish-language support",
      active: true
    };

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/gateGroups/${gateGroupId}/skills`,
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
        skillName: "Spanish Language",
        skillDesc: "Spanish-language support",
        active: true
      };

      const response = await ev.post(
        "/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills",
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
        "skillName": "Spanish Language",
        "skillDesc": "Spanish-language support",
        "active": True,
    }

    response = ev.post(
        "/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills",
        payload,
    ).json()
    print(response)
    ```

??? example "Response example"

    ```json
    {
      "skillId": 1455,
      "skillName": "Spanish Language",
      "skillDesc": "Spanish-language support",
      "active": true
    }
    ```

### Common Fields

| Field | Required | Description |
| --- | --- | --- |
| `skillName` | Yes | Display name for the skill. |
| `skillDesc` | No | Short description of the skill. |
| `active` | No | Whether the skill is available for routing. |
| `skillId` | No | Group skill ID. Omit it when creating a new skill. |
| `whisperAudio` | No | Optional audio prompt played to the agent. |
| `agentSkillProfiles` | No | Agent skill profile associations. |
| `requeueShortcut` | No | Requeue shortcut association. |

## Retrieve Group Skills

=== "HTTP"

    ```http
    GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills
    Authorization: Bearer <ringcxAccessToken>
    Accept: application/json
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    gate_group_id = "<gateGroupId>"
    access_token = "<ringcxAccessToken>"

    response = requests.get(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/gateGroups/{gate_group_id}/skills",
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
    const gateGroupId = "<gateGroupId>";
    const accessToken = "<ringcxAccessToken>";

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/gateGroups/${gateGroupId}/skills`,
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
        "/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills"
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
        "/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills"
    ).json()
    print(response)
    ```

Use the returned `skillId` values when retrieving, updating, or deleting a single skill.

??? example "Response example"

    ```json
    [
      {
        "skillId": 1455,
        "skillName": "Spanish Language",
        "skillDesc": "Spanish-language support",
        "active": true
      }
    ]
    ```

## Update Group Skills

Retrieve the current skill object first, update the fields that should change, and submit the updated object. Use the collection endpoint for batch updates or the `{skillId}` endpoint for one skill.

=== "HTTP"

    ```http
    PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills/{skillId}
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "skillId": 1455,
      "skillName": "Spanish Language",
      "skillDesc": "Spanish-language support and billing questions",
      "active": true
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    gate_group_id = "<gateGroupId>"
    skill_id = "<skillId>"
    access_token = "<ringcxAccessToken>"
    payload = {
        "skillId": 1455,
        "skillName": "Spanish Language",
        "skillDesc": "Spanish-language support and billing questions",
        "active": True,
    }

    response = requests.put(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/gateGroups/{gate_group_id}/skills/{skill_id}",
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
    const skillId = "<skillId>";
    const accessToken = "<ringcxAccessToken>";
    const payload = {
      skillId: 1455,
      skillName: "Spanish Language",
      skillDesc: "Spanish-language support and billing questions",
      active: true
    };

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/gateGroups/${gateGroupId}/skills/${skillId}`,
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
        skillId: 1455,
        skillName: "Spanish Language",
        skillDesc: "Spanish-language support and billing questions",
        active: true
      };

      const response = await ev.put(
        "/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills/{skillId}",
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
        "skillId": 1455,
        "skillName": "Spanish Language",
        "skillDesc": "Spanish-language support and billing questions",
        "active": True,
    }

    response = ev.put(
        "/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills/{skillId}",
        payload,
    ).json()
    print(response)
    ```

??? example "Response example"

    ```json
    {
      "skillId": 1455,
      "skillName": "Spanish Language",
      "skillDesc": "Spanish-language support and billing questions",
      "active": true
    }
    ```

## Delete a Group Skill

=== "HTTP"

    ```http
    DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills/{skillId}
    Authorization: Bearer <ringcxAccessToken>
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    gate_group_id = "<gateGroupId>"
    skill_id = "<skillId>"
    access_token = "<ringcxAccessToken>"

    response = requests.delete(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/gateGroups/{gate_group_id}/skills/{skill_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response.raise_for_status()
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const gateGroupId = "<gateGroupId>";
    const skillId = "<skillId>";
    const accessToken = "<ringcxAccessToken>";

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/gateGroups/${gateGroupId}/skills/${skillId}`,
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
        "/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills/{skillId}"
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
        "/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills/{skillId}"
    )
    ```

Delete a group skill only after confirming it is no longer referenced by agent skill profiles or queue routing behavior.
