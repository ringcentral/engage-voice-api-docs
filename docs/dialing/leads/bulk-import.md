# Bulk Import Leads

Use the lead loader APIs to add leads to an outbound campaign. RingCX supports direct JSON loading and a preview/process flow for uploaded files.

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

## Find the Campaign

Before loading leads, identify the target campaign:

=== "HTTP"

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

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    dial_group_id = "<dialGroupId>"
    access_token = "<ringcxAccessToken>"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }

    dial_groups = requests.get(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/dialGroups",
        headers=headers,
    )
    dial_groups.raise_for_status()

    campaigns = requests.get(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/dialGroups/{dial_group_id}/campaigns",
        headers=headers,
    )
    campaigns.raise_for_status()

    print(dial_groups.json())
    print(campaigns.json())
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const dialGroupId = "<dialGroupId>";
    const accessToken = "<ringcxAccessToken>";
    const headers = {
      Authorization: `Bearer ${accessToken}`,
      Accept: "application/json"
    };

    const dialGroups = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/dialGroups`,
      { headers }
    );
    if (!dialGroups.ok) throw new Error(await dialGroups.text());

    const campaigns = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/dialGroups/${dialGroupId}/campaigns`,
      { headers }
    );
    if (!campaigns.ok) throw new Error(await campaigns.text());

    console.log(await dialGroups.json());
    console.log(await campaigns.json());
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

      const dialGroups = await ev.get(
        "/api/v1/admin/accounts/{accountId}/dialGroups"
      );
      const campaigns = await ev.get(
        "/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns"
      );

      console.log(dialGroups.data);
      console.log(campaigns.data);
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

    dial_groups = ev.get(
        "/api/v1/admin/accounts/{accountId}/dialGroups"
    ).json()
    campaigns = ev.get(
        "/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns"
    ).json()

    print(dial_groups)
    print(campaigns)
    ```

Use the returned `campaignId` in the lead loader path.

## Choose an Import Method

| Method | Use when | Endpoint |
| --- | --- | --- |
| Direct lead loading | Your integration already has structured lead records and can send them as JSON. | `POST /voice/api/v1/admin/accounts/{accountId}/campaigns/{campaignId}/leadLoader/direct` |
| File preview and process | Users upload a CSV, Excel, pipe-delimited, or tab-delimited file and need to map file columns before loading. | `POST /voice/api/v1/admin/accounts/{accountId}/campaigns/{campaignId}/leadLoader/preview`, then `POST /voice/api/v1/admin/accounts/{accountId}/campaigns/{campaignId}/leadLoader/process` |

## Direct Lead Loading

Direct loading sends leads as JSON and is the simplest option when your integration already has structured lead data.

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
          "email": "ada@example.com",
          "state": "CA",
          "zip": "94105",
          "leadPriority": 5,
          "maxPasses": 3,
          "callerId": "4155550199",
          "auxData1": "renewal"
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
                "email": "ada@example.com",
                "state": "CA",
                "zip": "94105",
                "leadPriority": 5,
                "maxPasses": 3,
                "callerId": "4155550199",
                "auxData1": "renewal",
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
          email: "ada@example.com",
          state: "CA",
          zip: "94105",
          leadPriority: 5,
          maxPasses: 3,
          callerId: "4155550199",
          auxData1: "renewal"
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
            email: "ada@example.com",
            state: "CA",
            zip: "94105",
            leadPriority: 5,
            maxPasses: 3,
            callerId: "4155550199",
            auxData1: "renewal"
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
                "email": "ada@example.com",
                "state": "CA",
                "zip": "94105",
                "leadPriority": 5,
                "maxPasses": 3,
                "callerId": "4155550199",
                "auxData1": "renewal",
            }
        ],
    }

    response = ev.post(
        "/api/v1/admin/accounts/{accountId}/campaigns/{campaignId}/leadLoader/direct",
        payload,
    ).json()
    print(response)
    ```

### Direct Load Response

The direct load response summarizes accepted, inserted, converted, rejected, and DNC-affected leads.

```json
{
  "leadsSupplied": 1,
  "leadsAccepted": 1,
  "leadsInserted": 1,
  "leadsConverted": 1,
  "dncReturnedCount": 0,
  "failedAgentAssignment": 0,
  "listState": "ACTIVE",
  "timeZoneOption": "NOT_APPLICABLE",
  "processingResult": "OK",
  "rejectedRows": []
}
```

## File Preview and Process

For file-based imports, preview the file first so RingCX can identify columns and return mapping information. Then submit the process request with the selected mapping.

The `pageColumnMappings` values are zero-based column indexes from the selected preview page. For example, if the preview shows `LEAD_PHONE` in the first column, map `LEAD_PHONE` to `0`.

