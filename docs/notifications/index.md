# Introduction to Events and Notifications

There are a couple ways to receive events and notifications from RingCentral RingCX. One way is through Workforce Management integration that sends agent state events as well as call detail and the end of a call event.  Another is through Web Services that can be triggered by inbound queue events or outbound campaign events.


## Introduction to Workforce Management

Workforce management (WFM) is a set of processes that maximizes efficiency in the workplace.  The key to these internal business processes are metrics that support supplying the right number of agents, with the right skills, available at the right time. These real time metrics can be used for forecasting or monitoring of current agents for real time adherence through this API control.

### How do I integrate my workforce management with RingCentral RingCX?

Workforce management integration consists of two steps. Start by specifying the URL you want to send events to using the web interface.  Then read on to learn more about the data being sent to your endpoint.

* [Configure the workforce management integration via the web interface](wfm/configure-wfm.md)
* [Learn more about what is sent in the payload](wfm/payload-wfm.md)

## Introduction to Web Services

Web Services allow you to custom build the action you want to take upon an event. This includes setting your own endpoint, specifying your HTTP method, or passing only the parameters that matter to you.

Once you setup your Web Service, you'll need to trigger the web service from an inbound queue or outbound campaign. This is also known as [setting up webhooks](https://support.ringcentral.com/engagevoice/admin/voice-admin-set-up-webhooks.html).

* [Learn how to setup web services and link them to queues or campaigns](web-service/index.md)
