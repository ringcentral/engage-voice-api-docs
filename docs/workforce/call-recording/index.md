# Introduction to Call Recordings

Call recordings can be retrieved as single channel (mono) recordings or as dual channel (stereo) recordings, also known as [Agent Recordings](https://support.ringcentral.com/engagevoice/admin/voice-admin-set-up-agent-recording.html).  

### Single Channel Recordings (Mono)

Call recordings are the audio files of the call. You can retrieve single channel (mono) call recordings using the [End Call Event](../../notifications/wfm/payload-wfm/#end-call-events). If you miss the event or wish to just manually retrieve the call details, you can also use the [Global Call Type Detail](../../analytics/reports/global-call-type-detail-report#call-recordings) report.

If a call is answered and recorded, a call recording link will appear in the event, or as part of the report, under `recording_url`. Use this link to retrieve the call recording.

=== "Single Channel Recording"
    ```html
      https://c02-recordings.virtualacd.biz/api/v1/calls/recordings/?v=1&accountId=15300002&bucket=c02-recordings&region=us-east-1&compliance=false&file=15300002/202007/30/202007302136360132130000036446-1.WAV
    ```

!!! important
    While the recording URL is sent 1-3 seconds after a call is ended, the actual recording takes more time to encode. Depending on the length of the recording, the recording link may not be valid for up to 1-2 minutes after the end call event.


### Agent Recordings (Stereo, Dual Channel)

Dual channel (stereo) agent recordings can also be retrieved from the [Agent Segment Metadata Report](../../analytics/reports/agent-segment-metadata-report.md). You can find the agent recording from the `Segment Recording URL` field in the downloaded report.  Note that the agent recording is a `perspective` type recording and must be set manually.

#### Agent Recording (Dual Channel)
    ```html
      https://aws46-recordings.vacd.biz/api/v1/calls/recordings?v=1&accountId=15300002&bucket=aws46-recordings&region=us-west-2&compliance=true&file=perspective/15300002/202008/05/202008051517160139120000000370-session-2-stereo.WAV
    ```

!!! important
    This recording is only available for customer accounts that are manually activated. Please work with your RingCentral representative to activate dual channel recordings for the account you wish to gather dual channel call recordings from.

!!! alert "Please Note"
    This report may take some time to show new records so it's best to periodically retrieve this report and note that the most recent recordings may not be available until the next report gathering.
