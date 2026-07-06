# RingCX Dialing Quick Start

This quick start creates a dial group, the top-level container for outbound campaigns. After the dial group exists, create campaigns under it and load leads into those campaigns.

## Prerequisites

Before calling the Dialing APIs:

1. Create a RingCentral app with the `ReadAccounts` permission.
2. Complete the [RingCentral token exchange flow](../authentication/auth-ringcentral.md) and obtain a RingCX access token.
3. Get the RingCX sub-account ID from `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts`.

## Create a Dial Group

```http
POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups
Authorization: Bearer <ringcxAccessToken>
Content-Type: application/json
```

```json
{
  "dialGroupName": "Outbound Renewals",
  "dialGroupDesc": "Renewal outreach campaigns",
  "dialMode": "PREVIEW",
  "isActive": true
}
```

## Verify the Dial Group

```http
GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups
Authorization: Bearer <ringcxAccessToken>
Accept: application/json
```

Use the returned `dialGroupId` when creating campaigns.

## Python Example

```python
import requests

BASE_URL = "https://ringcx.ringcentral.com/voice/api"

def create_dial_group(token, account_id):
    response = requests.post(
        f"{BASE_URL}/v1/admin/accounts/{account_id}/dialGroups",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "dialGroupName": "Outbound Renewals",
            "dialGroupDesc": "Renewal outreach campaigns",
            "dialMode": "PREVIEW",
            "isActive": True,
        },
    )
    response.raise_for_status()
    return response.json()
```

## Next Steps

After creating a dial group:

1. Create an outbound [campaign](campaigns/campaigns.md).
2. Load leads into the campaign with [bulk import](leads/bulk-import.md).
3. Use [lead search](leads/search.md) and [lead actions](leads/actions.md) to manage campaign leads.
