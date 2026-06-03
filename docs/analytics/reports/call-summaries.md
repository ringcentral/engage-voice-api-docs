# RingCX Summaries API

The RingCX Summaries API retrieves AI-generated and agent-edited summaries for completed interaction segments. Use it when you want to attach concise conversation outcomes to a CRM, quality management workflow, compliance record, or custom analytics process.

Summaries are tied to interaction segments. Before calling these endpoints, use the [interaction metadata endpoint](../../integration/reports-orig.md#agent-segment-metadata) to find the RingCX sub-account ID and the segment ID for the completed interaction.

!!! important "Authentication"
    These endpoints do not use the standard `Authorization: Bearer <token>` header. Send the RingCX access token as an HTTP cookie named `access_token`.

    ```http
    Cookie: access_token=<rcRingCXAccessToken>
    ```

    You can obtain a RingCX access token by following the [RingCX authentication guide](../../authentication/auth-ringcentral.md).

## Summary Types

| Type | Endpoint suffix | Description |
| --- | --- | --- |
| Agent summary | `/agent` | Returns the summary filled in or edited by the agent for the interaction segment. |
| Auto summary | `/auto` | Returns the AI-generated summary for the interaction segment. |

## Find Segment IDs

To retrieve a summary, first query interaction metadata:

```http
POST https://ringcx.ringcentral.com/voice/api/cx/integration/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/interaction-metadata
Authorization: Bearer <rcRingCXAccessToken>
Content-Type: application/json
```

The metadata response includes the `segmentId` for each interaction segment. Use the `subAccountId` and `segmentId` values with the summary endpoints below.

## Get Agent Summary

```http
GET https://ringcx.ringcentral.com/voice/api/v1/summary/accounts/{subAccountId}/segments/{segmentId}/agent
Cookie: access_token=<rcRingCXAccessToken>
```

### Request

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `subAccountId` | String | Yes | RingCX sub-account ID. This is the `{accountId}` path value used by the API. |
| `segmentId` | String | Yes | Unique interaction segment ID from interaction metadata. |

### Example

```bash
curl --location 'https://ringcx.ringcentral.com/voice/api/v1/summary/accounts/21630001/segments/p-v-0b338efb877e48f0a3a321c73fcd4634-1772456952229-50caeaadd482c/agent' \
  --header 'Cookie: access_token=<rcRingCXAccessToken>'
```

### Response

```text
Customer requested a billing adjustment. Agent confirmed the account details and submitted the request for review.
```

## Get Auto Summary

```http
GET https://ringcx.ringcentral.com/voice/api/v1/summary/accounts/{subAccountId}/segments/{segmentId}/auto
Cookie: access_token=<rcRingCXAccessToken>
```

### Request

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `subAccountId` | String | Yes | RingCX sub-account ID. This is the `{accountId}` path value used by the API. |
| `segmentId` | String | Yes | Unique interaction segment ID from interaction metadata. |

### Example

```bash
curl --location 'https://ringcx.ringcentral.com/voice/api/v1/summary/accounts/21630001/segments/p-v-0b338efb877e48f0a3a321c73fcd4634-1772456952229-50caeaadd482c/auto' \
  --header 'Cookie: access_token=<rcRingCXAccessToken>'
```

### Response

```text
The customer called about a billing issue. The agent reviewed the account, explained the next steps, and created a follow-up request.
```

## Response Behavior

Successful responses return the summary as a raw string body rather than a JSON object.

| Status | Meaning |
| --- | --- |
| `200 OK` | The request succeeded. If the response body is empty, the requested summary field is not populated for that segment. |
| `401 Unauthorized` | The request did not include a valid `access_token` cookie, or the token is expired. |
| `404 Not Found` | The segment was not found or the summary is not available. |
| `500 Internal Server Error` | The summary service could not complete the request. |

!!! tip "Related APIs"
    Use the [Call Transcripts API](call-transcripts.md) when you need the full conversation text instead of the generated summary.
