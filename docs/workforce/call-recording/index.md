# Call Recording APIs

The Call Recording APIs allow developers to retrieve and manage audio files generated during voice interactions. This API provides access to both single-channel (mono) and dual-channel (stereo/perspective) recordings, enabling organizations to perform quality assurance, maintain compliance archives, and conduct sentiment analysis.

## Strategic Overview

Call recordings are essential for maintaining accountability and improving agent performance. By programmatically retrieving these files, organizations can automate the ingestion of audio data into third-party speech analytics tools, long-term storage buckets, or specialized Quality Management (QM) platforms.

### Key Use Cases

* **Compliance Archiving:** Automatically move recordings to secure, long-term storage to meet regulatory requirements (e.g., PCI or HIPAA).
* **Quality Management (QM):** Feed audio files into evaluation platforms for manual or automated scoring of agent performance.
* **Speech Analytics:** Integrate with AI-driven tools to perform sentiment analysis and automated categorization of customer intent.

### Real-Time vs. Latency Expectations

Retrieving recordings requires a specific waiting period to allow the system to finalize, encode, and index the audio media.

* **Data Availability:** For interaction metadata and recordings, it is recommended to allow a **15-minute window** for all media processing to complete.
* **Historical Access:** Reports used to discover recording metadata may take several minutes to reflect new records; periodic polling is recommended.

### Required Permissions & Scopes

Access to recording media is governed by account-level security and explicit administrative permissions.

#### 1. Configure OAuth Scopes

To successfully authenticate, your application must be configured with the following permission in the [Developer Portal](https://developers.ringcentral.com/my-account.html#/applications):

* **`ReadAccounts`**: Required to validate the account context and authorize media stream access.

#### 2. Enable Platform Permissions

The ability to access specific recording types depends on your account configuration:

1. Log in to **RingCX Admin**.
2. **Permissions:** Ensure the user has **READ on Account** permissions within their assigned Rights Document.
3. **For Stereo (Agent) Recordings:** These must be **manually activated** by your RingCentral representative.

---

## API Discovery

To retrieve a recording, you must first obtain the unique metadata associated with the call, specifically the storage parameters (bucket, region, and file path). These are discovered via the **interactionMetadata** report.

For a detailed walkthrough on discovering metadata, please refer to the [Agent Segment Metadata API Guide](../../integration/reports-orig.md#agent-segment-metadata).

`POST /voice/api/integration/v1/admin/reports/accounts/{subAccountId}/interactionMetadata`

### Request Body / Parameters

| Parameter | Type | Requirement | Description |
| --- | --- | --- | --- |
| `subAccountId` | String | **Required** | The unique identifier for the RingCX sub-account. |
| `segmentEndTime` | String | **Required** | Start date and time for the logging interval (ISO-8601). |
| `timeInterval` | Integer | **Required** | Interval length in seconds (Maximum 3600). |
| `timeZone` | String | **Required** | Timezone name used for report generation. |

---

## Main Endpoint: Download Recording

This endpoint returns a call recording stream (typically a `.WAV` file).

`GET /voice/api/internal/v1/calls/recordings`

### Request Body / Parameters

| Parameter | Type | Requirement | Description |
| --- | --- | --- | --- |
| `v` | String | **Required** | The API version. |
| `accountId` | String | **Required** | The unique identifier for the sub-account. |
| `region` | String | **Required** | The AWS region where the file is stored. |
| `bucket` | String | **Required** | The storage bucket name. |
| `file` | String | **Required** | The full path and filename of the `.WAV` file. |
| `compliance` | Boolean | Optional | Set to `true` to retrieve records from the compliance-protected store. |

### Response Details

The API returns a binary stream of the recording.

| Status | Code | Description |
| --- | --- | --- |
| **OK** | 200 | Successful operation. The body contains the audio stream. |
| **Unauthorized** | 401 | Authentication failed or token is invalid. |
| **Forbidden** | 403 | User does not have permission to access this recording. |
| **Not Found** | 404 | The specified recording file does not exist. |

---

## Implementation Strategy

### Recommended Pattern

1. **Poll Metadata:** Use the `interactionMetadata` endpoint to find calls that ended at least 15 minutes ago.
2. **Extract IDs:** Capture the specific storage parameters (bucket, region, file) provided in the metadata response.
3. **Stream Media:** Use those parameters to call the `recordings` endpoint to retrieve the `.WAV` file.

!!! important "Rate Limiting & Stability"

* **Limit:** Requests are limited to **2 calls per minute** for reporting/metadata endpoints.
* **Strategy:** Implement **exponential backoff** on `429` (Too Many Requests) errors.

### Sample Implementation (Python)

```python
import requests

# Base configuration
BASE_URL = "https://engage.ringcentral.com/voice/api"
ACCESS_TOKEN = "YOUR_TOKEN"

def download_recording(account_id, region, bucket, file_path):
    endpoint = f"{BASE_URL}/internal/v1/calls/recordings"
    
    params = {
        'v': '1',
        'accountId': account_id,
        'region': region,
        'bucket': bucket,
        'file': file_path
    }
    
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    
    response = requests.get(endpoint, headers=headers, params=params, stream=True)
    
    if response.status_code == 200:
        with open('call_recording.wav', 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print("Download complete.")
    else:
        print(f"Failed: {response.status_code}")

```

---

## Appendix: Recording Types

??? info "View Supported Recording Types"

| Type | Channel | Description |
| --- | --- | --- |
| **Single Channel** | Mono | A single audio track containing both the agent and customer mixed. |
| **Dual Channel** | Stereo | Also known as "Perspective" recordings. The agent and customer are on separate audio channels, preferred for high-accuracy transcription. |