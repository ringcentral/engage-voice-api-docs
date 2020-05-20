# Call Detail Report

The Call Detail Report provides cloud routing data for your cloud-based unified queues and includes every cloud-routed call based on filtering criteria that you supply when running the report.

## Report Request

### API Endpoint

The Call Detail Report can be downloaded at the following endpoint:

`GET api/v1/admin/accounts/{accountId}/reportsStreaming`

#### Supporting APIs

The following API endpoints are used to populate API properties.

* `GET api/v1/admin/accounts`
* `GET api/v1/admin/users`
* `GET api/v1/admin/accounts/{accountId}/users/{userId}/reports/inputControls?accountIds={accountId}&products=CLOUD_PROFILE`
* `GET api/v1/admin/accounts/{accountId}/users/{userId}/reports/inputControls?accountIds={accountId}&products=CLOUD_DESTINATION`

### Request Properties

It takes a JSON request body with the following notable parameters. See the example below for more.

| Property | Description |
|-|-|
| **`reportType`** | set to `CASPER_REPORT`. |
| **`reportTypeName`** | set to `Cloud_Call_Detail_Download`. |
| **`reportCriteria.accountIds`** | This is a string array. To retrieve a list of possible values, call the `/v1/admin/accounts` endpoint and use the `accountId` properties.
| **`reportCriteria.groupBy`** | Either `PROFILE` or `DESTINATION`. If using `PROFILE`, set the `reportCriteria.cloudProfileGroupIds` and `reportCriteria.cloudProfileIds` properties. If using `DESTINATION`, set the `reportCriteria.cloudDestinationGroupIds` and `reportCriteria.cloudDestinationIds` properties. |
| **`reportCriteria.cloudProfileGroupIds`** | Set if `groupBy` is set to `PROFILE`. Corresponds to "Cloud Profile Groups" in the Admin UI. Populate with an integer array of profile `groupId` values. Call the `GET api/v1/admin/accounts/{accountId}/users/{userId}/reports/inputControls?accountIds={accountId}&products=CLOUD_PROFILE` endpoint. Populate with the selected `groupId` values. |
| **`reportCriteria.cloudProfileIds`** | Set if `groupBy` is set to `PROFILE`. Corresponds to "Cloud Profiles" in the Admin UI. Populate with an integer array of profile `groupId` values. Call the `GET api/v1/admin/accounts/{accountId}/users/{userId}/reports/inputControls?accountIds={accountId}&products=CLOUD_PROFILE` endpoint. Populate with the selected group children `objId` values. The objId valuess musts correspond with `groupId` values in the `cloudProfileGroupIds` properties. |
| **`reportCriteria.cloudDestinationGroupIds`** | Set if `groupBy` is set to `DESTINATION`. Corresponds to "Cloud Destination Groups" in the Admin UI. Populate with an integer array of profile `groupId` values. Call the `GET api/v1/admin/accounts/{accountId}/users/{userId}/reports/inputControls?accountIds={accountId}&products=CLOUD_DESTINATION` endpoint. Populate with the selected `groupId` values. |
| **`reportCriteria.cloudDestinationIds`** | Set if `groupBy` is set to `DESTINATION`. Corresponds to "Cloud Destinations" in the Admin UI. Populate with an integer array of profile `groupId` values. Call the `GET api/v1/admin/accounts/{accountId}/users/{userId}/reports/inputControls?accountIds={accountId}&products=CLOUD_DESTINATION` endpoint. Populate with the selected group children `objId` values. The objId valuess musts correspond with `groupId` values in the `cloudProfileGroupIds` properties. |
| **`reportCriteria.startTimestamp`** | use ANSI SQL 92` TIMESTAMP` format such as: `2020-04-22 00:00:00.0000`. |
| **`reportCriteria.endTimestamp`** | use ANSI SQL 92` TIMESTAMP` format such as: `2020-04-22 00:00:00.0000`. |
| **`reportCriteria.timezoneName`** | |
| **`reportCriteria.criteriaType`** | set to `CASPER_CRITERIA`. |
| **`reportCriteria.reportName`** | set to `Cloud_Call_Detail_Download`. |
| **`reportCriteria.returnType`** | set to `CSV`. |
| **`reportCriteria.schedule`** | set to `{"repeatOption":"ONCE"}`. |

