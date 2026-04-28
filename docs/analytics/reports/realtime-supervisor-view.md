# Real-Time Supervisor View API

The Real-Time Supervisor View APIs allow supervisors and operations teams to monitor live agent activity and queue health across voice and digital channels so they can manage staffing, intervene on at-risk queues, and maintain service levels without waiting for a scheduled report.

## Strategic Overview

These endpoints are the data foundation for live wallboards and supervisor monitoring dashboards. Unlike historical reporting APIs which aggregate completed interactions, these endpoints return point-in-time snapshots of what is happening right now across agents and queues.

### Key Use Cases

* **Live Wallboard Displays:** Surface agent states, queue depths, and staffing levels on a real-time operations display visible to the floor.
* **Supervisor Intervention:** Identify agents stuck in pending disposition, queues with zero available agents, or calls exceeding SLA thresholds before they escalate.
* **Staffing Validation:** Cross-reference `staffed` vs. `available` counts against scheduled headcount to detect phantom logins or agents who have broken state.

### Real-Time vs. Latency Expectations

* **Data Availability:** Snapshot data is updated continuously. The `lastUpdate` field on each record reflects the timestamp of the most recent state change for that entity.
* **Counter Reset:** Daily counters (abandons, SLA pass/fail, etc.) reset at midnight in the account's configured timezone — not UTC. Agent session counters reset on logout.

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
    * **Strategy:** Poll at a **10–30 second interval** for wallboard use cases. Polling faster than 5 seconds is not recommended and may result in `429 Too Many Requests` errors. Implement exponential backoff on 429 responses.

---

## Agent States

Returns a live snapshot of every agent currently logged in to the account — their current state, active call details, and session-level performance counters.

`GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/realTimeData/agent`

### Request Parameters

| Parameter | Type | Requirement | Description |
| --- | --- | --- | --- |
| `accountId` | String | **Required** | The unique identifier for the RingCX sub-account. |

### Response Details

Returns an array of `AgentStats` objects — one per logged-in agent session. Key fields include the agent's current `agentState` (e.g., `AVAILABLE`, `ON_CALL`, `AWAY`, `WRAP_UP`), `stateTime` in seconds, live call identifiers (`callUii`, `callAni`, `callDnis`), and session counters (`callsHandled`, `totalTalkTime`) that reset on logout.

