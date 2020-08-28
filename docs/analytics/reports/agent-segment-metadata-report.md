# About Agent Segment Metadata Report

The Agent Segment Metadata Report provides granular details of agent activity for each call leg during the date range selected. Each record represents a call leg and details the activity of that leg including ring time, hold time, and talk time. The Agent Segment Metadata Report is split into two reports: one for inbound call and one for outbound dialing.

### Primary Parameters

To retrieve the report, send a JSON request body with the following notable parameters. See the example below for more.

| API Property | Description |
|-|-|
| **`reportType`** | set to `CASPER_REPORT`. |
| **`reportTypeName`** | set to `Agent_Segment_Metadata_Report`. |
| **`reportCriteria.startTimestamp`** | use ANSI SQL 92` TIMESTAMP` format such as: `2020-04-22 00:00:00.0000`. |
| **`reportCriteria.endTimestamp`** | use ANSI SQL 92` TIMESTAMP` format such as: `2020-04-22 00:00:00.0000`. |

### Request

Be sure to set the proper [BASE_URL](../../../basics/uris/#resources-and-parameters) and [authorization header](../../../authentication/auth-ringcentral) for your deployment.

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
Agent ID,Last Name,First Name,Username,Phone,Login DTS,Logout DTS,Dial Group,Presented,Accepted,Manual No Connect,RNA,Disp Xfers,%Calls Xfered,Talk Time (min),Avg Talk Time (min),Login Time (min),Login Utilization,Off Hook Time (min),Rounded OH Time (min),Off Hook Utilization,Off Hook to Login %,Work Time (min),Break Time (min),Away Time (min),Lunch Time (min),Training Time (min),Pending Disp Time (min),Avg Pending Disp Time,External Agent ID,Calls Placed On Hold,Time On Hold (min),Ring Time (min),EngagedTime (min),RNA Time (min),Available Time (min),Team,Login Session ID,Monitoring Sessions
1111111,Smiths,John,john.smith@gmail.,6505550100,4/27/20 12:02 PM,4/27/20 12:47 PM,,0,0,0,0,0,0.00%,0.00,0.00,45.45,0.00%,0.00,0.00,0.00%,0.00%,0.00,0.00,0.00,0.00,0.00,0.00,0.00,,0,0.00,0.00,0.00,0.00,0.00,[No Team Name],111222333,0
```
### Fields

| Field | Description |
|-|-|
| **`uii`** |	The unique identifier for the call |
| **`account_id`** | ID number for the account the agent is connected to |
| **`session_id`** | Every leg of a call has this session ID that starts at 1 and increments from there for each call leg. Most records will start with 2 because the first call leg is usually the outside party (not the agent). Since this is an agent segment report, the outside party session call legs will not be included in this report. Also note that multiple call legs may not involve the agent (like IVR routing or even transfers), such that the agent call leg session may even start later at 3 or 4 |
| **`call_ani`** | Automatic Number Identification (ANI) is the phone number of the caller |
| **`call_dnis`** | When the call type is `INBOUND` this number is the Dialed Number Identification Service (DNIS) of the agent. For `OUTBOUND` calls it is empty |
| **`call_type`** | The direction of this call is `INBOUND` (caller calls agent) or `OUTBOUND` (agent calls lead) |
| **`agent_login_id`** | An internal unique agent login identifier |
| **`agent_id`** | ID number of the agent for the row |
| **`agent_first`** | First Name of the agent |
| **`agent_last`** | Last name of the agent |
| **`agent_username`** | The username of the agent |
| **`product_type`** | Inbound calls have the product type of `QUEUE` while outbound calls are of product type `CAMPAIGN` |
| **`product_id`** | The unique identifier of the product queue, or campaign |
| **`product_name`** | The name of the queue or campaign |
| **`enqueue_dts`** | The date/time stamp when the call was queued |
| **`dequeue_dts`** | The date/time stamp when the call was removed from the queue |
| **`queue_duration`** | Amount of time the caller was in the queue |
| **`start_dts`** | The start date/time of the call, after the call is answered |
| **`end_dts`** | The end date/time of the call |
| **`duration`** | The length of time of the call in seconds |
| **`wrap_time`** | The amount of time to disposition (take notes) the call |
| **`dial_dts`** | The date/time stamp of the dialing, or also known as the date and time the call started to ring |
| **`dial_duration`** | Also known as ring time, this is the time in seconds the agent waits for a call to be picked up |
| **`hold_duration`** | The amount of time the call was on hold in seconds |
| **`agent_wait_duration`** | Amount of time the agent is available to receive a call, calculated in seconds, since the previous call was completed |
| **`term_party`** | Who terminated the call? Was it the `SYSTEM`? Or the `CALLER`? |
| **`term_reason`** | Why was the call terminated? Was it the end of the call (`EOC`) or was the call dropped (`DROP`), or maybe the caller hung up (`HANGUP`) |
| **`agent_disposition`** | Any notes that the agent took about the call |
| **`segment_recording_filename`** | The filename of the recording. This is the combination of a date/time stamp and session ID and is stored as a `WAV` file |
| **`segment_recording_url`** | A link to the segment of the audio call recording (`WAV`) |
