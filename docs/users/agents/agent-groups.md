# About Agent Groups

Agent groups are a the way to manage agents in Engage Voice. All agents are assigned to one and only one Agent Group. Agent groups can be used to organize your agents into different categories, which can be useful in situations like when you’d like to separate your agents into groups that represent the different teams in your contact center.

## Create Agent Group

Creating a new Agent Group only requires a group name.

### Primary Parameters
Only `groupName` is a required parameter to create a skill profile. All other parameters are optional.

| API Property |  | UI Display | UI Default | Description |
|-|-|-|-|-|
| **`agentGroupId`** | Optional | *hidden* | 0 | A unique identifier for this Agent Group. |
| **`groupName`** | Required | Name | *empty* | Give this Agent Group a name. |
| **`isDefault`** | Optional | *hidden* | false |  |


### Request

```html tab="HTTP"
POST {BASE_URL}/api/v1/admin/accounts/{accountId}/agentGroups
Content-Type: application/json

{
    "groupName": "My Agent Group"
}
```

## Read Agent Groups

To retrieve a list of Agent Groups, use the `agentGroups` API endpoint.

### Request

```html tab="HTTP"
GET api/v1/admin/accounts/{accountId}/agentGroups
```

### Response

```json tab="Response"
[
  {
    "permissions":[

    ],
    "agentGroupId":1111,
    "groupName":"Platform Team",
    "isDefault":false
  },
  {
    "permissions":[

    ],
    "agentGroupId":2222,
    "groupName":"Dev Support",
    "isDefault":false
  }
]
```

## Read Agent Group

To retrieve a single Agent Group, use the `agentGroups` API endpoint with a specific agent group ID.

### Request

```html tab="HTTP"
GET api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}
```

### Response

`account` data is omitted in the example below.

```json tab="Response"
{
  "permissions":[],
  "agentGroupId":1950,
  "groupName":"Test Group2",
  "isDefault":false,
  "account":{}
}
```

## Update Agent Group

To Update an Agent Group's name, get the Agent Group's JSON object, modify the `groupName` and then `PUT` the JSON to back the the Agent Group's endpoint:

```html tab="HTTP"
# Retrieve Agent Group JSON object
GET api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}

# Modify `groupName` and `PUT` JSON object
PUT api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}
Content-Type: application/json

{
    "agentGroupId":111,
    "groupName":"My Agent Group"
    ...
}
```

## Delete Agent Group

### Request

```html tab="HTTP"
DELETE api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}
```
