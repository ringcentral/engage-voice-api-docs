# Bulk Import Leads

Use the lead loader APIs to add leads to an outbound campaign. RingCX supports direct JSON loading and a preview/process flow for uploaded files.

## Find the Campaign

Before loading leads, identify the target campaign:

```http
GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups
Authorization: Bearer <ringcxAccessToken>
Accept: application/json
```

```http
GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns
Authorization: Bearer <ringcxAccessToken>
Accept: application/json
```

Use the returned `campaignId` in the lead loader path.

## Direct Lead Loading

Direct loading sends leads as JSON and is the simplest option when your integration already has structured lead data.

```http
POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaigns/{campaignId}/leadLoader/direct
Authorization: Bearer <ringcxAccessToken>
Content-Type: application/json
```

```json
{
  "description": "Renewal leads",
  "dialPriority": "NORMAL",
  "duplicateHandling": "REMOVE_FROM_LIST",
  "listState": "ACTIVE",
  "timeZoneOption": "NOT_APPLICABLE",
  "uploadLeads": [
    {
      "externId": "lead-1001",
      "leadPhone": "4155550100",
      "firstName": "Ada",
      "lastName": "Lovelace",
      "state": "CA"
    }
  ]
}
```

## File Preview and Process

For file-based imports, preview the file first so RingCX can identify columns and return mapping information. Then submit the process request with the selected mapping.

```http
POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaigns/{campaignId}/leadLoader/preview?fileType=COMMA
Authorization: Bearer <ringcxAccessToken>
Content-Type: multipart/form-data
```

```http
POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaigns/{campaignId}/leadLoader/process
Authorization: Bearer <ringcxAccessToken>
Content-Type: application/json
```

## Common Fields

| Field | Description |
| --- | --- |
| `description` | Name or description for the uploaded lead list. |
| `uploadLeads` | Array of lead records for direct loading. |
| `externId` | External lead identifier from your source system. |
| `leadPhone` | Primary lead phone number. |
| `leadPhoneE164` | E.164 primary phone number, when required for the account mode. |
| `duplicateHandling` | How RingCX handles duplicate leads during load. |
| `timeZoneOption` | How RingCX derives or applies lead time zones. |

## Persona Phone Leads

For strategic campaigns with multiple phone personas, add extra phone numbers in `personaPhoneConfig`. See [Lead Phone Persona Management](phone-persona-management.md) for the required campaign and phone-persona setup.