=== "HTTP"

    ```http
    POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaigns/{campaignId}/leadLoader/preview?fileType=COMMA
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: multipart/form-data

    file=@leads.csv
    ```

    ```http
    POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaigns/{campaignId}/leadLoader/process
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "transactionId": "<transactionId>",
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
      }
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    campaign_id = "<campaignId>"
    access_token = "<ringcxAccessToken>"
    headers = {"Authorization": f"Bearer {access_token}"}

    with open("leads.csv", "rb") as leads_file:
        preview = requests.post(
            f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/campaigns/{campaign_id}/leadLoader/preview",
            params={"fileType": "COMMA"},
            headers=headers,
            files={"file": leads_file},
        )
    preview.raise_for_status()
    preview_body = preview.json()

    process_payload = {
        "transactionId": preview_body["transactionId"],
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
    }

    process = requests.post(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/campaigns/{campaign_id}/leadLoader/process",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        json=process_payload,
    )
    process.raise_for_status()
    print(f"Lead file processing accepted: {process.status_code}")
    ```

=== "JavaScript"

    ```javascript
    import { readFile } from "node:fs/promises";

    const accountId = "<accountId>";
    const campaignId = "<campaignId>";
    const accessToken = "<ringcxAccessToken>";

    const formData = new FormData();
    formData.append("file", new Blob([await readFile("leads.csv")]), "leads.csv");

    const preview = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/campaigns/${campaignId}/leadLoader/preview?fileType=COMMA`,
      {
        method: "POST",
        headers: { Authorization: `Bearer ${accessToken}` },
        body: formData
      }
    );
    if (!preview.ok) throw new Error(await preview.text());
    const previewBody = await preview.json();

    const processPayload = {
      transactionId: previewBody.transactionId,
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
      }
    };

    const process = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/campaigns/${campaignId}/leadLoader/process`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify(processPayload)
      }
    );
    if (!process.ok) throw new Error(await process.text());
    console.log(`Lead file processing accepted: ${process.status}`);
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
    }

    response = ev.post(
        "/api/v1/admin/accounts/{accountId}/campaigns/{campaignId}/leadLoader/process",
        payload,
    ).json()
    print(response)
    ```

### Preview Response

The preview response includes the `transactionId` required by the process request, the mapping columns supported by the loader, and sample rows for each preview page.

```json
{
  "transactionId": "8c7406f8-31cf-4f6a-a5a4-7a6b25e35f52",
  "mappingColumns": [
    "LEAD_PHONE",
    "EXTERN_ID",
    "FIRST_NAME",
    "LAST_NAME"
  ],
  "pagePreviews": [
    {
      "pageNumber": 1,
      "pageName": "leads.csv",
      "rowData": [
        ["phone", "external_id", "first_name", "last_name"],
        ["4155550100", "lead-1001", "Ada", "Lovelace"]
      ]
    }
  ]
}
```

The process request returns an accepted or created status after RingCX accepts the file for processing.

## Common Fields

| Field | Description |
| --- | --- |
| `description` | Name or description for the uploaded lead list. |
| `uploadLeads` | Array of lead records for direct loading. |
| `externId` | External lead identifier from your source system. |
| `leadPhone` | Primary lead phone number. |
| `leadPhoneE164` | E.164 primary phone number, when required for the account mode. |
| `email`, `firstName`, `lastName`, `state`, `zip` | Standard contact fields that can be stored with each lead. |
| `leadPriority` | Numeric priority used by outbound dialing when prioritization is enabled. |
| `maxPasses` | Maximum number of dialing passes for the lead. |
| `callerId` | Caller ID to use for the lead when the campaign supports lead-level caller ID. |
| `auxData1` through `auxData5` | Custom fields for campaign- or integration-specific lead data. |
| `duplicateHandling` | Duplicate behavior during load. Values include `RETAIN_ALL`, `REMOVE_ALL_EXISTING`, and `REMOVE_FROM_LIST`. |
| `timeZoneOption` | How RingCX derives or applies lead time zones. Values include `NPA_NXX`, `ZIPCODE`, `EXPLICIT`, `COUNTRY`, and `NOT_APPLICABLE`. |
| `fileType` | File format for preview/process imports. Values are `EXCEL`, `PIPE`, `COMMA`, and `TAB`. |
| `pageColumnMappings` | Map of RingCX lead fields to zero-based column indexes from the preview response. |

## Persona Phone Leads

For strategic campaigns with multiple phone personas, add extra phone numbers in `personaPhoneConfig`. See [Lead Phone Persona Management](phone-persona-management.md) for the required campaign and phone-persona setup.
