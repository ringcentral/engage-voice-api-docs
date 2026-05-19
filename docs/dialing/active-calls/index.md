# Active Call Management APIs

The Active Call Management APIs allow developers and supervisors to programmatically observe and control voice calls while they are still in progress on the RingCX platform. Where reporting APIs surface what *happened* on a call after the fact, this API set governs what is *happening right now* — letting an integration list calls in flight, attach a supervisor session, toggle recording, set dispositions, and terminate calls or sessions on demand.

## Strategic Overview

Live call control is what separates a passive contact center integration from an operational one. By wrapping these endpoints, you can build supervisor consoles, automated coaching tools, or compliance enforcement systems that act on calls as they unfold rather than after they archive.

### Key Use Cases

* **Supervisor Monitoring & Coaching:** Build a custom supervisor dashboard that lets managers join active agent calls in `MONITOR`, `COACHING`, or `BARGEIN` mode without leaving your application.
* **Compliance-Driven Recording Control:** Programmatically pause and resume recording (for example, when a customer reads a credit card number) to satisfy PCI requirements without manual agent intervention.
* **Automated Outbound Dialing:** Trigger outbound calls from an agent's seat directly from a CRM or workflow engine, eliminating manual dialing and call-logging steps.
* **Forced Termination & Re-Queueing:** Programmatically end calls that exceed policy limits, or re-queue an active call to a different gate when an agent escalates.

### Real-Time vs. Latency Expectations

Unlike the analytics and audit endpoints in the platform, these APIs are **synchronous and real-time**. Each request acts on the live call state immediately and returns a boolean indicating whether the requested action succeeded.

* **Data Availability:** Real-time. State changes (hangup, recording toggle, disposition) take effect on the live call within seconds.
* **Call Lifetime:** Calls are addressable through this API only while their `callState` is `ACTIVE`. Once the call moves to the archived (READ-ONLY) state, control endpoints will no longer apply. Use the `pingCall` endpoint to keep a call active while pending operations finish.

### Required Permissions & Scopes

#### 1. Configure OAuth Scopes

