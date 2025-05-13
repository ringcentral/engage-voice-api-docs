# Historical Reporting APIs

The following reports are commonly used for workforce management and give you detailed agent interaction records or aggregated statistics across queues and agents.

## Integration Reports

The integration reports are special reports for integration purposes to assist with better workforce management. The integration reports consists of the following reports for agent and queue statistics.

!!! tip "The Reports API calls must be 5 minutes before now!"
    When making an API call for the following reports, you must specify a time period at least 5 minutes before the current time. This means you can not specify a time period in the future, or even the current time. You must specify at least an end time with the end time being 5 minutes before the current time.

!!! tip "Be aware of rate limits"
    The following report APIs are rate limited. This means you can only call the API a certain number of times before having to wait to call the report API again.

    The rate limit is currently set at 2 calls per minute (per node)

    What this means is you may call the report API up to 2 times per node, but your request may be distributed to another node where your API call will succeed. The best way to handle this rate limit is to make an API call and if you receive a rate limit warning `429 Too Many Requests` status code, implement a backoff mechanism (e.g. exponential backoff) to space out retry attempts. You should also log rate limit errors and adjust request strategies accordingly.

* **Agent Segment Metadata Report** - Also known as the interaction metadata report, this detailed agent interaction report has a record for each segment of a call
* **Queue Statistics Report** - A specific report that lists all the queues in a queue group and the agents within each queue.
* **Agent Extended Statistics Report** - An extended agent and queue report with call counts and durations

### Agent Segment Metadata Report

Also known as the interaction metadata report, this report is broken down into call legs, or also known as segments. Each segment consists of an interaction between a single agent and client. Each client could have have multiple segments as they are transferred to different agents, but each agent has only a single segment with a client. The interaction metadata reports are based upon completed interactions, but interactions may take time to be processed before being available in the report. Please allow a 15 minute window before invoking this API to retrieve the current completed interactions.

