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

## Configure Phone Personas

Use the persona phone configuration APIs to define the additional phone labels available for an account.

### Create a Phone Persona

=== "HTTP"

    ```http
    POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/persona-phone-config
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "phoneId": 2,
      "phoneLabel": "Mobile Phone"
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    access_token = "<ringcxAccessToken>"
    payload = {
        "phoneId": 2,
        "phoneLabel": "Mobile Phone",
    }

    response = requests.post(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/persona-phone-config",
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
      phoneId: 2,
      phoneLabel: "Mobile Phone"
    };

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/persona-phone-config`,
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
        phoneId: 2,
        phoneLabel: "Mobile Phone"
      };

      const response = await ev.post(
        "/api/v1/admin/accounts/{accountId}/persona-phone-config",
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
        "phoneId": 2,
        "phoneLabel": "Mobile Phone",
    }

    response = ev.post(
        "/api/v1/admin/accounts/{accountId}/persona-phone-config",
        payload,
    ).json()
    print(response)
    ```

The response returns the account's current persona phone configuration list:

```json
[
  {
    "accountId": "15300002",
    "phoneId": 1,
    "phoneLabel": "Lead Phone"
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
| `GET` | `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/persona-phone-config` | List configured phone personas. |
| `POST` | `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/persona-phone-config` | Create a phone persona. |
| `PUT` | `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/persona-phone-config` | Update a phone persona label. |
| `GET` | `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/persona-phone-config/active-campaigns/{phoneId}` | Check which campaigns currently use a phone persona. |
| `DELETE` | `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/persona-phone-config/{phoneId}` | Delete a phone persona. |

Before deleting a phone persona, call the active-campaigns endpoint to see whether the phone ID is still used by campaign calling preferences.

## Create a Strategic Campaign

Set `callingConfiguration` to `STRATEGIC` when you create the campaign. Then include `personaCallSchedules` to define which phone IDs should be dialed in each campaign calling window.

=== "HTTP"

    ```http
    POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns
    Authorization: Bearer <ringcxAccessToken>
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

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    dial_group_id = "<dialGroupId>"
    access_token = "<ringcxAccessToken>"
    payload = {
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
                    {"phoneId": 2, "priority": 1},
                    {"phoneId": 1, "priority": 2},
                ],
            },
            {
                "day": "MONDAY",
                "start": "12:01",
                "end": "17:00",
                "callPreferences": [
                    {"phoneId": 1, "priority": 1},
                    {"phoneId": 2, "priority": 2},
                ],
            },
        ],
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
      campaignDesc: "Strategic outbound campaign",
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
      sunSched: "00000000",
      callingConfiguration: "STRATEGIC",
      personaCallSchedules: [
        {
          day: "MONDAY",
          start: "08:00",
          end: "12:00",
          callPreferences: [
            { phoneId: 2, priority: 1 },
            { phoneId: 1, priority: 2 }
          ]
        },
        {
          day: "MONDAY",
          start: "12:01",
          end: "17:00",
          callPreferences: [
            { phoneId: 1, priority: 1 },
            { phoneId: 2, priority: 2 }
          ]
        }
      ]
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
        campaignDesc: "Strategic outbound campaign",
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
        sunSched: "00000000",
        callingConfiguration: "STRATEGIC",
        personaCallSchedules: [
          {
            day: "MONDAY",
            start: "08:00",
            end: "12:00",
            callPreferences: [
              { phoneId: 2, priority: 1 },
              { phoneId: 1, priority: 2 }
            ]
          },
          {
            day: "MONDAY",
            start: "12:01",
            end: "17:00",
            callPreferences: [
              { phoneId: 1, priority: 1 },
              { phoneId: 2, priority: 2 }
            ]
          }
        ]
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
                    {"phoneId": 2, "priority": 1},
                    {"phoneId": 1, "priority": 2},
                ],
            },
            {
                "day": "MONDAY",
                "start": "12:01",
                "end": "17:00",
                "callPreferences": [
                    {"phoneId": 1, "priority": 1},
                    {"phoneId": 2, "priority": 2},
                ],
            },
        ],
    }

    response = ev.post(
        "/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns",
        payload,
    ).json()
    print(response)
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

=== "HTTP"

    ```http
    POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaigns/{campaignId}/leadLoader/direct
    Authorization: Bearer <ringcxAccessToken>
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

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    campaign_id = "<campaignId>"
    access_token = "<ringcxAccessToken>"
    payload = {
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
                    "Work Phone": "+14155550102",
                },
            }
        ],
    }

    response = requests.post(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/campaigns/{campaign_id}/leadLoader/direct",
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
    const campaignId = "<campaignId>";
    const accessToken = "<ringcxAccessToken>";
    const payload = {
      description: "Renewal leads",
      dialPriority: "NORMAL",
      duplicateHandling: "REMOVE_FROM_LIST",
      listState: "ACTIVE",
      timeZoneOption: "NOT_APPLICABLE",
      uploadLeads: [
        {
          externId: "lead-1001",
          leadPhone: "4155550100",
          leadPhoneE164: "+14155550100",
          firstName: "Ada",
          lastName: "Lovelace",
          personaPhoneConfig: {
            "Mobile Phone": "+14155550101",
            "Work Phone": "+14155550102"
          }
        }
      ]
    };

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/campaigns/${campaignId}/leadLoader/direct`,
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
        description: "Renewal leads",
        dialPriority: "NORMAL",
        duplicateHandling: "REMOVE_FROM_LIST",
        listState: "ACTIVE",
        timeZoneOption: "NOT_APPLICABLE",
        uploadLeads: [
          {
            externId: "lead-1001",
            leadPhone: "4155550100",
            leadPhoneE164: "+14155550100",
            firstName: "Ada",
            lastName: "Lovelace",
            personaPhoneConfig: {
              "Mobile Phone": "+14155550101",
              "Work Phone": "+14155550102"
            }
          }
        ]
      };

      const response = await ev.post(
        "/api/v1/admin/accounts/{accountId}/campaigns/{campaignId}/leadLoader/direct",
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
                    "Work Phone": "+14155550102",
                },
            }
        ],
    }

    response = ev.post(
        "/api/v1/admin/accounts/{accountId}/campaigns/{campaignId}/leadLoader/direct",
        payload,
    ).json()
    print(response)
    ```

When the campaign uses `STRATEGIC` calling configuration, RingCX stores the persona phone mapping with the lead and uses the current persona call schedule to choose which phone numbers are eligible to dial.

### File Preview and Process

For file-based loading, call the preview endpoint first. The preview response includes the available `personaPhoneConfig` values for strategic campaigns so the client can present the additional phone fields for mapping.

=== "HTTP"

    ```http
    POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaigns/{campaignId}/leadLoader/preview?fileType=COMMA
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: multipart/form-data
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    campaign_id = "<campaignId>"
    access_token = "<ringcxAccessToken>"

    with open("leads.csv", "rb") as leads_file:
        response = requests.post(
            f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/campaigns/{campaign_id}/leadLoader/preview",
            params={"fileType": "COMMA"},
            headers={"Authorization": f"Bearer {access_token}"},
            files={"file": leads_file},
        )
    response.raise_for_status()
    print(response.json())
    ```

=== "JavaScript"

    ```javascript
    import { readFile } from "node:fs/promises";

    const accountId = "<accountId>";
    const campaignId = "<campaignId>";
    const accessToken = "<ringcxAccessToken>";

    const formData = new FormData();
    formData.append("file", new Blob([await readFile("leads.csv")]), "leads.csv");

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/campaigns/${campaignId}/leadLoader/preview?fileType=COMMA`,
      {
        method: "POST",
        headers: { Authorization: `Bearer ${accessToken}` },
        body: formData
      }
    );

    if (!response.ok) throw new Error(await response.text());
    console.log(await response.json());
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

