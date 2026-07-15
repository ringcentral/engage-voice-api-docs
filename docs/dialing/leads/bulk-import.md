# Bulk Import Leads

Use the lead loader APIs to add leads to an outbound campaign. RingCX supports direct JSON loading and a preview/process flow for uploaded files.

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

Use the returned `campaignId` in the lead loader path.

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
          "firstName": "Ada",
          "lastName": "Lovelace",
          "state": "CA"
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
                "firstName": "Ada",
                "lastName": "Lovelace",
                "state": "CA",
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
          firstName: "Ada",
          lastName: "Lovelace",
          state: "CA"
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

## File Preview and Process

For file-based imports, preview the file first so RingCX can identify columns and return mapping information. Then submit the process request with the selected mapping.

=== "HTTP"

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

    process_payload = {
        "transactionId": "<transactionId>",
        "description": "Renewal leads",
        "fileType": "COMMA",
        "fileContainsHeaders": True,
        "duplicateHandling": "REMOVE_FROM_LIST",
        "listState": "ACTIVE",
        "timeZoneOption": "NOT_APPLICABLE",
        "pageNumber": 1,
        "pageColumnMappings": {
            "LEAD_PHONE": 1,
            "EXTERN_ID": 2,
            "FIRST_NAME": 3,
            "LAST_NAME": 4,
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
    print(process.json())
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

    const processPayload = {
      transactionId: "<transactionId>",
      description: "Renewal leads",
      fileType: "COMMA",
      fileContainsHeaders: true,
      duplicateHandling: "REMOVE_FROM_LIST",
      listState: "ACTIVE",
      timeZoneOption: "NOT_APPLICABLE",
      pageNumber: 1,
      pageColumnMappings: {
        LEAD_PHONE: 1,
        EXTERN_ID: 2,
        FIRST_NAME: 3,
        LAST_NAME: 4
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
    console.log(await process.json());
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
