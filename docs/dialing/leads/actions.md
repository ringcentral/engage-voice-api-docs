# Lead Actions

Lead actions apply operational changes to one lead or a set of leads. Use them after locating the target leads with [lead search](search.md).

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

## Select Leads for an Action

Every lead action uses `campaignLeadSearchCriteria` to select the leads to update. Use narrow criteria, such as `leadIds`, `externIds`, `leadPhoneNumbers`, `campaignIds`, and `listIds`, when the action should target a known set of leads.

For bulk actions, run the same criteria against [lead search](search.md) first and confirm that the returned leads are the intended records. Then reuse the criteria with the action endpoint.

Actions that need extra values use `leadActionParams.paramMap`. The keys in `paramMap` are action-specific and are case-sensitive.

## Common Lead Actions

| Lead action | Use for | Required `paramMap` values |
| --- | --- | --- |
| `RESET_LEADS` | Reset pass count, set leads to ready, and make them eligible to dial again. | None |
| `CANCEL_LEADS` | Cancel leads so they are not dialed. | None |
| `DELETE_LEADS` | Permanently remove selected leads from the dialing list. | None |
| `PAUSE_LEADS` | Pause selected leads without using the cancel label. | None |
| `DIALER_REFRESH` | Refresh campaign lead cache state for matching campaigns. | Optional `force_dialer_cache_refresh` |
| `READY_LEADS` | Set selected leads to ready. | None |
| `MANUAL_LEADS` | Add a manual pass and update each selected lead based on the manual pass outcome. | `PASS_DISPOSITION`, `REQUEUE`, `DO_NOT_CALL`, `PASS_DELAY`, `MERGE_ORIGINAL` |
| `EMAIL_LEADS` | Email downloadable lead-search results. | `EMAIL_TO` |
| `CALLBACK_LEADS` | Set, reset, or cancel callbacks. | `ACTION_TYPE`; `RESERVATION_AGENT_ID` is required when `ACTION_TYPE` is `AGENT` |
| `MOVE_TO_CAMPAIGN` | Move or copy selected leads to another campaign or list. | `CAMPAIGN_ID`, `LIST_ID`, `DUPLICATE_ACTION_SETTING`, `CREATE_COPY_SETTING` |
| `AGENT_RESERVATION` | Reserve selected leads for an agent or clear an existing reservation. | `RESERVATION_AGENT_ID` |
| `SUPPRESS_LEADS` | Stop selected leads from dialing without changing their prior state. | None |
| `UNSUPPRESS_LEADS` | Remove suppression from selected leads. | None |

## Basic State Actions

Use the same request shape for `RESET_LEADS`, `CANCEL_LEADS`, `PAUSE_LEADS`, `READY_LEADS`, `SUPPRESS_LEADS`, and `UNSUPPRESS_LEADS`. Change only the `leadAction` query parameter and the search criteria.

```http
PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/actions?leadAction=READY_LEADS
Authorization: Bearer <ringcxAccessToken>
Content-Type: application/json

{
  "campaignLeadSearchCriteria": {
    "campaignIds": [12345],
    "listIds": [2222],
    "leadStates": ["PAUSED"]
  }
}
```

To suppress or unsuppress by phone number, use `leadPhoneNumbers`:

```json
{
  "campaignLeadSearchCriteria": {
    "campaignIds": [12345],
    "leadPhoneNumbers": [
      "4155550100",
      "4155550101"
    ]
  }
}
```

## Callback Leads

Use `CALLBACK_LEADS` to set an agent callback, cancel callbacks, or reset callback leads to ready.

| `ACTION_TYPE` | Use for | Additional values |
| --- | --- | --- |
| `AGENT` | Create agent callbacks for the selected leads. | `RESERVATION_AGENT_ID`; optional `CALLBACK_DATE` |
| `CANCEL` | Cancel callbacks for the selected leads. | None |
| `RESET` | Clear callback state and set the selected leads to ready. | None |

```http
PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/actions?leadAction=CALLBACK_LEADS
Authorization: Bearer <ringcxAccessToken>
Content-Type: application/json

{
  "campaignLeadSearchCriteria": {
    "campaignIds": [12345],
    "leadIds": [100000]
  },
  "leadActionParams": {
    "paramMap": {
      "ACTION_TYPE": "AGENT",
      "RESERVATION_AGENT_ID": 9001,
      "CALLBACK_DATE": "2026-07-24T16:00:00.000+0000"
    }
  }
}
```

## Agent Reservation

Use `AGENT_RESERVATION` to reserve leads for a specific agent. Set `RESERVATION_AGENT_ID` to `0` to clear the reservation.

```json
{
  "campaignLeadSearchCriteria": {
    "campaignIds": [12345],
    "leadIds": [100000, 100001]
  },
  "leadActionParams": {
    "paramMap": {
      "RESERVATION_AGENT_ID": 9001
    }
  }
}
```

