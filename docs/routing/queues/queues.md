# Queues Basics

Queues are where calls are routed to. Be sure to make your queue active if you want calls to be routed properly, otherwise, callers to that queue will get a disconnected message.

## Core Concepts
### Priority
You can set the priority of a queue up to the highest prioirty of six. The higher the priority, the more calls will be routed to that queue.  Lower priority queues will still get calls though.  If you want to redirect all calls to a queue, leave this field blank and use Priority Group instead.

### Outbound Caller ID
Agents (or third party for any transfer events) will see this caller ID when receiving an inbound call. 

### Manual Outbound Caller ID
When the Agent dials out to a call party, this is the caller ID the call party will see.

### Transfer Override Caller ID
When transfering a call, this caller ID will be shown to the transfer party.  This caller ID will override any manual outbound caller ID.

### Campaign Callback Mapping
If the customer is calling back, as identified by the system, then the call is moved to the selected Outbound Campaign.

### Abandon Campaign Mapping
If the customer in the queue hands up before speaking to an agent, the caller's number will be moved to a specified campaign leave list so they can be called back through the queue.

## Prerequisite
Before using *Queues*, make sure to configure your test Agent (User) with the right priority and permissions.  Your Agent should have a high enough priority so the inbound call is routed to them first.  Also, the permission for the Agent should be "Allow inbound calls" to give the Agent the right to receive inbound calls.

You must first create a Queue Group before creating Queues. Start with a simple [Queue Groups](../queue-groups) and then create your first [Queues](../queues). 