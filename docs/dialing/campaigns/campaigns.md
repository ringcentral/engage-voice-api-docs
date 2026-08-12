# Campaigns

Campaigns organize outbound dialing work inside a dial group. A campaign defines who to call, when to call, which caller ID to use, and how leads move through outbound states and dispositions.

Create a [dial group](dial-groups.md) before creating campaigns.

## Manage Campaigns

| Operation | Method and path |
| --- | --- |
| List campaigns in a dial group | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns` |
| Get campaign | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns/{campaignId}` |
| Create campaign | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns` |
| Update campaign | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns/{campaignId}` |
| Delete campaign | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns/{campaignId}` |
| Clear campaign cache | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns/{campaignId}/clearCache` |

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

## Create a Campaign

Campaign configuration is broad. At minimum, set the campaign name and the dialing window fields that apply to your workflow.

=== "HTTP"

    ```http
    POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "campaignName": "Renewal Outreach",
      "campaignDesc": "Outbound renewal reminders",
      "isActive": 1,
      "startDate": "2026-07-01T07:00:00.000+0000",
      "endDate": "2026-12-31T07:00:00.000+0000",
      "callerId": "4155550123",
      "monSched": "08001700",
      "tueSched": "08001700",
      "wedSched": "08001700",
      "thuSched": "08001700",
      "friSched": "08001700",
      "satSched": "00000000",
      "sunSched": "00000000"
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    dial_group_id = "<dialGroupId>"
    access_token = "<ringcxAccessToken>"
    payload = {
        "campaignName": "Renewal Outreach",
        "campaignDesc": "Outbound renewal reminders",
        "isActive": 1,
        "startDate": "2026-07-01T07:00:00.000+0000",
        "endDate": "2026-12-31T07:00:00.000+0000",
        "callerId": "4155550123",
        "monSched": "08001700",
        "tueSched": "08001700",
        "wedSched": "08001700",
        "thuSched": "08001700",
        "friSched": "08001700",
        "satSched": "00000000",
        "sunSched": "00000000",
    }

    response = requests.post(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/dialGroups/{dial_group_id}/campaigns",
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
      campaignName: "Renewal Outreach",
      campaignDesc: "Outbound renewal reminders",
      isActive: 1,
      startDate: "2026-07-01T07:00:00.000+0000",
      endDate: "2026-12-31T07:00:00.000+0000",
      callerId: "4155550123",
      monSched: "08001700",
      tueSched: "08001700",
      wedSched: "08001700",
      thuSched: "08001700",
      friSched: "08001700",
      satSched: "00000000",
      sunSched: "00000000"
    };

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/dialGroups/${dialGroupId}/campaigns`,
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
        campaignName: "Renewal Outreach",
        campaignDesc: "Outbound renewal reminders",
        isActive: 1,
        startDate: "2026-07-01T07:00:00.000+0000",
        endDate: "2026-12-31T07:00:00.000+0000",
        callerId: "4155550123",
        monSched: "08001700",
        tueSched: "08001700",
        wedSched: "08001700",
        thuSched: "08001700",
        friSched: "08001700",
        satSched: "00000000",
        sunSched: "00000000"
      };

      const response = await ev.post(
        "/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns",
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
        "campaignName": "Renewal Outreach",
        "campaignDesc": "Outbound renewal reminders",
        "isActive": 1,
        "startDate": "2026-07-01T07:00:00.000+0000",
        "endDate": "2026-12-31T07:00:00.000+0000",
        "callerId": "4155550123",
        "monSched": "08001700",
        "tueSched": "08001700",
        "wedSched": "08001700",
        "thuSched": "08001700",
        "friSched": "08001700",
        "satSched": "00000000",
        "sunSched": "00000000",
    }

    response = ev.post(
        "/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns",
        payload,
    ).json()
    print(response)
    ```

??? example "Response example"

    ```json
    {
      "campaignId": 136785,
      "campaignName": "Renewal Outreach",
      "campaignDesc": "Outbound renewal reminders",
      "isActive": 1,
      "callerId": "4155550123",
      "startDate": "2026-07-01T07:00:00.000+0000",
      "endDate": "2026-12-31T07:00:00.000+0000",
      "dialGroup": {
        "id": 115793,
        "description": "Outbound Renewals"
      },
      "permissions": []
    }
    ```

### Common Fields

| Field | Description |
| --- | --- |
| `campaignName` | Display name for the campaign. |
| `campaignDesc` | Short description of the campaign. |
| `isActive` | Whether the campaign is active. |
| `startDate` / `endDate` | Campaign date range. |
| `callerId` | Caller ID used for outbound dialing. |
| `monSched` through `sunSched` | Daily calling windows. |
| `dialGroup` | Parent dial group reference, when returned by the API. |
| `callingConfiguration` | Calling configuration, such as strategic persona dialing when enabled. |

## Retrieve Campaigns

=== "HTTP"

    ```http
    GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns
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
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/dialGroups/{dial_group_id}/campaigns",
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
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/dialGroups/${dialGroupId}/campaigns`,
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
        "/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns"
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
        "/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns"
    ).json()
    print(response)
    ```

