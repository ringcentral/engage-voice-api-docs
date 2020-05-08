# Agent Basics

Managing agents and automatically syncing them with your user management tools can be automated via the API. This article covers the basics oof creating, reading, updating deleting Agents.

Of note, Agents must be associated with an Agent Group so yuo neeed to have at least one Agent Group configured before managing Agents. See [Agent Groups](../agent-groups) for more.

## Create Agent

Before starting, make sure you have an Agent Group created and the `agentGroupId` of the group you wish to assign the Agent to.

### API Endpoint

To create an agent, send an API request to the following URL with a JSON encoded body as described and shown below.

* `POST /voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents`

#### Supporting APIs

The following APIs can be used to retrieve information to populate various properties in the requests.

* `GET api/v1/admin/accounts/{accountId}/auxStates/?activeOnly=true`
* `GET api/v1/admin/accounts/{accountId}/dialGroup`
* `GET api/v1/admin/accounts/{accountId}/gateGroups/withChildren`
* `GET api/v1/admin/accounts/{accountId}/ringcentral/extensions`

### Primary Properties

All properties for the agent are submitted in a JSON object in the request body.

The following API properties are primary properetiess to create an agent and are alos displayed in the Create Agent form in the Engage Voice Admin Console. The UI category section and property name is provided in the table below for easy mapping. Some supporting properties not visible in the UI are provided as well.

| API Property | UI Category | UI Property | Description |
|-|-|-|-|
| **`firstName`** | Agent Information | First Name | |
| **`lastName`** | Agent Information | Last Name | |
| **`email`** | Agent Information | Email | |
| **`externalAgentId`** | Agent Information | External Agent ID | |
| **`location`** | Agent Information | Location | |
| **`team`** | Agent Information | Team | |
| **`rcUserId`** | Agent Information | RC Office extension | Office extensionId. Retrieve a list using `/api/v1/admin/accounts/{accountId}/ringcentral/extensions` and use the `id` value. |
| **`userManagedByRC`** | Agent Information | RC Office extension  | `false` |
| **`allowLoginControl`** | Login Settings | Allow Login | `true` |
| **`allowLoginUpdates`** | Login Settings | Allow Login | `true` |
| **`username`** | Login Settings | Username | |
| **`password`** | Login Settings | Password | |
| **`agentType`** | Login Settings | Agent Type | `AGENT` or `SUPERVISOR` |
| **`agentRank`** | Login Settings | Agent Rank | `0` - `24` with `0` being the lowest, `12` being medium and `24` being high. |
| **`initLoginBaseState`** | Login Settings | Initial State | Example: `AVAILABLE`. For a list, call `api/v1/admin/accounts/{accountId}/auxStates/?activeOnly=true` and use the values in `baseAgentState.colKey`. |
| **`initLoginBaseStateId`** | Login Settings | Initial State | Example: `11786` For a list, call `api/v1/admin/accounts/{accountId}/auxStates/?activeOnly=true` and use the values in `stateId`. |
| **`ghostRnaAction`** | Login Settings | Ghost RNA Action | Example: `AVAILABLE` |
| **`dialGroupAssignments`** | Login Settings | Default Dial Group | Example: `{"id":111111}`. For a list of values, use the `api/v1/admin/accounts/{accountId}/dialGroups` API and use a `dialGroupId` value as the `dialGroupAssignments.id`. |
| **`manualOutboundDefaultGate`** | Login Settings | Manual Outbound Default Queue Assignment | `{id: 222222}`, For a list, use the `api/v1/admin/accounts/{accountId}/gateGroups/withChildren` API. Each `gateGroup` will contain a list of gates with a `gateId` can be used as the `manualOutboundDefaultGate.id` value in this request. |
| **`enableSoftphone`** | Phone Settings | Enable Softphone | `true` |
| **`defaultLoginDest`** | Phone Settings | Default Route | |
| **`altDefaultLoginDest`** | Phone Settings | Alt. Default Route | |
| **`phoneLoginPin`** | Phone Settings | Phone Login PIN | |
| **`directAgentExtension`** | Phone Settings | Direct Dial Extension | |
| **`manualOutboundDefaultCallerId`** | Phone Settings | Manual Outbound Default Caller ID | |
| **`maxChats`** | Chat Settings | Max Number of Concurrent Chats | |

