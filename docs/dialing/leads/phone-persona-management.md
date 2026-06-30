# Lead Phone Persona Management

Lead phone persona management lets a strategic outbound campaign load and dial more than one phone number per lead. Instead of treating all numbers as one undifferentiated pipe-delimited `leadPhone` value, you can label each phone type, load lead-specific values for those labels, and configure which phone types should be dialed during each campaign calling window.

Use this feature when a campaign needs to try different phone numbers, such as mobile, home, or work, in a specific order based on the campaign's business hours.

## How It Works

A strategic campaign uses three related API areas:

| Area | Purpose |
|-|-|
| Persona phone configuration | Defines the account-level phone IDs and labels that can be used by strategic campaigns. |
| Campaign calling configuration | Enables strategic calling for a campaign and defines the time windows and phone-priority order. |
| Lead loading | Supplies the lead's phone numbers and maps each additional phone to a configured persona phone ID. |

The primary lead phone is always represented by phone ID `1`. Use phone IDs `2` through `7` for additional phone personas. Treat phone ID `1` as reserved for the lead's primary `leadPhone`.

## Prerequisites

Before you load persona-based phone numbers:

1. Create or identify the dial group that will contain the campaign.
2. Configure the persona phone labels for the account.
3. Create the campaign with `callingConfiguration` set to `STRATEGIC`.
4. Add `personaCallSchedules` to the campaign so RingCX knows which phone personas to dial during each calling window.

The campaign calling configuration is selected when the campaign is created. Do not plan to switch an existing campaign between `SIMPLE` and `STRATEGIC` later.

## Configure Phone Personas

Use the persona phone configuration APIs to define the additional phone labels available for an account.

### Create a Phone Persona

```http
POST {BASE_URL}/api/v1/admin/accounts/{accountId}/persona-phone-config
Authorization: Bearer <accessToken>
Content-Type: application/json

{
  "phoneId": 2,
  "phoneLabel": "Mobile Phone"
}
```

The response returns the account's current persona phone configuration list:

```json
[
  {
    "accountId": "15300002",
    "phoneId": 1,
    "phoneLabel": "Leadphone"
  },
  {
    "accountId": "15300002",
    "phoneId": 2,
    "phoneLabel": "Mobile Phone"
  }
]
```

### Manage Phone Personas

| Method | Endpoint | Purpose |
|-|-|-|
| `GET` | `/api/v1/admin/accounts/{accountId}/persona-phone-config` | List configured phone personas. |
| `POST` | `/api/v1/admin/accounts/{accountId}/persona-phone-config` | Create a phone persona. |
| `PUT` | `/api/v1/admin/accounts/{accountId}/persona-phone-config` | Update a phone persona label. |
| `GET` | `/api/v1/admin/accounts/{accountId}/persona-phone-config/active-campaigns/{phoneId}` | Check which campaigns currently use a phone persona. |
| `DELETE` | `/api/v1/admin/accounts/{accountId}/persona-phone-config/{phoneId}` | Delete a phone persona. |

Before deleting a phone persona, call the active-campaigns endpoint to see whether the phone ID is still used by campaign calling preferences.

## Create a Strategic Campaign

Set `callingConfiguration` to `STRATEGIC` when you create the campaign. Then include `personaCallSchedules` to define which phone IDs should be dialed in each campaign calling window.

```http
POST {BASE_URL}/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns
Authorization: Bearer <accessToken>
Content-Type: application/json

{
  "campaignName": "Renewal Outreach",
  "campaignDesc": "Strategic outbound campaign",
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
  "callingConfiguration": "STRATEGIC",
  "personaCallSchedules": [
    {
      "day": "MONDAY",
      "start": "08:00",
      "end": "12:00",
      "callPreferences": [
        {
          "phoneId": 2,
          "priority": 1
        },
        {
          "phoneId": 1,
          "priority": 2
        }
      ]
    },
    {
      "day": "MONDAY",
      "start": "12:01",
      "end": "17:00",
      "callPreferences": [
        {
          "phoneId": 1,
          "priority": 1
        },
        {
          "phoneId": 2,
          "priority": 2
        }
      ]
    }
  ]
}
```

Persona call schedules use the following fields:

| Field | Description |
|-|-|
| `day` | Day of week for the calling window. |
| `start` | Start time in `HH:mm` format. |
| `end` | End time in `HH:mm` format. |
| `callPreferences` | Phone personas to dial in this window. |
| `phoneId` | The configured persona phone ID. |
| `priority` | Dial order within the window. Lower values are attempted first. |

Each schedule must include at least one call preference. For each configured day, schedule windows must fit inside and fully cover the campaign's business hours for that day. Windows cannot overlap. When you split a day into multiple windows, start each next window exactly one minute after the previous window ends, such as `08:00` to `12:00` followed by `12:01` to `17:00`.

