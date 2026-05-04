# Agent Segment Metadata Report (Deprecated)

The Agent Segment Metadata Report API provides granular details of agent activity for each call leg during the date range selected. Each record represents a call leg and details the activity of that leg including ring time, hold time, and talk time. The Agent Segment Metadata Report is split into two reports: one for inbound call and one for outbound dialing.

### Primary Parameters

To retrieve the report, send a JSON request body with the following notable parameters. See the example below for more.

| API Property | Description |
|-|-|
| **`reportType`** | set to `CASPER_REPORT`. |
| **`reportTypeName`** | set to `Agent_Segment_Metadata_Report`. |
| **`reportCriteria.startTimestamp`** | use ANSI SQL 92` TIMESTAMP` format such as: `2020-04-22 00:00:00.0000`. |
| **`reportCriteria.endTimestamp`** | use ANSI SQL 92` TIMESTAMP` format such as: `2020-04-22 00:00:00.0000`. |

### Request

Be sure to set the proper [BASE_URL](../../basics/uris.md#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral.md) for your deployment.

!!! info "Please Note"
    `gateGroupIds` and `gateIds` are actually Queue Groups and Queues. These IDs must be entered as integers (no quotes), and separated by commas for more than one Queue/Queue Group. `dialGroupIds` are groups of campaigns for a single or multiple `campaignIds`. These IDs are also integers and separated by commas.  `accountIds`, on the other hand, is a string value and must be encapsulated in quotes.

=== "Inbound"

    ```bash
    POST {BASE_URL}/api/v1/admin/accounts/{accountId}/reportsStreaming
    Authorization: bearer <myAccessToken>
    Content-Type: application/json;charset=UTF-8

    {
      "reportId":null,
      "destination":null,
      "delimiter":"COMMA",
      "reportType":"CASPER_REPORT",
      "cciReport":true,
      "reportTypeName":"Inbound_Agent_Segment_Metadata_Report",
      "reportCriteria":
      {
        "secureGateGroupIds":"",
        "gateGroupIds":[],
        "secureGateIds":"",
        "gateIds":[],
        "secureAgentGroupIds":"",
        "agentGroupIds":[],
        "secureAgentIds":"",
        "agentIds":[],
        "endUiiTableKey":"",
        "startUiiTableKey":"",
        "endTimestamp":"2020-08-26 23:59:00",
        "startTimestamp":"2020-08-01 00:00:00",
        "timezoneName":"US/Arizona",
        "criteriaType":"CASPER_CRITERIA",
        "reportName":"Inbound_Agent_Segment_Metadata_Report",
        "returnType":"CSV",
        "schedule":
        {
          "repeatOption":"ONCE"
        },
        "accountIds":[]
      }
    }
    ```

=== "Outbound"

    ```bash
    POST {BASE_URL}/api/v1/admin/accounts/{accountId}/reportsStreaming
    Authorization: bearer <myAccessToken>
    Content-Type: application/json;charset=UTF-8

    {
      "reportId":null,
      "destination":null,
      "delimiter":"COMMA",
      "reportType":"CASPER_REPORT",
      "cciReport":true,
      "reportTypeName":"Outbound_Agent_Segment_Metadata_Report",
      "reportCriteria":
      {
        "secureDialGroupIds":"",
        "dialGroupIds":[],
        "secureCampaignIds":"",
        "campaignIds":[],
        "secureAgentGroupIds":"",
        "agentGroupIds":[],
        "secureAgentIds":"",
        "agentIds":[],
        "endUiiTableKey":"",
        "startUiiTableKey":"",
        "endTimestamp":"2020-08-28 23:59:00",
        "startTimestamp":"2020-08-21 00:00:00",
        "timezoneName":"US/Arizona",
        "criteriaType":"CASPER_CRITERIA",
        "reportName":"Outbound_Agent_Segment_Metadata_Report",
        "returnType":"CSV",
        "schedule":
        {
          "repeatOption":"ONCE"
        },
        "accountIds":[]
      }
    }

    ```

### Response

The Agent Segment Metadata Report  endpoint returns data in a CSV format like the following.

```csv
Account ID,UII,Session ID,ANI,DNIS,Call Type,Agent ID,Agent Login ID,Agent First Name,Agent Last Name,Agent Username,Product Type,Product ID,Product Name,Enqueue Dts,Dequeue Dts,Queue Duration,Start Dts,End Dts,Duration,Wrap Time,Dial Dts,Dial Duration,Hold Duration,Agent Wait Duration,Term Party,Term Reason,Agent Disposition,Segment Recording File Name,Segment Recording URL
15300002,'202008281319380132120000030797,2,5106762637,2095466096,INBOUND,1369310,613812570,Craig,Chan,rc.craig.chan+15300002_1791@gmail.com,Queue,72992,My Queue,08/28/2020 10:19:39,08/28/2020 10:19:40,00:00:01,08/28/2020 10:19:40,08/28/2020 10:19:56,00:00:16,00:00:00,08/28/2020 10:19:40,00:00:00,00:00:00,00:00:17,SYSTEM,EOC,,,
```
### Fields

| Column Name | Description |
|-|-|
| **UII** |	The unique identifier for the call |
| **Account ID** | ID number for the account the agent is connected to |
| **Session ID** | Every leg of a call has this session ID that starts at 1 and increments from there for each call leg. Most records will start with 2 because the first call leg is usually the outside party (not the agent). Since this is an agent segment report, the outside party session call legs will not be included in this report. Also note that multiple call legs may not involve the agent (like IVR routing or even transfers), such that the agent call leg session may even start later at 3 or 4 |
| **ANI** | Automatic Number Identification (ANI) is the phone number of the caller |
| **DNIS** | When the call type is `INBOUND` this number is the Dialed Number Identification Service (DNIS) of the agent. For `OUTBOUND` calls it is empty |
| **Call Type** | The direction of this call is `INBOUND` (caller calls agent) or `OUTBOUND` (agent calls lead) |
| **Agent Login ID** | An internal unique agent login identifier |
| **Agent ID** | ID number of the agent for the row |
| **Agent First Name** | First Name of the agent |
| **Agent Last Name** | Last name of the agent |
| **Agent Username** | The username of the agent |
| **Product Type** | Inbound calls have the product type of `QUEUE` while outbound calls are of product type `CAMPAIGN` |
| **Product ID** | The unique identifier of the product queue, or campaign |
| **Product Name** | The name of the queue or campaign |
| **Enqueue Dts** | The date/time stamp when the call was queued |
| **Dequeue Dts** | The date/time stamp when the call was removed from the queue |
| **Queue Duration** | Amount of time the caller was in the queue |
| **Start Dts** | The start date/time of the call, after the call is answered |
| **End Dts** | The end date/time of the call |
| **Duration** | The length of time of the call in seconds |
| **Wrap Time** | The amount of time to disposition (take notes) the call |
| **Dial Dts** | The date/time stamp of the dialing, or also known as the date and time the call started to ring |
| **Dial Duration** | Also known as ring time, this is the time in seconds the agent waits for a call to be picked up |
| **Hold Duration** | The amount of time the call was on hold in seconds |
| **Agent Wait Duration** | Amount of time the agent is available to receive a call, calculated in seconds, since the previous call was completed |
| **Term Party** | Who terminated the call? Was it the `SYSTEM`? Or the `CALLER`? |
| **Term Reason** | Why was the call terminated? Was it the end of the call (`EOC`) or was the call dropped (`DROP`), or maybe the caller hung up (`HANGUP`) |
| **Agent Disposition** | Any notes that the agent took about the call |
| **Segment Recording File Name** | The filename of the recording. This is the combination of a date/time stamp and session ID and is stored as a `WAV` file |
| **Segment Recording URL** | A link to the segment of the audio call recording (`WAV`) |
