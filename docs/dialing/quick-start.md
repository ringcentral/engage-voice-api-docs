# RingCX Dialing Quick Start

This quick start creates a dial group, the top-level container for outbound campaigns. After the dial group exists, create campaigns under it and load leads into those campaigns.

## Prerequisites

Before calling the Dialing APIs:

1. Create a RingCentral app with the `ReadAccounts` permission.
2. Complete the [RingCentral token exchange flow](../authentication/auth-ringcentral.md) and obtain a RingCX access token.
3. Get the RingCX sub-account ID from `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts`.

## Create a Dial Group

=== "HTTP"

    ```http
    POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

    {
      "dialGroupName": "Outbound Renewals",
      "dialGroupDesc": "Renewal outreach campaigns",
      "dialMode": "PREVIEW",
      "isActive": true
    }
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    access_token = "<ringcxAccessToken>"
    payload = {
        "dialGroupName": "Outbound Renewals",
        "dialGroupDesc": "Renewal outreach campaigns",
        "dialMode": "PREVIEW",
        "isActive": True,
    }

    response = requests.post(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/dialGroups",
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
      dialGroupName: "Outbound Renewals",
      dialGroupDesc: "Renewal outreach campaigns",
      dialMode: "PREVIEW",
      isActive: true
    };

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/dialGroups`,
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

## Verify the Dial Group

=== "HTTP"

    ```http
    GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups
    Authorization: Bearer <ringcxAccessToken>
    Accept: application/json
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    access_token = "<ringcxAccessToken>"

    response = requests.get(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/dialGroups",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        },
    )
    response.raise_for_status()
    print(response.json())
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const accessToken = "<ringcxAccessToken>";

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/dialGroups`,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
          Accept: "application/json"
        }
      }
    );

    if (!response.ok) throw new Error(await response.text());
    console.log(await response.json());
    ```

Use the returned `dialGroupId` when creating campaigns.

## Next Steps

After creating a dial group:

1. Create an outbound [campaign](campaigns/campaigns.md).
2. Load leads into the campaign with [bulk import](leads/bulk-import.md).
3. Use [lead search](leads/search.md) and [lead actions](leads/actions.md) to manage campaign leads.
