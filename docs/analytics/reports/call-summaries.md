# RingCX Summaries API

The RingCX Summaries API provides programmatic access to AI-generated and agent-edited summaries for completed interaction segments. These endpoints allow developers to retrieve concise post-interaction outcomes so that conversation summaries can be attached to CRMs, quality management workflows, compliance records, or custom analytics systems.

## Strategic Overview

Summaries are useful when a downstream system needs the outcome of an interaction, but does not need the full transcript. The API is designed for post-interaction retrieval after RingCX has finalized the segment and generated the available summary data.

### Key Use Cases

* **CRM Enrichment:** Attach concise summaries to customer records so agents and supervisors can review prior conversations quickly.
* **Quality Management:** Feed summaries into QA workflows to speed up review and coaching without requiring a full transcript review for every interaction.
* **Compliance and Audit Review:** Store short, searchable interaction outcomes alongside metadata, recordings, and transcripts.

### Real-Time vs. Latency Expectations

These endpoints are not real-time event feeds. They are intended for retrieving summaries after an interaction segment has completed and post-processing has finished.

* **Data Availability:** Summary data is available after the segment is finalized and processed. Allow a short post-call processing window before polling.
* **Empty Summaries:** A successful response can have an empty body when the requested summary type has not been populated for that segment.

### Required Permissions & Scopes

#### 1. Configure OAuth Scopes

