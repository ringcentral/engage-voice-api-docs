# About Campaigns

Campaigns are a way to organize and manage the different types of outbound calls leaving your contact center. You can configure campaigns by creating custom agent dispositions, uploading lead lists, setting schedules for dialing, activating compliance-supporting tools, and more.

## Core Concepts
Campaigns are created for a specific period of time so a start and end date must be entered.

!!! alert "Please Note"
    Your Start Date and End Date fields affect whether or not the leads in this campaign will be dialed. If agents are dialing outside of the date range specified here, then none of the leads in this campaign will be automatically dialed (in Predictive mode) or fetchable (in Preview mode), even if the campaign is still technically active.

Caller ID must be an accurate number for this account. This should be the number that leads can call to reach a customer service representative. The customer service representative must be able to put the caller on your internal DNC list. If the Caller ID number goes to an automatic responder, the responder must also provide the lead with a way to request placement on your DNC list, either by leaving a voicemail or via a touchtone entry.

## Prerequisite
Once you’ve created and configured your [dial group](../dial-groups), you can begin creating campaigns within that group to segment and configure your outgoing calls. Remember that all the campaigns within any given dial group will use the dialing mode you selected in your dial group configuration settings.

## Create Campaigns
To create a campaign, first select your desired [dial group](../dial-groups) and then create your campaign with the following details.

### Primary Parameters
Your campaign must have name, start and end date, and valid caller ID. All other parameters are optional.

