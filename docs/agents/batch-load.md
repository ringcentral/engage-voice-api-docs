# Batch Load Leads

The Engage Voice API allows you to load one or multiple leads at a time. You can also load loads for immediate dialing at the top of the dialer cache or in normal priority.

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

* `dialPriority`: set this value to `IMMEDIATE` to add leads to the top of the dialer queue, `NORMAL` otherwise.
* `duplicateHandling`: Duplicates are determined by the lead's `leadPhone` property `REMOVE_ALL_EXISTING` means to remove the existing lead and any prior leads in the existing batch in favor of the new lead. `REMOVE_FROM_LIST` means do not insert the new lead. `RETAIN_ALL` means to keep all duplicates.
* `timeZoneOption`: this field tells the Engage how to set the timezone for the user. Use `NPA_NXX` to set the timezone via the lead's phone number. Use `ZIPCODE` to set the timezone via the lead's zipcode. Use `EXPLICIT` to set the timezone via the `CampaignLead` object's `leadTimezone` property. Finally, use `NOT_APPLICABLE` if there is no timezone desired.

Each load in the `uploadLeads` array consists of a lead with the following notable options:

* `externId`: this is a required string property. 
* `leadPhone`: this can be a single phone number or a pipe-deliminted field of multiple phone numbers. For US numbers, this is a 10 digit format including area code.

The following is a full example:

```
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

Leads are uploaded per Campaign which requires a `campaignId`. The following two API calls will enable enumerating the account's campign list.

1. Call the Get Dial Groups API to gete a list of dial groups. Each dial group will have a `dialGroupId` property.

`GET /api/admin/accounts/{accountId}/dialGroups`

2. For the Dial Group of interest, call the Get Dial Group Campaigns API:

`GET /api/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns`
