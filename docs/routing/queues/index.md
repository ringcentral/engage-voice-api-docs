# Queues Overview

Queues are a component of Inbound calls. Queues consist of Queue groups containing a list of queues. Inbound calls are routed to a **Queue** and **Agent** based upon a set of preconfigured rules and priorities. These can be based on:

* skill
* language
* ranking system
* schedules
* etc.

Primary inbound routing components consist of the Inbound Queue Groups and the Inbound Queues which are nested within the Queue Groups.

Beyond that, there are routing rules which can be configured by IVRs. And then routing priorities determine where a call will route to first.

## Prerequiste
Before using *Queues*, make sure to configure your test Agent (User) with the right priority and permissions.  Your Agent should have a high enough priority so the inbound call is routed to them first.  Also, the permission for the Agent should be "Allow inbound calls" to give the Agent the right to receive inbound calls.

## Getting Started
You must first create a Queue Group before creating Queues. Start with a simple [Queue Groups](../queue-groups) and then create your first [Queues](../queues). 

## Popular Use Cases and Documentation

<div class="card-deck">

  <div class="card" style="width: 18rem;">
    <div class="card-body pt-0 pb-0">
      <h5 class="card-title">Queue Group</h5>
      <h6 class="card-subtitle mb-2 text-muted">Queue Group API</h6>
      <p class="card-text">Use RingCentral Queue Groups to organize queues for incoming calls to route to.</p>
      <ul class="pl-0 ml-4">
      <li><a href="./queue-groups/" class="card-link">Create a Queue Group</a></li>
      </ul>
    </div>
  </div>
  
  <div class="card" style="width: 18rem;">
    <div class="card-body pt-0 pb-0">
      <h5 class="card-title">Queues</h5>
      <h6 class="card-subtitle mb-2 text-muted">Queues API</h6>
      <p class="card-text">Use RingCentral Queues to route customers to Agents based upon the Agent's experience and priority.</p>
      <ul class="pl-0 ml-4">
      <li><a href="./queues/" class="card-link">Create a Queue</a></li>
      </ul>
    </div>
  </div>
</div>