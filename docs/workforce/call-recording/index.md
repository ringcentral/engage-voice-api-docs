
# Call Recording APIs

The Call Recording APIs allow developers to programmatically retrieve and manage audio files generated during voice interactions. This API supports dual-channel recordings.

## Strategic Overview

Call recordings are vital for maintaining organizational accountability and driving performance improvements. By automating the retrieval of these files, organizations can feed audio data into third-party speech analytics, long-term cold storage, or specialized Quality Management (QM) platforms.

### Key Use Cases

* **Compliance Archiving:** Automatically migrate recordings to secure, long-term storage to satisfy regulatory requirements (e.g., PCI, HIPAA, or MiFID II).
* **Quality Management (QM):** Export audio to evaluation platforms for manual or automated agent performance scoring.
* **Speech Analytics:** Integrate with AI tools to perform transcription, sentiment analysis, and intent categorization.

### Real-Time vs. Latency Expectations

Retrieving recordings requires a processing window to allow the system to finalize, encode, and index the audio media.

* **Data Availability:** For interaction metadata and associated recordings, it is recommended to allow a **15-minute window** after the call ends for all media processing to complete.
* **Historical Access:** Reporting data may take several minutes to sync; periodic polling is recommended for automated workflows.

### Required Permissions & Scopes

Access to recording media is governed by account-level security and explicit administrative rights.

#### 1. Configure OAuth Scopes

To authenticate, your application must be configured with the following permission in the [Developer Portal](https://developers.ringcentral.com/my-account.html#/applications):

* **`ReadAccounts`**: Required to validate the account context and access interaction metadata.

!!! warning "Warning"
    ReadAccounts is the only Oauth Scope permission with any effect on RingCx APIs. Platform permissions are managed through the RingCx Admin portal.

#### 2. Enable Platform Permissions
1.  Log in to **RingCX Admin**.
2.  **Permissions:** Ensure the user has **READ on Account** permissions.
3.  **For Stereo (Agent) Recordings:** Stereo recording must be **manually activated** by your RingCentral representative.

---

## API Discovery: Interaction Metadata

To retrieve a recording, you must first identify the unique identifiers for the call. Unlike legacy systems that provided a direct URL, the current API requires a **Dialog ID** and a **Segment ID**, which are discovered via the `interaction-metadata` report.

`POST https://engage.ringcentral.com/voice/api/api/cx/integration/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/interaction-metadata`

For a detailed walkthrough on discovering metadata, please refer to the [Agent Segment Metadata API Guide](../../integration/reports-orig.md#agent-segment-metadata).


### Locating IDs in the Response
The response will contain a list of interaction segments. For each segment you wish to download, capture the following fields:
1.  **`dialogId`**: The unique ID for the entire call conversation.
2.  **`segmentId`**: The specific ID for the media segment within that dialog.

---

## Main Endpoint: Download Recording

Once you have the necessary IDs from the metadata report, use the following endpoint to stream the `.WAV` audio file.

`GET https://engage.ringcentral.com/voice/api/cx/integration/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/recordings/dialogs/{dialogId}/segments/{segmentId}`

### Path Parameters

| Parameter | Type | Requirement | Description |
| :--- | :--- | :--- | :--- |
| **`rcAccountId`** | String | **Required** | Your primary RingCentral Account ID. |
| **`subAccountId`** | String | **Required** | The RingCX sub-account ID where the call occurred. |
| **`dialogId`** | String | **Required** | The ID of the dialog (obtained via interaction-metadata). |
| **`segmentId`** | String | **Required** | The ID of the segment (obtained via interaction-metadata). |

### Response Details
The API returns a binary stream of the recording.

| Status | Code | Description |
| :--- | :--- | :--- |
| **OK** | 200 | Success. The response body contains the audio stream. |
| **Unauthorized**| 401 | Authentication failed or token is invalid. |
| **Forbidden** | 403 | Insufficient permissions to access this specific recording. |
| **Not Found** | 404 | The specified dialog or segment ID does not exist. |

---

## Implementation Strategy

### Recommended Pattern
1.  **Poll Metadata:** Call the `interaction-metadata` endpoint to find segments that ended at least 15 minutes ago.
2.  **Extract Identifiers:** Parse the JSON response to map the `dialogId` and `segmentId` for each record.
3.  **Stream Media:** Call the Download Recording endpoint using the path parameters to retrieve the `.WAV` file.

!!! [!IMPORTANT]
    **Rate Limiting:** Metadata and reporting endpoints are typically limited to **2 calls per minute**. To maintain stability, implement **exponential backoff** when encountering `429` (Too Many Requests) errors.

### Sample Implementation (Python)

```python
import requests

# Configuration
BASE_URL = "https://engage.ringcentral.com"
ACCESS_TOKEN = "YOUR_TOKEN"

def download_recording(rc_account_id, sub_account_id, dialog_id, segment_id):
    # Construct the path-based URL
    url = f"{BASE_URL}/cx/integration/v1/accounts/{rc_account_id}/sub-accounts/{sub_account_id}/recordings/dialogs/{dialog_id}/segments/{segment_id}"
    
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Accept': 'audio/wav'
    }
    
    # Request the stream
    response = requests.get(url, headers=headers, stream=True)
    
    if response.status_code == 200:
        file_name = f"recording_{segment_id}.wav"
        with open(file_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=4096):
                f.write(chunk)
        print(f"Download complete: {file_name}")
    else:
        print(f"Failed to retrieve recording. Status: {response.status_code}")
        print(response.text)
```

---


