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

```http
POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dncLists
Authorization: Bearer <ringcxAccessToken>
Content-Type: application/json
```

```json
{
  "phone": "4155550100",
  "countryId": "USA",
  "dncTagId": 12345,
  "externId": "lead-1001"
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
