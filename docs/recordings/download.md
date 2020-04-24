# Download CDRs and Recordings


Tee

adoption rate within account.
2000 useeer account. are 3 peoplee using Google Chrome.

2-3 times.





## Request

1600 user accoount

### General

```
POST /api/v1/admin/accounts/15300001/json
Authorization: bearer <myAccessToken>
Content-Type: application/json;charset=UTF-8
Accept: application/json
```

### Body

```json
{
  "reportId":null,
  "delimiter":"COMMA",
  "reportCriteria":{
    "criteriaType":"GLOBAL_CALL_TYPE_CRITERIA",
    "schedule":{
      "repeatOption":"ONCE",
      "scheduleTimezoneName":"US/Eastern"
    },
    "scriptId":null,
    "campaigns":[

    ],
    "dialGroups":[

    ],
    "gateGroups":[

    ],
    "ivrStudioGroups":[

    ],
    "cloudGroups":[

    ],
    "cloudProfiles":[

    ],
    "gates":[

    ],
    "ivrStudios":[

    ],
    "agents":[

    ],
    "agentGroups":[

    ],
    "tracNumbers":[

    ],
    "tracGroups":[

    ],
    "containGates":true,
    "containCampaigns":true,
    "containIvrStudios":true,
    "containCloudProfiles":true,
    "containTracNumbers":true,
    "containAgents":true,
    "includeNoAnswers":false,
    "startDate":"2020-04-22T00:00:00.000-07:00",
    "endDate":"2020-04-22T23:59:59.000-07:00",
    "timezoneName":"US/Arizona"
  },
  "reportType":"GLOBAL_CALL_TYPE_EXCEL"
}
```

## Response

```json
[
  {
    "uii":"202004220959490132100000055248",
    "sourceType":"ACD-INBOUND",
    "sourceGroupId":52532,
    "sourceGroupName":"Demo Queues",
    "sourceId":72870,
    "sourceName":"Demo VF",
    "sourceDescription":null,
    "ani":"6502700813",
    "dnis":"4154948797",
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
    "connectedRoute":"16506662168*102",
    "connectedDuration":15,
    "connectedDisposition":null,
    "finalDisposition":null,
    "connectedTermParty":"Smelik Alex (shmeltex+15444@gmail.com)",
    "connectedTermReason":"EOC",
    "connectedExternId":"",
    "recordingUrl":"https://c02-recordings.virtualacd.biz/api/v1/calls/recordings/?v=1&accountId=15300001&bucket=c02-recordings&region=us-east-1&compliance=false&file=15300001/202004/22/202004220959490132100000055248-1.WAV",
    "dialType":"N/A",
    "jsonResult":"",
    "callStartDts":"2020-04-22T13:59:49.000+0000",
    "callEndDts":"2020-04-22T14:00:24.000+0000",
    "connectedDts":"2020-04-22T14:00:10.000+0000"
  }
]
```