To authenticate, your application must be configured with the following permission in the [Developer Portal](https://developers.ringcentral.com/my-account.html#/applications):

* **`ReadAccounts`**: Required to validate the account context and authorize calls against the active call endpoints.

!!! warning "Warning"
    `ReadAccounts` is the only OAuth scope that materially affects RingCX APIs. The granular control over which calls a user can monitor, terminate, or re-queue is governed by RingCX Admin platform permissions, not OAuth scopes.

For a detailed walkthrough on exchanging your JWT for an access token, please refer to the [RingCentral Authentication Guide](https://developers.ringcentral.com/engage/voice/guide/authentication/auth-ringcentral).

#### 2. Enable RingCX Admin Permissions

The user authenticating the app must hold the appropriate supervisor permissions in RingCX Admin to act on calls owned by other agents.

1. Log in to **RingCX Admin**.
2. Navigate to **Users** > **Administrators**.
3. Select the target user and ensure the relevant call control permissions (e.g. **Monitor calls**, **Barge-in**, **Coaching**) are enabled.

!!! warning "Common Authorization Errors"
    If the application has the correct scope but the user lacks the platform permission, the API returns:
    ```json
    {
        "errorCode": "access.denied.exception",
        "generalMessage": "You do not have permission to access this resource",
        "details": "",
        "requestUri": "/api/v1/admin/accounts/{accountId}/activeCalls/list - GET",
        "timestamp": <TIMESTAMP>
    }
    ```

### Important Technical Constraints

* **Mandatory Account Context:** Every endpoint requires an `accountId` in the path. This scopes the operation to a specific sub-account and prevents cross-tenant action.
* **`uii` Is the Primary Key:** Every call control operation (except listing and creating calls) is keyed off the call's Unique Interaction Identifier (`uii`). You must obtain this from the listing endpoint before you can act on a specific call.
* **Phone Number Format:** Phone numbers passed as `destination`, `callerId`, or `phone` are accepted as digit-only strings (e.g. `6501234567`) or in E.164 format (e.g. `+15554150123`).

---

## Listing Active Calls

The list endpoint is the entry point for almost every workflow. It returns the `uii` for each call currently in flight, which subsequent endpoints require.

`GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/activeCalls/list`

### Query Parameters

| Parameter | Type | Requirement | Description |
| --- | --- | --- | --- |
| `product` | String | Optional | The category of resource to filter by. See the appendix for the full list of supported products. |
| `productId` | Integer | Optional | The numeric identifier of the selected product (e.g. the account ID when `product=ACCOUNT`). |
| `externalId` | String | Optional | Filter results to the call matching this custom external identifier. Use as an alternative to `product`/`productId` when you have a known external reference. |
| `page` | Integer | Optional | Zero-indexed page number for paginated results. |
| `maxRows` | Integer | Optional | Maximum number of records to return per page. |

!!! note
    Although `product` accepts a wide enum of values, only a subset return real results in practice: `ACCOUNT`, `ACD`, `OUTBOUND`, `VISUAL_IVR`, `CLOUD_PROFILE`, `TRAC_NUMBER`, and `DNIS`. Other product types are reserved for internal routing and generally return an empty array.

**Example Request:**

```http
GET /voice/api/v1/admin/accounts/{accountID}/activeCalls/list?product=ACCOUNT&productId=12440011
```

### Response Details

The endpoint returns an array of `ActiveCallListResponse` objects:

| Field | Type | Description |
| --- | --- | --- |
| `uii` | String | The Unique Interaction Identifier. **Use this as the path parameter for every other endpoint.** |
| `accountId` | String | The sub-account that owns the call. |
| `ani` | String | Automatic Number Identification — the calling party's number. |
| `dnis` | String | Dialed Number Identification Service — the number the call was placed to. |
| `dnisE164` | String | The DNIS in E.164 format. |
| `enqueueTime` | String | ISO-8601 timestamp marking when the call entered queue. |
| `dequeueTime` | String | ISO-8601 timestamp marking when the call left queue (null if still queued). |
| `callState` | String | The current state of the call (e.g. `ACTIVE`). |
| `archive` | Boolean | `true` once the call has moved to read-only state. |
| `agentFirstName` | String | First name of the agent currently assigned to the call. |
| `agentLastName` | String | Last name of the agent currently assigned to the call. |
| `destinationName` | String | Friendly name of the destination resource (e.g. queue or campaign). |
| `externalId` | String | A custom external identifier set on the call, if any. |
| `cnam` | String | Caller name (CNAM) lookup result, if available. |

**Example Response:**

```json
[
  {
    "uii": "202005081040440132050000019657",
    "accountId": "12440011",
    "ani": "6501234567",
    "dnis": "8661234567",
    "enqueueTime": "2020-05-08T14:40:47.000+0000",
    "dequeueTime": null,
    "callState": "ACTIVE",
    "archive": false,
    "agentFirstName": "Paco",
    "agentLastName": "Vu",
    "destinationName": null,
    "externalId": null,
    "cnam": null
  }
]
```

---

## Creating a Manual Agent Call

Triggers an outbound call from an agent's logged-in seat. The call rings the agent first, then dials the destination — the same behavior as if the agent had dialed manually from their softphone. The agent must be online and in an available state.

`POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/activeCalls/createManualAgentCall`

### Query Parameters

| Parameter | Type | Requirement | Description |
| --- | --- | --- | --- |
| `username` | String | **Required** | The username of the agent placing the call. URL-encode the `@` symbol as `%40`. |
| `destination` | String | **Required** | The phone number to dial. |
| `ringDuration` | Integer | **Required** | Number of seconds the agent's phone will ring before the call is abandoned. |
| `callerId` | String | **Required** | The phone number to present to the callee as the caller ID. |

**Example Request:**

```http
POST /voice/api/v1/admin/accounts/{accountId}/activeCalls/createManualAgentCall?username=some.name%40abc.com&destination=6501234567&ringDuration=5&callerId=1234567890
```

The endpoint returns `true` on success.

---

## Adding a Supervisor Session

Attaches a third party — typically a supervisor — to an active call. The `sessionType` parameter governs how the supervisor participates in the conversation.

`POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/activeCalls/{uii}/addSessionToCall`

### Query Parameters

| Parameter | Type | Requirement | Description |
| --- | --- | --- | --- |
| `destination` | String | **Required** | The phone number where the supervisor will receive the bridged call. |
| `sessionType` | String | **Required** | One of `MONITOR`, `COACHING`, or `BARGEIN`. See below. |

### Supervisor Session Types

| Mode | Agent hears supervisor? | Customer hears supervisor? | Use Case |
| --- | --- | --- | --- |
| `MONITOR` | No | No | Silent observation for QA scoring. |
| `COACHING` | Yes | No | Whisper coaching — the supervisor can guide the agent without the customer hearing. |
| `BARGEIN` | Yes | Yes | Full three-way conversation; used for escalation or rescue. |

**Example Request:**

```http
POST /voice/api/v1/admin/accounts/{accountId}/activeCalls/{uii}/addSessionToCall?destination=+15554150123&sessionType=MONITOR
```

---

## Setting a Call Disposition

Tags a finished or in-progress call with a preconfigured disposition code and releases the agent from `Pending Disposition` (PD) state. This is how outcome data flows back to reporting, and it works for both inbound and outbound calls.

`POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/activeCalls/{uii}/dispositionCall`

### Query Parameters

| Parameter | Type | Requirement | Description |
| --- | --- | --- | --- |
| `disposition` | String | **Required** | The name of a preconfigured disposition (e.g. `SALE`, `NO_ANSWER`). Must already exist in account configuration. |
| `callback` | Boolean | **Required** | `true` if the disposition includes scheduling a callback. |
| `callBackDTS` | String | Optional | Required when `callback=true`. Callback date and time formatted as `yyyyMMddHHmmss`. |
| `notes` | String | Optional | Free-text notes attached to the disposition record. |

---

## Terminating an Active Call

Forcibly ends the call. This terminates the entire interaction across all parties, including the agent and any attached supervisor sessions.

`POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/activeCalls/{uii}/hangupCall`

This endpoint takes no query parameters beyond the path. It returns `true` on successful termination.

---

## Terminating a Single Session

Removes a single party from a call without ending the call itself. This is the inverse of `addSessionToCall` — useful when a supervisor needs to drop off an observation but the agent and customer should remain connected.

`POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/activeCalls/{uii}/hangupSession`

### Query Parameters

| Parameter | Type | Requirement | Description |
| --- | --- | --- | --- |
| `phone` | String | **Required** | The phone number of the session to remove (i.e. the destination provided during `addSessionToCall`). |

---

## Toggling Call Recording

Starts or stops recording for an active call. Pair this with `dispositionCall` to satisfy compliance flows where recording must pause during sensitive segments.

`POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/activeCalls/{uii}/toggleCallRecording`

### Query Parameters

| Parameter | Type | Requirement | Description |
| --- | --- | --- | --- |
| `record` | Boolean | **Required** | `true` to start recording, `false` to stop. |

---

## Additional Control Endpoints

Beyond the primary endpoints above, several auxiliary actions are available on the same `/activeCalls/{uii}/` resource:

| Endpoint | Method | Purpose |
| --- | --- | --- |
| `/pingCall` | POST | Prevents the call from moving to archived (read-only) state while pending operations need to complete. Useful during long-running orchestrations. |
| `/toggleCallHold` | POST | Places the call on or off hold. Accepts a `state` query parameter: `ON` or `OFF`. |
| `/requeueCall` | POST | Sends an active call back into a queue. Accepts a `gateId` query parameter identifying the destination queue. |
| `/hangupSessionById` | POST | Same as `hangupSession`, but addresses the session by its internal `sessionId` rather than by `phone`. |

---

## Implementation Strategy

### Recommended Pattern: Poll-Then-Act

The active call APIs are synchronous, but most useful workflows still begin with a discovery loop:

1. **List** active calls for the relevant `product` (typically `ACCOUNT` for full visibility).
2. **Filter** in your code for the conditions you care about (e.g. calls in queue longer than a threshold, calls assigned to a specific agent, calls without a recording).
3. **Act** on the resulting `uii` values: monitor, requeue, hang up, or toggle recording.

For supervisor consoles, refresh the listing every 5–10 seconds. Avoid sub-second polling; the platform will rate-limit aggressive callers.

!!! important "Rate Limiting & Stability"
    * **Limit:** 120 requests per minute per token under standard platform rate limiting.
    * **Strategy:** Implement exponential backoff on `429 Too Many Requests` responses. For supervisor dashboards monitoring many calls, prefer a single list call followed by targeted action calls over per-call polling.

!!! warning "Acting on stale UIIs"
    A `uii` is only valid while the call's `callState` is `ACTIVE`. If you cache `uii` values and call control endpoints later, expect `404` responses for calls that have since archived. Always handle this gracefully rather than retrying.

### Sample Implementation (Python)

The following example polls for active calls under an account, identifies any in-flight calls assigned to a specific agent, and attaches a silent monitor session for a supervisor.

```python
import requests
import urllib.parse

# Configuration
BASE_URL = "https://ringcx.ringcentral.com/voice/api/v1/admin/accounts"
ACCOUNT_ID = "12440011"
SUPERVISOR_PHONE = "+15554150123"
TARGET_AGENT_LAST_NAME = "Vu"

def list_active_calls(account_id, token):
    """Returns all active calls for the account."""
    url = f"{BASE_URL}/{account_id}/activeCalls/list"
    params = {"product": "ACCOUNT", "productId": account_id}
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()

def attach_monitor(account_id, uii, supervisor_phone, token):
    """Attaches a silent MONITOR session to the given call."""
    url = f"{BASE_URL}/{account_id}/activeCalls/{uii}/addSessionToCall"
    params = {"destination": supervisor_phone, "sessionType": "MONITOR"}
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(url, params=params, headers=headers)
    if response.status_code == 200:
        print(f"Monitoring session attached to call {uii}")
    else:
        print(f"Failed to attach monitor for {uii}: {response.status_code}")

def supervise_target_agent(token):
    calls = list_active_calls(ACCOUNT_ID, token)
    for call in calls:
        if (call.get("callState") == "ACTIVE"
                and call.get("agentLastName") == TARGET_AGENT_LAST_NAME):
            attach_monitor(ACCOUNT_ID, call["uii"], SUPERVISOR_PHONE, token)

if __name__ == "__main__":
    supervise_target_agent("YOUR_ACCESS_TOKEN")
```

---

## Appendix: Supported Elements

??? info "View Supported `product` Values"

    | Value | Returns Results | Description |
    | --- | --- | --- |
    | `ACCOUNT` | Yes | All active calls under the account. |
    | `ACD` | Yes | Calls routed through Automatic Call Distribution queues. |
    | `OUTBOUND` | Yes | Calls dialed from an outbound campaign. |
    | `VISUAL_IVR` | Yes | Calls within a Visual IVR (Studio) flow. |
    | `CLOUD_PROFILE` | Yes | Calls bound to a Cloud Profile. |
    | `TRAC_NUMBER` | Yes | Calls routed through a legacy TRAC number. |
    | `DNIS` | Yes | Calls filtered by a specific dialed number. |
    | `AGENT` | No | Reserved. |
    | `CHAT_QUEUE` | No | Reserved (digital channels use a separate active chat API). |
    | `CLOUD_DESTINATION` | No | Reserved. |
    | `HTTP_SERVICES` | No | Reserved. |
    | `SCRIPTING` | No | Reserved. |
    | `TN_MANAGER` | No | Reserved. |
    | `SURVEY` | No | Reserved. |
    | `TEAMS` | No | Reserved. |
    | `KNOWLEDGE_BASE` | No | Reserved. |
    | `UTILITIES` | No | Reserved. |

??? info "View Supervisor Session Types"

    | Value | Description |
    | --- | --- |
    | `MONITOR` | The supervisor silently listens to the agent and the customer. Neither party hears the supervisor. |
    | `COACHING` | The supervisor can speak to the agent (whisper) without the customer hearing. |
    | `BARGEIN` | The supervisor joins as a full third party. All three participants hear and speak to one another. |