# Queue Groups Basics

Queue Groups are containers for one or more groups. Queue Groups must be created before creating a queue for routing.  Once a Queue Group is created, and you set the Group Skill, create your [Queues](../queues) in the Queue Group.

## Core Concepts

### Group Skills
Group skills are short descriptions that help you map Queue Groups to Agents.  First create the Queue Group and then define the Group Skill.  Later, you will assign this Group Skill to a Agent.

### Queue Group vs Gate Group
The original terminology for a Queue Group was Gate Group. In this way, Gates and Queues are synonymous. For backward compatibility, `gate` will continue to be supported.

## Create Queue Group

Creating a new Queue Group using the `gateGroups` endpoint. Only the Queue Group name is required.

### Optional Parameters
The following parameters are optional.

| API Property | UI Display | UI Default | Description |
|-|-|-|-|
| **`billingKey`** | Hidden | *null* | *Unknown usage* |
| **`gateGroupId`** | Hidden | 0 | You can specify your gateGroupId, but by default, the next available ID is chosen for you. |

### Request
```html tab="HTTP"
POST {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups
Content-Type: application/json

{
    "groupName": "My Queue Group"
}
```

## Retrieve Queue Groups

Retrieving a list of Queue Groups using the `gateGroups` endpoint.

### Optional Parameters
The following parameters are optional.

| API Property | Type | UI Display | UI Default | Description |
|-|-|-|-|-|
| **`page`** | Integer | Hidden | 1 | A way to specify which page to show for a long number of Queue Groups |
| **`maxRows`** | Integer | Hidden | ?? | You can specify the maximum number of Queue Groups to return in a single call. |

### Request
```html tab="HTTP"
GET {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups
```

### Response
```json tab="Response"
[
  {
    "groupSkills": None,
    "groupName": "Platform",
    "gateGroupId": 52653,
    "permissions": []
  },
  {
    "groupSkills": None,
    "groupName": "Evaluations",
    "gateGroupId": 52658,
    "permissions": []
  },
  {
    "groupSkills": None,
    "groupName": "John's Queue",
    "gateGroupId": 52671,
    "permissions": []
  }
]
```

## Retrieve a Single Queue Group

Retrieving details for a single Queue Group using the `gateGroups` endpoint.

### Request
```html tab="HTTP"
GET {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupsId}
```

### Response
```json tab="Response"
{
  "startDate":"2020-04-18T01:49:32.000+0000",
  "billingKey":None,
  "createdOn":"2020-04-18T01:49:32.000+0000",
  "groupName":"Platform",
  "groupSkills":None,
  "endDate":None,
  "gateGroupId":52653,
  "permissions": []
}
```
## Update a Single Queue Group

Update the details for a single Queue Group using the `gateGroups` endpoint. Several details need to be updated with a single `PUT` command so make sure to `GET` all details, modify the relevant fields, and then submit the entire object to update the Queue Group

### Request
```html tab="HTTP"

# Retrieve the entire Queue Group JSON object
GET {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupsId}

# Modify the groupName and send the entire JSON response backward
PUT {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupsId}
Content-Type: application/json
{
  "startDate":"2020-04-18T01:49:32.000+0000",
  "billingKey":None,
  "createdOn":"2020-04-18T01:49:32.000+0000",
  "groupName":"Platform-New",
  "groupSkills":None,
  "endDate":None,
  "gateGroupId":52653,
  "permissions": []
}

```

### Response
```json tab="Response"
{
  "startDate":"2020-04-18T01:49:32.000+0000",
  "billingKey":None,
  "createdOn":"2020-04-18T01:49:32.000+0000",
  "groupName":"Platform-New",
  "groupSkills":None,
  "endDate":None,
  "gateGroupId":52653,
  "permissions": []
}
```
## Delete a Single Queue Group

Delete a single Queue Group using the `gateGroups` endpoint.

### Request
```html tab="HTTP"
DELETE {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupsId}
```
