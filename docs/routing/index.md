# Introduction to Routing APIs
<img class="img-fluid" width="100%" src="../../images/routing-components.png">

In a contact center, inbound calls are normally routed to a queue and agent based on a set of preconfigured rules and priorities. Routing rules and priorities are set based on agent skills, languages, ranking systems, schedules and a few other components.

-   Inbound Queue Groups are containers for one or more queues.

-   Inbound Queues are nested within the queue groups.

-   Routing Rules determine where inbound calls get routed to. One way to preconfigure rules is creating IVRs.

-   Routing Priorities determine which queue and agent inbound calls are routing to first.

Routing components are comprised of lots of configurations. To create them via UI interfaces usually a time consuming process. The Queues, Routing Rules and other related APIs provide useful functionalities to fully or partially automate the creation process programmatically.

## Popular Use Cases and Documentation

<div class="card-deck">
  <div class="card" style="width: 18rem;">
    <div class="card-body pt-0 pb-0">
      <h5 class="card-title">Queue Groups and Queues</h5>
      <p class="card-text">Use Engage Voice Queues APIs to manage Queue groups and Queues.</p>
      <ul class="pl-0 ml-4">
      <li><a href="./queues/" class="card-link">Manage Queues</a></li>
      </ul>
    </div>
  </div>
</div>
