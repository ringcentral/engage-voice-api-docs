# About Queue Groups

Queue Groups are containers for one or more groups. Queue Groups must be created before creating a queue for routing.  Once a Queue Group is created, and you set the Group Skill, create your [Queues](queues.md) in the Queue Group.

## Core Concepts

### Group Skills
Group skills are short descriptions that help you map Queue Groups to Agents.  First create the Queue Group and then define the Group Skill.  Later, you will assign this Group Skill to a Agent.

### Queue Group vs Gate Group

The original terminology for a Queue Group was Gate Group. In this way, Gates and Queues are synonymous. For backward compatibility, `gate` will continue to be supported.

## Create Queue Group

Creating a new Queue Group using the `gateGroups` endpoint. Only the Queue Group name is required.

### Primary Parameters

Only `groupName` is a required parameter to create a Queue Group. All other parameters are optional.

| API Property | | UI Display | UI Default | Description |
|-|-|-|-|-|
| **`groupName`** | Required | Name | *empty* | Name for this new Queue Group |
| **`billingKey`** | Optional | *hidden* | *null* | If you use an external billing system, you can provide the billing code from that system in the queue to easily keep track of which customers (represented by the queue) are tied to which billing code.  This setting is for reporting purposes only |
| **`gateGroupId`** | Optional | *hidden* | 0 | You can specify your gateGroupId, but by default, the next available ID is chosen for you. |

### Code samples

Be sure to set the proper [BASE_URL](../../basics/uris.md#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral.md) for your deployment.

=== "Javascript"

    ```javascript
    {!> code-samples/routing/queue-group-create.js !}
    ```

=== "Python"

    ```python
    {!> code-samples/routing/queue-group-create.py !}
    ```

=== "PHP"

    ```php
    {!> code-samples/routing/queue-group-create.php !}
    ```

### Sample request

```http
POST {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups
Content-Type: application/json

{
    "groupName": "My New Queue Group"
}
```

### Sample response

```json
{!> code-samples/routing/queue-group-create-response.json !}
```

## Retrieve Queue Groups

Retrieve a list of Queue Groups using the `gateGroups` endpoint.

### Optional Parameters

The following parameters are optional.

| API Property | Type | UI Display | UI Default | Description |
|-|-|-|-|-|
| **`page`** | Integer | Hidden | 1 | A way to specify which page to show for a long number of Queue Groups |
| **`maxRows`** | Integer | Hidden | ?? | You can specify the maximum number of Queue Groups to return in a single call. |

### Code samples
Be sure to set the proper [BASE_URL](../../basics/uris.md#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral.md) for your deployment.

=== "Javascript"

    ```javascript
    {!> code-samples/routing/queue-group-retrieve.js !}
    ```
	
=== "Python"

    ```python
    {!> code-samples/routing/queue-group-retrieve.py !}
    ```
	
=== "PHP"

    ```php
    {!> code-samples/routing/queue-group-retrieve.php !}
    ```

### Sample request

=== "HTTP"

```html
GET {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups
```

### Sample response

```json
{!> code-samples/routing/queue-group-retrieve-response.json !}
```

## Retrieve a Single Queue Group

Retrieve details for a single Queue Group using the `gateGroups` endpoint.

### Code samples

Be sure to set the proper [BASE_URL](../../basics/uris.md#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral.md) for your deployment.

=== "Javascript"

    ```javascript
    {!> code-samples/routing/queue-group-retrieve-single.js !}
    ```

=== "Python"

    ```python
    {!> code-samples/routing/queue-group-retrieve-single.py !}
    ```

### Sample request 

```html
GET {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}
```


### Sample response

```json
{!> code-samples/routing/queue-group-retrieve-single-response.json !}
```

## Update a Single Queue Group

Update the details for a single Queue Group using the `gateGroups` endpoint. Several details need to be updated with a single `PUT` command so make sure to `GET` all details, modify the relevant fields, and then submit the entire object to update the Queue Group

### Code samples

Be sure to set the proper [BASE_URL](../../basics/uris.md#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral.md) for your deployment.
	
=== "Javascript"

    ```javascript
    {!> code-samples/routing/queue-group-update.js !}    
    ```
	
=== "Python"

    ```python
    {!> code-samples/routing/queue-group-update.py !}    
    ```
	
=== "PHP"

    ```php
    {!> code-samples/routing/queue-group-update.php !}    
    ```

### Sample request

#### Retrieve the entire Queue Group JSON object

```http 
GET {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}
```

#### Modify the groupName

```http
PUT {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}
Content-Type: application/json

{
  "groupName":"My New Queue Group Name - Updated",
}
```

### Sample response

```json
{!> code-samples/routing/queue-group-update-response.json !}    
```

## Delete a Single Queue Group

Delete a single Queue Group using the `gateGroups` endpoint.

Be sure to set the proper [BASE_URL](../../basics/uris.md#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral.md) for your deployment.

#### Sample request

```html
DELETE {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}
```