Use the returned `campaignId` for lead loading, lead search, lead actions, and campaign updates.

??? example "Response example"

    ```json
    [
      {
        "campaignId": 136785,
        "campaignName": "Renewal Outreach",
        "campaignDesc": "Outbound renewal reminders",
        "isActive": 1,
        "callerId": "4155550123",
        "dialGroup": {
          "id": 115793,
          "description": "Outbound Renewals"
        },
        "permissions": []
      }
    ]
    ```

## Update a Campaign

Retrieve the campaign first, update the fields you need to change, and submit the updated object with `PUT`.

=== "HTTP"

    ```http
    PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns/{campaignId}
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "campaignId": 67890,
      "campaignName": "Renewal Outreach",
      "campaignDesc": "Renewal and win-back reminders",
      "isActive": 1
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    dial_group_id = "<dialGroupId>"
    campaign_id = "<campaignId>"
    access_token = "<ringcxAccessToken>"
    payload = {
        "campaignId": 67890,
        "campaignName": "Renewal Outreach",
        "campaignDesc": "Renewal and win-back reminders",
        "isActive": 1,
    }

    response = requests.put(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/dialGroups/{dial_group_id}/campaigns/{campaign_id}",
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
    const campaignId = "<campaignId>";
    const accessToken = "<ringcxAccessToken>";
    const payload = {
      campaignId: 67890,
      campaignName: "Renewal Outreach",
      campaignDesc: "Renewal and win-back reminders",
      isActive: 1
    };

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/dialGroups/${dialGroupId}/campaigns/${campaignId}`,
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
        campaignId: 67890,
        campaignName: "Renewal Outreach",
        campaignDesc: "Renewal and win-back reminders",
        isActive: 1
      };

      const response = await ev.put(
        "/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns/{campaignId}",
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
        "campaignId": 67890,
        "campaignName": "Renewal Outreach",
        "campaignDesc": "Renewal and win-back reminders",
        "isActive": 1,
    }

    response = ev.put(
        "/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns/{campaignId}",
        payload,
    ).json()
    print(response)
    ```

??? example "Response example"

    ```json
    {
      "campaignId": 67890,
      "campaignName": "Renewal Outreach",
      "campaignDesc": "Renewal and win-back reminders",
      "isActive": 1,
      "dialGroup": {
        "id": 115793,
        "description": "Outbound Renewals"
      },
      "permissions": []
    }
    ```

## Lead Loading

After creating a campaign, load leads with the lead loader endpoints:

| Operation | Method and path |
| --- | --- |
| Direct lead load | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaigns/{campaignId}/leadLoader/direct` |
| Preview file mapping | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaigns/{campaignId}/leadLoader/preview` |
| Process previewed file | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaigns/{campaignId}/leadLoader/process` |

See [Bulk Import Leads](../leads/bulk-import.md) for lead-loading request examples.