### Additional Properties

The following propereties can also be set. Default values used by the UI are presented below.

| API Property | UI Default | Description |
|-|-|-|
| **`allowInbound`** | `true` | |
| **`allowOutbound`** | `false` | |
| **`allowExternalChat`** | `false` | |
| **`allowChat`** | `false` | |
| **`allowBlended`** | `false` | |
| **`allowChatVoiceConcurrent`** | `false` | |
| **`allowOffHook`** | `false` | |
| **`allowCallControl`** | `true` | |
| **`allowHold`** | `true` | |
| **`allowTransfer`** | `true` | |
| **`allowManualIntlTransfer`** | `false` | |
| **`allowDirectAgentTransfer`** | `DIRECT_TRANSFER_DISABLED` | |
| **`allowHangup`** | `true` | |
| **`allowRequeue`** | `true` | |
| **`allowLoginControl`** | `true` | |
| **`allowLoginUpdates`** | `true` | |
| **`allowCrossGateRequeue`** | `true` | |
| **`gatesControlAgentVisibility`** | `true` | |
| **`allowCampStats`** | `true` | |
| **`allowGateStats`** | `true` | |
| **`allowAgentStats`** | `true` | |
| **`allowSelfAgentStats`** | `false` | |
| **`allowChatStats`** | `true` | |
| **`disableSupervisorMonitoring`** | `false` | |
| **`allowAgentReports`** | `false` | |
| **`allowManualCalls`** | `true` | |
| **`allowManualIntlCalls`** | `false` | |
| **`allowInboundIntlTransfer`** | `false` | |
| **`allowLeadInserts`** | `false` | |
| **`allowAutoAnswer`** | `false` | |
| **`defaultAutoAnswerOn`** | `true` | |
| **`isActive`** | `true` | |
| **`loadBalanceEnabled`** | `false` | |
| **`transientAgent`** | `false` | |
| **`parentAgentId`** | `null` | |
| **`transientDelete`** | `false` | |
| **`multiAccountAgent`** | `false` | |
| **`enableSoftphone`** | `false` | |
| **`softphoneId`** | `0` | |
| **`showLeadHistory`** | `true` | |
| **`manualOutboundDefaultCallerId`** | `""` | |
| **`allowManualOutboundGates`** | `false` | |
| **`allowManualPass`** | `true` | |
| **`allowEndcallforeveryone`** | `true` | |
| **`allowHistoricalDialing`** | `true` | |
  
### Example Request

Be sure to sure the proper `BASE_URL` and authorization header for your deployment.

```
POST {BASE_URL}/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents

{
  "firstName":"John",
  "lastName":"Wang",
  "username":"johnwang",
  "password":"<myPassword>",
  "agentType":"AGENT",
  "initLoginBaseState":"AVAILABLE",
  "initLoginBaseStateId":11786,
  "ghostRnaAction":"AVAILABLE",
  "maxChats":5,
  "allowInbound":true,
  "allowOutbound":true
}
```

## Read Agents

```html tab="HTTP"
GET api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents`
```

## Read Agent

```html tab="HTTP"
GET api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}`
```

## Update Agent

To Update an Agent Group's name, get the Agent Group's JSON object, modify the `groupName` and then `PUT` the JSON to back the the Agent Group's endpoint:

```html tab="HTTP"
# Retrieve Agent Group JSON object
GET api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}

# Modify `groupName` and `PUT` JSON object
PUT api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}
Content-Type: application/json

{
    "groupName":"My New First Name"
    ...
}
```

## Delete Agent

```html tab="HTTP"
DELETE api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}`
```
