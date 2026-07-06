# Search Leads

Use the lead search APIs to find campaign leads by campaign, list, phone number, lead state, disposition, timezone, or custom lead fields.

## Search Endpoints

| Operation | Method and path |
| --- | --- |
| Search leads | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/leadSearch` |
| Search leads by phone list | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/leadSearchByPhoneList` |
| List lead states | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/leadStates` |
| List system dispositions | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/systemDispositions` |

## Search Leads

```http
POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/leadSearch
Authorization: Bearer <ringcxAccessToken>
Content-Type: application/json
```

```json
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

Use `campaignIds` when searching across more than one campaign. Use `campaignId` when the API operation or action expects a primary campaign context.

## Search by Phone Number

```http
POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/leadSearchByPhoneList
Authorization: Bearer <ringcxAccessToken>
Content-Type: application/json
```

```json
{
  "phoneList": [
    "4155550100",
    "4155550101"
  ],
  "campaignIds": [12345]
}
```

## Search Metadata

Use metadata endpoints to populate filters before building a search request.

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

## Results

The search response returns matching lead records and lead metadata. Use the returned lead IDs with [lead actions](actions.md) when you need to reset, suppress, move, email, or delete a set of leads.
