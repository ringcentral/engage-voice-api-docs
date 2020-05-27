# Routing Components

<img class="img-fluid" width="100%" src="../images/routing-components.png">

In a contact center, inbound calls are normally routed to a queue and agent based on a set of preconfigured rules and priorities. Routing rules and priorities are set based on agent skills, languages, ranking systems, schedules and a few other components.

-   Inbound Queue Groups are containers for one or more queues.

-   Inbound Queues are nested within the queue groups.

-   Routing Rules determine where inbound calls get routed to.

-   Routing Priorities determine which queue and agent inbound calls are routing to first.

Routing components are comprised of a lot of configuration settings. Creating them via UI interfaces is a time consuming process. The Queues, Routing Rules, Skills and other related APIs provide useful functionalities to fully or partially automate the creation process programmatically.

## Popular Use Cases and Documentation

<div class="card-deck">
  <div class="card" style="width: 18rem;">
    <div class="card-body pt-0 pb-0">
      <h5 class="card-title">Queue Group</h5>
      <h6 class="card-subtitle mb-2 text-muted">Queue Group API</h6>
      <p class="card-text">Use RingCentral Queue Groups to organize queues for incoming calls to route to.</p>
      <ul class="pl-0 ml-4">
      <li><a href="./queues/queue-groups/" class="card-link">Create a Queue Group</a></li>
      </ul>
    </div>
  </div>

  <div class="card" style="width: 18rem;">
    <div class="card-body pt-0 pb-0">
      <h5 class="card-title">Queues</h5>
      <h6 class="card-subtitle mb-2 text-muted">Queues API</h6>
      <p class="card-text">Use RingCentral Queues to route customers to Agents based upon the Agent's experience and priority.</p>
      <ul class="pl-0 ml-4">
      <li><a href="./queues/queues/" class="card-link">Create a Queue</a></li>
      </ul>
    </div>
  </div>

  <div class="card" style="width: 18rem;">
    <div class="card-body pt-0 pb-0">
      <h5 class="card-title">Queue Events</h5>
      <h6 class="card-subtitle mb-2 text-muted">Queue Events API</h6>
      <p class="card-text">Create a specific experience you want each caller to have while waiting for an agent to take their call.</p>
      <ul class="pl-0 ml-4">
      <li><a href="./queues/queue-events/" class="card-link">Create Queue Events</a></li>
      </ul>
    </div>
  </div>
</div>

<div class="card-deck">
  <div class="card" style="width: 18rem;">
    <div class="card-body pt-0 pb-0">
      <h5 class="card-title">Group Skills</h5>
      <h6 class="card-subtitle mb-2 text-muted">Skills API</h6>
      <p class="card-text">The first step in assigning skills to agents. Create a Group Skill so you have skills that can be bound to Agents..</p>
      <ul class="pl-0 ml-4">
      <li><a href="./queues/group-skills/" class="card-link">Create Group Skills</a></li>
      </ul>
    </div>
  </div>
</div>
