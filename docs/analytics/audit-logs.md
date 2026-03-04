# Administrative Audit Log APIs

The Administrative Audit Log APIs provide a forensic trail of configuration changes and sensitive actions performed within the RingCentral CX Voice platform. Unlike standard reporting APIs which aggregate performance metrics, the Audit Log API is a specialized governance tool. It allows organizations to verify compliance, investigate unauthorized changes, and maintain a high degree of accountability across administrative user sessions.

## Governance and Oversight

Audit logs are critical for organizations requiring rigorous change management protocols. This API provides the transparency needed to answer "who changed what and when" regarding the platform's configuration.

### Use Cases for Administrative Auditing
* **Compliance and Security:** Maintain an immutable record of system changes for regulatory requirements (e.g., PCI, HIPAA, or internal security audits).
* **Change Management:** Identify the precise origin of configuration changes that may have impacted contact center operations.
* **Forensic Investigation:** Track administrative user activity, including simulated sessions, to investigate suspicious or erroneous system modifications.

### Historical vs Real Time Audit Scope
The Audit API is designed for the retrieval of historical change records. It is not intended for real-time monitoring or alerting. The system logs administrative events as they occur, making them available for retrieval 5 minutes after the action is finalized. 

### Required App Permissions (Scopes)

Access to the administrative audit trail is governed by **OAuth Scopes** and specific **RingCX Admin Permissions**. These settings ensure that forensic data is only accessible to authorized applications and users.

#### 1. Configure OAuth Scopes

