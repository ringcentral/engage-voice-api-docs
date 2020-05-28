no_breadcrumb: true
# RingCentral Engage Voice Developer Guide
<img class="img-fluid" width="100%" src="../../images/users-components.png">

<div class="jumbotron pt-1">
  <h3 class="display-5">Let's Get Started!</h3>
  <p class="lead">New to the Engage Voice Platform? Let us help you build your first Engage Voice application in minutes using one of our Quick Start Guides.</p>
  <hr class="my-4">
  <p>The following Quick Start Guides have been created to assist developers in getting started in each of our major APIs:</p>
  <ul>
    <li><a href="./dialing/leads/bulk-import/">Bulk Import and Sync Leads</a> using our <strong>Leads API</strong>.</li>
    <li><a href="./dialing/active-calls/">Get a List of Active Calls</a> using our <strong>Active Calls API</strong>.</li>
    <li><a href="./analytics/reports/global-call-type-detail-report">Download Call Details and Recordings</a> using our <strong>Reports API</strong>.</li>
    <li><a href="./analytics/reports/agent-session-report">Download Agent Session Info</a> using our <strong>Reports API</strong>.</li>
  </ul>
  <!--<p>Not a programmer? <a href="./basics/explorer/">Try out the API with no programming</a>.</p>-->
  <hr class="my-4">
  <p>If you are a customer, get started as you already have access via your account.</p>

  <p>If you are a partner, fill out the following form to sign up for accesss.</p>

  <p><a class="btn btn-primary" href="https://docs.google.com/forms/d/1f4fxmM2maXyXtKbhDWd5ZQDAdYOzcEQUVytU96bUa-c">Partner Signup &raquo;</a></p>
</div>

Welcome RingCentral Engage Voice Developer! Here you have access to all the resources necessary to build an app successfully on the RingCentral Engage Voice Platform. Here are some specific resources and guides to help you get started.

## Inbound, Outbound, and Agents

There are three key elements to Engage Voice; Agents, who are your customer service representatives, Inbound Queues (Routing), where callers are routed to your Agents, and Outbound Campaigns, where your Agents dial out to contacts.

<div class="card-deck">

  <div class="card" style="width: 18rem;">
    <div class="card-body pt-0 pb-0">
      <h5 class="card-title">Agents</h5>
      <h6 class="card-subtitle mb-2 text-muted">Agents API</h6>
      <p class="card-text">Create and configure an agent account. Make sure to create Agent Groups first</p>
      <ul class="pl-0 ml-4">
      <li><a href="./agent-groups/" class="card-link">Create a New Agent Group</a></li>
      <li><a href="./agents/" class="card-link">Create a New Agent</a></li>
      </ul>
    </div>
  </div>

  <div class="card" style="width: 18rem;">
    <div class="card-body pt-0 pb-0">
      <h5 class="card-title">Inbound Queues</h5>
      <h6 class="card-subtitle mb-2 text-muted">Queues API</h6>
      <p class="card-text">Use RingCentral Queues to route customers to Agents based upon the Agent's experience and priority. Make sure to create Queue Groups first.</p>
      <ul class="pl-0 ml-4">
      <li><a href="./queues/queue-groups/" class="card-link">Create a Queue Group</a></li>
      <li><a href="./queues/queues/" class="card-link">Create a Queue</a></li>
      </ul>
    </div>
  </div>

  <div class="card" style="width: 18rem;">
    <div class="card-body pt-0 pb-0">
      <h5 class="card-title">Outbound Campaigns</h5>
      <h6 class="card-subtitle mb-2 text-muted">Campaigns API</h6>
      <p class="card-text">Campaigns are a way to organize and manage the different types of outbound calls leaving your contact center. Create Dial Groups first to collect  and group your campaigns.</p>
      <ul class="pl-0 ml-4">
      <li><a href="./campaigns/dial-groups" class="card-link">Create Dial Groups</a></li>
      <li><a href="./campaigns/campaigns" class="card-link">Create Campaigns</a></li>
      </ul>
    </div>
  </div>
</div>

## Managing Lead Lists

Leads are typically classified as contacts who have expressed some kind of interest in your company. For our purposes, we refer to your outbound contacts in general — whether they’re end-users or existing or prospective customers — as leads.

Leads are arranged into lead lists and uploaded into campaigns for agents to dial on. Typically, loading and managing lead lists becomes more efficient as an automated processes. Use the [Leads API](./dialing/leads) to bulk import leads and search leads.

## Getting Started with Engage Voice Embeddable

Want to embed the power of Engage Voice into your own webpage?

<a class="btn btn-primary" href="./embeddable/get-started">Learn more about Engage Embeddable &raquo;</a>

## Additional Resources


<div class="card-deck">
  <div class="card">
    <div class="card-body">
      <h5 class="h5 card-title">Engage Voice API Reference</h5>
      <p class="card-text">Consult our exhaustive API Reference Guide, and make API calls using ZERO CODE.</p>
      <a href="https://developers.ringcentral.com/engage/voice/api-reference" class="btn btn-primary">Learn more</a>
    </div>
  </div>
  <div class="card">
    <div class="card-body">
      <h5 class="h5 card-title">SDKs</h5>
      <p class="card-text">We offer development libraries in a number of languages (Python, PHP, Javascript and more) to made building apps easier.</p>
      <a href="./sdks" class="btn btn-primary">Learn more</a>
    </div>
  </div>
  <div class="card">
    <div class="card-body">
      <h5 class="h5 card-title">Engage Voice Docs</h5>
      <p class="card-text">Want to learn more about Engage Voice? Our UI documentation library is full of easily searchable details.</p>
      <a href="https://docs.ringcentral.com/engage/" class="btn btn-primary">Learn more</a>
    </div>
  </div>
</div>

## About RingCentral

RingCentral is a leading provider of global enterprise cloud communications and collaboration solutions. More flexible and cost-effective than legacy on-premises systems, RingCentral empowers modern mobile and distributed workforces to communicate, collaborate, and connect from any location, on any device and via any mode. RingCentral provides unified voice, video, team messaging and collaboration, conferencing, online meetings, digital customer engagement and integrated contact center solutions for enterprises globally. RingCentral’s open platform integrates with leading business apps and enables customers to easily customize business workflows.