| API Property |  | UI Display | UI Default | Description |
|-|-|-|-|-|
| **`isActive`** | Optional | Active | *unchecked* | Make the campaign active. `1` means active, `0` means inactive, and `2` means agent callbacks only. |
| **`campaignName`** | Required | Name | *empty* | Give this campaign a name. |
| **`campaignDesc`** | Optional | Description | *empty* | Set a short description for the new campaign. |
| **`campaignPriority`** | Optional | Campaign Priority | Priority 1 - Average | Set a short description for the new campaign. Use [Campaign Priority](./#campaign-priority) to retrieve valid values |
| **`startDate`** | Required | Start Date | *empty* | Set a start date for this campaign in ISO-8601 format such as: `2020-04-22T00:00:00.000-0000`. |
| **`endDate`** | Required | End Date | *empty* | Set an end date for this campaign in ISO-8601 format such as: `2020-04-22T00:00:00.000-0000`. |
| **Dialer Settings** | | | | |
| **`maxRingTime`** | Optional | Max Ring Time | 30 | This is the maximum amount of time (in seconds) that the system will wait for a call to ring before it moves on to the next lead. The maximum allowable ring time is 60 seconds. |
| **`maxRingTimeTransfer`** | Optional | Max Ring Time Transfers | 60 | This is the maximum amount of time (in seconds) that the system will wait for an answer when transferring a call. The maximum amount of time you can set is 120 seconds. |
| **`callerId`** | Required | Caller Id | *empty* | Enter the Caller ID you wish to display to leads contacted via this campaign. This should be the number that leads can call to reach a customer service representative. The customer service representative must be able to put the caller on your internal DNC list. If the Caller ID number goes to an automatic responder, the responder must also provide the lead with a way to request placement on your DNC list, either by leaving a voicemail or via a touchtone entry. |
| **`transferCallerId`** | Optional | Transfer Override Caller ID | *empty* | Enter a ten-digit phone number here (format: ##########) that the system can use to override the Caller ID number entered above if an agent transfers a lead from this campaign to another number (whether via manual transfer or disposition-based transfer). |
| **`scrubDisconnectNoanswer`** | Optional | Disconnect Scrubbing | 0 | This setting refers to a third-party integration that looks up system dispositions of ‘no-answer’ and determines whether they’re actually no-answers or if they’re simply disconnects. Please note that disconnect scrubbing is only performed if the first pass results in a no-answer. `0` means 'No, Disabled', and `1` means 'Yes, Enabled'. |
| **`dialLoadedOrder`** | Optional | Dial Leads In Order Loaded | Natural Sort | This setting allows you to choose the order in which leads will be dialed (we recommend you do NOT dial leads in the order in which they were loaded). Please note that before the system defaults to the order you select below, it will first respect features and settings like Quota Management, Timezone and Dial Zone Management, Custom Campaign Criteria, Lead List Priority, and Priority Requeue to determine which leads are available to dial. Once all relevant conditions have been satisfied, the system will then dial leads in the order of your choice. Use [Dial Lead in Order Loaded](./#dial-lead-in-order-loaded) to determine valid values |
| **`customDialZoneGroup`** | Optional | Custom Dial Zone Group | *empty* | Select a custom dial zone group from the dropdown if you wish to map custom timezone values for leads on this campaign. Please note that this is an advanced feature. |
| **`trackSpeedToLead`** | Optional | Track Speed To Lead | *unchecked* | This option allows you to track (via reporting) how much time passes between the time the system receives a new lead and when it actually dials that lead. |
| **`machineDetect`** | Optional | Voicemail Detection Enabled | *unchecked* | Check this box to direct the system not to connect to an agent if an answering machine is detected. |
| **`campaignUnlimitedFieldGroup`** | Optional | Custom Lead Data Fields Group | *empty* | Select a group of custom lead data fields from the dropdown to add to your campaign. |

### Supporting Values and APIs

The following value lists and APIs are used to retrieve predefined values for certain fields. Use these values to populate the correct parameter values of fields.

#### Campaign Priority

The parameter `campaignPriority` can take on the following values:

    | Value | Description |
    |-|-|
    | **`1`** | Priority 1 - Average - This is average priority |
    | **`2`** | Priority 2 - This priority is 1 level higher |
    | **`3`** | Priority 3 - This priority is 2 level higher |
    | **`4`** | Priority 4 - This priority is 3 level higher |
    | **`5`** | Priority 5 - High - This priority is highest priority |

#### Dial Lead in Order Loaded

The parameter `dialLoadedOrder` can take on the following values:

    | Value | Sort Name | Description |
    |-|-|-|
    | **`0`** | Natural Sort | This option will prioritize leads based on pass count (leads with zero passes will be dialed before leads that have already been called once or more). If all lead pass counts are identical, the system will default to dialing leads from the most recently loaded lists firsts. |
    | **`1`** | Natural Sort, Randomized | This option dials leads with the lowest pass count in random order. |
    | **`2`** | Yes — Ascending Order (Not Recommended!) | This option dials leads from first to last based on the order in which they were loaded. |
    | **`3`** | Yes — Descending Order (Not Recommended!) | This option dials leads from last to first based on the order in which they were loaded. Please note: We recommend against dialing leads in the order loaded because lead lists usually contain phone numbers from the same geographical area. If thousands of agents suddenly start dialing into the same geographical area, they can overwhelm the associated telecommunications central office, causing network disruptions. |
    | **`4`** | Using Lead Priority | This option dials leads according to the priority indicated via the Loaded Lists menu option. Please note that the system assigns all leads a default priority number of 999. You can add a Lead Priority column to your lead lists and use it to assign each lead a priority number. When you upload the list via Loaded Lists, be sure to use the custom list mapping setting to map that column to the system’s Lead Priority destination. Learn more about loading [lead lists](../../leads/bulk-import)|

### Request
Be sure to set the proper [BASE_URL](../../../basics/uris/#resources-and-parameters) and [authorization header](../../../authentication/auth-ringcentral) for your deployment.

```html tab="HTTP"

POST {BASE_URL}/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns
Content-Type: application/json

{
  "isActive":1,
  "campaignName":"My Predictive Campaign",
  "campaignDesc":"A test predictive campaign",
  "startDate":"2020-05-26T07:00:00.000+0000",
  "endDate":"2025-05-26T07:00:00.000+0000",
  "maxRingTime":30,
  "maxRingTimeTransfer":60,
  "callerId":"4155550123",
  "dialLoadedOrder":0
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

        // Get Dial Groups data
        const groupsEndpoint = "/api/v1/admin/accounts/{accountId}/dialGroups"
        const groupsResponse = await ev.get(groupsEndpoint)
        for (var group of groupsResponse.data) {
            // Create a Campaign under your Dial Group
            if (group.dialGroupName == "My New Dial Group") {
                const campaignEndpoint = groupsEndpoint + "/" + group.dialGroupId + "/campaigns"
                var postBody = {
                    "isActive": 1,
                    "campaignName": "My Predictive Campaign",
                    "campaignDesc": "A test predictive campaign",
                    "startDate": "2020-05-28T07:00:00.000+0000",
                    "endDate": "2025-05-30T07:00:00.000+0000",
                    "maxRingTime": 30,
                    "maxRingTimeTransfer": 60,
                    "callerId": "4155550123",
                    "dialLoadedOrder": 0
                }
                const campaignResponse = await ev.post(campaignEndpoint, postBody)
                console.log(campaignResponse.data)
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
#### Install Python SDK wrapper ####
# $ pip install engagevoice-sdk-wrapper
#####################################

from engagevoice.sdk_wrapper import *

# Instantiate the SDK wrapper object with your RingCentral app credentials
ev = RestClient("RC_APP_CLIENT_ID", "RC_APP_CLIENT_SECRET")

# Login your account with your RingCentral Office user credentials
try:
    ev.login("RC_USERNAME", "RC_PASSWORD", "RC_EXTENSION_NUMBER")
    endpoint = 'admin/accounts/~/dialGroups'
    resp = ev.get(endpoint)
    for group in resp:
      if (group['dialGroupName'] == "My Dial Group - Predictive"):
          # create a campaign under this dial group
          endpoint += '/%i/campaigns' % (group['dialGroupId'])
          params = {
            "isActive": 1,
            "campaignName": "My Predictive Campaign",
            "campaignDesc": "A test predictive campaign",
            "startDate": "2020-05-26T07:00:00.000+0000",
            "endDate": "2025-05-26T07:00:00.000+0000",
            "maxRingTime": 30,
            "maxRingTimeTransfer": 60,
            "callerId": "4155550123",
            "dialLoadedOrder": 0
          }
          resp = ev.post(endpoint, params)
          print (resp)
          break      
except Exception as e:
    print (e)
```

```php tab="PHP"
/************ Install PHP SDK wrapper **************
$ composer require engagevoice-sdk-wrapper:dev-master
*****************************************************/

<?php
require('vendor/autoload.php');

// Instantiate the SDK wrapper object with your RingCentral app credentials
$ev = new EngageVoiceSDKWrapper\RestClient("RC_APP_CLIENT_ID", "RC_APP_CLIENT_SECRET");
try{
  // Login your account with your RingCentral Office user credentials
  $ev->login("RC_USERNAME", "RC_PASSWORD", "RC_EXTENSION_NUMBER");
  $endpoint = 'admin/accounts/~/dialGroups';
  $response = $ev->get($endpoint);
  $jsonObj = json_decode($response);
  foreach ($jsonObj as $group){
      if ($group->dialGroupName == "My Dial Group - Predictive"){
          // create a campaign under this dial group
          $endpoint .= '/' . $group->dialGroupId . '/campaigns';
          $params = array (
            "isActive" => 1,
            "campaignName" => "My Predictive Campaign",
            "campaignDesc" => "A test predictive campaign",
            "startDate" => "2020-05-26T07:00:00.000+0000",
            "endDate" => "2025-05-26T07:00:00.000+0000",
            "maxRingTime" => 30,
            "maxRingTimeTransfer" => 60,
            "callerId" => "4155550123",
            "dialLoadedOrder" => 0
          );
          $response = $ev->post($endpoint, $params);
          print ($response."\r\n");
          break;
      }
  }
}catch (Exception $e) {
  print $e->getMessage();
}
```

### Response

```json
{
  "isActive":0,
  "campaignId":136785,
  "permissions":[],
  "campaignName":"My Predictive Campaign",
  "campaignDesc":"A test predictive campaign",
  "countryId":"USA",
  "billingCode":"",
  "startDate":"2020-05-26T07:00:00.000+0000",
  "endDate":"2025-05-26T07:00:00.000+0000",
  "maxRingTime":30,
  "maxRingTimeTransfer":60,
  "callerId":"4155550123",
  "transferCallerId":"",
  "scrubDisconnectNoanswer":0,
  "dialLoadedOrder":0,
  "customDialZoneGroup":null,
  "trackSpeedToLead":0,
  "machineDetect":false,
  "campaignUnlimitedFieldGroup":null,
  "sunSched":"00000000",
  "monSched":"08002100",
  "tueSched":"08002100",
  "wedSched":"08002100",
  "thuSched":"08002100",
  "friSched":"08002100",
  "satSched":"00000000",
  "dncScrubOption":"DO_NOT_SCRUB",
  "campaignPriority":1,
  "passDelayMin":60,
  "whisperMsg":"PLAY-AUDIO:beep",
  "abandonMsg":"",
  "onHoldMsg":"PLAY-AUDIO-LOOP:holdmusic",
  "endCallMsg":"PLAY-AUDIO:dialer.endofcalltone",
  "machAnswerMsg":"",
  "liveAnswerMsg":"",
  "maxPasses":3,
  "maxPassesExclude":"",
  "maxDailyPasses":-1,
  "maxDailyPassesInclude":"",
  "maxDialLimit":-1,
  "seedSuccessRate":75.000,
  "seedAbandonRate":3.000,
  "targetAbandonRate":3.000,
  "minPredictiveCallsHistory":500,
  "showLeadInfo":0,
  "appUrl":"",
  "surveyPopType":"",
  "recordCall":0,
  "stopRecordingOnTransfer":false,
  "recordingInConference":true,
  "agentPopMessage":"",
  "afterCallBaseState":"AVAILABLE",
  "hangupOnDisposition":0,
  "allowLeadUpdates":0,
  "allowLeadInserts":0,
  "requeueType":"ADVANCED",
  "showLeadPasses":true,
  "lastPassDts":null,
  "exportFlag":true,
  "enableGlobalPhoneBook":false,
  "aux1Label":"",
  "aux2Label":"",
  "aux3Label":"",
  "aux4Label":"",
  "aux5Label":"",
  "showListName":true,
  "genericKeyValuePairs":"",
  "filterEnabled":0,
  "filterType":"",
  "useGlobalWhitelist":false,
  "rescrubInterval":30,
  "pauseRecordingSec":30,
  "dispositionTimeout":60,
  "realtimeDncUrl":"",
  "afterCallState":
    {
      "id":11786,
      "description":"Available"
    },
  "postCallSoapService":null,
  "postDispSoapService":null,
  "agentConnectSoapService":null,
  "agentTermSoapService":null,
  "transferTermSoapService":null,
  "campaignResultDest":null,
  "survey":null,
  "dialGroup":
    {
      "id":115801,
      "description":"My Dial Group - Predictive"
    },
  "script":null,
  "quotaGroup":null,
  "callerIdBucket":null,
  "campaignDispositions":null,
  "campaignRequeueShortcuts":null,
  "campaignFilterStates":null,
  "campaignFilterTimezones":null,
  "campaignWhitelistTagMembers":null,
  "groupId":115801
}
```

## Clone Campaigns
To create a copy of a campaign (clone), first select your desired [dial group](../dial-groups) and then clone your campaign with the following details.

### Primary Parameters
Your campaign must have name, start and end date, and valid caller ID. All other parameters are optional.

| Parameter | Description |
|-|-|
| **Path Parameters** | |
| **`accountId`** | The unique account identifier. |
| **`dialGroupId`** | The unique [Dial Group](../dial-groups) identifier. |
| **`campaignId`** | The unique [Campaign](../campaigns#response) identifier. |
| **Query Parameters** | |
| **`newCampaignName`** | A new name for this clone of the campaign. Use `+` for spaces. |
| **`newCountryCode`** | The country for this campaign, with a default of `USA`. |

### Request
Be sure to set the proper [BASE_URL](../../../basics/uris/#resources-and-parameters) and [authorization header](../../../authentication/auth-ringcentral) for your deployment.

```html tab="HTTP"

POST {BASE_URL}/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns/{campaignId}/clone?newCampaignName={newCampaignName}&newCountryCode=USA
Content-Type: application/json
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

        // Get Dial Groups data
        const groupsEndpoint = "/api/v1/admin/accounts/{accountId}/dialGroups"
        const groupsResponse = await ev.get(groupsEndpoint)
        for (var group of groupsResponse.data) {
            // Find your Dial Group
            if (group.dialGroupName == "My New Dial Group") {
                const campaignsEndpoint = groupsEndpoint + "/" + group.dialGroupId + "/campaigns"
                const campaignsResponse = await ev.get(campaignsEndpoint)
                for (var campaign of campaignsResponse.data) {
                    // Find your Campaign and clone it into another one
                    if (campaign.campaignName == "My Predictive Campaign") {
                        const cloneCampaignEndpoint = campaignsEndpoint + "/" + campaign.campaignId + "/clone?newCampaignName=My New Predictive Campaign&newCountryCode=USA"
                        const cloneCampaignResponse = await ev.post(cloneCampaignEndpoint)
                        console.log(cloneCampaignResponse.data);
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