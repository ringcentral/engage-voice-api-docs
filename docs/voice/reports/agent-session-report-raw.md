# Agent Session Report Raw

## Report Request

The agent Session Raw Report is available at the following endpoint:

`accounts/{accountId}/reportsStreaming`

It takes a JSON request body with the following notable parameters. See the example below for more.

| Property | Description |
|-|-|
| **reportType** | set this to `CASPER_REPORT`. |
| **reportTypeName** | set this to `Agent_Session_Report_Raw`. |
| **reportCriteria.startTimestamp** | use ANSI SQL 92` TIMESTAMP` format such as: `2020-04-22 00:00:00.0000`. |
| **reportCriteria.endTimestamp** | use ANSI SQL 92` TIMESTAMP` format such as: `2020-04-22 00:00:00.0000`. |
| **reportCriteria.returnTypes** | this sets the return report format. By default, CSV is returned. You can set this explicitly by using `CSV` and `XML` options. |

```bash tab="HTTP"
POST /api/v1/admin/accounts/{accountId}/reportsStreaming
Authorization: bearer <myAccessToken>
Content-Type: application/json;charset=UTF-8
Accept: application/json

{
  "reportId":null,
  "destination":null,
  "delimiter":"COMMA",
  "reportType":"CASPER_REPORT",
  "cciReport":true,
  "reportTypeName":"Agent_Session_Report_Raw",
  "reportCriteria":{
    "rollupAgent":"",
    "agentTeams":[

    ],
    "secureAgentGroupIds":"",
    "agentGroupIds":[

    ],
    "secureAgentIds":"",
    "agentIds":[

    ],

    "timezoneName":"US/Arizona",
    "criteriaType":"CASPER_CRITERIA",
    "reportName":"Agent_Session_Report_Raw",
    "returnType":"CSV",
    "schedule":{
      "repeatOption":"ONCE"
    },
    "accountIds":[

    ]
  }
}
```

## Report Response

The Agent Session Report Raw endpoint returns data in a CSV format like the following.

```csv
Agent ID,Last Name,First Name,Username,Phone,Login DTS,Logout DTS,Dial Group,Presented,Accepted,Manual No Connect,RNA,Disp Xfers,%Calls Xfered,Talk Time (min),Avg Talk Time (min),Login Time (min),Login Utilization,Off Hook Time (min),Rounded OH Time (min),Off Hook Utilization,Off Hook to Login %,Work Time (min),Break Time (min),Away Time (min),Lunch Time (min),Training Time (min),Pending Disp Time (min),Avg Pending Disp Time,External Agent ID,Calls Placed On Hold,Time On Hold (min),Ring Time (min),EngagedTime (min),RNA Time (min),Available Time (min),Team,Login Session ID,Monitoring Sessions
1111111,Smiths,John,john.smith@gmail.,6505550100,4/27/20 12:02 PM,4/27/20 12:47 PM,,0,0,0,0,0,0.00%,0.00,0.00,45.45,0.00%,0.00,0.00,0.00%,0.00%,0.00,0.00,0.00,0.00,0.00,0.00,0.00,,0,0.00,0.00,0.00,0.00,0.00,[No Team Name],111222333,0
```