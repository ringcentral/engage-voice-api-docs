# Introduction to Quality Management

Quality Management takes Workforce Management one step further, giving you the tools to measure and monitor agent performance by looking at the quality of customer interactions. To accomplish this goal, you'll need to collect information about two things: the agent and the call.

## Agent Events

Tracking your agents in real time is important for workforce management, but knowing when an agent is engaged with a customer is equally important. Follow the guide for [Configuring Workforce Management](../../notifications/wfm/configure-wfm.md) and track in real time your agents interaction with customers. When an agent state changes to `ENGAGED`, then they are on a call with a customer.

## Call Events

When a call is ended, a call event is triggered so you can know that a call is ready for processing. Follow the guide for [Configuring Workforce Management](../../notifications/wfm/configure-wfm.md) and make sure to select `End Call Events`. See the details of an [End Call Event](../../notifications/wfm/payload-wfm/#end-call-events) payload that is sent to your endpoint.

## Call Details and Recordings

Sometimes, you may miss an event due to server issues or connection issues.  In these cases, you can reconcile your call events with the [Call Details and Recordings](../../analytics/reports/global-call-type-detail-report/) report. All the call details are available in this historical report including the [single channel call recording](../../analytics/reports/global-call-type-detail-report/#call-recordings).

## Agent Reports

Not all agent performance can be tracked via events. Some details like ring time, hold time, and talk time are all captured and report on after the call. You can find these report details in the [Agent Segment Metadata Report](../../analytics/reports/agent-segment-metadata-report.md). This report also includes the call recording, stored as a `WAV` file and can be retrieved 1-2 minutes after the call ends. To determine when a call ends, use the [Configuring Workforce Management](../../notifications/wfm/configure-wfm.md) to listen for End Call Events.

## Call Recordings

There are two types of [call recordings](../call-recording): single channel (mono) or dual channel (also known as Agent Recordings). These recording links can be sent as events, or retrieved from reports.

!!! important
    This recording is only available for customer accounts that are manually activated. Please work with your RingCentral representative to activate dual channel recordings for the account you wish to gather dual channel call recordings from.
