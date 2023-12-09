# About Queue Group Skills

Creating group skills is the first step in the process of assigning skills to your agents. After you create group skills, you’ll also need to add these skills (via Queue Events) to any queue that you assign these agents to.  First create the [Queue Group](queue-groups.md) and then define the Group Skill.  Later, you will assign this Group Skill to the desired [Agent](../../users/agents/agents.md).

## Create Groups Skills

Create a set of new Group Skills using the `skills` endpoint. Only the Queue Group name is required. You can create multiple Group Skills with this command.  To create only a single Group Skill, create an array with only a single entry.

### Primary Parameters
Only `gateName` is a required parameter to create a Queue. All other parameters are optional.

| API Property |  | UI Display | UI Default | Description |
|-|-|-|-|-|
| **`skillId`** | Optional | ID | 0 | A Group Skill unique ID. If not provided an available skill ID will be created for you. |
| **`skillName`** | Required | Name | *empty* | Give this skill a name that will be assigned to this Queue Group. |
| **`skillDesc`** | Optional | Description | *empty* | Provide a short description of the skill. |
| **`active`** | Optional | Active | Yes | Set this skill to Active by setting it to `true`. |
| **`whisperAudio`** | Optional | **None** | *empty* | A link to the short audio file that plays a message to the agent as they connect with a customer. The audio may inform the agent about the incoming call, or prompt the agent to accept the call. |
| **`createOn`** | Optional | Created | *current date* | A date in Simple Date Format. |
| **`agentSkillProfiles`** | Optional | **None** | *empty* | Custom skills defined and bound to an Agent to redirect these queues to. |
| **`requeueShortcut`** | Optional | **None** | *empty* | Allow agents to manually send their current call to a specific inbound queue, or to another agent with a special skill. |

### Sample request

