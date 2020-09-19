# About Bulk Lead Import

The Engage Voice API allows you to load one or multiple leads at a time. You can also load leads for immediate dialing at the top of the dialer cache or in normal priority.

!!! alert "Please Note"
    To enumerate a list of Campaigns for the `campaignId` path property, please review section [Enumerating Campaigns](./#enumerating-campaigns) below.

The JSON body consists of a set of options along with an array of leads in the `uploadLeads` property

## Primary parameters

Some key options for the request body include:

| Property | Description |
|-|-|
| **dialPriority** | set this value to `IMMEDIATE` to add leads to the top of the dialer queue, `NORMAL` otherwise. |
| **duplicateHandling** | Duplicates are determined by the lead's `leadPhone` property. `REMOVE_ALL_EXISTING` means to remove the existing lead and any prior leads in the existing batch in favor of the new lead. `REMOVE_FROM_LIST` means do not insert the new lead. `RETAIN_ALL` means to keep all duplicates. |
| **timeZoneOption** | this field tells the Engage how to set the timezone for the user. Use `NPA_NXX` to set the timezone via the lead's phone number. Use `ZIPCODE` to set the timezone via the lead's zipcode. Use `EXPLICIT` to set the timezone via the `CampaignLead` object's `leadTimezone` property. Finally, use `NOT_APPLICABLE` if there is no timezone desired. |

Each load in the `uploadLeads` array consists of a lead with the following notable options:

| Property | Description |
|-|-|
| **externId** | this is a required string property. |
| **leadPhone** | this can be a single phone number or a pipe-deliminted field of multiple phone numbers. For US numbers, this is a 10 digit format including area code. |

## Enumerating Campaigns

Leads are uploaded per Campaign which requires a `campaignId`. The following two API calls will enable enumerating the account's campaign list.

1. Call the Get Dial Groups API to get a list of dial groups. Each dial group will have a `dialGroupId` property.

     `GET /api/admin/accounts/{accountId}/dialGroups`

2. For the Dial Group of interest, call the Get Dial Group Campaigns API:

     `GET /api/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns`

## Upload Leads for a campaign

To upload leads for a campaign, we will need a campaign Id. As campaigns are members of a dialing group.

## Enumerating Campaigns and Import Leads

### Request
Be sure to set the proper [BASE_URL](../../../basics/uris/#resources-and-parameters) and [authorization header](../../../authentication/auth-ringcentral) for your deployment.

```http tab="HTTP"
POST {baseURL}/api/admin/accounts/{accountId}/campaigns/{campaignId}/leadLoader/direct
Authorization: Bearer <yourAccessToken>

{
    description: "Prospect customers",
    dialPriority: "IMMEDIATE",
    duplicateHandling: "REMOVE_FROM_LIST",
    listState: "ACTIVE",
    timeZoneOption: "NOT_APPLICABLE",
    uploadLeads: [
      {
         leadPhone:"1111111111",
         externId:"1",
         title:"Dr.",
         firstName:"Jeff",
         midName:"John",
         lastName:"Malfetti",
         suffix:"Jr.",
         address1:"3101 Fake St.",
         address2:"Suite 120",
         city:"Rock",
         state:"CO",
         zip:"80500",
         email:"test@test.com",
         gateKeeper:"Some one",
         auxData1:30,
         auxData2:"a",
         auxData3:100,
         auxData4:"aa",
         auxData5:1000,
         auxPhone:"1111111110",
         extendedLeadData:{
            important:"data",
            interested:true
         }
      },{
         leadPhone:"2222222222",
         externId:"222",
         firstName:"Jason",
         midName:"",
         lastName:"Black",
         address1:"1514 Bernardo Ave",
         city:"New York",
         state:"NY",
         zip:"10001",
      },{
         leadPhone:"3333333333",
         externId:"333",
         firstName:"Rich",
         lastName:"Dunbard"
      }
    ],
   "dncTags":[

   ]
}
```

```javascript tab="Node JS"
/****** Install Node JS SDK wrapper *******
$ npm install engagevoice-sdk-wrapper --save
*******************************************/

const EngageVoice = require('engagevoice-sdk-wrapper')

// Instantiate the SDK wrapper object with your RingCentral app credentials
var ev = new EngageVoice.RestClient("RC_CLIENT_ID", "RC_CLIENT_SECRET")

// Login your account with your RingCentral Office user credentials
ev.login("RC_USERNAME", "RC_PASSWORD", "RC_EXTENSION_NUMBER", function(err, response){
  if (!err){
    read_dial_groups()
  }
})  

// List dial groups and get a dial group id
function read_dial_groups(){
  var endpoint = 'admin/accounts/~/dialGroups'
  ev.get(endpoint, null, function(err, response){
    if (!err){
      var jsonObj = JSON.parse(response)
      for (var group of jsonObj){
        if (group.dialGroupName == "My Dial Group - Predictive"){
          read_group_campaigns(group.dialGroupId)
          break
        }
      }
    }
  })
}

// List campaigns under a dial group and get a campaign id
function read_group_campaigns(dialGroupId){
  var endpoint = 'admin/accounts/~/dialGroups/' + dialGroupId + "/campaigns"
  ev.get(endpoint, null, function(err, response){
    if (!err){
      var jsonObj = JSON.parse(response)
      for (var campaign of jsonObj){
        if (campaign.campaignName == "Customer Acquisition"){
          import_campaign_leads(campaign.campaignId)
          break
        }
      }
    }
  })
}

// import leads to a campaign
function import_campaign_leads(campaignId){
  var endpoint = 'admin/accounts/~/campaigns/' + campaignId + "/leadLoader/direct"
  var params = {
    description: "Prospect customers",
    dialPriority: "IMMEDIATE",
    duplicateHandling: "REMOVE_FROM_LIST",
    listState: "ACTIVE",
    timeZoneOption: "NOT_APPLICABLE",
    uploadLeads: [
      {
         leadPhone:"1111111111",
         externId:"1",
         title:"Dr.",
         firstName:"Jeff",
         midName:"John",
         lastName:"Malfetti",
         suffix:"Jr.",
         address1:"3101 Fake St.",
         address2:"Suite 120",
         city:"Rock",
         state:"CO",
         zip:"80500",
         email:"test@test.com",
         gateKeeper:"Some one",
         auxData1:30,
         auxData2:"a",
         auxData3:100,
         auxData4:"aa",
         auxData5:1000,
         auxPhone:"1111111110",
         extendedLeadData:{
            important:"data",
            interested:true
         }
      },{
         leadPhone:"2222222222",
         externId:"222",
         firstName:"Jason",
         midName:"",
         lastName:"Black",
         address1:"1514 Bernardo Ave",
         city:"New York",
         state:"NY",
         zip:"10001",
      },{
         leadPhone:"3333333333",
         externId:"333",
         firstName:"Rich",
         lastName:"Dunbard"
      }
    ]
  }
  ev.post(endpoint, params, function(err, response){
    if (!err){
      console.log(response)
    }
  })
}
```

```python tab="Python"
#### Install Python SDK wrapper ####
# $ pip install engagevoice-sdk-wrapper
#####################################

from engagevoice.sdk_wrapper import *

# List dial groups and get a dial group id
def read_dial_groups():
    endpoint = 'admin/accounts/~/dialGroups'
    resp = ev.get(endpoint)
    for group in resp:
        if (group['dialGroupName'] == "My Dial Group - Predictive"):
            read_group_campaigns(group['dialGroupId'])
            break


# List campaigns under a dial group and get a campaign id
def read_group_campaigns(dialGroupId):
    endpoint = 'admin/accounts/~/dialGroups/%i/campaigns/' % (dialGroupId)
    resp = ev.get(endpoint)
    for campaign in resp:
        if (campaign['campaignName'] == "API Test"):
            #import_campaign_leads(campaign['campaignId'])
            search_campaign_leads()
            break


# import leads to a campaign
def import_campaign_leads(campaignId):
    endpoint = 'admin/accounts/~/campaigns/%i/leadLoader/direct' % campaignId
    params = {
        "description": "Prospect customers",
        "dialPriority": "IMMEDIATE",
        "duplicateHandling": "REMOVE_FROM_LIST",
        "listState": "ACTIVE",
        "timeZoneOption": "NOT_APPLICABLE",
        "uploadLeads": [
          {
             "leadPhone": "1111111111",
             "externId":"1",
             "title":"Dr.",
             "firstName":"Jeff",
             "midName":"John",
             "lastName":"Malfetti",
             "suffix":"Jr.",
             "address1":"3101 Fake St.",
             "address2":"Suite 120",
             "city":"Rock",
             "state":"CO",
             "zip":"80500",
             "email":"test@test.com",
             "gateKeeper":"Some one",
             "auxData1":30,
             "auxData2":"a",
             "auxData3":100,
             "auxData4":"aa",
             "auxData5":1000,
             "auxPhone":"1111111110",
             "extendedLeadData":{
                "important":"data",
                "interested":true
             }
          },{
             "leadPhone":"2222222222",
             "externId":"222",
             "firstName":"Jason",
             "midName":"",
             "lastName":"Black",
             "address1":"1514 Bernardo Ave",
             "city":"New York",
             "state":"NY",
             "zip":"10001",
          },{
             "leadPhone":"3333333333",
             "externId":"333",
             "firstName":"Rich",
             "lastName":"Dunbard"
          }
        ]
      }
    resp = ev.post(endpoint, params)
    print (resp)

ev = RestClient("RC_APP_CLIENT_ID", "RC_APP_CLIENT_SECRET")
try:
    ev.login("RC_USERNAME", "RC_PASSWORD", "RC_EXTENSION_NUMBER")
    read_dial_groups()
except Exception as e:
    print (e)
```

```php tab="PHP"
/************ Install PHP SDK wrapper **************
$ composer require engagevoice-sdk-wrapper:dev-master
*****************************************************/

<?php
require('vendor/autoload.php');

require('vendor/autoload.php');

// Instantiate the SDK wrapper object with your RingCentral app credentials
$ev = new EngageVoiceSDKWrapper\RestClient("RC_APP_CLIENT_ID", "RC_APP_CLIENT_SECRET");
try{
  // Login your account with your RingCentral Office user credentials
  $ev->login("RC_USERNAME", "RC_PASSWORD", "RC_EXTENSION_NUMBER");
    read_dial_groups();
}catch (Exception $e) {
    print $e->getMessage();
}

function read_dial_groups(){
  global $ev;
  $endpoint = 'admin/accounts/~/dialGroups';
  try{
    $resp = $ev->get($endpoint);
    $jsonObj = json_decode($resp);
    foreach ($jsonObj as $group){
      if ($group->dialGroupName == "My Dial Group - Predictive"){
        read_group_campaigns($group->dialGroupId);
        break;
      }
    }
  }catch (Exception $e) {
      print $e->getMessage();
  }
}

function read_group_campaigns($dialGroupId){
  global $ev;
  $endpoint = 'admin/accounts/~/dialGroups/' . $dialGroupId . "/campaigns";
  try{
    $resp = $ev->get($endpoint);
    $jsonObj = json_decode($resp);
    foreach ($jsonObj as $campaign){
      if ($campaign->campaignName == "API Test"){
          load_campaign_leads($campaign->campaignId)
          break;
      }
    }
  }catch(Exception $e) {
      print $e->getMessage();
  }
}

function load_campaign_leads($campaignId){
  global $ev;
  $endpoint = 'admin/accounts/~/campaigns/' . $campaignId . "/leadLoader/direct";
  $params = array (
    "description" => "Prospect customers",
    "dialPriority" => "IMMEDIATE",
    "duplicateHandling" => "REMOVE_FROM_LIST",
    "listState" => "ACTIVE",
    "timeZoneOption" => "NOT_APPLICABLE",
    "uploadLeads" => array (
      array (
         "leadPhone" => "1111111111",
         "externId" => "1",
         "title" => "Dr.",
         "firstName" => "Jeff",
         "midName" => "John",
         "lastName" => "Malfetti",
         "suffix" => "Jr.",
         "address1" => "3101 Fake St.",
         "address2" => "Suite 120",
         "city" => "Rock",
         "state" => "CO",
         "zip" => "80500",
         "email" => "test@test.com",
         "gateKeeper" => "Some one",
         "auxData1" => 30,
         "auxData2" => "a",
         "auxData3" => 100,
         "auxData4" => "aa",
         "auxData5" => 1000,
         "auxPhone" => "1111111110",
         "extendedLeadData" => array (
            "important" => "data",
            "interested" => true
         )
      ),
      array (
         "leadPhone" => "2222222222",
         "externId" => "222",
         "firstName" => "Jason",
         "midName" => "",
         "lastName" => "Black",
         "address1" => "1514 Bernardo Ave",
         "city" => "New York",
         "state" => "NY",
         "zip" => "10001",
      ),
      array (
         "leadPhone" => "3333333333",
         "externId" => "333",
         "firstName" => "Rich",
         "lastName" => "Dunbard"
      )
    )
  );
  try{
    $resp = $ev->post($endpoint, $params);
    print ($resp);
  }catch(Exception $e) {
      print $e->getMessage();
  }
}
```
