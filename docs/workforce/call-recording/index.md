# Call Recording APIs

The Call Recording APIs allow developers to retrieve and manage audio files generated during voice interactions. This API provides access to both single-channel (mono) and dual-channel (stereo/perspective) recordings, enabling organizations to perform quality assurance, maintain compliance archives, and conduct sentiment analysis.

## Strategic Overview

Call recordings are essential for maintaining accountability and improving agent performance. By programmatically retrieving these files, organizations can automate the ingestion of audio data into third-party speech analytics tools, long-term storage buckets (S3/Azure), or specialized Quality Management (QM) platforms.

### Key Use Cases

* **Compliance Archiving:** Automatically move recordings to secure, long-term storage to meet regulatory requirements (e.g., PCI or HIPAA).
* **Quality Management (QM):** Feed audio files into evaluation platforms for manual or automated scoring of agent performance.
* **Speech Analytics:** Integrate with AI-driven tools to perform sentiment analysis, keyword spotting, and automated categorization of customer intent.

### Real-Time vs. Latency Expectations

Retrieving recordings requires a specific waiting period to allow the system to finalize, encode, and index the audio media.

* **Real-Time Trigger:** The **End Call Event** notification is sent **1-3 seconds** after a call ends and contains the initial `recording_url`.
* **Encoding Latency:** While the URL is generated immediately, the actual file may take **1-2 minutes** to become valid and accessible, depending on the call length.
* **Historical Access:** The Agent Segment Metadata report may take several minutes to reflect new records; periodic polling is recommended.

### Required Permissions & Scopes

Access to recording media is governed by account-level security and explicit administrative permissions.

#### 1. Configure OAuth Scopes

To successfully authenticate, your application must be configured with the following permission in the [Developer Portal](https://developers.ringcentral.com/my-account.html#/applications):

* **`ReadAccounts`**: Required to validate the account context and authorize media stream access.

#### 2. Enable Platform Permissions

The ability to access specific recording types depends on your account configuration:

1. Log in to **RingCX Admin**.
2. **For Stereo (Agent) Recordings:** Navigate to **Account Settings**. These must be **manually activated** by your RingCentral representative.
3. **For API Access:** Ensure the user has **READ on Account** permissions within their assigned Rights Document.

---

## API Discovery

To retrieve a recording, you must first obtain the unique metadata associated with the call (such as the `bucket`, `region`, and `file` name).

| Source | Method | Field to Capture |
| --- | --- | --- |
| **End Call Event** | Webhook | `recording_url` |
| **Global Call Type Report** | REST API | `recording_url` |
| **Agent Segment Metadata** | REST API | `Segment Recording URL` |

---

## Main Endpoint: Download Recording

This endpoint returns a call recording stream (typically a `.WAV` file).

`GET https://[cluster]-recordings.[domain]/api/v1/calls/recordings`

### Request Parameters

| Parameter | Type | Requirement | Description |
| --- | --- | --- | --- |
| `v` | Integer | **Required** | The API version (usually `1`). |
| `accountId` | String | **Required** | The unique identifier for the sub-account. |
| `region` | String | **Required** | The AWS region where the file is stored (e.g., `us-east-1`). |
| `bucket` | String | **Required** | The storage bucket name (e.g., `c02-recordings`). |
| `file` | String | **Required** | The full path and filename of the `.WAV` file. |
| `compliance` | Boolean | Optional | Set to `true` to retrieve records from the compliance-protected store. |

**Example Request:**

```html
GET https://c02-recordings.virtualacd.biz/api/v1/calls/recordings/?v=1&accountId=15300002&bucket=c02-recordings&region=us-east-1&compliance=false&file=15300002/202007/30/202007302136360132130000036446-1.WAV

```

### Response Details

The API returns a binary stream of the recording.

| Status | Code | Description |
| --- | --- | --- |
| **OK** | 200 | Successful operation. The body contains the audio stream. |
| **Accepted** | 202 | Recording is still encoding; try again in 60 seconds. |
| **Not Found** | 404 | The specified recording file does not exist. |

---

## Implementation Strategy

### Recommended Pattern

1. **Subscribe to Webhooks:** Use [End Call Events](https://www.google.com/search?q=../../notifications/wfm/payload-wfm.md%23end-call-events) to receive the `recording_url` immediately.
2. **Queue for Processing:** Do not attempt to download immediately. Place the URL in a processing queue.
3. **Delayed Polling:** Trigger the download worker **2 minutes** after the call ends to ensure encoding is finished.
4. **Error Handling:** If you receive a `404` or an empty body, implement exponential backoff and retry up to 3 times.

!!! important "Rate Limiting & Stability"
  * **Limit:** Standard platform limits apply to the metadata reports; however, the media server itself is optimized for streaming.
  * **Strategy:** Implement exponential backoff for `503` (Service Unavailable) or `429` (Too Many Requests) errors.

### Sample Implementation (Python)

```python
import requests
import time

# Example parameters from an End Call Event
params = {
    'v': '1',
    'accountId': '15300002',
    'region': 'us-east-1',
    'bucket': 'c02-recordings',
    'file': '15300002/202007/30/20200730213636-1.WAV'
}

url = "https://c02-recordings.virtualacd.biz/api/v1/calls/recordings"

def download_recording(target_url, request_params):
    # Wait for encoding (recommended 1-2 minutes)
    print("Waiting for media encoding...")
    time.sleep(120) 
    
    response = requests.get(target_url, params=request_params, stream=True)
    
    if response.status_code == 200:
        with open('call_recording.wav', 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print("Download complete.")
    else:
        print(f"Error: {response.status_code}")

download_recording(url, params)

```

---

## Appendix: Recording Types

??? info "View Supported Recording Types"

  | Type | Channel | Description |
  | :--- | :--- | :--- |
  | **Single Channel** | Mono | A single audio track containing both the agent and customer mixed. |
  | **Dual Channel** | Stereo | Also known as "Perspective" recordings. The agent and customer are on separate audio channels, which is preferred for high-accuracy transcription. |

