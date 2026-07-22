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

SDK examples in this article use JWT authentication. Set `RC_CLIENT_ID`, `RC_CLIENT_SECRET`, and `RC_JWT` in your environment; the SDK wrapper handles the RingCentral login and RingCX token exchange. For JavaScript, install `ringcentral-engage-voice-client` and `dotenv`. For Python, install `ringcentral_engage_voice` and `python-dotenv`.

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
        phone: "4155550100",
        countryId: "USA",
        dncTagId: 12345,
        externId: "lead-1001"
      };

      const response = await ev.post(
        "/api/v1/admin/accounts/{accountId}/dncLists",
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
        "phone": "4155550100",
        "countryId": "USA",
        "dncTagId": 12345,
        "externId": "lead-1001",
    }

    response = ev.post(
        "/api/v1/admin/accounts/{accountId}/dncLists",
        payload,
    ).json()
    print(response)
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
