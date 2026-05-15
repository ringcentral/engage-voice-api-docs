# Dialer Result Download (Deprecated)

The Dialer Result Download provides data on all calls matching the search criteria. Administrators use this report to get information on specific agents and call/chat activities including agent notes.

!!! alert "Please Note"
    Calls will appear in this report a few minutes after a call ends or agent dispositions, whichever comes last. Live calls are not included in this report. If you wish to retrieve information on live calls, see the [Active Calls API](../../dialing/active-calls/index.md).

### Primary Parameters

The dialer result report has a number of request properties that allow filtering results (criteria):

| API Property | Description |
|-|-|
| **`reportType`** | set this to `DIALER_RESULT_DOWNLOAD`. This corresponds to the Dialer Result Download real-time report in the analytics console. |
Criteria
| **`reportCriteria.criteriaType`** | set this to `DIALER_RESULT_DOWNLOAD_CRITERIA`. This defines the criteria type for this specific report.
| **`reportCriteria.startDate`** | a start date is required. This should be in ISO-8601 format such as: `2020-04-22T00:00:00.000-0000`. |
| **`reportCriteria.endDate`** | field is optional and uses the same format as `startDate`. |
| **`reportCriteria.includeAuxData`** | Set to `true` to download all aux data. |
| **`reportCriteria.includeXferData`** | Set to `true` to download all transfer data (fields that start with ‘transfer_’). |
| **`reportCriteria.includeSpeedToLead`** | Set to `true` to download all speed to lead data (fields that start with ‘speed_to_lead_’). |
| **`reportCriteria.dialedLeadsReportType`** | set to `ALL_LEADS` to retrieve all the leads, or `ALL_PASSES` to just retrieve passes for each lead, or `LAST_PASSES` to retrieve lead's last pass only. |
| **`reportCriteria.systemDisposition`** | a predefined set of disposition states. Please review the list of available [disposition types](#system-disposition). |
Schedule
| **`reportCriteria.schedule.repeatOption`** | set to `ONCE` to only run this report with this criteria a single time |
| **`reportCriteria.schedule.scheduleTimezoneName`** | Use the "TZ database name" from the [tz database](https://en.wikipedia.org/wiki/Tz_database). For example, `US/Pacific`. |


###  Request

Be sure to set the proper [BASE_URL](../../basics/uris.md#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral.md) for your deployment.

#### HTTP

```http
POST /api/v1/admin/accounts/{accountId}/reportsStreaming
Authorization: bearer <myAccessToken>
Content-Type: application/json;charset=UTF-8
Accept: application/json

{
	"reportType":"DIALER_RESULT_DOWNLOAD",
	"reportCriteria":{
		"criteriaType":"DIALER_RESULT_DOWNLOAD_CRITERIA",
		"startDate":"2020-04-22T00:00:00.000-0000",
    "includeAuxData":true,
    "includeXferData":true,
    "includeSpeedToLead":true,
    "dialedLeadsReportType":"ALL_LEADS",
    "systemDisposition:":"ALL",
    "schedule": {
      "repeatOption":"ONCE",
      "scheduleTimezoneName":"US/Eastern"
    }
	}
}
```

### System Disposition

| API Property | Description |
|-|-|
| **`ALL`** | returns all dialed calls regardless of disposition type |
| **`ANSWER`** | returns answered calls |
| **`NOANSWER`** | returns calls with no answer |
| **`MACHINE`** | returns calls sent to a voicemail or an answering machine |
| **`BUSY`** | returns calls with a busy signal |
| **`INTERCEPT`** | returns calls noted as invalid numbers |
| **`CONGESTION`** | returns calls that ended due to excessive network traffic or insufficient bandwidth |
| **`ABANDON`** | returns calls that ended because the system could not find an available agent after dialing the lead |
| **`ANSWER-NOT-PERSON`** | returns calls that were answered, but the response was not a real person |

### Response

The dialer result report returns data in a CSV format like the following.

```csv
"callID","ID","campaign_id","campaign_name","country_name","lead_phone","lead_state","lead_timezone","title","first_name","mid_name","last_name","suffix","address1","address2","city","state","zip","lead_passes","pass_disposition","agent_disposition","call_start","duration","agent_notes","agent_id","extern_agent_id","username","agent_first_name","agent_last_name","loaded_caller_id","on_hold","dial_type","billing_code","aux_data1","aux_data2","aux_data3","aux_data4","aux_data5","aux_phone","upload_date","list_state","list_desc","recording_url","term_session","email","gate_keeper","live_answer_message","mach_answer_message","int_prefix","int_dest","int_cost","transfer_phone","transfer_disp","transfer_duration","transfer_type","speed_to_lead_first_pass","speed_to_lead_agent_conn","dial_duration","agent_wait_time","agent_wrap_time","transfer_dial_duration","dial_group_id","dial_group_name"
```
### Fields

| Column Name | Description |
|-|-|
| **`callID`** | The unique identifier for the call |
| **`ID`** | The unique record ID for this call |
| **`campaign_id`** | ID for the campaign |
| **`campaign_name`** | A friendly name for the campaign |
| **`country_name`** | The call's country of origin |
| **`lead_phone`** | The phone number of the lead being called |
| **`lead_state`** | The state in which the lead resides |
| **`lead_timezone`** | The timezone in which the lead resides |
| **`title`** | Name prefix like Mr., Mrs., Dr., etc. |
| **`first_name`** | The lead's first name |
| **`mid_name`** | The lead's middle name |
| **`last_name`** | The lead's last name |
| **`suffix`** | The leads suffix at the end of their name, like Jr. |
| **`address1`** | First line of address, typically containing street |
| **`address2`** | Second line of address |
| **`city`** | City where the lead resides |
| **`state`** | State where the lead resides |
| **`zip`** | Zip code where the lead resides |
| **`lead_passes`** | The number of passes the lead has accured so far |
| **`pass_disposition`** | The system disposition for the pass. See [system disposition](#system-disposition) for disposition types  |
| **`agent_disposition`** | The disposition created by the agent for this pass |
| **`call_start`** | The date and time the call began |
| **`duration`** | The duration of the call (in minutes) |
| **`agent_notes`** | Any notes the agent inserted into the disposition |
| **`agent_id`** | The agent ID associated with the pass |
| **`extern_agent_id`** | An external agent ID to associated with the pass |
| **`username`** | The agent's username |
| **`agent_first_name`** | The agent's first name |
| **`agent_last_name`** | The agent's last name |
| **`loaded_caller_id`** | The loaded caller ID to show the lead when the agent calls |
| **`on_hold`** | Duration, in seconds, the call was placed on hold by the agent |
| **`dial_type`** | Originating dial type of the call |
| **`billing_code`** | Billing code from the lead |
| **`aux_data1-5`** | Auxiliary data for the lead. This can be any information you wish to store for a lead |
| **`aux_phone`** | Auxiliary phone number for the lead. This can be any information you wish to store for a lead |
| **`upload_date`** | Upload date for a lead list. *Note*: If leads are added to an existing list, later on the upload date will still reflect the original upload date for the list, not the date the new leads were added |
| **`list_state`** | The state of the lead list |
| **`list_desc`** | A description of the lead list |
| **`recording_url`** | Web address (link) to access the recording of the call |
| **`term_session`** | Attempts to determine which party ended the call |
| **`email`** | The lead's email address |
| **`live_answer_message`** | Field from the lead, an audio file to be played on live answer of power dial |
| **`mach_answer_message`** | Field from the lead, an audio file to be played if machine answer is detected |
| **`int_prefix`** | The international prefix that was prepended to a lead number for international dialing |
| **`int_dest`** | Country destination for an international call |
| **`int_cost`** | Cost calculated for international call |
| **`transfer_phone`** | The phone number the call was transferred to |
| **`transfer_disp`** | The disposition of the transferred call |
| **`transfer_duration`** | The amount of time, in seconds, the call was connected to the transfer destination |
| **`transfer_type`** | The type of transfer (such as warm or cold) that occurred when the system transferred a connected lead |
| **`speed_to_lead_first_pass`** | The amount of time that passed between a lead first being loaded into the system and when the first attempt was made to dial the lead |
| **`speed_to_lead_agent_conn`** | The amount of time that passed between a lead first being loaded into the system and when the lead was connected to an agent |
| **`dial_duration`** | The amount of time the call spent dialing the destination, in seconds |
| **`agent_wait_time`** | The amount of time the agent spent waiting to be connected to the call |
| **`agent_wrap_time`** | The amount of time the agent spends pending disposition after a call |
| **`transfer_dial_duration`** | Time, in seconds, the call was dialing to the transfer destination |
| **`dial_group_id`** | The unique identifier for the dial group |
| **`dial_group_name`** | The name of the dial group |
