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
    "groupName": "My New Queue Group"
}
```

```javascript tab="Node JS"
const EngageVoice = require('engagevoice-sdk-wrapper')

// Instantiate the SDK wrapper object with your RingCentral app credentials
var ev = new EngageVoice.RestClient("RC_CLIENT_ID", "RC_CLIENT_SECRET")

// Login your account with your RingCentral Office user credentials
ev.login("RC_USERNAME", "RC_PASSWORD", "RC_EXTENSION_NUMBER", function(err, response){
  if (err)
    console.log(err)
  else{
    endpoint = 'admin/accounts/~/gateGroups'
    params = {
                "groupName":"My New Queue Group"
                  }
    ev.post(endpoint, params, function(err, response){
      if (err){
        console.log(err)
      }else {
        var jsonObj = JSON.parse(response)
        console.log(jsonObj)
      }
    })
  }
})        
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

```html tab="HTTP"
GET {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups
```

```javascript tab="Node JS"
const EngageVoice = require('engagevoice-sdk-wrapper')

// Instantiate the SDK wrapper object with your RingCentral app credentials
var ev = new EngageVoice.RestClient("RC_CLIENT_ID", "RC_CLIENT_SECRET")

// Login your account with your RingCentral Office user credentials
ev.login("RC_USERNAME", "RC_PASSWORD", "RC_EXTENSION_NUMBER", function(err, response){
  if (err)
    console.log(err)
  else{
    var endpoint = 'admin/accounts/~/gateGroups'
    ev.get(endpoint, null, function(err, response){
      if (err){
        console.log(err)
      }else {
        var jsonObj = JSON.parse(response)
        for (var group of jsonObj){
          console.log("Queue group name: " + group.groupName)
          console.log("Queue group id: " + group.gateGroupId)
        }
      }
    })
  }
})        
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

```html tab="HTTP"
GET {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}
```

```javascript tab="Node JS"
const EngageVoice = require('engagevoice-sdk-wrapper')

// Instantiate the SDK wrapper object with your RingCentral app credentials
var ev = new EngageVoice.RestClient("RC_CLIENT_ID", "RC_CLIENT_SECRET")

// Login your account with your RingCentral Office user credentials
ev.login("RC_USERNAME", "RC_PASSWORD", "RC_EXTENSION_NUMBER", function(err, response){
  if (err)
    console.log(err)
  else{
    var endpoint = 'admin/accounts/~/gateGroups'
    ev.get(endpoint, null, function(err, response){
      if (err){
        console.log(err)
      }else {
        var jsonObj = JSON.parse(response)
        for (var group of jsonObj){
          endpoint = 'admin/accounts/~/gateGroups/' + group.gateGroupId
          ev.get(endpoint, null, function(err, response){
            if (err){
              console.log(err)
            }else {
              print (response)
              print ("========")
            }
          })
        }
      }
    })
  }
})        
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
const EngageVoice = require('engagevoice-sdk-wrapper')

// Instantiate the SDK wrapper object with your RingCentral app credentials
var ev = new EngageVoice.RestClient("RC_CLIENT_ID", "RC_CLIENT_SECRET")

// Login your account with your RingCentral Office user credentials
ev.login("RC_USERNAME", "RC_PASSWORD", "RC_EXTENSION_NUMBER", function(err, response){
  if (!err){
    var endpoint = 'admin/accounts/~/gateGroups'
    ev.get(endpoint, null, function(err, response){
      if (!err){
        var jsonObj = JSON.parse(response)
        for (var group of jsonObj){
          if (group.groupName == "My New Queue Group"){
            endpoint = 'admin/accounts/~/gateGroups/' + group.gateGroupId
            var params = {
              "groupName": group.groupName + " - Update"
            }
            ev.put(endpoint, params, function(err, response){
              if (!err){
                console.log (response)
              }
            })
          }
        }
      }
    })
  }
})        
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
```html tab="HTTP"
DELETE {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}
```
