# Agent Availability for Queues

Supervisors want to have clear and reliable metrics to assess agent availability and understand how inbound calls are being handled within a queue. These availability metrics gives supervisors that insight in order to make decisions on agent staffing and how to best handle customers waiting in the queue.

!!! tip "App Scope for CX Routing is required"
    To use the agent availability APIs, you must have the `CX Routing` app scope assigned to your application. For instructions on how to add app scopes to your application, please use the [App scopes](https://developers.ringcentral.com/guide/basics/permissions) guide.

## Parameters

The following describe the important parameters, including `path` and `query` parameters, and how to use them:

|Name|Type||Description|
|-|-|-|-|
| `rcxSubAccountId`|Path|**Required**|This is the RingCX sub account ID. Each RingCX Main account can have one or more sub-accounts where queues and agents reside. Usually customers have only one sub account, but may have more for different use cases such as a production one and a test one.|
|`queueId`|Path|**Required**|Each queue has a unique identifier, but to find a queue ID, you first need to get a list of queue groups, find your queue within the queue group and capture the individual queue ID. Each queue must belong to a queue group.|
|`queueType`|Query|**Required**|The queue type can consists of one of two values, `Voice` when it's a voice all or `Digital` when it's an incoming chat interaction. You must choose between these two values as the API will only return one type of interaction at a time.|

## Response Metrics

Below are critical descriptions to understand the following metrics returned in the response of this API:

|Name|Type|Description|
|-|-|-|
|`longestWaitingTimeInSeconds`|Integer|When many customers are in a queue, this metric gives an accurate value for the longest amount of time in seconds that one of those customers has spent in that queue.|
|`numberOfWaitingInteractions`|Integer|When agents are available to interact with customers, this value with be 0. But if all agents are busy interacting with other customers, customers will start to wait in the queue. This value tells you how many customers are waiting in the queue for an available agent.|
|`numberOfAgentsAvailable`|Integer|This is the number of agents available and not currently interacting with customers. This means these agents are ready to handle customers that come into the queue. This value is 0 when agents are busy interacting with customers or dispositioning their interaction.|
|`numberOfAgentsLoggedIn`|Integer|These are the number of agents currently logged in to a queue. This number includes agents that are interacting with customers, dispositioning interactions, or waiting for the next customer to enter the queue.|
|`isQueueOpen`|Boolean|This is dependent on the business hours of your queue. Make sure you have set business hours you expect your queue to be open in your timezone and that you monitor daylight savings time (DST) as well. You can confirm your time zone in the [business hours settings](https://support.ringcentral.com/article-v2/Setting-up-daily-inbound-queue-business-hours-in-RingCX.html?brand=RingCentral&product=RingCX&language=en_US) in the admin console and assure that any business overrides have not been set that close your queue unexpectedly.|