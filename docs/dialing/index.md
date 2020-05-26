# Dialing Components

Outbound calling activities can be planned and managed effectively using Engage Voice dialing components. They are not only helping a business determine objectives of outbound calls, but also ensure high agent performance, great customer service and deliver quality reports.

<img class="img-fluid" width="70%" src="../../images/dialing-components.png">

-   Dialing groups determine the dialing mode - this is the "How" a call will be made.

-   Campaigns are nested within the dialing groups, and are the reasons for calling - this is the "Why" we are calling.

-   Leads are the contacts, the people or the customers we are dialing - this is the "Who" we are calling.

-   Dispositions allows agents to mark the outcomes of a call - this describes "What" happened on that call.

As you can see dialing components are comprised of several different components that need configuration. To create them via UI interfaces will take a lot of time and navigation. The Campaigns, Leads and other related APIs provide useful functionality to fully or partially automate the creation of outbound dialing components programmatically. This is even more important to automate, when it comes to importing data from other data sources, e.g. importing leads information from your own CRM system.

## Popular Use Cases and Documentation

<div class="card-deck">
  <div class="card" style="width: 18rem;">
    <div class="card-body pt-0 pb-0">
      <h5 class="card-title">Create Dial Groups</h5>
      <h6 class="card-subtitle mb-2 text-muted">Dial Groups API</h6>
      <p class="card-text">Dial groups are configurable groups of (outbound) campaigns that can be differentiated by the type of dialer you are using.</p>
      <ul class="pl-0 ml-4">
      <li><a href="./campaigns/dial-groups" class="card-link">Manage Dial Groups</a></li>
      </ul>
    </div>
  </div>

  <div class="card" style="width: 18rem;">
    <div class="card-body pt-0 pb-0">
      <h5 class="card-title">Create Outbound Campaigns</h5>
      <h6 class="card-subtitle mb-2 text-muted">Campaigns API</h6>
      <p class="card-text">Campaigns are a way to organize and manage the different types of outbound calls leaving your contact center. You can configure campaigns by creating custom agent dispositions, uploading lead, setting schedules for dialing, activating compliance-supporting tools, and more.</p>
      <ul class="pl-0 ml-4">
      <li><a href="./campaigns/campaigns" class="card-link">Manage Campaigns</a></li>
      </ul>
    </div>
  </div>

  <div class="card" style="width: 18rem;">
    <div class="card-body pt-0 pb-0">
      <h5 class="card-title">Bulk Load Leads</h5>
      <h6 class="card-subtitle mb-2 text-muted">Campaign Loader API</h6>
      <p class="card-text">Leads are arranged into a JSON body and uploaded into campaigns for agents to dial on.</p>
      <ul class="pl-0 ml-4">
      <li><a href="./leads/bulk-import" class="card-link">Manage Leads</a></li>
      </ul>
    </div>
  </div>
</div>

<div class="card-deck">
  <div class="card" style="width: 18rem;">
    <div class="card-body pt-0 pb-0">
      <h5 class="card-title">Search Leads</h5>
      <h6 class="card-subtitle mb-2 text-muted">Lead Search API</h6>
      <p class="card-text">Find leads using Primary Search Fields and Extended Search Fields.</p>
      <ul class="pl-0 ml-4">
      <li><a href="./leads/search" class="card-link">Search for Leads</a></li>
      </ul>
    </div>
  </div>
