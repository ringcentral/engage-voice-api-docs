# About Searching for Leads

You can search for leads using Primary Search Fields and Extended Search Fields. The Primary Search Fields can be used for performing basic searches on leads such as the campaign or list they are found in, while the Extended Search Fields provide search parameters that you can use to get more granular with your lead search.

## Primary Search Fields
The primary search fields include a selection of basic search parameters. You can search for leads by campaign, or you can search only for leads whose status is SUPPRESSED. You can look for leads that have been orphaned, or you can search for leads by loaded lists, according to disposition, or whether they were inserted by an agent or supplied by the system.

| API Property | UI Display | UI Default | Description |
|-|-|-|-|
| **`campaignId`** | Campaign | *first available campaign* | Search from a list of available dial groups and campaigns. Use [Dial Groups and Campaigns](./#dial-groups-and-campaigns) to retrieve valid values. |
| **`suppressed`** | Suppressed | *first available campaign* | Suppressed leads are leads the system will not dial. They will still maintain their lead status, however, unlike paused or cancelled leads (whose lead status will change once they have been paused or cancelled). Allowed values include `ONLY_SUPPRESSED`, `ONLY_UNSUPPRESSED`, `ALL` |
| **`listIds`** | Loaded Lists | *Select lists...* | Search from any loaded leads list by their ID. Please note that this parameter depends upon a campaign in the campaignId setting. Use [Leads List](./#leads-list) to retrieve valid values. |
| **`agentDispositions`** | Agent Dispositions | *Select agent dispositions...* | Search for leads from a list of agent dispositions by campaign. This parameters depends upon a campaign in the campaignId Use [Campaign Dispositions](./#campaign-dispositions) to retrieve a valid list of values. |
| **`systemDispositions`** | System Dispositions | *Select system dispositions...* | Search from a list of system dispositions by account. Use [System Dispositions](./#system-dispositions) for a list of valid values. |
| **`leadStates`** | Lead Status | *Select lead status...* | Search from a list of lead status by account. Use [Lead Status](./#lead-status) for a list of valid values. |
| **`physicalStates`** | State | *Select states...* | Search for leads by their (geographical) state. You can select one or more states via the dropdown list. The list includes all of the United States and all provinces and territories of Canada. Use [States](./#states) for a list of valid values |
| **`leadTimezones`** | Timezone | *Select timezones...* | Search for leads by timezone. You need only include the name of the timezone, but the list must be written as an array of objects. Use [Lead Timezones](./#lead-timezones) for a list of valid values |

## Supporting Values and APIs

The following value lists and APIs are used to retrieve predefined values for certain fields. Use these values to populate the correct parameter values of fields.

The `BASE_DIAL_GROUP_URL` is `{BASE_URL}/api/v1/admin/accounts/{accountId}/dialGroups`

### Dial Groups and Campaigns

Gets a list of dial groups with associated campaigns created under this account. Campaigns are contained within Dial Groups and this call will retrieve both.

  `GET {BASE_DIAL_GROUP_URL}/withChildren`

### Leads List

Gets a list of leads that are part of this campaign. Multiple lead lists can be linked to a campaign and this command returns list IDs for each lead list.

  `GET {BASE_DIAL_GROUP_URL}/{dialGroupId}/campaigns/{campaignId}/lists`

### Campaign Dispositions

Gets a list of the agent dispositions for this campaign

  `GET {BASE_DIAL_GROUP_URL}/{dialGroupId}/campaigns/{campaignId}/campaignDispositions`

### System Dispositions

The parameter `systemDispositions` can take on the following values:

| Value | Description |
|-|-|
| **`ANSWER`** | Search all calls that were answered by a lead and connected to a live agent |
| **`NOANSWER`** | Search all calls that rang without being answered by a lead |
| **`BUSY`** | Search all calls that the system dispositioned as a busy response |
| **`MACHINE`** | Search all calls that resulted in a machine answer |
| **`INTERCEPT`** | Search all calls for which the phone number was unreachable |
| **`DISCONNECT`** | Search all calls that were disconnected |
| **`ABANDON`** | Search all calls that ended because the system could not find an available agent after dialing the lead |
| **`CONGESTION`** | Search all calls that ended due to excessive network traffic or insufficient bandwidth |
| **`MANUAL_PASS`** | Search all calls that calls that had a manual pass applied to them |
| **`INBOUND_CALLBACK`** | Search all calls designated as (inbound) callbacks |
| **`APP_DNC`** | Search all calls that have been skipped due to a DNC list verification |
| **`APP_REQUEUE`** | Search all call legs that have been requeued via IVR (this setting only applies to certain accounts. Please contact your CSM for more information) |
| **`APP_REQUEUE_COMPLETE`** | Search all call legs that have been requeued via IVR in which the call has been received in the new queue. |
| **`APP_REQUEUE_ABANDON`** | Search all call legs that have been requeued via IVR in which the call was abandoned before a connection was made |
| **`INBOUND_ABANDON`** | Search all calls where the caller abandoned the call while waiting in queue |

### Lead Status

The parameter `leadState` can take on the following values:

    | Value | Description |
    |-|-|
    | **`ACTIVE`** | Search for all leads currently engaged on an active call |
    | **`AGENT_CALLBACK`** | Search for all leads that have been flagged for an agent-specific callback |
    | **`CALLBACK_CANCELLED`** | Search for all leads that have had a callback flag removed |
    | **`CALLBACK`** | Search for all leads that have been flagged for a callback |
    | **`CANCELLED`** | Search for all leads that have been cancelled from dialing |
    | **`COMPLETE`** | Search for all leads that have been cancelled (and will not be requeued for dialing) |
    | **`DISCONNECTED`** | Search for all leads that have been assigned a DISCONNECTED lead state |
    | **`DO_NOT_CALL`** | Search for all leads whose phone number is on the DNC list |
    | **`INTERCEPT`** | Search for all leads with a disconnected or otherwise unreachable number |
    | **`MAX_DIAL_LIMIT`** | Search for all leads that have been dialed the maximum number of times |
    | **`PAUSED`** | Search for all leads that have been paused from dialing |
    | **`PENDING_CALLBACK`** | Search for all leads that are awaiting a scheduled callback time set by an agent-specific callback disposition |
    | **`PENDING_ERR`** | Search for all leads that have been set to PENDING and remain in that state |
    | **`PENDING_HCI`** | Search for all leads that have not yet been dialed by an HCI agent |
    | **`PENDING`** | Search for all leads that have been fetched by the preview dialer or are actively being dialed by the predictive dialer |
    | **`READY`** | Search for all leads that are ready for dialing (including leads that have reached the maximum number of passes) |
    | **`TRANSITIONED`** | Search for all leads that have been copied in transition mode and sent to another campaign. Please note that when a lead is copied in Transition mode, the original lead retains the original Lead ID, while the copied version gets a new Lead ID |
    | **`WHITELIST`** | Search for all leads that have been whitelisted via the Whitelist Manager |

### Lead Timezones

The parameter `leadTimezones` can take on the following values:

    | Value | Description |
    |-|-|
    | **`ADT`** | ADT - Atlantic Daylight Time |
    | **`AKDT`** | AKDT - Alaska Daylight Time |
    | **`AKST`** | AKST - Alaska Standard Time |
    | **`AST`** | AST - Atlantic Standard Time |
    | **`CDT`** | CDT - Central Daylight Time |
    | **`CST`** | CST - Central Standard Time |
    | **`EDT`** | EDT - Eastern Daylight Time |
    | **`EST`** | EST - Eastern Standard Time |
    | **`HADT`** | HADT - Hawaii-Aleutian Daylight Time |
    | **`HAST`** | HAST - Hawaii-Aleutian Standard Time |
    | **`MDT`** | MDT - Mountain Daylight Time |
    | **`MST`** | MST - Mountain Standard Time |
    | **`NDT`** | NDT - Newfoundland Daylight Time |
    | **`NST`** | NST - Newfoundland Standard Time |
    | **`PDT`** | PDT - Pacific Daylight Time |
    | **`PMDT`** | PMDT - Pierre/Miquelon Daylight Time |
    | **`PMST`** | PMST - Pierre/Miquelon Standard Time |
    | **`PST`** | PST - Pacfic Standard Time |
    | **`WSDT`** | WSDT - Samoa Daylight Time |
    | **`WSST`** | WSST - Somoa Standard Time |

### States

Get a list of states from the United States and all provinces and territories of Canada.

`GET {BASE_URL}/api/v1/admin/states`

## Request
Be sure to set the proper [BASE_URL](../../../basics/uris/#resources-and-parameters) and [authorization header](../../../authentication/auth-ringcentral) for your deployment.

```http tab="HTTP"

    POST {BASE_URL}/api/v1/admin/accounts/{accountId}/campaignLeads/leadSearch
    Authorization: bearer <myAccessToken>
    Content-Type: application/json;charset=UTF-8
    Accept: application/json


    {
      "firstName":"Jon",
      "campaignId":136785,
      "listIds":[],
      "agentDispositions":[],
      "systemDispositions":[],
      "leadStates":[],
      "physicalStates":[],
      "leadTimezones":
      	[
      		{"name":"CST"},
      		{"name":"PST"}
      	],
      "suppressed":"ALL",
      "campaignIds":[136785]
    }
```

```bash tab="cURLs"

    curl -XPOST 'https://engage.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/leadSearch' \
       -H 'Authorization: Bearer {myAccessToken}' \
       -d '{"firstName":"John"}' \
       -H 'Content-Type: application/json'
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

        // Search Leads with first name John
        const endpoint = "/api/v1/admin/accounts/{accountId}/campaignLeads/leadSearch"
        const postBody = {
            "firstName": "John"
        }
        const response = await ev.post(endpoint, postBody)
        console.log(response.data);
    }
    catch (err) {
        console.log(err.message)
    }
}

RunRequest();
```

```python tab="Python"
/****** Install Python SDK wrapper **
$ pip install engagevoice-sdk-wrapper
*************************************/

from engagevoice.sdk_wrapper import *

# Instantiate the SDK wrapper object with your RingCentral app credentials
ev = RestClient("RC_APP_CLIENT_ID", "RC_APP_CLIENT_SECRET")

# Login your account with your RingCentral Office user credentials
try:
    ev.login("RC_USERNAME", "RC_PASSWORD", "RC_EXTENSION_NUMBER")
    endpoint = 'admin/accounts/~/campaignLeads/leadSearch'
    params = { "firstName" : "John" }
    response = ev.post(endpoint, params)
    print (response)        
except Exception as e:
    print (e)
```

```php tab="PHP"
/****** Install PHP SDK wrapper **
$ composer require engagevoice-sdk-wrapper:dev-master
*************************************/

<?php
require('vendor/autoload.php');

// Instantiate the SDK wrapper object with your RingCentral app credentials
$ev = new EngageVoiceSDKWrapper\RestClient("RC_APP_CLIENT_ID", "RC_APP_CLIENT_SECRET");
try{
  // Login your account with your RingCentral Office user credentials
  $ev->login("RC_USERNAME", "RC_PASSWORD", "RC_EXTENSION_NUMBER");
  $endpoint = "admin/accounts/~/campaignLeads/leadSearch";
  $params = array ( "firstName" => "John" );
  $response = $ev->post($endpoint, $params);
  print ($response."\r\n");
}catch (Exception $e) {
  print $e->getMessage();
}
```
## References

* [Web console documentation: Using the Leads search](https://docs.ringcentral.com/engage/article/voice-admin-use-lead-search)
