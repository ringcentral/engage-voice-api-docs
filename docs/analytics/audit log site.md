# Administrative Audit Log APIs

The Administrative Audit Log APIs provide a forensic trail of configuration changes and sensitive actions performed within the RingCentral CX Voice platform. Unlike standard reporting APIs which aggregate performance metrics, the Audit Log API is a specialized governance tool. It allows organizations to verify compliance, investigate unauthorized changes, and maintain a high degree of accountability across administrative user sessions.

## Governance and Oversight

Audit logs are critical for organizations requiring rigorous change management protocols. This API provides the transparency needed to answer "who changed what and when" regarding the platform's configuration.

### Use Cases for Administrative Auditing
* **Compliance and Security:** Maintain an immutable record of system changes for regulatory requirements (e.g., PCI, HIPAA, or internal security audits).
* **Change Management:** Identify the precise origin of configuration changes that may have impacted contact center operations.
* **Forensic Investigation:** Track administrative user activity, including simulated sessions, to investigate suspicious or erroneous system modifications.

### Historical vs Real Time Audit Scope
The Audit API is designed for the retrieval of historical change records. It is not intended for real-time monitoring or alerting. The system logs administrative events as they occur, making them available for retrieval shortly after the action is finalized.

### Required App Permissions (Scopes)
Access to the administrative audit trail is governed by **OAuth Scopes**. These must be enabled in your application settings within the [RingCentral Developer Portal](https://developers.ringcentral.com/my-account.html#/applications).

To successfully invoke these endpoints, your app must be configured with the following permissions:

* **`ReadAuditTrail`**: The primary scope required to search and retrieve audit log records.
* **`ReadAccounts`**: Required for the Discovery API and to validate the `accountId` context used in search requests.

> [!IMPORTANT]
> Since you are using a **JWT** or **3-Legged OAuth** flow, the user authenticating the app must also have administrative privileges within the account to view this forensic data. If the app has the correct scopes but the user lacks the necessary platform permissions, the API will return a `403 Forbidden` error.

### Be Aware of Rate Limits
Standard platform rate limiting applies to audit requests. The limit is 10 requests per minute. To ensure system stability during large data extractions, implement a robust backoff mechanism. If the API returns a `429 Too Many Requests` status code, utilize an exponential backoff strategy for subsequent retry attempts.


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
Field | Description
--- | ---
accountId | **Required.** The unique identifier for the sub-account being audited.
startDateTime | **Required.** The start of the search interval (ISO-8601 with offset).
endDateTime | **Required.** The end of the search interval (ISO-8601 with offset).
auditActions | Filter results by specific actions: `CREATE`, `UPDATE`, or `DELETE`.
searchEntities | An optional array of entity names (from the Discovery API) to narrow the audit scope.
createUserId | Filter for actions performed by a specific administrator's unique ID.
auditedEntityId | Filter for actions performed on a specific resource (e.g., a specific Agent's ID).
orderBy | The field used for record sorting (commonly `createTime`).
ascOrDesc | The sort direction for the audit trail: `ASCENDING` or `DESCENDING`.

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

(Add a list of what kind of actions (like login/logout, and stuff) can appear and what they will look like)

The response object provides a chronological trail of administrative actions. Each record in the results array contains the following key attributes:

| Field | Type | Description |
| --- | --- | --- |
| `element` | String | The entity type that was modified (e.g., `Agent`, `Campaign`, `IVR`). |
| `elementId` | String | The unique internal system identifier for the modified entity. |
| `description` | String | A human-readable name for the entity, such as a Campaign name or Agent email. |
| `action` | String | The specific operation performed: `CREATE`, `UPDATE`, or `DELETE`. |
| `dateTime` | String | ISO-8601 timestamp of when the administrative event occurred. |
| `user` | String | The email address of the administrator who performed the action. |
| `simulatedBy` | String | Populated if an admin performed the action while "simulating" another user. |
| `changes` | Array | A collection of specific field modifications (populated for `UPDATE` actions). |

#### Changes Object Structure

For `UPDATE` actions, the `changes` array details precisely which settings were altered:

* **field**: The internal name of the setting that was changed (e.g., `dialingMode`).
* **previousValue**: The value of the setting before the update.
* **newValue**: The updated value of the setting.

---

### Example Response JSON
Below is an example output from the audit log search showing a configuration **UPDATE** to an existing `VisualIvr` object and a **CREATE** action for a new `GateDisposition` entity.
```json
[
    {
        "id": "UNIQUE-UUID-HEX-STRING",
        "authUser": {
            "sourceId": "IP-ADDRESS",
            "firstName": "USER-FIRST-NAME",
            "lastName": "USER-LAST-NAME",
            "userName": "user.email@example.com",
            "userId": "INTERNAL-USER-ID",
            "fullJson": null,
            "simulatedByUserId": null,
            "simulatedByUserName": null,
            "simulatedFromIP": null
        },
        "createTime": 1767745493366,
        "auditLogResultList": [
            {
                "attributeName": "debug",
                "originalValue": "false",
                "newValue": "true",
                "classType": "com.connectfirst.api.model.intelliqueue_globalcatalog.ivrStudio.VisualIvr"
            },
            {
                "attributeName": "debugEmail",
                "originalValue": null,
                "newValue": "user.email@example.com",
                "classType": "com.connectfirst.api.model.intelliqueue_globalcatalog.ivrStudio.VisualIvr"
            }
        ],
        "auditedClass": "com.connectfirst.api.model.intelliqueue_globalcatalog.ivrStudio.VisualIvr",
        "auditedEntityId": "ENTITY-ID-STRING",
        "auditedEntityDescription": "OBJECT-NAME-OR-DESCRIPTION",
        "actionType": "UPDATE",
        "affectedEntityJson": null,
        "accountId": "ACCOUNT-ID-STRING",
        "createTimeAsDateTime": "2026-01-07T00:24:53.366+0000",
        "_class": "com.connectfirst.api.model.documents.AuditLog"
    },
    {
        "id": "UNIQUE-UUID-HEX-STRING",
        "authUser": {
            "sourceId": "IP-ADDRESS",
            "firstName": "USER-FIRST-NAME",
            "lastName": "USER-LAST-NAME",
            "userName": "user.email@example.com",
            "userId": "INTERNAL-USER-ID",
            "fullJson": null,
            "simulatedByUserId": null,
            "simulatedByUserName": null,
            "simulatedFromIP": null
        },
        "createTime": 1767752574376,
        "auditLogResultList": null,
        "auditedClass": "com.connectfirst.api.model.intelliqueue_globalcatalog.acd.GateDisposition",
        "auditedEntityId": "ENTITY-ID-STRING",
        "auditedEntityDescription": "OBJECT-NAME-OR-DESCRIPTION",
        "actionType": "CREATE",
        "affectedEntityJson": "{\"gateDispositionId\":123456,\"disposition\":\"Placeholder Name\",\"isRequeued\":0,\"isActive\":true}",
        "accountId": "ACCOUNT-ID-STRING",
        "createTimeAsDateTime": "2026-01-07T02:22:54.376+0000",
        "_class": "com.connectfirst.api.model.documents.AuditLog"
    }
]

```

### Response Characteristics

* **Deletions**: If an entity is deleted, the `changes` array will be empty as the entire record is removed from the active system.
* **Simulated Actions**: The `simulatedBy` and `simulatedFromIP` fields are critical for forensic auditing when troubleshooting changes made by external support or high-level administrators acting on behalf of a local user.

### Supported elements

To help developers navigate the audit logs, the following list represents the system elements that can be tracked. These values correspond to the final segment of the auditedClass string found in the API response.

<details>
<summary>View Supported Audited Elements</summary>

| Element | Description |
| --- | --- |
| **Account** | Core account configuration and feature enablement. |
| **AccountAuthConfig** | Basic and OAuth authentication credentials for remote services. |
| **AccountAuxState** | Customized agent presence and auxiliary states. |
| **AccountCallerId** | Configured outbound caller ID settings for the account. |
| **AdminRegionalSettings** | Account-wide regional and localization configurations. |
| **Agent** | User profiles and core agent permissions. |
| **AgentChatGroupAccess** | Assignments between agents and digital chat groups. |
| **AgentChatQueueAccess** | Direct assignments between agents and specific chat queues. |
| **AgentDialGroupMember** | Membership associations between agents and dial groups. |
| **AgentGateAccess** | Individual agent assignments to voice queues (Gates). |
| **AgentGateGroupAccess** | Agent associations with voice queue groups. |
| **AgentGroup** | Administrative groupings for organizing agents. |
| **AgentRegionalSettings** | Individual localization settings for specific agents. |
| **AgentSkillProfile** | Bundled sets of skills assigned to agents. |
| **AgentSupervisor** | Associations between supervisors and their subordinate agents. |
| **Alert** | System notification and threshold alert configurations. |
| **AmdProfile** | Answering Machine Detection behavior profiles. |
| **AssignedDnis** | Dialed Number Identification Service mappings for voice traffic. |
| **AssignedSmsDnis** | Phone number mappings for SMS-based digital traffic. |
| **BlockedANI** | Inbound caller ID blacklists. |
| **BlockedIP** | Network-level access restriction lists. |
| **CallRecordingAccess** | Permissions and settings for managing call recordings. |
| **Campaign** | Outbound dialing campaign configurations. |
| **CampaignCriteriaGroupAccess** | Targeting criteria used for campaign lead selection. |
| **CampaignDisposition** | Outcome labels specific to outbound campaigns. |
| **CampaignFilterTimezones** | Active timezone windows for outbound dialing. |
| **CampaignLeadList** | Management of phone number lists assigned to campaigns. |
| **CampaignPass** | Configuration for lead recycling attempts. |
| **CampaignPassCustomDelay** | Timing rules for specific lead pass attempts. |
| **CampaignPassDisposition** | Disposition-based rules for lead recycling. |
| **CampaignUnlimitedFieldGroup** | Custom data field definitions for campaign leads. |
| **Canvas** | Visual layout and configuration data for the design interface. |
| **ChatGroup** | Organizational groups for digital chat queues. |
| **ChatGroupSkill** | Skill requirements for routing digital interactions. |
| **ChatPriorityGroup** | Weighting rules for digital interaction queues. |
| **ChatQueue** | Configuration for digital chat interaction queues. |
| **ChatQueueChatWidgetAccess** | Mappings between chat queues and customer-facing widgets. |
| **ChatQueueDisposition** | Outcome labels for digital chat interactions. |
| **ChatQueueEvent** | Automated actions triggered during chat queueing. |
| **ChatQueueScheduleOverride** | Temporary calendar-based rules for chat availability. |
| **ChatRequeueShortcut** | Quick-actions for transferring chat interactions. |
| **ChatRequeueShortcutGroup** | Administrative sets of chat transfer shortcuts. |
| **ChatRequeueShortcutGroupChatQueueAccess** | Permission mappings for chat shortcut groups. |
| **ChatRoom** | Virtual environments for persistent internal or external chat. |
| **ChatWidget** | Appearance and behavior settings for embedded chat interfaces. |
| **CloudRouteAssignedDestination** | Routing targets within a Cloud Route profile. |
| **CloudRouteAssignedOverride** | Temporary routing overrides for specific destinations. |
| **CloudRouteDestination** | Individual endpoints used in Cloud Routing. |
| **CloudRouteDestinationOverride** | Specific behavior overrides for routing endpoints. |
| **CloudRouteDtmfEvent** | DTMF-triggered actions within Cloud Routing. |
| **CloudRouteGroup** | Shared collections of Cloud Route profiles. |
| **CloudRouteProfile** | Global routing strategies and profiles. |
| **CustomCriteriaGroup** | User-defined logic blocks for advanced routing. |
| **CustomCriteriaPlan** | Strategic plans utilizing custom criteria logic. |
| **CustomDialZone** | Regional time zone rules for outbound dialing. |
| **CustomDialZoneGroups**: | Collections of regional dialing rules. |
| **DialGroup** | Configuration for outbound dialer behavior and mode. |
| **DncListEntry** | Individual records on the Do Not Call list. |
| **DncTag** | Custom labels for classifying DNC records. |
| **DncUploadedFileResults** | Logs from bulk DNC list imports. |
| **DnisNotification** | Triggers based on incoming dialed numbers. |
| **DnisPool** | Standard groups of phone numbers for inbound traffic. |
| **DnisPoolV2** | Enhanced phone number pool configurations. |
| **EmailTemplate** | Definitions for automated system emails. |
| **EmailTemplateAttachment** | Files associated with automated email templates. |
| **Gate** | Configuration for voice queues. |
| **GateDisposition** | Outcome labels for voice calls. |
| **GateGroup** | Organizational groupings for voice queues. |
| **GateGroupSkill** | Skill requirements for voice call routing. |
| **GatePriorityGroup** | Logic for weighting different voice queues. |
| **GateQueueDtmfEvent** | DTMF-based menus and actions while in queue. |
| **GateQueueEvent** | Automated actions (like hold music) while in queue. |
| **GateScheduleOverride** | Temporary calendar-based rules for voice queue availability. |
| **GateSpecialAni** | Customized handling for specific inbound caller IDs. |
| **HttpServiceMapping** | Data transformations for internal HTTP service calls. |
| **IVRApplication** | Hosted application logic for interactive menus. |
| **KnowledgeBaseArticle** | Content records for agent-facing help documentation. |
| **KnowledgeBaseCategory** | Taxonomy used to organize help documentation. |
| **KnowledgeBaseGroup** | Permission-based sets of knowledge base content. |
| **MainAccount** | Parent account attributes in multi-account hierarchies. |
| **MappingTemplate** | Reusable data structure templates. |
| **NotificationGroup** | Collections of recipients for system alerts. |
| **NotificationTarget** | Individual endpoints (email/URL) for system alerts. |
| **PendingAccount** | Staging records for new account provisioning. |
| **PhoneBookEntry** | Speed-dial and contact records. |
| **QuotaGroup** | Logic sets for managing outbound dialing limits. |
| **QuotaTarget** | Specific thresholds for outbound limits. |
| **RcAccountData** | Synchronized data from the RingCentral core platform. |
| **RecordingDestinationV2** | Storage targets for system media. |
| **RecordingTaskV2** | Scheduled logic for media processing or archival. |
| **RemoteHttpService** | Core configuration for outbound API integrations. |
| **RemoteHttpServiceGroup** | Collections of related external API calls. |
| **RemoteHttpServiceInput** | Input parameter definitions for API integrations. |
| **RequeueShortcut** | Transfer shortcuts for voice queues. |
| **ResultFileDestination** | Automated targets for campaign report delivery. |
| **RightsDocTable** | Internal security and permission mappings. |
| **RTASubscriptionConfig** | Real-time analytics subscription settings. |
| **Script** | Dynamic agent guidance scripts used during calls. |
| **ScriptGroup** | Administrative sets for organizing agent scripts. |
| **TracGroup** | Logic groups for legacy routing numbers. |
| **TracLocation** | Geographic definitions for legacy routing. |
| **TracLocator** | Search logic for legacy routing targets. |
| **TracNumber** | Legacy inbound routing numbers. |
| **TracRoutingRule** | Specific logic applied to legacy routing. |
| **TracScheduleOverride** | Temporary availability rules for legacy routing. |
| **UploadedFileResults** | Status logs for general bulk file uploads. |
| **User** | System user accounts and portal access. |
| **VisualIvr** | High-level configuration for Studio-based IVR workflows. |
| **VisualIvrConfig** | Specific node-level logic and data for Visual IVR scripts. |
| **VisualIvrGroup** | Organizational containers for grouping Visual IVR workflows. |
| **WhitelistEntry** | Records permitted to bypass security filters. |
| **WhitelistLogEntry** | Audit records of whitelist activity. |
| **WhitelistTag** | Labels used to classify whitelist entries. |
| **WhitelistTagMembers** | Member lists associated with security tags. |
| **Workflow** | Automated multi-step business process logic. |
| **WorkflowConfig** | Specific configuration versions for workflows. |
| **WorkflowGroup** | Organizational groupings for business workflows. |

</details>