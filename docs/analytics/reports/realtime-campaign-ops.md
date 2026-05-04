# Real-Time Campaign Operations API

The Real-Time Campaign Operations APIs allow campaign managers and operations teams to monitor live outbound dialing activity and IVR self-service traffic so they can assess campaign pacing, diagnose dial outcome issues, and track containment rates without waiting for end-of-day reports.

## Strategic Overview

These endpoints surface the real-time state of your outbound campaigns and IVR applications. While historical reporting APIs provide post-hoc analysis, these endpoints answer operational questions in the moment: Is this campaign agent-starved? What is my current human answer rate? How many callers are self-serving through IVR versus transferring to a queue?

### Key Use Cases

* **Campaign Pacing Dashboards:** Monitor active calls, agent availability, and lead state counts in real time to identify campaigns that are under- or over-dialing.
* **Dial Outcome Monitoring:** Track live answer rate, AMD detection, and abandon rate to catch campaign health issues as they develop.
* **IVR Containment Tracking:** Measure how many callers are completing IVR self-service flows versus transferring to a live agent queue.

### Real-Time vs. Latency Expectations

* **Data Availability:** Snapshot data is updated continuously. The `lastUpdate` field on each record reflects the timestamp of the most recent update for that entity.
* **Counter Reset:** All daily counters reset at midnight in the account's configured timezone — not UTC.

### Required Permissions & Scopes

#### 1. Configure OAuth Scopes