Be sure to set the proper [BASE_URL](../../basics/uris.md#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral.md) for your deployment.

```http
POST {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills
Content-Type: application/json

[
  {
    "skillName":"Spanish Language",
    "skillDesc":"A test skill for Spanish",
    "active":true,
  },
  {
    "skillName":"French Language",
    "skillDesc":"A test skill for French",
    "active":true,
  }
]
```

### Sample response

```json
[
  {
    "skillId":1455,
    "skillName":"Spanish Language",
    "skillDesc":"A test skill for Spanish",
    "active":true,
    "whisperAudio":null,
    "createdOn":"2020-05-19T16:53:17.000+0000",
    "agentSkillProfiles":null,
    "requeueShortcut":null
  },
  {
    "skillId":1456,
    "skillName":"French Language",
    "skillDesc":"A test skill for French",
    "active":true,
    "whisperAudio":null,
    "createdOn":"2020-05-19T17:25:13.000+0000",
    "agentSkillProfiles":null,
    "requeueShortcut":null
  }
]
```

## Retrieve Group Skills

Retrieve a list of Group Skills using the `skills` endpoint.

### Sample request

Be sure to set the proper [BASE_URL](../../basics/uris.md#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral.md) for your deployment.

```html
GET {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills
```

### Sample response

```json
[
  {
    "skillId":1455,
    "skillName":"Spanish Language",
    "skillDesc":"A test skill for Spanish",
    "active":true,
    "whisperAudio":null,
    "createdOn":"2020-05-19T16:53:17.000+0000",
    "agentSkillProfiles":null,
    "requeueShortcut":null
  },
  {
    "skillId":1456,
    "skillName":"French Language",
    "skillDesc":"A test skill for French",
    "active":true,
    "whisperAudio":null,
    "createdOn":"2020-05-19T17:25:13.000+0000",
    "agentSkillProfiles":null,
    "requeueShortcut":null
  }
]
```

## Update a list of Group Skills

Update a list of Group Skills using the `skills` endpoint.  This `PUT` allows you to update muliple skills for the Queue Group in a single call.

### Sample request

Be sure to set the proper [BASE_URL](../../basics/uris.md#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral.md) for your deployment.

#### Retrieve the list of current skills as JSON

```http hl_lines="7 17 32 42"
GET {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills

[
  {
    "skillId":1455,
    "skillName":"Spanish Language",
    "skillDesc":"A test skill for Spanish",
    "active":true,
    "whisperAudio":null,
    "createdOn":"2020-05-19T16:53:17.000+0000",
    "agentSkillProfiles":null,
    "requeueShortcut":null
  },
  {
    "skillId":1456,
    "skillName":"French Language",
    "skillDesc":"A test skill for French",
    "active":true,
    "whisperAudio":null,
    "createdOn":"2020-05-19T17:25:13.000+0000",
    "agentSkillProfiles":null,
    "requeueShortcut":null
  }
]
```
#### Modify a field like `skillDesc` and send back the entire JSON skill object

```http
PUT {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills

[
  {
    "skillId":1455,
    "skillName":"Spanish Language",
    "skillDesc":"A *new* skill for Spanish",
    "active":true,
    "whisperAudio":null,
    "createdOn":"2020-05-19T16:53:17.000+0000",
    "agentSkillProfiles":null,
    "requeueShortcut":null
  },
  {
    "skillId":1456,
    "skillName":"French Language",
    "skillDesc":"A *new* skill for French",
    "active":true,
    "whisperAudio":null,
    "createdOn":"2020-05-19T17:25:13.000+0000",
    "agentSkillProfiles":null,
    "requeueShortcut":null
  }
]
```

### Sample response

```json
[
  {
    "skillId":1455,
    "skillName":"Spanish Language",
    "skillDesc":"A *new* skill for Spanish",
    "active":true,
    "whisperAudio":null,
    "createdOn":"2020-05-19T16:53:17.000+0000",
    "agentSkillProfiles":null,
    "requeueShortcut":null
  },
  {
    "skillId":1456,
    "skillName":"French Language",
    "skillDesc":"A *new* skill for French",
    "active":true,
    "whisperAudio":null,
    "createdOn":"2020-05-19T17:25:13.000+0000",
    "agentSkillProfiles":null,
    "requeueShortcut":null
  }
]
```

## Retrieve a Single Group Skill

Retrieve details of a single Group Skill using the `skills` endpoint.

### Sample request

Be sure to set the proper [BASE_URL](../../basics/uris.md#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral.md) for your deployment.

```html
GET {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills/{skillId}
```

### Sample response

```json
{
  "skillId":1455,
  "skillName":"Spanish Language",
  "skillDesc":"A test skill for Spanish",
  "active":true,
  "whisperAudio":null,
  "createdOn":"2020-05-19T16:53:17.000+0000",
  "agentSkillProfiles":null,
  "requeueShortcut":null
}
```

## Update a Single Group Skill

Update a single Group Skill using the `skills` endpoint.  This `PUT` focuses on just a single skill for the Queue Group.

### Sample request

Be sure to set the proper [BASE_URL](../../basics/uris.md#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral.md) for your deployment.

#### Retrieve the list of current skills as JSON

```http hl_lines="6"
GET {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills

{
  "skillId":1455,
  "skillName":"Spanish Language",
  "skillDesc":"A test skill for Spanish",
  "active":true,
  "whisperAudio":null,
  "createdOn":"2020-05-19T16:53:17.000+0000",
  "agentSkillProfiles":null,
  "requeueShortcut":null
}
```
#### Modify a field like `skillDesc` and send back the entire JSON skill object

```http hl_lines="6"
PUT {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills

{
  "skillId":1455,
  "skillName":"Spanish Language",
  "skillDesc":"A *new* skill for Spanish",
  "active":true,
  "whisperAudio":null,
  "createdOn":"2020-05-19T16:53:17.000+0000",
  "agentSkillProfiles":null,
  "requeueShortcut":null
}
```

### Sample response

```json
{
  "skillId":1455,
  "skillName":"Spanish Language",
  "skillDesc":"A *new* skill for Spanish",
  "active":true,
  "whisperAudio":null,
  "createdOn":"2020-05-19T16:53:17.000+0000",
  "agentSkillProfiles":null,
  "requeueShortcut":null
}
```

## Delete a Single Skill

Delete a single Skill using the `skills` endpoint.  You can only delete a single skill at a time.

### Sample request

Be sure to set the proper [BASE_URL](../../basics/uris.md#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral.md) for your deployment.

```html
DELETE {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/skills/{skillId}
```
