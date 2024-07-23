# Call Details and Recordings (Deprecated)

Call detail records (CDRs) and recordings are available via the Global Call Type Detail (GCTD) Report which provides complete real-time data for all calls in RingCX. When recordings are available, a media URL is provided in the call detail record.

!!! alert "Please Note"
    Calls will appear in this report a few minutes after a call ends or agent dispositions, whichever comes last. Live calls are not included in this report. If you wish to retrieve information on live calls, see the [Active Calls API](../../dialing/active-calls/index.md).

### Primary Parameters

The call detail report has a number of request properties that allow filtering results:

| API Property | Description |
|-|-|
| **`reportType`** | set this to `GLOBAL_CALL_TYPE_EXCEL` to download this report in MS Excel format or set this to `GLOBAL_CALL_TYPE_DELIMITED` to download this report in comma delimited format. This corresponds to the Global Call Type Detail real-time report in the analytics console. |
| **`startDate`** | a start date is required. This should be in ISO-8601 format such as: `2020-04-22T00:00:00.000-0000`. |
| **`endDate`** | field is optional and uses the same format as `startDate`. |

###  Request

Be sure to set the proper [BASE_URL](../../basics/uris.md#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral.md) for your deployment.

```http
POST /api/v1/admin/accounts/{accountId}/reportsStreaming
Authorization: bearer <myAccessToken>
Content-Type: application/json;charset=UTF-8
Accept: application/json

{
	"reportType":"GLOBAL_CALL_TYPE_DELIMITED",
	"reportCriteria":{
		"criteriaType":"GLOBAL_CALL_TYPE_CRITERIA",
		"startDate":"2020-04-22T00:00:00.000-0000",
		"containGates":true,
		"containCampaigns":true,
		"containIvrStudios":true,
		"containCloudProfiles":true,
		"containTracNumbers":true,
		"containAgents":true,
		"includeNoAnswers":false
	}
}
```

### Response

The call detail record includes a number of properties for the call, allowing you to identify specific information regarding the call including wait times can caller ID

```json
[
  {
    "uii":"111111111111",
    "sourceType":"ACD-INBOUND",
    "sourceGroupId":22222,
    "sourceGroupName":"Demo Queues",
    "sourceId":33333,
    "sourceName":"Demo VF",
    "sourceDescription":null,
    "ani":"6505550100",
    "dnis":"4155550100",
    "callStatus":"COMPLETE",
    "callResult":"CONNECTED",
    "queueTime":"4",
    "callDuration":35,
    "callTermParty":null,
    "callTermReason":null,
    "billingCode":null,
    "callNotes":null,
    "connectId":1364236,
    "connectedName":"Smelik, Jim",
    "connectedRoute":"16505550150*102",
    "connectedDuration":15,
    "connectedDisposition":null,
    "finalDisposition":null,
    "connectedTermParty":"Smelik Jim (mr.smelik@gmail.com)",
    "connectedTermReason":"EOC",
    "connectedExternId":"",
    "recordingUrl":"https://c02-recordings.virtualacd.biz/api/v1/calls/recordings/?...&file=.../11111111111111111111-1.WAV",
    "dialType":"N/A",
    "jsonResult":"",
    "callStartDts":"2020-04-22T13:59:49.000+0000",
    "callEndDts":"2020-04-22T14:00:24.000+0000",
    "connectedDts":"2020-04-22T14:00:10.000+0000"
  }
]
```

### Unique Item Identifier

The `uii` is the unique identifier in the call in RingCX.

### Calculating Wait Times

The call detail record provides 3 times for the call, and can be used to calculate the caller wait time:

| API Property | Description |
|-|-|
| **`callStartDts`** | time when the call started |
| **`callEndDts`** | time when call ended |
| **`connectedDts`** | time when an agent was connected |

Calculate the difference between `callStartDts` and `connectedDts` for the caller wait time.

### Phone Numbers

Detailed phone number information is also provided in the Call Detail Record including:

| API Property | Description |
|-|-|
| **`ani`** | (Automatic Number Identification - ANI): This indicates the caller's phone number. |
| **`dnis`** | (Dialed Number Identification Service - DNIS): This number identifies the number dialed by the caller which can be used to identify the number when the agent is responding to calls on multiple numbers. |

## Call Recordings

If a recording is available the report CDR will include the `recordingUrl` property with a URL to the recording file. Call recordings are provided in WAV format.

The call recording URLs can be secured using basic auth or accessible anonymously without authentication.

An example recording media request follows:

=== "HTTP"

    ```http
    GET https://c02-recordings.virtualacd.biz/api/v1/calls/recordings/?... \
    &file=.../11111111111111111111-1.WAV
    Authorization: Basic <base64-encoded-username-password>
    ```

=== "cURL"
    ```bash
    > curl https://c02-recordings.virtualacd.biz/api/v1/calls/recordings/?... \
         &file=.../11111111111111111111-1.WAV
         -u {username}:{password}
    ```
