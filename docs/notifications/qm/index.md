# Introduction to Quality Management

Quality Management takes Workforce Management one step further, giving you the tools to measure and monitor agent performance by looking at the quality of customer interactions. To accomplish this goal, you'll need to collect information about two things: the agent and the call.

## Agent Events

Tracking your agents in real time is important for workforce management, but knowing when an agent is engaged with a customer is equally important. Follow the guide for [Configuring Workforce Management](../wfm/configure-wfm.md) and track in real time your agents interaction with customers. When an agent state changes to `ENGAGED`, then they are on a call with a customer.

## Call Events

When a call is ended, a call event is triggered so you can know that a call is ready for processing. Follow the guide for [Configuring Workforce Management](../wfm/configure-wfm.md) and make sure to select `End Call Events`. See the details of an [End Call Event](../wfm/payload-wfm/#end-call-events) payload that is sent to your endpoint.

## Call Details and Recordings

Sometimes, you may miss an event due to server issues or connection issues.  In these cases, you can reconcile your call events with the [Call Details and Recordings](../../analytics/reports/global-call-type-detail-report/) report. All the call details are available in this historical report including the mono [call recording](../../analytics/reports/global-call-type-detail-report/#call-recordings).

## Agent Reports

Not all agent performance can be tracked via events. Some details like ring time, hold time, and talk time are all captured and report on after the call. You can find these report details in the [Agent Segment Metadata Report](../../analytics/reports/agent-segment-metadata-report.md). This report also includes the call recording, stored as a `WAV` file and can be retrieved 1-2 minutes after the call ends. To determine when a call ends, use the [Configuring Workforce Management](../wfm/configure-wfm.md) to listen for End Call Events.

## Call Recordings

Call recordings can be retrieved as mono (single channel) recordings or as stereo (dual channel) recordings.  

### Mono Call Recordings (Single Channel)

Call recordings are the audio files of the call. You can retrieve mono (single channel) call recordings using the [End Call Event](../wfm/payload-wfm/#end-call-events). If a call is answered and recorded, a call recording link will appear in the event under `recording_url`. Use this link to retrieve the call recording.

=== "Mono Call Recording"
    ```html
      https://c02-recordings.virtualacd.biz/api/v1/calls/recordings/?v=1&accountId=15300002&bucket=c02-recordings&region=us-east-1&compliance=false&file=15300002/202007/30/202007302136360132130000036446-1.WAV
    ```

!!! important
    While the recording URL is sent 1-3 seconds after a call is ended, the actual recording takes more time to encode. Depending on the length of the recording, the recording link may not be valid for up to 1-2 minutes after the end call event.


### Stereo Call Recordings (Dual Channel)

Stereo Call (dual channel) recordings can also be retrieved from the [Agent Segment Metadata Report](../../analytics/reports/agent-segment-metadata-report.md). You can find the call recording from the `Segment Recording URL` field in the downloaded report.  Note that the stereo call recording is a `perspective` type recording and must be set manually.

=== "Stereo Call Recording"
    ```html
      https://aws46-recordings.vacd.biz/api/v1/calls/recordings?v=1&accountId=15300002&bucket=aws46-recordings&region=us-west-2&compliance=true&file=perspective/15300002/202008/05/202008051517160139120000000370-session-2-stereo.WAV
    ```

!!! important
    This recording is only available for customer accounts that are manually activated. Please work with your RingCentral representative to activate stereo recordings for the account you wish to gather stereo recordings from.

!!! alert "Please Note"
    This report may take some time to show new records so it's best to periodically retrieve this report and note that the most recent recordings may not be available until the next report gathering.