To authenticate, your application must be configured with the following permission in the [Developer Portal](https://developers.ringcentral.com/my-account.html#/applications):

* **`ReadAccounts`**: Required to validate account context and complete the RingCX authentication flow.

For a detailed walkthrough on exchanging your RingCentral token for a RingCX access token, see the [RingCentral Authentication Guide](../../authentication/auth-ringcentral.md).

#### 2. Enable Platform Permissions

To generate and retrieve summaries, AI summaries must be enabled for the queue or campaign that handled the interaction.

1. Log in to **RingCX Admin**.
2. Navigate to **Routing** > **Voice/Digital Queues & Skills**.
3. Select the target queue or campaign.
4. Enable **AI Summaries** for the interaction type you want to summarize.

!!! warning "Common Authorization Errors"
    If the token is missing, expired, or cannot be authenticated, the API will return a `401 Unauthorized` response. If the authenticated user lacks access to the requested account, the API may return an access denied error:

    ```json
    {
        "errorCode": "access.denied.exception",
        "generalMessage": "You do not have permission to access this resource",
        "timestamp": 1611847650696
    }
    ```

!!! important "Special Authentication Requirement"
    Most RingCX APIs use the `Authorization: Bearer <token>` header. The Summary API is different. For these endpoints, send the RingCX access token as the value of the `access_token` cookie, and send the header name in lowercase as `cookie`.

    ```http
    cookie: access_token=<token>
    ```

    Do not send the token as the `Authorization` header when calling the summary endpoints.

!!! important "Rate Limiting & Stability"
    * **Limit:** Standard platform rate limiting applies to summary requests.
    * **Strategy:** If the API returns a `429 Too Many Requests` status code, implement exponential backoff before retrying.

---

## API Discovery

Summary endpoints require the RingCX sub-account ID and the interaction segment ID. Use the interaction metadata API to find the completed segments you want to summarize.

```http
POST https://ringcx.ringcentral.com/voice/api/cx/integration/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/interaction-metadata
Authorization: Bearer <rcRingCXAccessToken>
Content-Type: application/json
```

### Prerequisites & Constraints

* **Sub-Account Context:** Use the RingCX sub-account ID as the `{subAccountId}` path value in the summary URL.
* **Segment Context:** Use the `segmentId` value returned by interaction metadata. A segment represents one participant's portion of the interaction.
* **Processing Window:** Query completed interactions and allow time for post-interaction processing before requesting summaries.

For more details on interaction metadata, see the [Reports API](../../integration/reports-orig.md#agent-segment-metadata).

---

## Get Agent Summary

```http
GET https://engage.ringcentral.com/voice/api/v1/summary/accounts/{subAccountId}/segments/{segmentId}/agent
cookie: access_token=<token>
```

The Agent Summary endpoint returns the summary filled in or edited by the agent for a completed interaction segment.

### Request Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `subAccountId` | String | Yes | RingCX sub-account ID. This is the `{accountId}` path value used by the API. |
| `segmentId` | String | Yes | Unique interaction segment ID from interaction metadata. |

### Example Request

```bash
curl --location 'https://engage.ringcentral.com/voice/api/v1/summary/accounts/21630001/segments/p-v-0b338efb877e48f0a3a321c73fcd4634-1772456952229-50caeaadd482c/agent' \
  --header 'cookie: access_token=<token>'
```

### Response Details

Successful responses return the agent summary as a raw string body.

```text
Customer requested a billing adjustment. Agent confirmed the account details and submitted the request for review.
```

---

## Get Auto Summary

```http
GET https://engage.ringcentral.com/voice/api/v1/summary/accounts/{subAccountId}/segments/{segmentId}/auto
cookie: access_token=<token>
```

The Auto Summary endpoint returns the AI-generated summary for a completed interaction segment.

### Request Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `subAccountId` | String | Yes | RingCX sub-account ID. This is the `{accountId}` path value used by the API. |
| `segmentId` | String | Yes | Unique interaction segment ID from interaction metadata. |

### Example Request

```bash
curl --location 'https://engage.ringcentral.com/voice/api/v1/summary/accounts/21630001/segments/p-v-0b338efb877e48f0a3a321c73fcd4634-1772456952229-50caeaadd482c/auto' \
  --header 'cookie: access_token=<token>'
```

### Response Details

Successful responses return the generated summary as a raw string body.

```text
The customer called about a billing issue. The agent reviewed the account, explained the next steps, and created a follow-up request.
```

---

## Response Status Codes

Both summary endpoints use the same response behavior.

| Status | Meaning |
| --- | --- |
| `200 OK` | The request succeeded. If the response body is empty, the requested summary field is not populated for that segment. |
| `401 Unauthorized` | The request did not include a valid `cookie: access_token=<token>` header, or the token is expired. |
| `404 Not Found` | The segment was not found or the summary is not available. |
| `500 Internal Server Error` | The summary service could not complete the request. |

!!! tip "Related APIs"
    Use the [Call Transcripts API](call-transcripts.md) when you need the full conversation text instead of the generated summary.

---

## Implementation Strategy

Use interaction metadata as the source of truth for which segments to request. Store the `segmentId` with your interaction record, then request either the agent summary, the auto summary, or both depending on your downstream workflow.

### Recommended Pattern

1. Query interaction metadata for completed segments.
2. Filter to segments that need summaries in your external system.
3. Wait for post-interaction processing to complete before making summary requests.
4. Request `/agent`, `/auto`, or both for each segment.
5. Treat an empty `200 OK` response as "summary not populated" rather than a transport failure.

### Sample Implementation (Python)

```python
import requests

BASE_URL = "https://engage.ringcentral.com/voice/api/v1"
SUB_ACCOUNT_ID = "21630001"

def get_summary(segment_id, token, summary_type="auto"):
    """Retrieves the auto or agent summary for a completed interaction segment."""
    url = f"{BASE_URL}/summary/accounts/{SUB_ACCOUNT_ID}/segments/{segment_id}/{summary_type}"

    headers = {
        "cookie": f"access_token={token}",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    if response.status_code == 404:
        return None

    response.raise_for_status()

segment_id = "p-v-0b338efb877e48f0a3a321c73fcd4634-1772456952229-50caeaadd482c"
summary = get_summary(segment_id, "<token>", "auto")

if summary:
    print(summary)
else:
    print("Summary is not available for this segment.")
```