## Manual Lead Pass

Use `MANUAL_LEADS` when an external workflow should record a manual pass result for selected leads.

| Parameter | Description |
| --- | --- |
| `PASS_DISPOSITION` | Agent disposition text to record with the manual pass. |
| `REQUEUE` | Set to `true` to make the lead ready again after `PASS_DELAY` minutes. |
| `DO_NOT_CALL` | Set to `true` to mark the lead do-not-call and add the selected phone or external ID to DNC according to the search criteria. |
| `PASS_DELAY` | Number of minutes before a requeued lead becomes available. Use `0` when no delay is needed. |
| `MERGE_ORIGINAL` | Set to `true` to merge the manual pass into the original lead when the lead is a copied or transitioned record. |

```json
{
  "campaignLeadSearchCriteria": {
    "campaignIds": [12345],
    "leadIds": [100000]
  },
  "leadActionParams": {
    "paramMap": {
      "PASS_DISPOSITION": "Interested",
      "REQUEUE": true,
      "DO_NOT_CALL": false,
      "PASS_DELAY": 60,
      "MERGE_ORIGINAL": false
    }
  }
}
```

## Email Lead Results

Use `EMAIL_LEADS` to email a downloadable export of lead search results.

```json
{
  "campaignLeadSearchCriteria": {
    "campaignIds": [12345],
    "listIds": [2222],
    "leadStates": ["READY"]
  },
  "leadActionParams": {
    "paramMap": {
      "EMAIL_TO": "ops@example.com"
    }
  }
}
```

## Refresh Dialer Cache

Use `DIALER_REFRESH` when campaign lead changes need to be reflected by the dialer. The optional `force_dialer_cache_refresh` value forces a lead-cache refresh for the selected campaign IDs.

```json
{
  "campaignLeadSearchCriteria": {
    "campaignIds": [12345]
  },
  "leadActionParams": {
    "paramMap": {
      "force_dialer_cache_refresh": true
    }
  }
}
```

## Delete Leads

=== "HTTP"

    ```http
    PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/actions?leadAction=DELETE_LEADS
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "campaignLeadSearchCriteria": {
        "campaignIds": [12345],
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
            "campaignIds": [12345],
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
        campaignIds: [12345],
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
        "campaignIds": [12345],
        "listIds": [],
        "leadStates": [],
        "agentDispositions": [],
        "systemDispositions": []
      },
      "leadActionParams": {
        "paramMap": {
          "CAMPAIGN_ID": 67890,
          "LIST_ID": 0,
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
            "campaignIds": [12345],
            "listIds": [],
            "leadStates": [],
            "agentDispositions": [],
            "systemDispositions": [],
        },
        "leadActionParams": {
            "paramMap": {
                "CAMPAIGN_ID": 67890,
                "LIST_ID": 0,
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
        campaignIds: [12345],
        listIds: [],
        leadStates: [],
        agentDispositions: [],
        systemDispositions: []
      },
      leadActionParams: {
        paramMap: {
          CAMPAIGN_ID: 67890,
          LIST_ID: 0,
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
          campaignIds: [12345],
          listIds: [],
          leadStates: [],
          agentDispositions: [],
          systemDispositions: []
        },
        leadActionParams: {
          paramMap: {
            CAMPAIGN_ID: 67890,
            LIST_ID: 0,
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
            "campaignIds": [12345],
            "listIds": [],
            "leadStates": [],
            "agentDispositions": [],
            "systemDispositions": [],
        },
        "leadActionParams": {
            "paramMap": {
                "CAMPAIGN_ID": 67890,
                "LIST_ID": 0,
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
| `CREATE_COPY_SETTING` | Use `false` to move the original lead, `true` to create a standard copy, or `TRANSITION` to create a transition copy. |
| `DUPLICATE_ACTION_SETTING` | Use `MOVE` to allow duplicates in the target list or `IGNORE` to leave duplicates in the original list. |

### Move Leads to an Existing List

To move leads into an existing lead list, first retrieve the target campaign's lists and identify the `listId` to use.

```http
GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns/{campaignId}/lists
Authorization: Bearer <ringcxAccessToken>
Accept: application/json
```

Then use that `listId` as `LIST_ID` in the `MOVE_TO_CAMPAIGN` action. Omit `LIST_NAME` because RingCX should use the existing list instead of creating a new one.

```json
{
  "leadActionParams": {
    "paramMap": {
      "CAMPAIGN_ID": 67890,
      "LIST_ID": 3333,
      "CREATE_COPY_SETTING": "false",
      "DUPLICATE_ACTION_SETTING": "MOVE"
    }
  }
}
```

## Safety

Actions such as `DELETE_LEADS`, `CANCEL_LEADS`, and `MOVE_TO_CAMPAIGN` can affect live dialing. Test search criteria first and confirm the selected leads before applying an action.