??? info "View Full AgentStats Schema"

    **Identity & Assignment**

    | Field | Type | Description |
    | --- | --- | --- |
    | `agentId` | Integer | Unique agent identifier. |
    | `accountId` | String | Sub-account the agent belongs to. |
    | `accountName` | String | Sub-account display name. |
    | `firstName` | String | Agent's first name. |
    | `lastName` | String | Agent's last name. |
    | `username` | String | Agent login username. |
    | `email` | String | Agent email address. |
    | `agentType` | String | Agent type (e.g., `AGENT`, `SUPERVISOR`). |
    | `agentGroupId` | Integer | Agent group ID. |
    | `agentGroupName` | String | Agent group display name. |
    | `agentLoginId` | Integer | Current login session ID. |
    | `agentPhone` | String | Phone number the agent is logged in with. |
    | `profileName` | String | Skill profile currently assigned. |

    **Current State**

    | Field | Type | Description |
    | --- | --- | --- |
    | `agentState` | String | Current state (e.g., `AVAILABLE`, `ON_CALL`, `AWAY`, `WRAP_UP`). |
    | `agentLoginType` | String | How the agent is logged in. |
    | `stateTime` | Integer | Seconds the agent has been in the current state. |
    | `loginTime` | Integer | Seconds since the agent logged in. |
    | `pendingDisposition` | Integer | `1` if the agent is pending disposition, `0` otherwise. |
    | `pendingDispositionTime` | Integer | Seconds the agent has been pending disposition. |
    | `isOffhook` | Integer | `1` if the agent's phone line is currently off-hook. |
    | `isGhostLogin` | Integer | `1` if this is a ghost or phantom login. |
    | `isDequeueAgent` | Integer | `1` if this agent is the dequeue agent for an active interaction. |
    | `lastUpdate` | String (date-time) | Timestamp of the most recent state change. |

    **Active Call** *(populated when agent is on a call, empty otherwise)*

    | Field | Type | Description |
    | --- | --- | --- |
    | `callUii` | String | Unique interaction identifier for the active call. |
    | `callAni` | String | ANI (caller's number) of the active call. |
    | `callDnis` | String | DNIS (dialed number) of the active call. |
    | `gateId` | Integer | Inbound queue the call arrived on, if inbound. |
    | `campaignId` | Integer | Outbound campaign the call belongs to, if outbound. |
    | `loginDialGroupId` | Integer | Dial group the agent is logged into, if outbound. |
    | `callSource` | String | Source classification of the active call. |
    | `callSourceDesc` | String | Human-readable call source description. |

    **Session Counters** *(reset on logout, not at midnight)*

    | Field | Type | Description |
    | --- | --- | --- |
    | `callsHandled` | Integer | Total calls handled this session. |
    | `rna` | Integer | Ring-no-answer count this session. |
    | `totalTalkTime` | Integer | Total talk time in seconds this session. |

---

## Inbound Queue Health (ACD)

Returns real-time statistics for every inbound voice queue in the account, including live activity, staffing levels, and daily performance counters.

`GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/realTimeData/inbound`

### Request Parameters

| Parameter | Type | Requirement | Description |
| --- | --- | --- | --- |
| `accountId` | String | **Required** | The unique identifier for the RingCX sub-account. |

### Response Details

Returns an array of `AcdStats` objects — one per inbound queue. Key fields include `inQueue` (calls waiting), `longestInQueue` (seconds the oldest waiting call has been holding), `staffed` and `available` agent counts, and daily SLA counters (`slaPass`, `slaFail`) that reset at midnight.

??? info "View Full AcdStats Schema"

    **Identity & Status**

    | Field | Type | Description |
    | --- | --- | --- |
    | `gateId` | Integer | Unique queue (gate) identifier. |
    | `gateGroupId` | Integer | Queue group identifier. |
    | `accountId` | String | Sub-account the queue belongs to. |
    | `gateName` | String | Queue display name. |
    | `groupName` | String | Queue group display name. |
    | `schedule` | String | Name of the active schedule. |
    | `scheduleOverride` | String | Active schedule override, if one is in effect. |
    | `state` | String | Current queue state (e.g., open, closed, override). |
    | `lastUpdate` | String (date-time) | Timestamp of the most recent data refresh. |

    **Live Activity**

    | Field | Type | Description |
    | --- | --- | --- |
    | `active` | Integer | Calls currently in conversation with an agent. |
    | `inQueue` | Integer | Calls currently waiting in queue. |
    | `routing` | Integer | Calls ringing an agent but not yet answered. |
    | `longestInQueue` | Integer | Seconds the longest-waiting call has been in queue. |

    **Staffing**

    | Field | Type | Description |
    | --- | --- | --- |
    | `staffed` | Integer | Agents logged in and assigned to this queue. |
    | `available` | Integer | Agents in an available state for this queue. |

    **Daily Counters** *(reset at midnight in the account's configured timezone)*

    | Field | Type | Description |
    | --- | --- | --- |
    | `presented` | Integer | Total calls offered today. |
    | `accepted` | Integer | Total calls answered today. |
    | `abandoned` | Integer | Total calls abandoned today. |
    | `deflected` | Integer | Total calls deflected today. |
    | `shortAbandon` | Integer | Abandons within the short-abandon threshold, typically excluded from service level calculations. |
    | `slaPass` | Integer | Calls answered within the configured SLA threshold today. |
    | `slaFail` | Integer | Calls that missed the SLA threshold today. |
    | `shortCall` | Integer | Calls below the short-call duration threshold today. |
    | `longCall` | Integer | Calls above the long-call duration threshold today. |
    | `successDispositions` | Integer | Calls dispositioned with a success outcome today. |
    | `totalQueueTime` | Integer (int64) | Cumulative queue wait time today, in seconds. |
    | `totalAnswerTime` | Integer (int64) | Cumulative time from queue entry to answer today, in seconds. |
    | `totalTalkTime` | Integer (int64) | Cumulative talk time today, in seconds. |
    | `totalAbandonTime` | Integer (int64) | Cumulative time callers waited before abandoning today, in seconds. |

---

## Chat Queue Health

Returns real-time statistics for every chat queue in the account, mirroring the structure of the inbound voice endpoint for digital channels.

`GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/realTimeData/chat`

### Request Parameters

| Parameter | Type | Requirement | Description |
| --- | --- | --- | --- |
| `accountId` | String | **Required** | The unique identifier for the RingCX sub-account. |

### Response Details

Returns an array of `ChatStats` objects — one per chat queue. Key fields mirror the inbound voice schema: `inQueue`, `longestInQueue`, `staffed`, `available`, and daily counters including `totalChatTime` which accumulates active session duration.

??? info "View Full ChatStats Schema"

    **Identity & Status**

    | Field | Type | Description |
    | --- | --- | --- |
    | `chatQueueId` | Integer | Unique chat queue identifier. |
    | `chatQueueGroupId` | Integer | Chat queue group identifier. |
    | `accountId` | String | Sub-account the queue belongs to. |
    | `chatQueueName` | String | Chat queue display name. |
    | `chatQueueGroupName` | String | Chat queue group display name. |
    | `schedule` | String | Name of the active schedule. |
    | `scheduleOverride` | String | Active schedule override, if one is in effect. |
    | `lastUpdate` | String (date-time) | Timestamp of the most recent data refresh. |

    **Live Activity**

    | Field | Type | Description |
    | --- | --- | --- |
    | `active` | Integer | Chats currently in an active session with an agent. |
    | `inQueue` | Integer | Chats currently waiting in queue. |
    | `routing` | Integer | Chats being routed to an agent. |
    | `longestInQueue` | Integer | Seconds the longest-waiting chat has been in queue. |

    **Staffing**

    | Field | Type | Description |
    | --- | --- | --- |
    | `staffed` | Integer | Agents logged in and assigned to this chat queue. |
    | `available` | Integer | Agents in an available state for this chat queue. |

    **Daily Counters** *(reset at midnight in the account's configured timezone)*

    | Field | Type | Description |
    | --- | --- | --- |
    | `presented` | Integer | Total chats offered today. |
    | `accepted` | Integer | Total chats accepted today. |
    | `abandoned` | Integer | Total chats abandoned today. |
    | `deflected` | Integer | Total chats deflected today. |
    | `totalQueueTime` | Integer (int64) | Cumulative queue wait time today, in seconds. |
    | `totalAnswerTime` | Integer (int64) | Cumulative time from queue entry to acceptance today, in seconds. |
    | `totalChatTime` | Integer (int64) | Cumulative active chat duration today, in seconds. |
    | `totalAbandonTime` | Integer (int64) | Cumulative time interactions waited before abandoning today, in seconds. |

---

## Implementation Strategy

For most supervisor dashboards, a single polling loop fetches all three endpoints in sequence and updates the display on each cycle.

### Recommended Pattern

Poll all three endpoints on a consistent interval and use `lastUpdate` on each record to detect whether an entity's state has actually changed before triggering a UI update.

!!! important "Rate Limiting & Stability"
    * **Limit:** 120 requests per minute across all real-time endpoints combined.
    * **Strategy:** A 15-second polling interval across three endpoints consumes 12 requests per minute — well within limits. Do not poll faster than 5 seconds. Implement exponential backoff on `429 Too Many Requests` responses.

!!! warning "SLA Threshold Alerting"
    `longestInQueue` is the most actionable signal for SLA risk on both inbound and chat queues. If this value exceeds your SLA target and `available` is zero, the next caller in queue will breach SLA before an agent becomes free.

### Sample Implementation (Python)

```python
import requests
import time

BASE_URL = "https://ringcx.ringcentral.com/voice/api/v1/admin/accounts"
ACCOUNT_ID = "12345"
POLL_INTERVAL_SECONDS = 15

def fetch_supervisor_snapshot(token):
    """Fetches agent states, inbound queue stats, and chat queue stats in one pass."""
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }

    endpoints = {
        'agents':  f"{BASE_URL}/{ACCOUNT_ID}/realTimeData/agent",
        'inbound': f"{BASE_URL}/{ACCOUNT_ID}/realTimeData/inbound",
        'chat':    f"{BASE_URL}/{ACCOUNT_ID}/realTimeData/chat",
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
        snapshot = fetch_supervisor_snapshot(token)

        # Example: flag any inbound queue where longest wait exceeds 60 seconds
        for queue in snapshot.get('inbound', []):
            if queue.get('longestInQueue', 0) > 60:
                print(f"ALERT: {queue['gateName']} — longest wait {queue['longestInQueue']}s")

        time.sleep(POLL_INTERVAL_SECONDS)

if __name__ == "__main__":
    monitor("YOUR_ACCESS_TOKEN")
```
