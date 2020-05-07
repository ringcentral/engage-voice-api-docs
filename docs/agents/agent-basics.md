# Agent Basics

Managing agents and automatically syncing them with your user management tools can be automated via the API.

## Create Agent

### API Endpoints

* `POST /voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents`

Supporting APIs

* `GET /voice/api/v1/admin/accounts/{accountId}/ringcentral/extensions`
* `GET /voice/api/v1/admin/accounts/{accountId}/auxStates/?activeOnly=true`

### UI to API Property Mapping

| UI Category | UI Property | API Property | Description |
|-|-|-|-|
| Agent Information | First Name | **`firstName`** | |
| Agent Information | Last Name | **`lastName`** | |
| Agent Information | Email | **`email`** | |
| Agent Information | External Agent ID | **`externalAgentId`** | |
| Agent Information | Location | **`location`** | |
| Agent Information | Team | **`team`** | |
| Agent Information | RC Office extension | **`rcUserId`** | Office extensionId. Retrieve a list using `/api/v1/admin/accounts/{accountId}/ringcentral/extensions` |
| Login Settings | Allow Login | **`allowLoginControl`** | `true` |
| Login Settings | Allow Login | **`allowLoginUpdates`** | `true` |
| Login Settings | Username | **`username`** | |
| Login Settings | Password | **`password`** | |
| Login Settings | Agent Type | **`agentType`** | |
| Login Settings | Agent Rank | **`agentRank`** | `0` - Lowest |
| Login Settings | Initial State | **`initLoginBaseState`** | `AVAILABLE` |
| Login Settings | Initial State | **`initLoginBaseStateId`** | `11786` |
| Login Settings | Ghost RNA Action | **`ghostRnaAction`** | `AVAILABLE` |
| Login Settings | Default Dial Group | **`dialGroupAssignments`** | |
| Login Settings | Manual Outbound Default Queue Assignment | **`manualOutboundDefaultGate`** | `{id: 72899}` |
| Phone Settings | Enable Softphone | **`enableSoftphone`** | `true` |
| Phone Settings | Default Route | **`defaultLoginDest`** | |
| Phone Settings | Alt. Default Route | **`altDefaultLoginDest`** | |
| Phone Settings | Phone Login PIN | **`phoneLoginPin`** | |
| Phone Settings | Direct Dial Extension | **`directAgentExtension`** | |
| Phone Settings | Manual Outbound Default Caller ID | **`manualOutboundDefaultCallerId`** | |
| Chat Settings | Max Number of Concurrent Chats | **`maxChats`** | |

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
