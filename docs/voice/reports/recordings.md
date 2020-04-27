# Call Details and Recordings

Call detail records (CDRs) and recordings are available via the Reports API, which contains URLs for call recordings in each call detail record.

## Call Detail Records Request

The call detail report a number of request properties that allow filtering results:

* `reportType`*: set this to `GLOBAL_CALL_TYPE_EXCEL`. This corresponds to the Global Call Type Detail real-time report in the analytics console.
* `startDate`*: a start datee is required. This should be in ISO-8601 format such as: `2020-04-22T00:00:00.000-0000`.
* `endDate`: field is optional and usess the same format as `startDate`.

Make an API request to the `accounts/{accountId}/json` endpoint as follows:

```bash tab="HTTP"
POST /api/v1/admin/accounts/{accountId}/json
Authorization: bearer <myAccessToken>
Content-Type: application/json;charset=UTF-8
Accept: application/json

{
	"reportType":"GLOBAL_CALL_TYPE_EXCEL",
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

## Call Detail Records Report Response

The call detail record includes a number of properties for thee call, allowing you to identify specific information regarding the call including wait times can caller ID

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
    "connectedName":"Smelik, Alex",
    "connectedRoute":"16505550150*102",
    "connectedDuration":15,
    "connectedDisposition":null,
    "finalDisposition":null,
    "connectedTermParty":"Smelik Alex (shmeltex+15444@gmail.com)",
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

The `uii` is the unique identifier in the call in Engage.

### Calculating Wait Times

The call detail record provides 3 times for the call, and can be used to calculate the caller wait time:

* `callStartDts`: time when the call started
* `connectedDts`: time when an agent was connecteed
* `callEndDts`: time when call ended

Calculate the difference between `callStartDts` and `connectedDts` for the caller wait time.

### Phone Numbers

Detailed phone number information also provided in the Call Detail Record including:

* `ani` (Automatic Number Identification - ANI): This indicates the caller's phone number.
* `dnis` (Dialed Number Identification Service - DNIS): This number identifies the number dialed by the caller which can be used to identify the number when the agent is responding to calls on multiple numbers.

## Call Recordings

If a recording is available the report CDR will include the `recordingUrl` property with a URL to the recoridng file. Call recordings are provided in WAV format.

The call recording URLs can be secured using basic auth or accessible anonymously without authentication.

An example recording media request follows:

```tab="HTTP"
GET https://c02-recordings.virtualacd.biz/api/v1/calls/recordings/?... \
&file=.../11111111111111111111-1.WAV
Authorization: Basic <base64-encoded-userrname-password>
```

```tab="cURL"
curl https://c02-recordings.virtualacd.biz/api/v1/calls/recordings/?... \
&file=.../11111111111111111111-1.WAV
-u {username}:{password}
```
