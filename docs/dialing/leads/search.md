# Search Leads

Use the lead search APIs to find campaign leads by campaign, list, phone number, lead state, disposition, timezone, or custom lead fields.

## Search Endpoints

| Operation | Method and path |
| --- | --- |
| Search leads | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/leadSearch` |
| Search leads by phone list | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/leadSearchByPhoneList` |
| List lead states | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/leadStates` |
| List system dispositions | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/systemDispositions` |

SDK examples in this article use JWT authentication. Set `RC_CLIENT_ID`, `RC_CLIENT_SECRET`, and `RC_JWT` in your environment; the SDK wrapper handles the RingCentral login and RingCX token exchange. For JavaScript, install `ringcentral-engage-voice-client` and `dotenv`. For Python, install `ringcentral_engage_voice` and `python-dotenv`.

## Search Leads

=== "HTTP"

    ```http
    POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/leadSearch
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "campaignId": 12345,
      "campaignIds": [12345],
      "listIds": [],
      "leadStates": ["READY"],
      "agentDispositions": [],
      "systemDispositions": [],
      "physicalStates": ["CA"],
      "leadTimezones": []
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    access_token = "<ringcxAccessToken>"
    payload = {
        "campaignId": 12345,
        "campaignIds": [12345],
        "listIds": [],
        "leadStates": ["READY"],
        "agentDispositions": [],
        "systemDispositions": [],
        "physicalStates": ["CA"],
        "leadTimezones": [],
    }

    response = requests.post(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/campaignLeads/leadSearch",
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
      campaignId: 12345,
      campaignIds: [12345],
      listIds: [],
      leadStates: ["READY"],
      agentDispositions: [],
      systemDispositions: [],
      physicalStates: ["CA"],
      leadTimezones: []
    };

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/campaignLeads/leadSearch`,
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
        campaignId: 12345,
        campaignIds: [12345],
        listIds: [],
        leadStates: ["READY"],
        agentDispositions: [],
        systemDispositions: [],
        physicalStates: ["CA"],
        leadTimezones: []
      };

      const response = await ev.post(
        "/api/v1/admin/accounts/{accountId}/campaignLeads/leadSearch",
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
        "campaignId": 12345,
        "campaignIds": [12345],
        "listIds": [],
        "leadStates": ["READY"],
        "agentDispositions": [],
        "systemDispositions": [],
        "physicalStates": ["CA"],
        "leadTimezones": [],
    }

    response = ev.post(
        "/api/v1/admin/accounts/{accountId}/campaignLeads/leadSearch",
        payload,
    ).json()
    print(response)
    ```

Use `campaignIds` when searching across more than one campaign. Use `campaignId` when the API operation or action expects a primary campaign context.

## Search by Phone Number

=== "HTTP"

    ```http
    POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/leadSearchByPhoneList
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "phoneList": [
        "4155550100",
        "4155550101"
      ],
      "campaignIds": [12345]
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    access_token = "<ringcxAccessToken>"
    payload = {
        "phoneList": [
            "4155550100",
            "4155550101",
        ],
        "campaignIds": [12345],
    }

    response = requests.post(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/campaignLeads/leadSearchByPhoneList",
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
      phoneList: [
        "4155550100",
        "4155550101"
      ],
      campaignIds: [12345]
    };

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/campaignLeads/leadSearchByPhoneList`,
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

## Search Metadata

Use metadata endpoints to populate filters before building a search request.

=== "HTTP"

    ```http
    GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/leadStates
    Authorization: Bearer <ringcxAccessToken>
    Accept: application/json
    ```

    ```http
    GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/systemDispositions
    Authorization: Bearer <ringcxAccessToken>
    Accept: application/json
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    access_token = "<ringcxAccessToken>"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }

    lead_states = requests.get(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/campaignLeads/leadStates",
        headers=headers,
    )
    lead_states.raise_for_status()

    system_dispositions = requests.get(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/campaignLeads/systemDispositions",
        headers=headers,
    )
    system_dispositions.raise_for_status()

    print(lead_states.json())
    print(system_dispositions.json())
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const accessToken = "<ringcxAccessToken>";
    const headers = {
      Authorization: `Bearer ${accessToken}`,
      Accept: "application/json"
    };

    const leadStates = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/campaignLeads/leadStates`,
      { headers }
    );
    if (!leadStates.ok) throw new Error(await leadStates.text());

    const systemDispositions = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/campaignLeads/systemDispositions`,
      { headers }
    );
    if (!systemDispositions.ok) throw new Error(await systemDispositions.text());

    console.log(await leadStates.json());
    console.log(await systemDispositions.json());
    ```

## Results

The search response returns matching lead records and lead metadata. Use the returned lead IDs with [lead actions](actions.md) when you need to reset, suppress, move, email, or delete a set of leads.
