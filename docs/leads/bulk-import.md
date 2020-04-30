# Bulk Lead Import

The Engage Voice API allows you to load one or multiple leads at a time. You can also load leads for immediate dialing at the top of the dialer cache or in normal priority.

Use the following endpoint with the JSON body described below.

`POST {baseURL}/api/admin/accounts/{accountId}/campaigns/{campaignId}/loader/direct`

The `baseURL` for your server is one of the following:

* `https://engage.ringcentral.com/voice`
* `https://portal.vacd.biz/`
* `https://portal.virtualacd.biz/`

See the [authentication pages](../basics/authentication) for the [current system API](../basics/auth-ringcentral) and [legacy system API](../basics/auth-legacy) for more.

> Note: to enumerate a list of Campaigns for the `campaignId` path property, section "Enumerating Campaigns" below.

The JSON body consists of a set of options along with an array of leads in the `uploadLeads` property

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

The following is a full example:

```http
POST {baseURL}/api/admin/accounts/{accountId}/campaigns/{campaignId}/loader/direct
Authorization: Bearer <yourAccessToken>

{
   "listState":"ACTIVE",
   "duplicateHandling":"RETAIN_ALL",
   "timeZoneOption":"NPA_NXX",
   "description":"(list name goes here)",
   "dialPriority":"IMMEDIATE",
   "uploadLeads":[
      {
         "leadPhone":"8888888888",
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
         "auxPhone":8888888888,
         "extendedLeadData":{
            "important":"data",
            "interested":true
         }
      }
   ],
   "dncTags":[

   ]
}
```

## Enumerating Campaigns

Leads are uploaded per Campaign which requires a `campaignId`. The following two API calls will enable enumerating the account's campaign list.

1. Call the Get Dial Groups API to get a list of dial groups. Each dial group will have a `dialGroupId` property.

     `GET /api/admin/accounts/{accountId}/dialGroups`

2. For the Dial Group of interest, call the Get Dial Group Campaigns API:

     `GET /api/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns`

## Sample Code: Enumerating Campaigns

The following code sample shows how to list all campaigns of a dial group.

```javascript tab="Node JS"
/****** Install Node JS SDK wrapper *******
$ npm install engagevoice-sdk-wrapper --save
*******************************************/

const EngageVoice = require('engagevoice-sdk-wrapper')

var ev = new EngageVoice.RestClient()

ev.login("legacy-username", "legacy-password", "", function(err, response){
    if (err)
      console.log(err)
    else{
      list_account_dial_groups()
    }
})

function list_account_dial_groups(){
    var endpoint = 'admin/accounts/~/dialGroups'
    ev.get(endpoint, null, function(err, response){
        if (err){
            console.log(err)
        }else {
            var jsonObj = JSON.parse(response)
            for (var item of jsonObj){
              console.log(item)
              console.log("======")
              list_campaigns(item.dialGroupId)
            }
        }
    })
}

function list_campaigns(dialGroupId){
    var endpoint = `admin/accounts/~/dialGroups/${dialGroupId}/campaigns`
    ev.get(endpoint, null, function(err, response){
        if (err){
            console.log(err)
        }else {
            var jsonObj = JSON.parse(response)
            console.log(jsonObj)
        }
    })
}
```

```python tab="Python"
#### Install Python SDK wrapper ####
# $ pip install engagevoice-sdk-wrapper
#####################################

from engagevoice.sdk_wrapper import *

def list_account_dial_groups():
    try:
        endpoint = "admin/accounts/~/dialGroups"
        response = ev.get(endpoint)
        jsonObj = json.loads(response)
        for item in jsonObj:
            print (item)
            print ("======")
            list_campaigns(item['dialGroupId'])
    except Exception as e:
        print (e)


def list_campaigns(dialGroupId):
    try:
        endpoint = 'admin/accounts/~/dialGroups/%s/campaigns' % (dialGroupId)
        response = ev.get(endpoint)
        jsonObj = json.loads(response)
        print (jsonObj)
    except Exception as e:
        print (e)


ev = RestClient()
try:
    resp = ev.login("legacy-username", "legacy-password")
    if resp:
        list_account_dial_groups()
except Exception as e:
    print (e)
```

```php tab="PHP"
/************ Install PHP SDK wrapper **************
$ composer require engagevoice-sdk-wrapper:dev-master
*****************************************************/

<?php
require('vendor/autoload.php');

$ev = new EngageVoiceSDKWrapper\RestClient();
try{
    $ev->login("legacy-username", "legacy-password", null, function($response){
      list_account_dial_groups();
    });
}catch (Exception $e) {
    print $e->getMessage();
}

function list_account_dial_groups(){
    global $ev;
    $endpoint = "admin/accounts/~/dialGroups";
    try{
        $resp = $ev->get($endpoint);
        $jsonObj = json_decode($resp);
        foreach ($jsonObj as $item){
          print(json_encode($item)."\r\n");
          print ("======\r\n");
          list_campaigns($item->dialGroupId);
          print ("======\r\n");
        }
    }catch (Exception $e) {
        print $e->getMessage();
    }
}

function list_campaigns($dialGroupId){
    global $ev;
    $endpoint = 'admin/accounts/~/dialGroups/'.$dialGroupId.'/campaigns';
    $resp = $ev->get($endpoint);
    print ($resp."\r\n");
}
```