Be sure to set the proper [BASE_URL](../basics/uris.md#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral.md) for your deployment.

`POST https://{BASE_URL}/api/cx/integration/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/interaction-metadata`

#### Request

| Field | Description|
|-|-|
| segmentEndTime | Start date and time for the logging interval |
| timeInterval | Interval length in seconds. Maximum allowed length is 3600 (1 hour). Note: if your time interval start or end in the future consecutive requests may return different list of segment. Idempotent results only guaranteed for the completed intervals. Segment recording URL may be added after delay. Allow 1-2min for processing |
| timeZone | Timezone name which should be used for report generation |

!!! info "Quick example"
    Let's say we want to find the report with call start time `2022-10-20T07:47:48`, we'll have `segmentEndTime` < `2022-10-20T07:47:48` < `segmentEndTime + timeInterval` (assuming no time zone offset). So a valid set of values for request body will be:

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
| subAccountId | The customer's account that they operate within. |
| dialogId | Each interaction is uniquely identified by this ID. For a call, the interaction starts when a call is made and last until the call is ended. For a chat, the interaction starts when a chat is started and lasts until the chat ends. |
| interactionId | Unique interaction ID (UII) used to connect different call segments together in transfer/conference scenarios. |
| channelId | A unique channel ID for the source associated with an account such as X/Twitter, Facebook, email, or webpage chat. |
| channelType | A more detailed version of the `channelClass`. The `VOICE` channel can have types such as `VOICE`, `MVP_CALL`, or `MVP_MEETING`. The `DIGITAL` channel can consists of many types such as `EMAIL`, `SMS`, or even `TWITTER`. |
| channelClass | RingCX has `VOICE` channels and `DIGITAL` channels to choose from. |
| channelEndpointAddress | The ANI of the interaction. The phone number or user name of the person making the call/chat (this could be the agent or the customer) |
| contactEndpointAddress | The DNIS of the interaction. The phone number or the user name of the person who is receiving the call/chat (this could be the agent or the customer) |
| dialogOrigination | the direction of the call/chat from the perspective of the agent whether `INBOUND` or `OUTBOUND`. For chats, the direction is always `INBOUND` |
| interactionRecordingLocation | the link for entire call recording in mono format |
| dialogStartTimeMs | Start time of the dialog. Could be different from segment start time if customer was engaged with the IVR, waited in queue, etc before agent joined the conversation. Milliseconds precision. |
| dialogDurationMs | The total duration of the dialog, including all agent segments. This can be different from the `segmentDurationMs` because a segment is measured by the agent time with the participant and a dialog can include other agents, IVR, or queue. Milliseconds precision |
| segmentID | Unique segment sequence ID within the interaction. A new segment is created whenever an agent or contact leaves a call or joins a call. There can multiple segments for each dialog (see `dialogId` above). |
| segmentType | A segment is a portion of a dialog. A segment can consist of the `AGENT` or `BOT` talking to a participant, or a participant interacting with an `IVR`. |
| segmentParticipantId | the participant identifier (RingCentral user id) of the participant for this call leg |
| segmentParticipantRcExtensionId | The unique RingCentral identifier represented by their internal extension ID (not extension number that you can dial) |
| segmentStartTimeMs | Time participant joined the conversation. Milliseconds precision and time zone is in UTC. |
| segmentEndTimeMs | Time participant left the conversation. Milliseconds precision and time zone is in UTC. |
| segmentDurationMs | Segment duration (available even when segmentContactEndTime is not provided) in milliseconds. |
| segmentAgentGroupId | the agent group identifier of the agent group this agent belongs to, for this call leg |
| segmentRecordingURL | the call recording for this call leg (note, there could be many legs to a single call if the call is transferred) |
| segmentEvents | Ordered list of events. Can be empty if segmentRecordingURL is empty. In other cases array start with the event REC_START. Events don't overlap each other. A child element has `eventTimeMs`(event time with milliseconds precision. Server side), `clientEventTimeMs`(event time with milliseconds precision. Client side) and `eventType`(can be either `REC_START` or `REC_STOP`)|

### Retrieving Agent Segment Recordings

To retrieve the agent call recording you must first ensure the agent segment recording feature is enabled for each [queue](https://support.ringcentral.com/article-v2/Using-AI-generated-transcripts-and-summaries.html?brand=RingCentral&product=RingCX&language=en_US) or [campaign](https://support.ringcentral.com/article-v2/Configuring-outbound-call-recording-settings.html?brand=RingCentral&product=RingCX&language=en_US) that you want to record (click each type to see how). Once enabled, the interaction-metadata API will indicate an interaction will have a recording available. To retrieve the recording, please wait at least 10 minutes for the recording to be processed and ready.

To retrieve the call recording you will need your account information including your [RingEX account ID](https://developers.ringcentral.com/api-reference/Company/readAccountInfo) and [RingCX subaccount ID](https://developers.ringcentral.com/engage/voice/api-reference/Integration-Account-Controller/getSubAccountsByMainAccountId).

Then you will need two fields from the interaction metadata report including the `dialogId` and the `segmentId`. With these four parameters, you can retriee the call recording in `audio/wav` format

Be sure to set the proper [BASE_URL](../basics/uris.md#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral.md) for your deployment.

`POST https://{BASE_URL}/api/cx/integration/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/recordings/dialogs/{dialogId}/segments/{segmentId}`

### Retrieving Agent Segment Transcripts

#### Special Note About Call Recording Formats

Call recordings are normally returned as a WAV file with PCM 16 bit encoding when using the API. If using the API via a browswer interface, a compressed MP3 file is returned instead. If you need the compressed audio file, you can set a browser like type as the `User-Agent`:

| Key | Value |
|-|-|
| User-Agent | Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 |

### Queue Statistics Report

This report returns statistics for a single queue over a period of time and returns the statistics in JSON format. When making an agent extended statistics report request, you will want to specify the `startDate` in the following format: `YYYY-MM-DD HH:MM:SS`. If you do not specify and `endDate` you will receive all report statistics to the current date. You should specify an `endDate` to limit your response to based upon your `timeZone`. The `timeInterval` will return records in 15, 30, 45, and 60 minute intervals.

Be sure to set the proper [BASE_URL](../basics/uris.md#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral.md) for your deployment.

`POST https://{BASE_URL}/api/cx/integration/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/agg-queue-stats`

#### Request

| Field | Description|
|-|-|
| startDate | Start date and time for the logging interval in `YYYY-MM-DD HH:MM:SS` format |
| endDate | End date and time for the logging interval in `YYYY-MM-DD HH:MM:SS` format |
| timeInterval | Interval length in minutes. This will return records in 15, 30, 45, and 60 minute intervals |
| timeZone | Timezone name which should be used for report generation |

The table below explains the fields of each interval.

#### Response

| Field | Description |
|-|-|
| interval | period of time in minutes in 15, 30, 45, or 60 minute lengths. |
| dateTimeFrom | start date for this interval |
| queue | the queue’s unique numeric identifier |
| queueName | given name of the queue |
| offDirectIxnCnt | inbound calls or chats to this queue, this queue being the original receiver |
| overflowInIxnCnt | number of calls or chats to this queue with another queue as original receiver (Overflow in) |
| abandIxnCnt | number of lost/abandoned calls or chats during this interval |
| overflowOutIxnCnt | number of overflow calls or chats that were sent to another queue in this interval |
| answIxnCnt | number of answered calls in this interval |
| queuedAndAnswIxnDur | total queue time for all queued calls and chats that were answered (in seconds) |
| queuedAndAbandIxnDur | total queue time for all queued calls and chats that were abandoned (in seconds) |
| talkingIxnDur | length of time in seconds for the call and chats |
| wrapUpDur | length of time ins seconds for the agent to disposition the call |
| queuedAnswLongestQueDur | the longest time a caller was in the queue before it was answered by an agent (in seconds) |
| queuedAbandLongestQueDur | the longest time a caller was in the queue before the caller abandoned (or lost) the call (in seconds) |
| ansServicelevelCnt | number of answered conatct on this queue within service level |
| waitDur | total waiting time for agents ready and waiting on contacts (in seconds) |
| abandShortIxnCnt | number of abandoned contacts, e.g. contacts with a queue time less than 5 seconds |
| abandWithinSlCnt | number of abandoned contacts within service level. Any abandoned contacts reported in `aband_short_call_cnt` should not be included |

### Agent Extended Statistics Report

This report returns statistics of all queues along with their agents for given Sub-Account and duration in JSON format. When making an agent extended statistics report request, you will want to specify the `startDate` in the following format: `YYYY-MM-DD HH:MM:SS`. If you do not specify and `endDate` you will receive all report statistics to the current date. You should specify an `endDate` to limit your response to based upon your `timeZone`. The `timeInterval` will return records in 15, 30, 45, and 60 minute intervals.

Be sure to set the proper [BASE_URL](../basics/uris.md#resources-and-parameters) and [authorization header](../../authentication/auth-ringcentral.md) for your deployment.

`POST https://{BASE_URL}/api/cx/integration/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/agg-agent-extended-stats`

#### Request

| Field | Description|
|-|-|
| startDate | Start date and time for the logging interval in `YYYY-MM-DD HH:MM:SS` format |
| endDate | End date and time for the logging interval in `YYYY-MM-DD HH:MM:SS` format |
| timeInterval | Interval length in minutes. This will return records in 15, 30, 45, and 60 minute intervals |
| timeZone | Timezone name which should be used for report generation |

The table below explains the fields of each interval.

#### Response

| Field | Description |
|-|-|
| interval | period of time in minutes in 15, 30, 45, or 60 minute lengths. |
| dateTimeFrom | start date for this interval |
| agentId | the agent's unique identifier |
| agentName | the agent's full name |
| queue | the queue's unique identifier in which the agent is in |
| queueName | the queue's name in which the agent is in |
| talkingIxnDur | total handling time (in seconds) on the call or chat |
| wrapUpDur | total wrap-up time or after call/chat work (in seconds), associated with queue calls or chat answered by the agent |
| answIxnCnt | number of answered calls or chats (only calls or chats through a queue)|
| transferOutIxnCnt | number of calls or chats answered and then transferred to a queue |
