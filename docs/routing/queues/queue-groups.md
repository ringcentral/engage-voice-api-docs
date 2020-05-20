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

=== "HTTP"
    ```html
    POST {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups
    Content-Type: application/json

    {
        "groupName": "My Queue Group"
    }
    ```
=== "Python"
    ```python
    from engagevoice.sdk_wrapper import *

    # Use your Developer Client App credentials
    RC_APP_CLIENT_ID = ""
    RC_APP_CLIENT_SECRET = ""

    # Enter your credentials here.  Usually consists of Main Number and Extension number. Main number includes international codes including '+'
    RC_USERNAME = ""
    RC_PASSWORD = ""
    RC_EXTENSION_NUMBER = ""

    # Login with RingCentral Office user credentials.
    ev = RestClient(RC_APP_CLIENT_ID, RC_APP_CLIENT_SECRET)

    # When you login, the account information is returned in the response
    try:
        resp = ev.login(RC_USERNAME, RC_PASSWORD, RC_EXTENSION_NUMBER)
        print (resp)

    except Exception as e:
        print (e)

    # Now that we are logged in, get the first account we belong to
    acctId = resp["agentDetails"][0]["accountId"]
    print ("My Account ID: " + acctId)

    # Create a payload to POST a new Queue Group
    data = {
        "gropuName":"My Queue Group"
        }

    endpoint = 'admin/accounts/'+acctId+'/gateGroups'
    try:
        response = ev.post(endpoint, data)
        print ("Creating new Queue Group")
        print (json.dumps(response))
    except Exception as e:
        print (e)
    ```

### Response
    ```json tab="Response"
    {
      "startDate":"2020-04-18T01:49:32.000+0000",
      "billingKey":null,
      "createdOn":"2020-04-18T01:49:32.000+0000",
      "groupName":"My Queue Group",
      "groupSkills":null,
      "endDate":null,
      "gateGroupId":52653,
      "permissions": []
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

=== "HTTP"
    ```html
    GET {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups
    ```
=== "Python"
    ```python
    from engagevoice.sdk_wrapper import *

    # Use your Developer Client App credentials
    RC_APP_CLIENT_ID = ""
    RC_APP_CLIENT_SECRET = ""

    # Enter your credentials here.  Usually consists of Main Number and Extension number. Main number includes international codes including '+'
    RC_USERNAME = ""
    RC_PASSWORD = ""
    RC_EXTENSION_NUMBER = ""

    # Login with RingCentral Office user credentials.
    ev = RestClient(RC_APP_CLIENT_ID, RC_APP_CLIENT_SECRET)

    # When you login, the account information is returned in the response
    try:
        resp = ev.login(RC_USERNAME, RC_PASSWORD, RC_EXTENSION_NUMBER)
        print (resp)

    except Exception as e:
        print (e)

    # Now that we are logged in, get the first account we belong to and get a list of Queue Groups
    acctId = resp["agentDetails"][0]["accountId"]
    print ("My Account ID: " + acctId)
    endpoint = 'admin/accounts/'+acctId+'/gateGroups'

    try:
        response = ev.get(endpoint)
        print (response)
    except Exception as e:
        print (e)

    # Now that we are logged in, and we know our account number, get a list of Queue Groups
    endpoint = 'admin/accounts/'+acctId+'/gateGroups'

    try:
        response = ev.get(endpoint)
        print (response)
        gateGrpId = str(response[0]["gateGroupId"])
        print ("My Queue Group ID: " + gateGrpId)
    except Exception as e:
        print (e)
    ```

### Response
```json tab="Response"
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

Retrieving details for a single Queue Group using the `gateGroups` endpoint.

### Request

=== "HTTP"
    ```html
    GET {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}
    ```
=== "Python"
    ```python
    from engagevoice.sdk_wrapper import *

    # Use your Developer Client App credentials
    RC_APP_CLIENT_ID = ""
    RC_APP_CLIENT_SECRET = ""

    # Enter your credentials here.  Usually consists of Main Number and Extension number. Main number includes international codes including '+'
    RC_USERNAME = ""
    RC_PASSWORD = ""
    RC_EXTENSION_NUMBER = ""

    # Login with RingCentral Office user credentials.
    ev = RestClient(RC_APP_CLIENT_ID, RC_APP_CLIENT_SECRET)

    # When you login, the account information is returned in the response
    try:
        resp = ev.login(RC_USERNAME, RC_PASSWORD, RC_EXTENSION_NUMBER)
        print (resp)
    except Exception as e:
        print (e)

    # Now that we are logged in, get the first account we belong to and get a list of Queue Groups
    acctId = resp["agentDetails"][0]["accountId"]
    print ("My Account ID: " + acctId)
    endpoint = 'admin/accounts/'+acctId+'/gateGroups'

    try:
        response = ev.get(endpoint)
        print (response)
    except Exception as e:
        print (e)

    # And grab a single Queue Group. We are looking for the first queue we can find.
    gateGrpId = str(response[0]["gateGroupId"])
    print ("My Queue Group ID: " + gateGrpId)
    endpoint = 'admin/accounts/'+acctId+'/gateGroups/'+gateGrpId

    try:
        response = ev.get(endpoint)
        print (response)
    except Exception as e:
        print (e)
    ```

### Response
```json tab="Response"
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
=== "HTTP"
    ```html hl_lines="11"
    # Retrieve the entire Queue Group JSON object
    GET {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}

    # Modify the groupName and send the entire JSON response backward
    PUT {BASE_URL}/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}
    Content-Type: application/json
    {
      "startDate":"2020-04-18T01:49:32.000+0000",
      "billingKey":null,
      "createdOn":"2020-04-18T01:49:32.000+0000",
      "groupName":"Platform-New",
      "groupSkills":null,
      "endDate":null,
      "gateGroupId":52653,
      "permissions": []
    }
    ```
=== "Python"
    ```python
    from engagevoice.sdk_wrapper import *

    # Use your Developer Client App credentials
    RC_APP_CLIENT_ID = ""
    RC_APP_CLIENT_SECRET = ""

    # Enter your credentials here.  Usually consists of Main Number and Extension number. Main number includes international codes including '+'
    RC_USERNAME = ""
    RC_PASSWORD = ""
    RC_EXTENSION_NUMBER = ""

    # Login with RingCentral Office user credentials.
    ev = RestClient(RC_APP_CLIENT_ID, RC_APP_CLIENT_SECRET)

    # When you login, the account information is returned in the response
    try:
        resp = ev.login(RC_USERNAME, RC_PASSWORD, RC_EXTENSION_NUMBER)
        print (resp)

    except Exception as e:
        print (e)

    # Now that we are logged in, get the first account we belong to and get a list of Queue Groups
    acctId = resp["agentDetails"][0]["accountId"]
    print ("My Account ID: " + acctId)
    endpoint = 'admin/accounts/'+acctId+'/gateGroups'

    try:
        response = ev.get(endpoint)
        print (response)
    except Exception as e:
        print (e)

    # And grab a single Queue Group. We are looking for the first queue we can find.
    gateGrpId = str(response[0]["gateGroupId"])
    print ("My Queue Group ID: " + gateGrpId)
    endpoint = 'admin/accounts/'+acctId+'/gateGroups/'+gateGrpId

    try:
        response = ev.get(endpoint)
        print (response)
    except Exception as e:
        print (e)
    ```
### Response
```json tab="Response"
{
  "startDate":"2020-04-18T01:49:32.000+0000",
  "billingKey":null,
  "createdOn":"2020-04-18T01:49:32.000+0000",
  "groupName":"Platform-New",
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