To successfully exchange a JWT for an access token using your client credentials, your application must be configured with the following permission in the [Developer Portal](https://developers.ringcentral.com/my-account.html#/applications):

* **`ReadAccounts`**: Required to validate the account context and complete the authentication flow.

For a detailed walkthrough on exchanging your JWT for an access token, please refer to the [RingCentral Authentication Guide](https://developers.ringcentral.com/engage/voice/guide/authentication/auth-ringcentral).

#### 2. Enable RingCX Admin Access

In addition to app scopes, the user authenticating the app must have the specific **Audit log access** permission enabled within the RingCX Admin portal. Without this, the API will fail to authorize the request.

To enable this:

1. Log in to **RingCX Admin**.
2. Navigate to **Users** > **Administrators**.
3. Select the target user and ensure the **Audit log access** box is checked.

![Audit Log Access Configuration](../images/audit-log-access.png)

!!! warning
    If the application has the correct scopes but the user lacks this platform permission, the API will return the following error:
    > ```json
    > {
    >     "errorCode": "access.denied.exception",
    >     "generalMessage": "You do not have permission to access this resource",
    >     "details": "",
    >     "requestUri": "/api/v1/admin/auditLogs/search - PUT",
    >     "timestamp": <TIMESTAMP>
    > }
    > 
    > ```

!!! important "Important - Be Aware of Rate Limits"
    Standard platform rate limiting applies to audit requests. The limit is 120 requests per minute. For high-volume data uploads, you can include up to 1000 leads per single API call to maximize throughput. If the API returns a 429 Too Many Requests status code, implement an exponential backoff strategy for subsequent retry attempts to ensure system stability.


### Important Technical Constraints
When querying the Audit Log Search endpoint, developers must adhere to these strict requirements:

* **Mandatory Account Context:** The `accountId` is a required field in the request body. It constrains the search to a specific sub-account to maintain data isolation.
* **ISO-8601 Offset Requirement:** Time parameters (`startDateTime` and `endDateTime`) must be formatted using ISO-8601 with an explicit UTC offset. The "Z" (Zulu) suffix is unsupported and will result in a request failure.
    * **Accepted Format:** `2025-11-20T00:00:00.000-08:00`
    * **Unsupported Format:** `2025-11-20T00:00:00.000Z`
* **Audit Action Categorization:** Administrative events are classified into three primary action types: `CREATE` (entity creation), `UPDATE` (modification of existing settings), and `DELETE` (removal of system entities).

---

## Audit Log Discovery
Before searching, you may use the Discovery API to identify which system entities (such as Agents, Gates, or Queues) are eligible for auditing. The `name` values returned here are used to populate the `searchEntities` filter in your search requests.

`GET https://ringcx.ringcentral.com/voice/api/v1/admin/auditLogs/auditable`


### Response Object
Field | Description
--- | ---
fullPath | The internal system path representing the location of the auditable entity.
name | The specific entity type name (e.g., "Agent", "Gate") used for search filtering.



---

## Audit Log Search
The Search API serves as the primary extraction point for audit records. It allows you to reconstruct the history of administrative tasks by filtering for specific timeframes, action types, or individual actors.

`PUT https://ringcx.ringcentral.com/voice/api/v1/admin/auditLogs/search`

### Request Body
| Parameter | Type | Requirement | Description |
| --- | --- | --- | --- |
| `accountId` | String | **Required** | The unique identifier for the sub-account being audited. |
| `startDateTime` | String | **Required** | The start of the search interval (ISO-8601 `date-time`). |
| `endDateTime` | String | **Required** | The end of the search interval (ISO-8601 `date-time`). |
| `auditActions` | Array | Optional | Filter results by specific actions: `CREATE`, `UPDATE`, or `DELETE`. |
| `searchEntities` | Array | Optional | An optional array of entity names to narrow the audit scope (e.g., `Agent`, `Campaign`). |
| `createUserId` | String | Optional | Filter for actions performed by a specific administrator's unique ID. |
| `auditedEntityId` | String | Optional | Filter for actions performed on a specific resource (e.g., a specific Agent's ID). |
| `orderBy` | String | Optional | The field name used for record sorting. |
| `ascOrDesc` | String | Optional | The sort direction for the audit trail: `ASCENDING` or `DESCENDING`. |
| `startDateTimeAsUnix` | Integer | Optional | Unix timestamp for the start date (alternative to `startDateTime`). |
| `endDateTimeAsUnix` | Integer | Optional | Unix timestamp for the end date (alternative to `endDateTime`). |

**Example Request:**
```json
{
  "accountId": "12345",
  "auditActions": ["UPDATE", "DELETE"],
  "startDateTime": "2025-11-20T00:00:00.000-08:00",
  "endDateTime": "2025-12-03T23:59:00.228-08:00",
  "ascOrDesc": "DESCENDING"
}
```

### Audit Log Response Details

The Audit Log API tracks administrative changes across the platform. The `actionType` field identifies the nature of the event:

* **CREATE**: A new entity (such as an Agent or Campaign) was added to the system.
* **UPDATE**: An existing entity was modified. These records include an `auditLogResultList` detailing specific field changes.
* **DELETE**: An entity was removed from the system.

The response object provides a chronological trail of administrative actions. Each record in the results array contains the following key attributes:

| Field | Type | Description |
| --- | --- | --- |
| `id` | String | The unique identifier (UUID) for the specific audit log entry. |
| `auditedClass` | String | The Java class path of the entity type that was modified (e.g., `com.connectfirst...Gate`). |
| `auditedEntityId` | String | The unique internal system identifier for the modified entity. |
| `auditedEntityDescription` | String | A human-readable name for the entity, such as a Gate name or Agent email. |
| `actionType` | String | The specific operation performed: `CREATE`, `UPDATE`, or `DELETE`. |
| `createTimeAsDateTime` | String | ISO-8601 timestamp of when the administrative event occurred. |
| `accountId` | String | The unique identifier for the sub-account where the action occurred. |
| `authUser` | Object | Contains details about the administrator who performed the action, including `userName` and `sourceId` (IP address). |
| `auditLogResultList` | Array | A collection of specific field modifications (populated for `UPDATE` actions). |
| `affectedEntityJson` | String | A JSON string representation of the entity (usually populated for `CREATE` and `DELETE` actions). |
| `_class` | String | Internal system identifier indicating the underlying document model (e.g., `com.connectfirst.api.model.documents.AuditLog`). |

#### auditLogResultList Object Structure

For `UPDATE` actions, the `auditLogResultList` array details precisely which settings were altered:

* **attributeName**: The internal name of the setting that was changed (e.g., `gatePriority`).
* **originalValue**: The value of the setting before the update.
* **newValue**: The updated value of the setting.
* **classType**: The full Java class path of the entity being modified.

---

### Example Response JSON

Below is an example output from the audit log search showing a configuration **UPDATE** to an existing `Gate` object.

```json
[
    {
        "id": "00000000-0000-0000-0000-000000000000",
        "authUser": {
            "sourceId": "0.0.0.0",
            "firstName": "Admin",
            "lastName": "User",
            "userName": "admin.user@example.com",
            "userId": "00000",
            "fullJson": null,
            "simulatedByUserId": null,
            "simulatedByUserName": null,
            "simulatedFromIP": null
        },
        "createTime": 1111111111111,
        "auditLogResultList": [
            {
                "attributeName": "gatePriority",
                "originalValue": "0",
                "newValue": "1",
                "classType": "com.connectfirst.api.model.intelliqueue_globalcatalog.acd.Gate"
            }
        ],
        "auditedClass": "com.connectfirst.api.model.intelliqueue_globalcatalog.acd.Gate",
        "auditedEntityId": "000000",
        "auditedEntityDescription": "Example Entity Name",
        "actionType": "UPDATE",
        "affectedEntityJson": null,
        "accountId": "00000000",
        "createTimeAsDateTime": "2026-01-13T00:00:00.000+0000",
        "_class": "com.connectfirst.api.model.documents.AuditLog"
    }
]

```

### Supported elements

To help developers navigate the audit logs, the following list represents the system elements that can be tracked. These values correspond to the final segment of the auditedClass string found in the API response.

??? info "View Supported Audited Elements"

    | Element | Description |
    | :--- | :--- |
    | `Account` | Core account configuration and feature enablement. |
    | `AccountAuthConfig` | Basic and OAuth authentication credentials for remote services. |
    | `AccountAuxState` | Customized agent presence and auxiliary states. |
    | `AccountCallerId` | Configured outbound caller ID settings for the account. |
    | `AdminRegionalSettings` | Account-wide regional and localization configurations. |
    | `Agent` | User profiles and core agent permissions. |
    | `AgentChatGroupAccess` | Assignments between agents and digital chat groups. |
    | `AgentChatQueueAccess` | Direct assignments between agents and specific chat queues. |
    | `AgentDialGroupMember` | Membership associations between agents and dial groups. |
    | `AgentGateAccess` | Individual agent assignments to voice queues (Gates). |
    | `AgentGateGroupAccess` | Agent associations with voice queue groups. |
    | `AgentGroup` | Administrative groupings for organizing agents. |
    | `AgentRegionalSettings` | Individual localization settings for specific agents. |
    | `AgentSkillProfile` | Bundled sets of skills assigned to agents. |
    | `AgentSupervisor` | Associations between supervisors and their subordinate agents. |
    | `Alert` | System notification and threshold alert configurations. |
    | `AmdProfile` | Answering Machine Detection behavior profiles. |
    | `AssignedDnis` | Dialed Number Identification Service mappings for voice traffic. |
    | `AssignedSmsDnis` | Phone number mappings for SMS-based digital traffic. |
    | `BlockedANI` | Inbound caller ID blacklists. |
    | `BlockedIP` | Network-level access restriction lists. |
    | `CallRecordingAccess` | Permissions and settings for managing call recordings. |
    | `Campaign` | Outbound dialing campaign configurations. |
    | `CampaignCriteriaGroupAccess` | Targeting criteria used for campaign lead selection. |
    | `CampaignDisposition` | Outcome labels specific to outbound campaigns. |
    | `CampaignFilterTimezones` | Active timezone windows for outbound dialing. |
    | `CampaignLeadList` | Management of phone number lists assigned to campaigns. |
    | `CampaignPass` | Configuration for lead recycling attempts. |
    | `CampaignPassCustomDelay` | Timing rules for specific lead pass attempts. |
    | `CampaignPassDisposition` | Disposition-based rules for lead recycling. |
    | `CampaignUnlimitedFieldGroup` | Custom data field definitions for campaign leads. |
    | `Canvas` | Visual layout and configuration data for the design interface. |
    | `ChatGroup` | Organizational groups for digital chat queues. |
    | `ChatGroupSkill` | Skill requirements for routing digital interactions. |
    | `ChatPriorityGroup` | Weighting rules for digital interaction queues. |
    | `ChatQueue` | Configuration for digital chat interaction queues. |
    | `ChatQueueChatWidgetAccess` | Mappings between chat queues and customer-facing widgets. |
    | `ChatQueueDisposition` | Outcome labels for digital chat interactions. |
    | `ChatQueueEvent` | Automated actions triggered during chat queueing. |
    | `ChatQueueScheduleOverride` | Temporary calendar-based rules for chat availability. |
    | `ChatRequeueShortcut` | Quick-actions for transferring chat interactions. |
    | `ChatRequeueShortcutGroup` | Administrative sets of chat transfer shortcuts. |
    | `ChatRequeueShortcutGroupChatQueueAccess` | Permission mappings for chat shortcut groups. |
    | `ChatRoom` | Virtual environments for persistent internal or external chat. |
    | `ChatWidget` | Appearance and behavior settings for embedded chat interfaces. |
    | `CloudRouteAssignedDestination` | Routing targets within a Cloud Route profile. |
    | `CloudRouteAssignedOverride` | Temporary routing overrides for specific destinations. |
    | `CloudRouteDestination` | Individual endpoints used in Cloud Routing. |
    | `CloudRouteDestinationOverride` | Specific behavior overrides for routing endpoints. |
    | `CloudRouteDtmfEvent` | DTMF-triggered actions within Cloud Routing. |
    | `CloudRouteGroup` | Shared collections of Cloud Route profiles. |
    | `CloudRouteProfile` | Global routing strategies and profiles. |
    | `CustomCriteriaGroup` | User-defined logic blocks for advanced routing. |
    | `CustomCriteriaPlan` | Strategic plans utilizing custom criteria logic. |
    | `CustomDialZone` | Regional time zone rules for outbound dialing. |
    | `CustomDialZoneGroups` | Collections of regional dialing rules. |
    | `DialGroup` | Configuration for outbound dialer behavior and mode. |
    | `DncListEntry` | Individual records on the Do Not Call list. |
    | `DncTag` | Custom labels for classifying DNC records. |
    | `DncUploadedFileResults` | Logs from bulk DNC list imports. |
    | `DnisNotification` | Triggers based on incoming dialed numbers. |
    | `DnisPool` | Standard groups of phone numbers for inbound traffic. |
    | `DnisPoolV2` | Enhanced phone number pool configurations. |
    | `EmailTemplate` | Definitions for automated system emails. |
    | `EmailTemplateAttachment` | Files associated with automated email templates. |
    | `Gate` | Configuration for voice queues. |
    | `GateDisposition` | Outcome labels for voice calls. |
    | `GateGroup` | Organizational groupings for voice queues. |
    | `GateGroupSkill` | Skill requirements for voice call routing. |
    | `GatePriorityGroup` | Logic for weighting different voice queues. |
    | `GateQueueDtmfEvent` | DTMF-based menus and actions while in queue. |
    | `GateQueueEvent` | Automated actions (like hold music) while in queue. |
    | `GateScheduleOverride` | Temporary calendar-based rules for voice queue availability. |
    | `GateSpecialAni` | Customized handling for specific inbound caller IDs. |
    | `HttpServiceMapping` | Data transformations for internal HTTP service calls. |
    | `IVRApplication` | Hosted application logic for interactive menus. |
    | `KnowledgeBaseArticle` | Content records for agent-facing help documentation. |
    | `KnowledgeBaseCategory` | Taxonomy used to organize help documentation. |
    | `KnowledgeBaseGroup` | Permission-based sets of knowledge base content. |
    | `MainAccount` | Parent account attributes in multi-account hierarchies. |
    | `MappingTemplate` | Reusable data structure templates. |
    | `NotificationGroup` | Collections of recipients for system alerts. |
    | `NotificationTarget` | Individual endpoints (email/URL) for system alerts. |
    | `PendingAccount` | Staging records for new account provisioning. |
    | `PhoneBookEntry` | Speed-dial and contact records. |
    | `QuotaGroup` | Logic sets for managing outbound dialing limits. |
    | `QuotaTarget` | Specific thresholds for outbound limits. |
    | `RcAccountData` | Synchronized data from the RingCentral core platform. |
    | `RecordingDestinationV2` | Storage targets for system media. |
    | `RecordingTaskV2` | Scheduled logic for media processing or archival. |
    | `RemoteHttpService` | Core configuration for outbound API integrations. |
    | `RemoteHttpServiceGroup` | Collections of related external API calls. |
    | `RemoteHttpServiceInput` | Input parameter definitions for API integrations. |
    | `RequeueShortcut` | Transfer shortcuts for voice queues. |
    | `ResultFileDestination` | Automated targets for campaign report delivery. |
    | `RightsDocTable` | Internal security and permission mappings. |
    | `RTASubscriptionConfig` | Real-time analytics subscription settings. |
    | `Script` | Dynamic agent guidance scripts used during calls. |
    | `ScriptGroup` | Administrative sets for organizing agent scripts. |
    | `TracGroup` | Logic groups for legacy routing numbers. |
    | `TracLocation` | Geographic definitions for legacy routing. |
    | `TracLocator` | Search logic for legacy routing targets. |
    | `TracNumber` | Legacy inbound routing numbers. |
    | `TracRoutingRule` | Specific logic applied to legacy routing. |
    | `TracScheduleOverride` | Temporary availability rules for legacy routing. |
    | `UploadedFileResults` | Status logs for general bulk file uploads. |
    | `User` | System user accounts and portal access. |
    | `VisualIvr` | High-level configuration for Studio-based IVR workflows. |
    | `VisualIvrConfig` | Specific node-level logic and data for Visual IVR scripts. |
    | `VisualIvrGroup` | Organizational containers for grouping Visual IVR workflows. |
    | `WhitelistEntry` | Records permitted to bypass security filters. |
    | `WhitelistLogEntry` | Audit records of whitelist activity. |
    | `WhitelistTag` | Labels used to classify whitelist entries. |
    | `WhitelistTagMembers` | Member lists associated with security tags. |
    | `Workflow` | Automated multi-step business process logic. |
    | `WorkflowConfig` | Specific configuration versions for workflows. |
    | `WorkflowGroup` | Organizational groupings for business workflows. |


## Implementation Strategy

To build a reliable synchronization service (e.g., exporting audit logs to an external security database), developers should implement a "Sliding Window" polling strategy.


!!! important "Important - Handling Data Propagation Delay"
    Administrative actions are not available for API retrieval in real-time. There is a **5-minute propagation delay** before logs are finalized in the search index.

### Recommended Polling Pattern

To ensure 100% data integrity and account for the propagation delay, we recommend retrieving audit logs in **15-minute intervals**, initiated 5 minutes after the window closes.

**Example Schedule:**

| Execution Time | Search Time Range (`start` to `end`) | Purpose |
| --- | --- | --- |
| **08:05** | 07:45 — 08:00 | Captures all events finalized by 08:00. |
| **08:20** | 08:00 — 08:15 | Captures all events finalized by 08:15. |
| **08:35** | 08:15 — 08:30 | Captures all events finalized by 08:30. |

### Sample Implementation (Python)

The following example demonstrates how to poll the API and persist the results into a local SQLite database for downstream reporting.

```python
import requests
import datetime
import sqlite3
import json

# Configuration
BASE_URL = "https://ringcx.ringcentral.com/voice/api/v1/admin/auditLogs/search"
ACCOUNT_ID = "12345"

def save_to_database(logs):
    """Simulates persisting audit logs to an SQL database."""
    conn = sqlite3.connect('audit_trail.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs 
        (id TEXT PRIMARY KEY, action TEXT, user TEXT, timestamp TEXT, raw_json TEXT)
    ''')

    for entry in logs:
        cursor.execute('''
            INSERT OR IGNORE INTO logs (id, action, user, timestamp, raw_json)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            entry.get('id'),
            entry.get('actionType'),
            entry['authUser'].get('userName'),
            entry.get('createTimeAsDateTime'),
            json.dumps(entry)
        ))
    
    conn.commit()
    conn.close()
    print(f"Successfully synced {len(logs)} entries.")

def sync_audit_logs():
    # 1. Define the 15-minute window with a 5-minute delay
    now = datetime.datetime.now(datetime.timezone.utc)
    end_time = now - datetime.timedelta(minutes=5)
    start_time = end_time - datetime.timedelta(minutes=15)

    payload = {
        "accountId": ACCOUNT_ID,
        "startDateTimeAsUnix": int(start_time.timestamp() * 1000),
        "endDateTimeAsUnix": int(end_time.timestamp() * 1000),
        "ascOrDesc": "ASCENDING"
    }

    headers = {
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
        'Content-Type': 'application/json'
    }

    # 2. Invoke the API
    response = requests.put(BASE_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        logs = response.json()
        # 3. Persist logs to database
        save_to_database(logs)
    else:
        print(f"Error fetching logs: {response.status_code}")

if __name__ == "__main__":
    sync_audit_logs()
```