## Load Leads With Persona Phones

You can load persona phone numbers through direct lead loading or through the file preview and process flow.

### Direct Lead Loading

For direct lead loading, keep the lead's primary phone number in `leadPhone`. If the account is enabled for E.164 or international phone-number handling, also provide the primary number in `leadPhoneE164`; RingCX uses `leadPhoneE164` as the primary number for that account mode.

Add extra phone numbers in `personaPhoneConfig`. The keys in `personaPhoneConfig` are the configured `phoneLabel` values, and the values are that lead's phone numbers. The primary number must be a single number, not a pipe-delimited list, because strategic campaigns use persona configuration to manage additional numbers.

```http
POST {BASE_URL}/api/v1/admin/accounts/{accountId}/campaigns/{campaignId}/leadLoader/direct
Authorization: Bearer <accessToken>
Content-Type: application/json

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
      "leadPhoneE164": "+14155550100",
      "firstName": "Ada",
      "lastName": "Lovelace",
      "personaPhoneConfig": {
        "Mobile Phone": "+14155550101",
        "Work Phone": "+14155550102"
      }
    }
  ]
}
```

When the campaign uses `STRATEGIC` calling configuration, RingCX stores the persona phone mapping with the lead and uses the current persona call schedule to choose which phone numbers are eligible to dial.

### File Preview and Process

For file-based loading, call the preview endpoint first. The preview response includes the available `personaPhoneConfig` values for strategic campaigns so the client can present the additional phone fields for mapping.

```http
POST {BASE_URL}/api/v1/admin/accounts/{accountId}/campaigns/{campaignId}/leadLoader/preview?fileType=COMMA
Authorization: Bearer <accessToken>
Content-Type: multipart/form-data
```

The preview response includes phone IDs and labels:

```json
{
  "transactionId": "4431e90b-4c26-44d4-9093-2479e789f051",
  "mappingColumns": [
    "LEAD_PHONE",
    "EXTERN_ID",
    "FIRST_NAME",
    "LAST_NAME"
  ],
  "personaPhoneConfig": [
    {
      "phoneId": 2,
      "phoneLabel": "Mobile Phone"
    },
    {
      "phoneId": 3,
      "phoneLabel": "Work Phone"
    }
  ]
}
```

When you process the upload, use `additionalPhoneMappings` to map each persona phone ID to the source column index from the uploaded file.

```http
POST {BASE_URL}/api/v1/admin/accounts/{accountId}/campaigns/{campaignId}/leadLoader/process
Authorization: Bearer <accessToken>
Content-Type: application/json

{
  "transactionId": "4431e90b-4c26-44d4-9093-2479e789f051",
  "description": "Renewal leads",
  "fileType": "COMMA",
  "fileContainsHeaders": true,
  "duplicateHandling": "REMOVE_FROM_LIST",
  "listState": "ACTIVE",
  "timeZoneOption": "NOT_APPLICABLE",
  "pageNumber": 1,
  "pageColumnMappings": {
    "LEAD_PHONE": 1,
    "EXTERN_ID": 2,
    "FIRST_NAME": 3,
    "LAST_NAME": 4
  },
  "additionalPhoneMappings": {
    "2": 5,
    "3": 6
  }
}
```

In this example, phone ID `2` is loaded from column `5`, and phone ID `3` is loaded from column `6`.

## End-to-End Flow

1. Create account-level phone personas with `/persona-phone-config`.
2. Create the campaign with `callingConfiguration` set to `STRATEGIC`.
3. Add `personaCallSchedules` to the campaign so each calling window has phone IDs and priorities.
4. Load leads with a single primary phone number, using `leadPhoneE164` when the account is enabled for E.164 phone numbers, plus either per-lead `personaPhoneConfig` values for direct load or `additionalPhoneMappings` for file processing.
5. Let the dialer evaluate the current campaign calling window and dial the eligible phone personas in priority order.

## Troubleshooting

If the preview response does not include `personaPhoneConfig`, confirm that the campaign uses `callingConfiguration: "STRATEGIC"` and that persona phone configurations exist for the account.

If direct lead loading accepts the request but a lead is not loaded or does not map an additional phone, confirm that the primary phone is populated in the field used by the account mode. Accounts enabled for E.164 phone numbers must provide `leadPhoneE164`. Also confirm that the primary phone is not pipe-delimited and that each `personaPhoneConfig` key exactly matches a configured `phoneLabel`.

If campaign creation or update fails for persona schedules, verify that each schedule has at least one `callPreferences` entry, that the phone IDs exist, that schedule windows fully cover the campaign's business hours for that day, and that consecutive windows use the one-minute handoff rule.
