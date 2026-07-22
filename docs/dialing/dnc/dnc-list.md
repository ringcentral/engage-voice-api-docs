# Do Not Call Lists

Use DNC APIs to add, search, upload, and remove phone numbers that should not be dialed by outbound campaigns.

## Manage DNC Entries

The DNC endpoints use the current RingCX Voice API base URL.

| Operation | Method and path |
| --- | --- |
| List DNC entries | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dncLists` |
| Create DNC entry | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dncLists` |
| Advanced DNC search | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dncLists/advancedSearch` |
| Upload DNC file | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dncLists/uploadDncFile` |
| Delete entries by tag | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dncLists/tags/{dncTagId}` |
| Delete entries by tag and country | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dncLists/tags/{dncTagId}/countries/{countryId}` |
| Delete one phone entry | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dncLists/tags/{dncTagId}/phones/{phone}/countries/{country}` |

## Create a DNC Entry

=== "HTTP"

    ```http
    POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dncLists
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "phone": "4155550100",
      "countryId": "USA",
      "dncTagId": 12345,
      "externId": "lead-1001"
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    access_token = "<ringcxAccessToken>"
    payload = {
        "phone": "4155550100",
        "countryId": "USA",
        "dncTagId": 12345,
        "externId": "lead-1001",
    }

    response = requests.post(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/dncLists",
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
      phone: "4155550100",
      countryId: "USA",
      dncTagId: 12345,
      externId: "lead-1001"
    };

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/dncLists`,
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

??? example "Response example"

    ```json
    {
      "phone": "4155550100",
      "tag": "GLOBAL",
      "countryCode": {
        "id": "USA",
        "description": null
      },
      "addedDate": "2026-07-22T18:10:11.740+0000",
      "addedBy": "Admin User",
      "reason": "Do not call",
      "dncTagId": 12345
    }
    ```

## DNC Tags

Use DNC tags to group DNC entries for management and deletion.

| Operation | Method and path |
| --- | --- |
| List DNC tags | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dncTags` |
| Create DNC tag | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dncTags` |
| Delete DNC tag | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dncTags/{dncTagId}` |

## Safety

DNC entries affect compliance and live dialing behavior. Confirm the target account, country, phone number, and tag before creating or deleting entries.
