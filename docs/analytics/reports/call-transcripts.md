# RingCX Transcript Extraction API

The RingCX Transcript Extraction API allows developers and administrators to programmatically retrieve text-based transcripts for both voice and digital interactions. This API enables the automated flow of conversational data into downstream systems like CRMs, quality management tools, or custom analytics engines, solving the problem of manual review and data entry.

## Strategic Overview

Extracting transcripts programmatically provides significant business value by enabling automated compliance auditing, agent performance coaching, and deep sentiment analysis.

### Key Use Cases

* **Automated QA Scoring:** Feed transcripts into AI models to automatically score interactions based on custom rubrics.
* **CRM Enrichment:** Automatically attach full conversation text to customer records for better historical context.
* **Compliance Archival:** Maintain long-term, searchable text records of all customer interactions for regulatory verification.

### Real-Time vs. Latency Expectations

This API is designed for post-interaction retrieval. Transcripts are generated after a segment is finalized.

* **Data Availability:** Transcripts are typically available **5 minutes** after a call or chat segment ends.
* **Retention Policy:** Transcript availability matches your account's configured data retention policy.

### Required Permissions & Scopes

#### 1. Configure OAuth Scopes

To authenticate, your application must be configured with the following permission in the [Developer Portal](https://developers.ringcentral.com/my-account.html#/applications):

* **`ReadAccounts`**: Required to validate the account context and access interaction metadata.

#### 2. Enable Platform Permissions

To use AI-generated transcripts, ensure the feature is active within the RingCX Admin portal:

1. Log in to **RingCX Admin**.
2. Navigate to **Routing** > **Voice/Digital Queues & Skills**.
3. Select the target queue and navigate to the **AI Tools** section.
4. Check the **"Enable AI Summaries"** box to activate transcription.

!!! warning "Common Authorization Errors"
    If the user lacks the necessary platform permissions, the API will return:
    ```json 
    { "errorCode": "access.denied.exception", "generalMessage": "You do not have permission to access this resource", "timestamp": 1611847650696 } 
    ```

---

## API Discovery: Finding Dialog and Segment IDs

To retrieve a transcript, you must first obtain the unique `dialogId` and `segmentId` using the interaction metadata endpoint.

`POST https://ringcx.ringcentral.com/voice/api/cx/integration/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/interaction-metadata`

### Prerequisites & Constraints

* **Account Context:** You must provide both the `rcAccountId` and the `subAccountId` in the path.
* **Time Windows:** The `timeInterval` for metadata retrieval cannot exceed 3600 seconds (1 hour).

---

## Main Endpoint: Get Transcript

`GET https://ringcx.ringcentral.com/voice/api/cx/integration/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/transcripts/dialogs/{dialogId}/segments/{segmentId}`

### Request Body / Parameters

| Parameter | Type | Requirement | Description |
| --- | --- | --- | --- |
| `rcAccountId` | String | **Required** | The unique identifier for the main RingCentral account. |
| `subAccountId` | String | **Required** | The unique identifier for the RingCX sub-account. |
| `dialogId` | String | **Required** | The unique ID connecting different segments of an interaction. |
| `segmentId` | String | **Required** | The unique identifier for the specific part of the call or chat. |

**Example Response:**

```json
{
  "channelClass": "VOICE",
  "transcript": [
    {
      "participantId": "449438",
      "participantName": "Agent Smith",
      "timestamp": "1721651880000",
      "message": "Hello, how can I help you today?"
    },
    {
      "participantId": "cust_123",
      "participantName": "Customer",
      "timestamp": "1721651885000",
      "message": "I'm having trouble with my recent order."
    }
  ]
}

```

---

## Implementation Strategy

### Recommended Pattern

We recommend a **"Sliding Window"** polling strategy to account for the generation delay and ensure no data is missed.

1. **Poll for Metadata:** Query for metadata in 15-minute intervals with a 5-minute offset to allow for AI processing.
2. **Filter Results:** Only call the transcript endpoint for segments where the metadata indicates `hasTranscript: true`.
3. **Handle Latency:** If you receive a 404 error, implement an exponential backoff strategy for subsequent retry attempts.

!!! important "Rate Limiting & Stability"
    * **Limit:** Standard platform rate limiting is 120 requests per minute.
    * **Strategy:** Implement exponential backoff when hitting 429 "Too Many Requests" errors.

### Sample Implementation (Python)

```python
import requests

# Configuration
BASE_URL = "https://ringcx.ringcentral.com/voice/api"
RC_ACCOUNT_ID = "980634004"
SUB_ACCOUNT_ID = "99999999"

def get_transcript(dialog_id, segment_id, token):
    """Retrieves the transcript for a specific interaction segment."""
    endpoint = f"/cx/integration/v1/accounts/{RC_ACCOUNT_ID}/sub-accounts/{SUB_ACCOUNT_ID}/transcripts/dialogs/{dialog_id}/segments/{segment_id}"
    url = f"{BASE_URL}{endpoint}"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get('transcript')
    else:
        print(f"Error fetching transcript: {response.status_code}")
        return None

```

---

## Appendix: Supported Elements

??? info "View System Dispositions"

    | Element | Description |
    | --- | --- |
    | `ANSWER` | Call was successfully answered. |
    | `ABANDON` | Interaction was abandoned by the contact. |
    | `BUSY` | The line returned a busy signal. |
    | `MACHINE` | Answering machine was detected. |
