# Agent Basics

Managing agents and automatically syncing them with your user management tools can be automated via the API.

## Create Agent

### API Endpoints

* `POST /voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents`

#### Supporting APIs

* `GET /voice/api/v1/admin/accounts/{accountId}/ringcentral/extensions`
* `GET /voice/api/v1/admin/accounts/{accountId}/auxStates/?activeOnly=true`

### API to UI Property Mapping

The following API properties are displayed in the Create Agent form in the Engage Voice Admin Console.

| API Property | UI Category | UI Property | Description |
|-|-|-|-|
| **`firstName`** | Agent Information | First Name | |
| **`lastName`** | Agent Information | Last Name | |
| **`email`** | Agent Information | Email | |
| **`externalAgentId`** | Agent Information | External Agent ID | |
| **`location`** | Agent Information | Location | |
| **`team`** | Agent Information | Team | |
| **`rcUserId`** | Agent Information | RC Office extension | Office extensionId. Retrieve a list using `/api/v1/admin/accounts/{accountId}/ringcentral/extensions` |
| **`allowLoginControl`** | Login Settings | Allow Login | `true` |
| **`allowLoginUpdates`** | Login Settings | Allow Login | `true` |
| **`username`** | Login Settings | Username | |
| **`password`** | Login Settings | Password | |
| **`agentType`** | Login Settings | Agent Type | |
| **`agentRank`** | Login Settings | Agent Rank | `0` - Lowest |
| **`initLoginBaseState`** | Login Settings | Initial State | `AVAILABLE` |
| **`initLoginBaseStateId`** | Login Settings | Initial State | `11786` |
| **`ghostRnaAction`** | Login Settings | Ghost RNA Action | `AVAILABLE` |
| **`dialGroupAssignments`** | Login Settings | Default Dial Group | |
| **`manualOutboundDefaultGate`** | Login Settings | Manual Outbound Default Queue Assignment | `{id: 72899}` |
| **`enableSoftphone`** | Phone Settings | Enable Softphone | `true` |
| **`defaultLoginDest`** | Phone Settings | Default Route | |
| **`altDefaultLoginDest`** | Phone Settings | Alt. Default Route | |
| **`phoneLoginPin`** | Phone Settings | Phone Login PIN | |
| **`directAgentExtension`** | Phone Settings | Direct Dial Extension | |
| **`manualOutboundDefaultCallerId`** | Phone Settings | Manual Outbound Default Caller ID | |
| **`maxChats`** | Chat Settings | Max Number of Concurrent Chats | |

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

## Read Agent

## Update Agent

* `PUT /voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}`

## Delete Agent
