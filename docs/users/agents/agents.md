# About Agents

Managing agents and automatically syncing them with your user management tools can be automated via the API. This article covers the basics of creating, reading, updating deleting Agents.

Of note, Agents must be associated with an Agent Group so you need to have at least one Agent Group configured before managing Agents. See [Agent Groups](../agent-groups) for more.

## Create Agent

Before starting, make sure you have an Agent Group created and the `agentGroupId` of the group you wish to assign the Agent to.

### Primary Parameters

The following API properties are primary properties to create an agent and are also displayed in the Create Agent form in the Engage Voice Admin Console. The UI category section and property name is provided in the table below for easy mapping. Some supporting properties that are not visible in the UI are provided as well.

| API Property | | UI Category | UI Property | Description |
|-|-|-|-|-|
| **`firstName`** | Optional | Agent Information | First Name | Agent’s first name |
| **`lastName`** | Optional | Agent Information | Last Name | Agent's last name |
| **`email`** | Optional | Agent Information | Email | Agent's email address |
| **`externalAgentId`** | Optional | Agent Information | External Agent ID | If you have external systems that reference agents by their own unique identifiers, enter that unique identifier in this setting |
| **`location`** | Optional | Agent Information | Location | Agent's location |
| **`team`** | Optional | Agent Information | Team | Agent's team name |
| **`rcUserId`** | Optional | Agent Information | RC Office extension | Office extensionId. Sync a RingCentral Office user to the new agent user. This will link the agent’s basic information from RingCentral Office to their information in Engage Voice, such as their first and last name, their email address, and username and password. Retrieve a list of [Extensions](./#extensions) and use the `id` value. |
| **`userManagedByRC`** | Optional | Agent Information | RC Office extension  | `false` |
| **`allowLoginControl`** | Optional | Login Settings | Allow Login | `true` |
| **`allowLoginUpdates`** | Optional | Login Settings | Allow Login | `true` |
| **`username`** | Required | Login Settings | Username | |
| **`password`** | Required | Login Settings | Password | |
| **`agentType`** | Optional | Login Settings | Agent Type | Select what type this agent is `AGENT` or `SUPERVISOR`. Use values from [Agent Type](./#agent-type) |
| **`agentRank`** | Optional | Login Settings | Agent Rank | `0` - `24` with `0` being the lowest, `12` being medium and `24` being high. |
| **`initLoginBaseState`** | Optional | Login Settings | Initial State | Example: `AVAILABLE`. Retrieve a list of valid states using [Initial State](./#initial-state) and use the values in `baseAgentState.colKey`. |
| **`initLoginBaseStateId`** | Optional | Login Settings | Initial State | Example: `11786` Retrieve a list of valid states using [Initial State](./#initial-state) and use the values in `stateId`. |
| **`ghostRnaAction`** | Optional | Login Settings | Ghost RNA Action | Example: `AVAILABLE` |
| **`dialGroupAssignments`** | Optional | Login Settings | Default Dial Group | Enter the dial group you wish to show to be preselected when the agent first logs in. Example: `{"id":111111}`. Retrieve a list of valid values using [Dial Groups](./#dial-groups) and use a `dialGroupId` value as the `dialGroupAssignments.id`. |
| **`manualOutboundDefaultGate`** | Optional | Login Settings | Manual Outbound Default Queue Assignment | Example: `{id: 222222}`. Retrieve a list of valid values using [Queue Groups](./#queue-groups). Each `gateGroup` will contain a list of queues with a `gateId` and can be used as the `manualOutboundDefaultGate.id` value in this request. |
| **`enableSoftphone`** | Optional | Phone Settings | Enable Softphone | `true` |
| **`defaultLoginDest`** | Optional | Phone Settings | Default Route | |
| **`altDefaultLoginDest`** | Optional | Phone Settings | Alt. Default Route | |
| **`phoneLoginPin`** | Optional | Phone Settings | Phone Login PIN | |
| **`directAgentExtension`** | Optional | Phone Settings | Direct Dial Extension | |
| **`manualOutboundDefaultCallerId`** | Optional | Phone Settings | Manual Outbound Default Caller ID | |
| **`maxChats`** | Optional | Chat Settings | Max Number of Concurrent Chats | |

### Supporting APIs

The following APIs can be used to retrieve information to populate various properties in the requests.

#### Initial State

The default agent state is `AVAILABLE` (that is, ready to take or make a call or chat). Any other state will require the agent to manually set themselves to an Available base state after login in order to take calls The options presented here will depend on the agent states created via the Agent States configuration panel option at the account level

  `GET {BASE_URL}/api/v1/admin/accounts/{accountId}/auxStates/?activeOnly=true`

#### Dial Groups

Get a list of dial groups.

  `GET {BASE_URL}/api/v1/admin/accounts/{accountId}/dialGroup`

#### Queue Groups

Get a list of queue groups and corresponding queues in this account.

  `GET api/v1/admin/accounts/{accountId}/gateGroups/withChildren`

#### Extensions

Gets a list agents and their corresponding extensions.

  `GET {BASE_URL}/api/v1/admin/accounts/{accountId}/ringcentral/extensions`

#### Agent Type

The parameter `agentType` can take on the following values:

    | Value | Description |
    |-|-|
    | **`AGENT`** | If you don’t want the agent to monitor other agents, select this option |
    | **`SUPERVISOR`** | If you want the agent to listen in and monitor other agent calls, select this option |

### Request

Be sure to sure to use the proper `BASE_URL` and authorization header for your deployment.

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
    "firstName":"My New First Name"
    ...
}
```

## Delete Agent

```html tab="HTTP"
DELETE api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}`
```