To authenticate, your application must be configured with the following permission in the [Developer Portal](https://developers.ringcentral.com/my-account.html#/applications):

* **`ReadAccounts`**: Required to validate account context and access real-time platform data.

#### 2. Enable Platform Permissions

The authenticating user must have reporting access enabled in the RingCX Admin portal:

1. Log in to **RingCX Admin**.
2. Navigate to **Users** > **Administrators**.
3. Select the target user and ensure the appropriate reporting rights are enabled.

!!! warning "Common Authorization Errors"
    If the user lacks the necessary platform permissions, the API will return:
    ```json
    {
        "errorCode": "access.denied.exception",
        "generalMessage": "You do not have permission to access this resource",
        "timestamp": 1611847650696
    }
    ```

!!! important "Rate Limiting & Stability"
    * **Limit:** Standard platform rate limiting applies at 120 requests per minute across all real-time endpoints.
    * **Strategy:** Poll at a **10–30 second interval** for live operations dashboards. Polling faster than 5 seconds is not recommended and may result in `429 Too Many Requests` errors. Implement exponential backoff on 429 responses.

---

## Outbound Campaign Stats

Returns real-time dial activity and outcome counters for every outbound campaign in the account.

`GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/realTimeData/outbound`

### Request Parameters

| Parameter | Type | Requirement | Description |
| --- | --- | --- | --- |
| `accountId` | String | **Required** | The unique identifier for the RingCX sub-account. |

### Response Details

Returns an array of `OutboundStats` objects — one per campaign. Key fields include `active` (calls in progress), `ready` and `pending` lead counts, `staffed` and `available` agent counts, and daily dial outcomes broken out by result type (`answer`, `machine`, `noanswer`, `abandon`, etc.).

A few particularly useful derived metrics:

* **Agent occupancy:** If `available` drops to zero while `ready` is non-zero, the campaign is agent-starved and leads are backing up.
* **Human answer rate:** `answer` ÷ `connects` gives a live view of the proportion of calls reaching a live person.
* **AMD rate:** `machine` ÷ `connects` shows the proportion of calls landing on voicemail — a sudden spike may indicate list quality issues.

??? info "View Full OutboundStats Schema"

    **Identity**

    | Field | Type | Description |
    | --- | --- | --- |
    | `campaignId` | Integer | Unique campaign identifier. |
    | `campaignName` | String | Campaign display name. |
    | `accountId` | String | Sub-account the campaign belongs to. |
    | `dialGroupId` | Integer | Dial group the campaign runs under. |
    | `dialGroupName` | String | Dial group display name. |
    | `lastUpdate` | String (date-time) | Timestamp of the most recent data refresh. |

    **Live Activity**

    | Field | Type | Description |
    | --- | --- | --- |
    | `active` | Integer | Calls currently in progress. |
    | `ready` | Integer | Leads in a ready-to-dial state. |
    | `pending` | Integer | Leads staged and pending dialing. |
    | `complete` | Integer | Leads marked complete today. |
    | `other` | Integer | Leads in other non-standard states. |

    **Staffing**

    | Field | Type | Description |
    | --- | --- | --- |
    | `staffed` | Integer | Agents logged in for this campaign. |
    | `available` | Integer | Agents in an available state for this campaign. |

    **Daily Dial Outcomes** *(reset at midnight in the account's configured timezone)*

    | Field | Type | Description |
    | --- | --- | --- |
    | `connects` | Integer | Total connects today (any outcome where the call was answered). |
    | `answer` | Integer | Live-person answer connects today. |
    | `noanswer` | Integer | No-answer outcomes today. |
    | `machine` | Integer | Answering machine detections today. |
    | `busy` | Integer | Busy signal outcomes today. |
    | `intercept` | Integer | Intercept (SIT tone / number not in service) outcomes today. |
    | `fax` | Integer | Fax machine detections today. |
    | `abandon` | Integer | Calls abandoned today — connected but no agent was available. |
    | `dnc` | Integer | Do-not-call list hits today. |
    | `notHumanAnswers` | Integer | Combined non-human outcomes today: `machine` + `fax` + `intercept`. |
    | `successDispositions` | Integer | Calls dispositioned with a success outcome today. |
    | `totalTalkTime` | Integer (int64) | Cumulative agent talk time today, in seconds. |

---

## IVR Application Stats

Returns real-time traffic counts for every Visual IVR application in the account, enabling monitoring of self-service load and agent handoff volumes.

`GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/realTimeData/ivr`

### Request Parameters

| Parameter | Type | Requirement | Description |
| --- | --- | --- | --- |
| `accountId` | String | **Required** | The unique identifier for the RingCX sub-account. |

### Response Details

Returns an array of `IvrStats` objects — one per IVR application. Key fields include `active` (callers currently in the IVR), `presented` (total calls entered today), and transfer destination counters (`transferGate`, `transferCloud`, `transferTrac`) that let you calculate a real-time self-service containment rate:

```
containment = (presented - transferGate - transferCloud - transferTrac) / presented
```

??? info "View Full IvrStats Schema"

    **Identity**

    | Field | Type | Description |
    | --- | --- | --- |
    | `visualIvrId` | Integer | Unique IVR application identifier. |
    | `ivrGroupId` | Integer | IVR group identifier. |
    | `accountId` | String | Sub-account the IVR belongs to. |
    | `visualIvrName` | String | IVR application display name. |
    | `ivrGroupName` | String | IVR group display name. |
    | `lastUpdate` | String (date-time) | Timestamp of the most recent data refresh. |

    **Live Activity**

    | Field | Type | Description |
    | --- | --- | --- |
    | `active` | Integer | Callers currently traversing this IVR application. |

    **Daily Counters** *(reset at midnight in the account's configured timezone)*

    | Field | Type | Description |
    | --- | --- | --- |
    | `presented` | Integer | Total calls that entered this IVR today. |
    | `connected` | Integer | Total calls that completed the IVR flow and connected today. |
    | `transferGate` | Integer | Calls transferred from this IVR to an inbound queue today. |
    | `transferCloud` | Integer | Calls transferred from this IVR to a cloud destination today. |
    | `transferTrac` | Integer | Calls transferred from this IVR via TRAC today. |

---

## Implementation Strategy

For campaign operations dashboards, poll both endpoints on the same cycle to correlate outbound performance with IVR activity.

### Recommended Pattern

Poll both endpoints on a consistent interval and use `lastUpdate` on each record to detect whether data has changed before refreshing display elements.

!!! important "Rate Limiting & Stability"
    * **Limit:** 120 requests per minute across all real-time endpoints combined.
    * **Strategy:** A 15-second polling interval across both endpoints consumes 8 requests per minute. Do not poll faster than 5 seconds. Implement exponential backoff on `429 Too Many Requests` responses.

### Sample Implementation (Python)

```python
import requests
import time

BASE_URL = "https://ringcx.ringcentral.com/voice/api/v1/admin/accounts"
ACCOUNT_ID = "12345"
POLL_INTERVAL_SECONDS = 15

def fetch_campaign_snapshot(token):
    """Fetches outbound campaign stats and IVR stats in one pass."""
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }

    endpoints = {
        'outbound': f"{BASE_URL}/{ACCOUNT_ID}/realTimeData/outbound",
        'ivr':      f"{BASE_URL}/{ACCOUNT_ID}/realTimeData/ivr",
    }

    snapshot = {}
    for key, url in endpoints.items():
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            snapshot[key] = response.json()
        elif response.status_code == 429:
            print(f"Rate limited on {key} — backing off.")
            time.sleep(5)
        else:
            print(f"Error fetching {key}: {response.status_code}")

    return snapshot

def monitor(token):
    while True:
        snapshot = fetch_campaign_snapshot(token)

        # Example: flag agent-starved campaigns
        for campaign in snapshot.get('outbound', []):
            if campaign.get('available', 0) == 0 and campaign.get('ready', 0) > 0:
                print(f"ALERT: {campaign['campaignName']} — agent-starved, {campaign['ready']} leads waiting")

        # Example: log IVR containment rate
        for ivr in snapshot.get('ivr', []):
            presented = ivr.get('presented', 0)
            if presented > 0:
                transfers = ivr.get('transferGate', 0) + ivr.get('transferCloud', 0) + ivr.get('transferTrac', 0)
                containment = round((presented - transfers) / presented * 100, 1)
                print(f"{ivr['visualIvrName']} containment: {containment}%")

        time.sleep(POLL_INTERVAL_SECONDS)

if __name__ == "__main__":
    monitor("YOUR_ACCESS_TOKEN")
```
