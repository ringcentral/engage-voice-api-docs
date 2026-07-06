# Lead Actions

Lead actions apply operational changes to one lead or a set of leads. Use them after locating the target leads with [lead search](search.md).

## Endpoint

```http
PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/actions?leadAction={leadAction}
Authorization: Bearer <ringcxAccessToken>
Content-Type: application/json
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

```http
PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/actions?leadAction=DELETE_LEADS
Authorization: Bearer <ringcxAccessToken>
Content-Type: application/json
```

```json
{
  "campaignLeadSearchCriteria": {
    "leadIds": [
      100000,
      100001
    ]
  }
}
```

## Move Leads to Another Campaign

Use `MOVE_TO_CAMPAIGN` when leads should be moved from one campaign to another campaign or lead list.

```http
PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/actions?leadAction=MOVE_TO_CAMPAIGN
Authorization: Bearer <ringcxAccessToken>
Content-Type: application/json
```

```json
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
