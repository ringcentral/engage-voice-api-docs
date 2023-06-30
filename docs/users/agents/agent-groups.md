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
Be sure to set the proper [BASE_URL](../../../basics/uris/#resources-and-parameters) and [authorization header](../../../authentication/auth-ringcentral) for your deployment.

=== "HTTP"

    ```html
    POST {BASE_URL}/api/v1/admin/accounts/{accountId}/agentGroups
    Content-Type: application/json
    
    {
        "groupName": "My Agent Group"
    }
    ```

## Read Agent Groups

To retrieve a list of Agent Groups, use the `agentGroups` API endpoint.

### Request
Be sure to set the proper [BASE_URL](../../../basics/uris/#resources-and-parameters) and [authorization header](../../../authentication/auth-ringcentral) for your deployment.

=== "Node JS"

    ```javascript
    {!> code-samples/agent-groups/quick-start.js !}
    ```

=== "Python"

    ```python
    {!> code-samples/agent-groups/quick-start.py !}
    ```

### Sample response

```json
{!> code-samples/agent-groups/response.json !}
```

## Read Agent Group

To retrieve a single Agent Group, use the `agentGroups` API endpoint with a specific agent group ID.

### Request
Be sure to set the proper [BASE_URL](../../../basics/uris/#resources-and-parameters) and [authorization header](../../../authentication/auth-ringcentral) for your deployment.

=== "HTTP"
    ```html
    GET {BASE_URL}/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}
    ```

### Response

`account` data is omitted in the example below.

```json
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

### Request
Be sure to set the proper [BASE_URL](../../../basics/uris/#resources-and-parameters) and [authorization header](../../../authentication/auth-ringcentral) for your deployment.

=== "HTTP"
    ```html
    # Retrieve Agent Group JSON object
    GET {BASE_URL}/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}

    # Modify `groupName` and `PUT` JSON object
    PUT {BASE_URL}/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}
    Content-Type: application/json

    {
        "agentGroupId":111,
        "groupName":"My Agent Group"
        ...
    }
    ```
=== "Node JS"
    ```javascript
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

            // Get Agent Groups data
            const agentGroupsEndpoint = "/api/v1/admin/accounts/{accountId}/agentGroups"
            const agentGroupsResponse = await ev.get(agentGroupsEndpoint)
            for (var group of agentGroupsResponse.data) {
                // Update your Agent Group
                if (group.groupName == "My New Agent Group") {
                    const singleAgentGroupEndpoint = agentGroupsEndpoint + "/" + group.agentGroupId
                    group.groupName += " - updated"
                    const singleAgentGroupResponse = await ev.put(singleAgentGroupEndpoint, group)
                    console.log(singleAgentGroupResponse.data);
                    break
                }
            }
        }
        catch (err) {
            console.log(err.message)
        }
    }

    RunRequest();
    ```
=== "Python"
    ```python
    #### Install Python SDK wrapper ####
    # $ pip3 install ringcentral_engage_voice
    #  or
    # $ pip install ringcentral_engage_voice
    #####################################

    from ringcentral_engage_voice import RingCentralEngageVoice

    def update_agent_group():
        try:
            agentGroupsEndpoint = "/api/v1/admin/accounts/{accountId}/agentGroups"
            agentGroupsResponse = ev.get(agentGroupsEndpoint).json()
            for group in agentGroupsResponse:
                # Update your Agent Group
                if group['groupName'] == "My New Agent Group":
                    singleAgentGroupEndpoint = f"{agentGroupsEndpoint}/{group['agentGroupId']}"    # f      string:https://www.python.org/dev/peps/pep-0498/
                    group['groupName'] += " - Updated"
                    singleAgentGroupResponse = ev.put(singleAgentGroupEndpoint, group).json()
                    print(singleAgentGroupResponse)
                    break
        except Exception as e:
            print(e)


    # Instantiate the SDK wrapper object with your RingCentral app credentials
    ev = RingCentralEngageVoice(
        "RINGCENTRAL_CLIENTID",
        "RINGCENTRAL_CLIENTSECRET")

    try:
        # Authorize with your RingCentral Office user credentials
        ev.authorize(
            username="RINGCENTRAL_USERNAME",
            password="RINGCENTRAL_PASSWORD",
            extension="RINGCENTRAL_EXTENSION"
        )

        update_agent_group()
    except Exception as e:
        print(e)
    ```

## Delete Agent Group

### Request
Be sure to set the proper [BASE_URL](../../../basics/uris/#resources-and-parameters) and [authorization header](../../../authentication/auth-ringcentral) for your deployment.
=== "HTTP"
    ```html
    DELETE {BASE_URL}/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}
    ```
