# Lead Actions

Lead actions apply operational changes to one lead or a set of leads. Use them after locating the target leads with [lead search](search.md).

SDK examples in this article use JWT authentication. Set `RC_CLIENT_ID`, `RC_CLIENT_SECRET`, and `RC_JWT` in your environment; the SDK wrapper handles the RingCentral login and RingCX token exchange. For JavaScript, install `ringcentral-engage-voice-client` and `dotenv`. For Python, install `ringcentral_engage_voice` and `python-dotenv`.

## Endpoint

=== "HTTP"

    ```http
    PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/actions?leadAction={leadAction}
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    lead_action = "<leadAction>"
    access_token = "<ringcxAccessToken>"

    response = requests.put(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/campaignLeads/actions",
        params={"leadAction": lead_action},
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        json={},
    )
    response.raise_for_status()
    print(response.json())
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const leadAction = "<leadAction>";
    const accessToken = "<ringcxAccessToken>";

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/campaignLeads/actions?leadAction=${leadAction}`,
      {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({})
      }
    );

    if (!response.ok) throw new Error(await response.text());
    console.log(await response.json());
    ```

## Common Lead Actions

| Lead action | Use for |
| --- | --- |
| `RESET_LEADS` | Reset pass count, set leads to ready, and make them eligible to dial again. |
| `CANCEL_LEADS` | Cancel leads so they are not dialed. |
| `DELETE_LEADS` | Permanently remove selected leads from the dialing list. |
| `PAUSE_LEADS` | Pause selected leads without using the cancel label. |
| `READY_LEADS` | Set selected leads to ready. |
| `MANUAL_LEADS` | Add a manual pass and agent disposition update. |
| `EMAIL_LEADS` | Email downloadable lead-search results. |
| `CALLBACK_LEADS` | Set or cancel callbacks. |
| `MOVE_TO_CAMPAIGN` | Move selected leads to another campaign or list. |
| `AGENT_RESERVATION` | Set or cancel agent-specific reservation. |
| `SUPPRESS_LEADS` | Stop selected leads from dialing without changing their prior state. |
| `UNSUPPRESS_LEADS` | Remove suppression from selected leads. |

## Delete Leads

=== "HTTP"

    ```http
    PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/actions?leadAction=DELETE_LEADS
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "campaignLeadSearchCriteria": {
        "leadIds": [
          100000,
          100001
        ]
      }
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    access_token = "<ringcxAccessToken>"
    payload = {
        "campaignLeadSearchCriteria": {
            "leadIds": [
                100000,
                100001,
            ]
        }
    }

    response = requests.put(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/campaignLeads/actions",
        params={"leadAction": "DELETE_LEADS"},
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
      campaignLeadSearchCriteria: {
        leadIds: [
          100000,
          100001
        ]
      }
    };

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/campaignLeads/actions?leadAction=DELETE_LEADS`,
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

## Move Leads to Another Campaign

Use `MOVE_TO_CAMPAIGN` when leads should be moved from one campaign to another campaign or lead list.

=== "HTTP"

    ```http
    PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/actions?leadAction=MOVE_TO_CAMPAIGN
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "campaignLeadSearchCriteria": {
        "campaignId": 12345,
        "campaignIds": [12345],
        "listIds": [],
        "leadStates": [],
        "agentDispositions": [],
        "systemDispositions": []
      },
      "leadActionParams": {
        "paramMap": {
          "CAMPAIGN_ID": "67890",
          "LIST_ID": "0",
          "LIST_NAME": "Moved Leads",
          "CREATE_COPY_SETTING": "false",
          "DUPLICATE_ACTION_SETTING": "MOVE"
        }
      }
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    access_token = "<ringcxAccessToken>"
    payload = {
        "campaignLeadSearchCriteria": {
            "campaignId": 12345,
            "campaignIds": [12345],
            "listIds": [],
            "leadStates": [],
            "agentDispositions": [],
            "systemDispositions": [],
        },
        "leadActionParams": {
            "paramMap": {
                "CAMPAIGN_ID": "67890",
                "LIST_ID": "0",
                "LIST_NAME": "Moved Leads",
                "CREATE_COPY_SETTING": "false",
                "DUPLICATE_ACTION_SETTING": "MOVE",
            }
        },
    }

    response = requests.put(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/campaignLeads/actions",
        params={"leadAction": "MOVE_TO_CAMPAIGN"},
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
      campaignLeadSearchCriteria: {
        campaignId: 12345,
        campaignIds: [12345],
        listIds: [],
        leadStates: [],
        agentDispositions: [],
        systemDispositions: []
      },
      leadActionParams: {
        paramMap: {
          CAMPAIGN_ID: "67890",
          LIST_ID: "0",
          LIST_NAME: "Moved Leads",
          CREATE_COPY_SETTING: "false",
          DUPLICATE_ACTION_SETTING: "MOVE"
        }
      }
    };

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/campaignLeads/actions?leadAction=MOVE_TO_CAMPAIGN`,
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
        campaignLeadSearchCriteria: {
          campaignId: 12345,
          campaignIds: [12345],
          listIds: [],
          leadStates: [],
          agentDispositions: [],
          systemDispositions: []
        },
        leadActionParams: {
          paramMap: {
            CAMPAIGN_ID: "67890",
            LIST_ID: "0",
            LIST_NAME: "Moved Leads",
            CREATE_COPY_SETTING: "false",
            DUPLICATE_ACTION_SETTING: "MOVE"
          }
        }
      };

      const response = await ev.put(
        "/api/v1/admin/accounts/{accountId}/campaignLeads/actions?leadAction=MOVE_TO_CAMPAIGN",
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
        "campaignLeadSearchCriteria": {
            "campaignId": 12345,
            "campaignIds": [12345],
            "listIds": [],
            "leadStates": [],
            "agentDispositions": [],
            "systemDispositions": [],
        },
        "leadActionParams": {
            "paramMap": {
                "CAMPAIGN_ID": "67890",
                "LIST_ID": "0",
                "LIST_NAME": "Moved Leads",
                "CREATE_COPY_SETTING": "false",
                "DUPLICATE_ACTION_SETTING": "MOVE",
            }
        },
    }

    response = ev.put(
        "/api/v1/admin/accounts/{accountId}/campaignLeads/actions?leadAction=MOVE_TO_CAMPAIGN",
        payload,
    ).json()
    print(response)
    ```

### Move Parameters

| Parameter | Description |
| --- | --- |
| `CAMPAIGN_ID` | Target campaign ID. |
| `LIST_ID` | Target list ID. Use `0` when creating a new list. |
| `LIST_NAME` | Name for the new list when `LIST_ID` is `0`. |
| `CREATE_COPY_SETTING` | Whether to copy instead of move the original lead. |
| `DUPLICATE_ACTION_SETTING` | How to handle duplicates in the target list. |

## Safety

Actions such as `DELETE_LEADS`, `CANCEL_LEADS`, and `MOVE_TO_CAMPAIGN` can affect live dialing. Test search criteria first and confirm the selected leads before applying an action.