When you process the upload, use `additionalPhoneMappings` to map each persona phone ID to the source column index from the uploaded file. The `pageColumnMappings` and `additionalPhoneMappings` values are zero-based column indexes from the selected preview page.

=== "HTTP"

    ```http
    POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaigns/{campaignId}/leadLoader/process
    Authorization: Bearer <ringcxAccessToken>
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
        "LEAD_PHONE": 0,
        "EXTERN_ID": 1,
        "FIRST_NAME": 2,
        "LAST_NAME": 3
      },
      "additionalPhoneMappings": {
        "2": 4,
        "3": 5
      }
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    campaign_id = "<campaignId>"
    access_token = "<ringcxAccessToken>"
    payload = {
        "transactionId": "4431e90b-4c26-44d4-9093-2479e789f051",
        "description": "Renewal leads",
        "fileType": "COMMA",
        "fileContainsHeaders": True,
        "duplicateHandling": "REMOVE_FROM_LIST",
        "listState": "ACTIVE",
        "timeZoneOption": "NOT_APPLICABLE",
        "pageNumber": 1,
        "pageColumnMappings": {
            "LEAD_PHONE": 0,
            "EXTERN_ID": 1,
            "FIRST_NAME": 2,
            "LAST_NAME": 3,
        },
        "additionalPhoneMappings": {
            "2": 4,
            "3": 5,
        },
    }

    response = requests.post(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/campaigns/{campaign_id}/leadLoader/process",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        json=payload,
    )
    response.raise_for_status()
    print(f"Lead file processing accepted: {response.status_code}")
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const campaignId = "<campaignId>";
    const accessToken = "<ringcxAccessToken>";
    const payload = {
      transactionId: "4431e90b-4c26-44d4-9093-2479e789f051",
      description: "Renewal leads",
      fileType: "COMMA",
      fileContainsHeaders: true,
      duplicateHandling: "REMOVE_FROM_LIST",
      listState: "ACTIVE",
      timeZoneOption: "NOT_APPLICABLE",
      pageNumber: 1,
      pageColumnMappings: {
        LEAD_PHONE: 0,
        EXTERN_ID: 1,
        FIRST_NAME: 2,
        LAST_NAME: 3
      },
      additionalPhoneMappings: {
        "2": 4,
        "3": 5
      }
    };

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/campaigns/${campaignId}/leadLoader/process`,
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
    console.log(`Lead file processing accepted: ${response.status}`);
    ```

After the preview response returns a `transactionId`, you can submit the process request with the SDK:

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
        transactionId: "<transactionId>",
        description: "Renewal leads",
        fileType: "COMMA",
        fileContainsHeaders: true,
        duplicateHandling: "REMOVE_FROM_LIST",
        listState: "ACTIVE",
        timeZoneOption: "NOT_APPLICABLE",
        pageNumber: 1,
        pageColumnMappings: {
          LEAD_PHONE: 0,
          EXTERN_ID: 1,
          FIRST_NAME: 2,
          LAST_NAME: 3
        },
        additionalPhoneMappings: {
          "2": 4,
          "3": 5
        }
      };

      const response = await ev.post(
        "/api/v1/admin/accounts/{accountId}/campaigns/{campaignId}/leadLoader/process",
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
        "transactionId": "<transactionId>",
        "description": "Renewal leads",
        "fileType": "COMMA",
        "fileContainsHeaders": True,
        "duplicateHandling": "REMOVE_FROM_LIST",
        "listState": "ACTIVE",
        "timeZoneOption": "NOT_APPLICABLE",
        "pageNumber": 1,
        "pageColumnMappings": {
            "LEAD_PHONE": 0,
            "EXTERN_ID": 1,
            "FIRST_NAME": 2,
            "LAST_NAME": 3,
        },
        "additionalPhoneMappings": {
            "2": 4,
            "3": 5,
        },
    }

    response = ev.post(
        "/api/v1/admin/accounts/{accountId}/campaigns/{campaignId}/leadLoader/process",
        payload,
    ).json()
    print(response)
    ```

In this example, phone ID `2` is loaded from the fifth column, and phone ID `3` is loaded from the sixth column.

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
