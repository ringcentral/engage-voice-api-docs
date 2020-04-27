# Searching Leads

Use the Search Leads APIs to search leads.

```bash tab="HTTP"
POST /api/v1/admin/accounts/{accountId}/campaignLeads/leadSearch
Authorization: bearer <myAccessToken>
Content-Type: application/json;charset=UTF-8
Accept: application/json

{"firstName":"Jon"}
```

```bash tab="cURLs"
curl -XPOST 'https://engage.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/leadSearch' -H 'Authorization: Bearer {myAccessToken}' -d '{"firstName":"John"}' -H 'Content-Type: application/json'
```

## References

* [Web console documentation: Using the Leads search](https://docs.ringcentral.com/engage/article/voice-admin-use-lead-search)