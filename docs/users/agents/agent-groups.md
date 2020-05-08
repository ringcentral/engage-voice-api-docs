# Agent Groups

Agent groups are a the way to manage agents in Engage Voice. All agents are assigned to one and only one Agent Group.

## Create Agent Group

Creating a new Agent Group only requires a group name.

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