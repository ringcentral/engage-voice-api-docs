# Unique Integration APIs

When integrating workforce management with our contact center platform, you may also want to connect to our RingCentral MVP platform. For example, agents may have a need to contact other employees who are not agents and are part of the back office. Those employees will have a RingCentral MVP account and you'll need the RingCentral user ID to lookup the address book and find contacts that are only in the back office. In those cases, you need a mapping between the RingCentral user ID and Engage Voice agent ID.

## User List

The [public user list](https://developers.ringcentral.com/engage/voice/api-reference/Users/listAllUsers) most developers will use has many details including creation date, enabled status, and roles. However, for integrations, a smaller set of user data may be all that is needed, but with the added ability to distinguish the Engage user name from the RingCentral user name and the environment ID. For this purpose, there's an [integration user list](https://developers.ringcentral.com/engage/voice/api-reference/Integration-User-Controller/getUserList) that can be used instead.

## Sub-Accounts

Each main account has a sub-account where most customers reside. However, for partners, more sub-accounts may exist and retrieving [sub-accounts](https://developers.ringcentral.com/engage/voice/api-reference/Integration-Account-Controller/getSubAccountsByMainAccountId) may be useful for determining which account is being used by the customer.

## Agents

Most developers will want a list of agents and agent groups, but for workforce management, there are additional details that are important to know about agents.  [Agents](https://developers.ringcentral.com/engage/voice/api-reference/Agents/getAgentList) are derived from RingCentral MVP users and the RingCentral User ID will map to an agent ID in Engage Voice.  Along with this detail, you can also retrieve the agent's supervisors as an array of agent IDs, or if the agent is a supervisor, a list of agents that the agent supervises (`superviseeAgentIds`).

## Queue Groups

Once known as gates, queues are inbound routing rules for customers calling in to a number. Typically, queues have agents assigned to them and each queue would have to be iterated through to find all the agents assigned to a queue group. However, the [gate group with agents](https://developers.ringcentral.com/engage/voice/api-reference/Integration-Gate-Group-Controller/getGateGroupsWithAgents) integration API allows you to get a complete list of all queues in a queue group and the agents contained in that queue in a single call.

## Integration Reports

The integration reports are special reports for integration purposes to assist with better workforce management. The integration reports consists of the following reports for agent and queue statistics.

* Agent Extended Statistics Report - An extended agent and queue report with call counts and durations
* Agent Segment Metadata Report - A detailed agent interaction report by segment for each call
* Queue Statistics Report - A specific report that lists all the queues in a queue group and the agents within each queue.

### Agent Extended Statistics Report

The report file can be in either CSV or XML format. The table below explains the fields of each interval.

| Field | Description |
|-|-|
| interval | period of time in minutes in 15, 30, 45, or 60 minute lengths. |
| date_from | start date for this interval |
| time (H24:MI) | time in hour:minute format of the current interval |
| agent_id | the agent's unique identifier |
| agent_name | the agent's full name |
| queue | the queue's unique identifier in which the agent is in |
| queue_name | the queue's name in which the agent is in |
| talking_call_dur | total handling time (in seconds) on the call |
| wrap_up_dur | Total wrap-up time or after call work (in seconds), associated with queue calls answered by the agent |
| answ_call_cnt | number of answered calls (only calls through a queue)|
| transfer_out_call_cnt | number of calls answered and then transferred to a queue |

### Agent Segment Metadata Report

Also known as the interaction metadata report, this report is broken down into call legs, or also known as segments. Each segment consists of an interaction between a single agent and client. Each client could have have multiple segments as they are transferred to different agents, but each agent has only a single segment with a client.

`POST https://{BASE_URL}/voice/api/integration/v2/admin/reports/accounts/{subAccountId}/interactionMetadata`

#### Request Body

| Field | Description|
| segmentEndTime | Start date and time for the logging interval |
| timeInterval | Interval length in seconds. Maximum allowed length is 3600 (1 hour). Note: if your time interval start or end in the future consecutive requests may return different list of segment. Idempotent results only guaranteed for the completed intervals. Segment recording URL may be added after delay. Allow 1-2min for processing |
| timeZone | Timezone name which should be used for report generation |

Quick example: let's say we want to find the report with call start time `2022-10-20T07:47:48`, we'll have `segmentEndTime` < `2022-10-20T07:47:48` < `segmentEndTime + timeInterval` (assuming no time zone offset). So a valid set of values for request body will be:

```json
{
    "segmentEndTime": "2022-10-20T07:40:00",
    "timeInterval": 600,
    "timeZone": "US/Eastern"
}
```

#### Response

| Field | Description |
|-|-|
| interactionId | Unique interaction ID (UII) used to connect different call segments together in transfer/conference scenarios. |
| interactionRecordingLocation | the link for entire call recording in mono format |
| interactionStartTimeMs | Start time of the interaction. Could be different from segment start time if customer was engaged with the IVR, waited in queue, etc before agent joined the conversation. Milliseconds precision |
| interactionDurationMs | The total duration of the interaction. Milliseconds precision |
| interactionCallingAddress | The ANI of the interaction. The phone number of the person making the call (this could be the agent or the customer) |
| interactionCalledAddress | The DNIS of the interaction. The phone number of the person who is receiving the call (this could be the agent or the customer) |
| interactionDirection | the direction of the call whether `INBOUND` or `OUTBOUND` |
| segmentID | Unique segment sequence ID within the interaction that typically begins at `2` |
| segmentAgentId | the agent identifier (RingCentral user id) of the agent for this call leg |
| segmentAgentGroupId | the agent group identifier of the agent group this agent belongs to, for this call leg |
| segmentContactStartTimeMs | Time agent joined the conversation. Milliseconds precision |
| segmentContactEndTimeMs | Time agent left the conversation. Milliseconds precision |
| segmentDuration | Segment duration (available even when segmentContactEndTime is not provided) seconds |
| segmentRecordingURL | the call recording for this call leg (note, there could be many legs to a single call if the call is transferred) |
| segmentEvents | Ordered list of events. Can be empty if segmentRecordingURL is empty. In other cases array start with the event REC_START. Events don't overlap each other. A child element has `eventTimeMs`(event time with milliseconds precision. Server side), `clientEventTimeMs`(event time with milliseconds precision. Client side) and `eventType`(can be either `REC_START` or `REC_STOP`)|

### Queue Statistics Report

The report file can be in either CSV or XML format. The table below explains the fields of each interval.

| Field | Description |
|-|-|
| interval | period of time in minutes in 15, 30, 45, or 60 minute lengths. |
| date_from | start date for this interval |
| time (H24:MI) | time in hour:minute format of the current interval |
| queue | the queue’s unique numeric identifier |
| queue_name | given name of the queue |
| offd_direct_call_cnt | inbound calls to this queue, this queue being the original receiver |
| overflow_in_call_cnt | number of calls to this queue with another queue as original receiver (Overflow in) |
| aband_call_cnt | number of lost/abandoned calls during this interval |
| overflow_out_call_cnt | number of overflow calls in this interval |
| answ_call_cnt | number of answered calls in this interval |
| queued_and_answ_call_dur | total queue time for all queued calls that were answered (in seconds) |
| queued_and_aband_call_dur | total queue time for all queued calls that were abandoned (in seconds) |
| talking_call_dur | length of time for the call |
| wrap_up_dur | length of time for the agent to disposition the call |
| queued_answ_longest_que_dur | the longest time a caller was in the queue before it was answered by an agent (in seconds) |
| queued_aband_longest_que_dur | the longest time a caller was in the queue before the caller abandoned (or lost) the call (in seconds) |
| ans_servicelevel_cnt | number of items answered within service level |
| wait_dur | total waiting time for agents ready and waiting on items (in seconds) |
| aband_short_call_cnt | number of abandoned short items, e.g. items with a queue time less than 5 seconds |
| aband_within_sl_cnt | number of abandoned items within service level. Any abandoned items reported in `aband_short_call_cnt` should not be included |