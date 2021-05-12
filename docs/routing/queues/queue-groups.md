# About Queue Groups

Queue Groups are containers for one or more groups. Queue Groups must be created before creating a queue for routing.  Once a Queue Group is created, and you set the Group Skill, create your [Queues](../queues) in the Queue Group.

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

### Request
Be sure to set the proper [BASE_URL](../../../basics/uris/#resources-and-parameters) and [authorization header](../../../authentication/auth-ringcentral) for your deployment.

```html tab="HTTP"
POST {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups
Content-Type: application/json

{
    "groupName": "My New Queue Group"
}
```

```javascript tab="Node JS"
/****** Install Node JS SDK wrapper *******
$ npm install ringcentral-engage-voice-client
*******************************************/

const RunRequest = async function () {
    const EngageVoice = require('ringcentral-engage-voice-client').default

    // Instantiate the SDK wrapper object with your RingCentral app credentials
    const ev = new EngageVoice({
        clientId: "RINGCENTRAL_CLIENTID",
        clientSecret: "RINGCENTRAL_CLIENTSECRET"
    })

    try {
        // Authorize with your RingCentral Office user credentials
        await ev.authorize({
            username: "RINGCENTRAL_USERNAME",
            extension: "RINGCENTRAL_EXTENSION",
            password: "RINGCENTRAL_PASSWORD"
        })

        // Create a new Queue Group
        const postBody = {
            "groupName": "My New Queue Group"
        }
        const response = await ev.post('/api/v1/admin/accounts/{accountId}/gateGroups', postBody)
        console.log(response);
    }
    catch (err) {
        console.log(err.message)
    }
}

RunRequest();
```

```python tab="Python"
from engagevoice.sdk_wrapper import *

# Instantiate the SDK wrapper object with your RingCentral app credentials
ev = RestClient("RC_APP_CLIENT_ID", "RC_APP_CLIENT_SECRET")

# Login your account with your RingCentral Office user credentials
try:
    ev.login("RC_USERNAME", "RC_PASSWORD", "RC_EXTENSION_NUMBER")
    endpoint = 'admin/accounts/~/gateGroups'
    params = {
              "groupName":"My New Queue Group"
                }
    response = ev.post(endpoint, params)
    print (response)        
except Exception as e:
    print (e)
```

```php tab="PHP"
<?php
require('vendor/autoload.php');

// Instantiate the SDK wrapper object with your RingCentral app credentials
$ev = new EngageVoiceSDKWrapper\RestClient("RC_APP_CLIENT_ID", "RC_APP_CLIENT_SECRET");
try{
  // Login your account with your RingCentral Office user credentials
  $ev->login("RC_USERNAME", "RC_PASSWORD", "RC_EXTENSION_NUMBER");
  $endpoint = "admin/accounts/~/gateGroups";
  $params = array ( 'groupName' => "My New Queue Group" );
  $response = $ev->post($endpoint, $params);
  print ($response."\r\n");
}catch (Exception $e) {
  print $e->getMessage();
}
```

### Sample response
    ```json
    {
      "startDate":"2020-04-18T01:49:32.000+0000",
      "billingKey":null,
      "createdOn":"2020-04-18T01:49:32.000+0000",
      "groupName":"My New Queue Group",
      "groupSkills":null,
      "endDate":null,
      "gateGroupId":52653,
      "permissions": []
    }
    ```

## Retrieve Queue Groups

Retrieve a list of Queue Groups using the `gateGroups` endpoint.

### Optional Parameters
The following parameters are optional.

| API Property | Type | UI Display | UI Default | Description |
|-|-|-|-|-|
| **`page`** | Integer | Hidden | 1 | A way to specify which page to show for a long number of Queue Groups |
| **`maxRows`** | Integer | Hidden | ?? | You can specify the maximum number of Queue Groups to return in a single call. |

### Request
Be sure to set the proper [BASE_URL](../../../basics/uris/#resources-and-parameters) and [authorization header](../../../authentication/auth-ringcentral) for your deployment.

```html tab="HTTP"
GET {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups
```

```javascript tab="Node JS"
/****** Install Node JS SDK wrapper *******
$ npm install ringcentral-engage-voice-client
*******************************************/

const RunRequest = async function () {
    const EngageVoice = require('ringcentral-engage-voice-client').default

    const ev = new EngageVoice({
        clientId: "RINGCENTRAL_CLIENTID",
        clientSecret: "RINGCENTRAL_CLIENTSECRET"
    })

    try {
        // Authorize with your RingCentral Office user credentials
        await ev.authorize({
            username: "RINGCENTRAL_USERNAME",
            extension: "RINGCENTRAL_EXTENSION",
            password: "RINGCENTRAL_PASSWORD"
        })

        // Get Queue Groups data
        const groupsEndpoint = "/api/v1/admin/accounts/{accountId}/gateGroups"
        const groupsResponse = await ev.get(groupsEndpoint)
        for (var group of groupsResponse.data) {
            // Get Queues under your Queue Group
            if (group.groupName == "My New Queue Group") {
                const queueEndpoint = groupsEndpoint + "/" + group.gateGroupId + "/gates"
                const queueResponse = await ev.get(queueEndpoint)
                console.log(queueResponse.data);
            }
        }
    }
    catch (err) {
        console.log(err.message)
    }
}

RunRequest();
```

```python tab="Python"
from engagevoice.sdk_wrapper import *

# Instantiate the SDK wrapper object with your RingCentral app credentials
ev = RestClient("RC_APP_CLIENT_ID", "RC_APP_CLIENT_SECRET")

# Login your account with your RingCentral Office user credentials
try:
    ev.login("RC_USERNAME", "RC_PASSWORD", "RC_EXTENSION_NUMBER")
    endpoint = 'admin/accounts/~/gateGroups'
    resp = ev.get(endpoint)
    for group in resp:
        print ("Queue group name: " + group['groupName'])
        print ("Queue group id: " + str(group['gateGroupId']))
except Exception as e:
    print (e)
```

```php tab="PHP"
<?php
require('vendor/autoload.php');

// Instantiate the SDK wrapper object with your RingCentral app credentials
$ev = new EngageVoiceSDKWrapper\RestClient("RC_APP_CLIENT_ID", "RC_APP_CLIENT_SECRET");
try{
  // Login your account with your RingCentral Office user credentials
  $ev->login("RC_USERNAME", "RC_PASSWORD", "RC_EXTENSION_NUMBER");
  $endpoint = "admin/accounts/~/gateGroups";
  $response = $ev->get($endpoint);
  $jsonObj = json_decode($response);
  foreach ($jsonObj as $group){
    print ("Queue group name: ".$group->groupName."\r\n");
    print ("Queue group id: ".$group->gateGroupId."\r\n");
  }
}catch (Exception $e) {
  print $e->getMessage();
}
```

### Response
```json
[
  {
    "groupSkills": null,
    "groupName": "Platform",
    "gateGroupId": 52653,
    "permissions": []
  },
  {
    "groupSkills": null,
    "groupName": "Evaluations",
    "gateGroupId": 52658,
    "permissions": []
  },
  {
    "groupSkills": null,
    "groupName": "John's Queue",
    "gateGroupId": 52671,
    "permissions": []
  }
]
```

## Retrieve a Single Queue Group

Retrieve details for a single Queue Group using the `gateGroups` endpoint.

### Request
Be sure to set the proper [BASE_URL](../../../basics/uris/#resources-and-parameters) and [authorization header](../../../authentication/auth-ringcentral) for your deployment.

```html tab="HTTP"
GET {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}
```

```javascript tab="Node JS"
/****** Install Node JS SDK wrapper *******
$ npm install ringcentral-engage-voice-client
*******************************************/

const RunRequest = async function () {
    const EngageVoice = require('ringcentral-engage-voice-client').default

    // Instantiate the SDK wrapper object with your RingCentral app credentials
    const ev = new EngageVoice({
        clientId: "RINGCENTRAL_CLIENTID",
        clientSecret: "RINGCENTRAL_CLIENTSECRET"
    })

    try {
        // Authorize with your RingCentral Office user credentials
        await ev.authorize({
            username: "RINGCENTRAL_USERNAME",
            extension: "RINGCENTRAL_EXTENSION",
            password: "RINGCENTRAL_PASSWORD"
        })

        // Get Queue Groups data
        const groupsEndpoint = "/api/v1/admin/accounts/{accountId}/gateGroups"
        const groupsResponse = await ev.get(groupsEndpoint)
        for (var group of groupsResponse.data) {
            // Get every single Queue under your Queue Group
            if (group.groupName == "My New Queue Group") {
                const queuesEndpoint = groupsEndpoint + "/" + group.gateGroupId + "/gates"
                const queuesResponse = await ev.get(queuesEndpoint)
                for (var queue of queuesResponse.data) {
                    const singleQueueEndpoint = queuesEndpoint + "/" + queue.gateId
                    const singleQueueResponse = await ev.get(singleQueueEndpoint)
                    console.log(singleQueueResponse.data);
                    console.log("=========")
                }
            }
        }
    }
    catch (err) {
        console.log(err.message)
    }
}

RunRequest();  
```

```python tab="Python"
from engagevoice.sdk_wrapper import *

# Instantiate the SDK wrapper object with your RingCentral app credentials
ev = RestClient("RC_APP_CLIENT_ID", "RC_APP_CLIENT_SECRET")

# Login your account with your RingCentral Office user credentials
try:
    ev.login("RC_USERNAME", "RC_PASSWORD", "RC_EXTENSION_NUMBER")
    endpoint = 'admin/accounts/~/gateGroups'
    resp = ev.get(endpoint)
    for group in resp:
        endpoint = 'admin/accounts/~/gateGroups/%i' % (group['gateGroupId'])
        response = ev.get(endpoint)
        print (response)
        print ("========")
except Exception as e:
    print (e)
```

```php tab="PHP"
<?php
require('vendor/autoload.php');

// Instantiate the SDK wrapper object with your RingCentral app credentials
$ev = new EngageVoiceSDKWrapper\RestClient("RC_APP_CLIENT_ID", "RC_APP_CLIENT_SECRET");
try{
    // Login your account with your RingCentral Office user credentials
    $ev->login("RC_USERNAME", "RC_PASSWORD", "RC_EXTENSION_NUMBER");
    $endpoint = "admin/accounts/~/gateGroups";
    $response = $ev->get($endpoint);
    $jsonObj = json_decode($response);
    foreach ($jsonObj as $group){
        $endpoint = 'admin/accounts/~/gateGroups/' . $group->gateGroupId;
        $response = $ev->get($endpoint);
        print ($response."\r\n");
        print ("========\r\n");
    }
}catch (Exception $e) {
    print $e->getMessage();
}
```

### Response
```json
{
  "startDate":"2020-04-18T01:49:32.000+0000",
  "billingKey":null,
  "createdOn":"2020-04-18T01:49:32.000+0000",
  "groupName":"Platform",
  "groupSkills":null,
  "endDate":null,
  "gateGroupId":52653,
  "permissions": []
}
```
## Update a Single Queue Group

Update the details for a single Queue Group using the `gateGroups` endpoint. Several details need to be updated with a single `PUT` command so make sure to `GET` all details, modify the relevant fields, and then submit the entire object to update the Queue Group

### Request
Be sure to set the proper [BASE_URL](../../../basics/uris/#resources-and-parameters) and [authorization header](../../../authentication/auth-ringcentral) for your deployment.

```html hl_lines="11" tab="HTTP"
# Retrieve the entire Queue Group JSON object
GET {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}

# Modify the groupName
PUT {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}
Content-Type: application/json
    {
      "groupName":"My New Queue Group Name - Updated",
    }
```

```javascript tab="Node JS"
/****** Install Node JS SDK wrapper *******
$ npm install ringcentral-engage-voice-client
*******************************************/

const RunRequest = async function () {
    const EngageVoice = require('ringcentral-engage-voice-client').default

    const ev = new EngageVoice({
        clientId: "RINGCENTRAL_CLIENTID",
        clientSecret: "RINGCENTRAL_CLIENTSECRET"
    })

    try {
        // Authorize with your RingCentral Office user credentials
        await ev.authorize({
            username: "RINGCENTRAL_USERNAME",
            extension: "RINGCENTRAL_EXTENSION",
            password: "RINGCENTRAL_PASSWORD"
        })

        // Get Queue Groups info
        const groupEndpoint = "/api/v1/admin/accounts/{accountId}/gateGroups"
        const groupResponse = await ev.get(groupEndpoint)
        for (var group of groupResponse.data) {
            // Update your Queue under your Queue Group
            if (group.groupName == "My New Queue Group") {
                const queueEndpoint = groupEndpoint + "/" + group.gateGroupId + "/gates"
                const queueResponse = await ev.get(queueEndpoint)
                for (var queue of queueResponse.data) {
                    if (queue.gateName == "My Node Queue") {
                        const singleQueueEndpoint = queueEndpoint + "/" + queue.gateId
                        queue.gateDesc = "An *edited* queue description for this Queue"
                        const singleQueueResponse = await ev.put(singleQueueEndpoint, queue)
                        console.log(singleQueueResponse.data);
                        break
                    }
                }
            }
        }
    }
    catch (err) {
        console.log(err.message)
    }
}

RunRequest();     
```

```python tab="Python"
from engagevoice.sdk_wrapper import *

# Instantiate the SDK wrapper object with your RingCentral app credentials
ev = RestClient("RC_APP_CLIENT_ID", "RC_APP_CLIENT_SECRET")

# Login your account with your RingCentral Office user credentials
try:
    ev.login("RC_USERNAME", "RC_PASSWORD", "RC_EXTENSION_NUMBER")
    endpoint = 'admin/accounts/~/gateGroups'
    resp = ev.get(endpoint)
    for group in resp:
        if (group['groupName'] == "My New Queue Group"):
            endpoint = 'admin/accounts/~/gateGroups/%i' % (group['gateGroupId'])
            params = {
              "groupName": group['groupName'] + " - Updated"
            }
            response = ev.put(endpoint, params)
            print (response)
            print ("========")
except Exception as e:
    print (e)
```

```php tab="PHP"
<?php
require('vendor/autoload.php');

// Instantiate the SDK wrapper object with your RingCentral app credentials
$ev = new EngageVoiceSDKWrapper\RestClient("RC_APP_CLIENT_ID", "RC_APP_CLIENT_SECRET");
try{
    // Login your account with your RingCentral Office user credentials
    $ev->login("RC_USERNAME", "RC_PASSWORD", "RC_EXTENSION_NUMBER");
    $endpoint = "admin/accounts/~/gateGroups";
    $response = $ev->get($endpoint);
    $jsonObj = json_decode($response);
    foreach ($jsonObj as $group){
        if ($group->groupName == "My New Queue Group"){
            $endpoint = 'admin/accounts/~/gateGroups/' . $group->gateGroupId;
            $params = array ( "groupName" => $group->groupName . " - Updated" );
            $response = $ev.put($endpoint, $params);
            print ($response);
        }
    }
}catch (Exception $e) {
    print $e->getMessage();
}
```

### Response
```json
{
  "startDate":"2020-04-18T01:49:32.000+0000",
  "billingKey":null,
  "createdOn":"2020-04-18T01:49:32.000+0000",
  "groupName":"My New Queue Group - Update",
  "groupSkills":null,
  "endDate":null,
  "gateGroupId":52653,
  "permissions": []
}
```
## Delete a Single Queue Group

Delete a single Queue Group using the `gateGroups` endpoint.

### Request
Be sure to set the proper [BASE_URL](../../../basics/uris/#resources-and-parameters) and [authorization header](../../../authentication/auth-ringcentral) for your deployment.

```html tab="HTTP"
DELETE {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}
```