### Example Request

Be sure to sure the proper `BASE_URL` and authorization header for your deployment.

=== "HTTP"
```bash
POST {BASE_URL}api/v1/admin/accounts/{accountId}/reportsStreaming
Authorization: bearer <myAccessToken>
Content-Type: application/json;charset=UTF-8

{
  "delimiter":"COMMA",
  "reportType":"CASPER_REPORT",
  "reportTypeName":"Cloud_Call_Detail_Download",
  "reportCriteria":{
    "accountIds":[
      "13670001",
      "15300001"
    ],
    "groupBy":"PROFILE",
    "cloudDestinationGroupIds":[

    ],
    "cloudDestinationIds":[

    ],
    "cloudProfileGroupIds":[
      111,
      null
    ],
    "cloudProfileIds":[
      1111,
      2222,
      3333,
      4444
    ],
    "endTimestamp":"2020-05-19 23:59:59",
    "startTimestamp":"2020-04-19 12:00:00",
    "timezoneName":"US/Arizona",
    "criteriaType":"CASPER_CRITERIA",
    "reportName":"Cloud_Call_Detail_Download",
    "returnType":"CSV",
    "schedule":{
      "repeatOption":"ONCE"
    }
  }
}
```

## Report Response

When uisng the `CSV` type a `text/csv` response is provided.

### Properties

The CSV has the following properties.

1. `cloud_profile_id`
1. `profile_name`
1. `uii`
1. `ani`
1. `dnis`
1. `outbound_externid`
1. `media_isci`
1. `media_network`
1. `smedia_market`
1. `media_code`
1. `media_format`
1. `media_version`
1. `media_length`
1. `enqueue_time`
1. `dequeue_time`
1. `queue_time`
1. `call_state`
1. `is_cellular`
1. `dequeue_attempts`
1. `call_result`
1. `inbound_duration`
1. `recording_url`
1. `connected_id`
1. `connected_name`
1. `connected_route`
1. `connected_duration`
1. `attempt_1_id`
1. `attempt_1_name`
1. `attempt_1_route`
1. `attempt_1_disp`
1. `attempt_2_id`
1. `attempt_2_name`
1. `attempt_2_route`
1. `attempt_2_disp`

### Example Response

The Call Detail Report API returns data in a CSV format like the following.

```csv
cloud_profile_id,profile_name,uii,ani,dnis,outbound_externid,media_isci,media_network,media_market,media_code,media_format,media_version,media_length,enqueue_time,dequeue_time,queue_time,call_state,is_cellular,dequeue_attempts,call_result,inbound_duration,recording_url,connected_id,connected_name,connected_route,connected_duration,attempt_1_id,attempt_1_name,attempt_1_route,attempt_1_disp,attempt_2_id,attempt_2_name,attempt_2_route,attempt_2_disp
1111,DTE,'202004250912250132110000003150,2312866364,8889918278,,,,,,,,0,4/20/20 6:12 AM,4/20/20 6:12 AM,5,COMPLETE            ,No,2,CONNECTED,24,,4546,DTE,5854987200,19,4546,DTE,5854987282,ANSWER(5),,,,
2222,IT TFN,'202004251035200132150000009531,6317967722,8774489485,,,,,,,,0,4/20/20 7:35 AM,4/20/20 7:35 AM,5,COMPLETE            ,No,2,CONNECTED,53,,4467,IT TFN,5127776541,48,4467,IT TFN,5127776551,ANSWER(4),,,,
3333,DTE,'202004251101260132100000073341,2482069215,8889918238,,,,,,,,0,4/20/20 8:01 AM,4/20/20 8:01 AM,5,COMPLETE            ,No,2,CONNECTED,301,,4546,DTE,5854987200,296,4546,DTE,5854987234,ANSWER(4),,,,
```