# Group Skills

Group skills are queue-group-level skills that can be assigned to agents and used by queue routing. Create the [queue group](queue-groups.md) first, then create the group skills that belong to that queue group.

## Manage Group Skills

The API path uses `gateGroups` because queue groups are represented as gate groups in the API.

| Operation | Method and path |
| --- | --- |
| List group skills | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills` |
| Get group skill | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills/{skillId}` |
| Create group skills | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills` |
| Update group skills | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills` |
| Update one group skill | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills/{skillId}` |
| Delete group skill | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills/{skillId}` |

## Create Group Skills

Create one or more group skills by sending an array of skill objects. To create a single skill, send an array with one object.

=== "HTTP"

    ```http
    POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    [
      {
        "skillName": "Spanish Language",
        "skillDesc": "Spanish-language support",
        "active": true
      },
      {
        "skillName": "French Language",
        "skillDesc": "French-language support",
        "active": true
      }
    ]
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    gate_group_id = "<gateGroupId>"
    access_token = "<ringcxAccessToken>"
    payload = [
        {
            "skillName": "Spanish Language",
            "skillDesc": "Spanish-language support",
            "active": True,
        },
        {
            "skillName": "French Language",
            "skillDesc": "French-language support",
            "active": True,
        },
    ]

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
    const payload = [
      {
        skillName: "Spanish Language",
        skillDesc: "Spanish-language support",
        active: true
      },
      {
        skillName: "French Language",
        skillDesc: "French-language support",
        active: true
      }
    ];

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

??? example "Response example"

    ```json
    [
      {
        "skillId": 1455,
        "skillName": "Spanish Language",
        "skillDesc": "Spanish-language support",
        "active": true
      },
      {
        "skillId": 1456,
        "skillName": "French Language",
        "skillDesc": "French-language support",
        "active": true
      }
    ]
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

Delete a group skill only after confirming it is no longer referenced by agent skill profiles or queue routing behavior.
