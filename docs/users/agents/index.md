# Agents Overview

Managing agents and automatically syncing them with your user management tools can be automated via the API. This article covers the basics of creating, reading, updating deleting Agents.

Of note, Agents must be associated with an Agent Group so you need to have at least one Agent Group configured before managing Agents. See [Agent Groups](./agent-groups) for more.

## Popular Use Cases and Documentation

<div class="card-deck">

  <div class="card" style="width: 18rem;">
    <div class="card-body pt-0 pb-0">
      <h5 class="card-title">Agents</h5>
      <h6 class="card-subtitle mb-2 text-muted">Messaging API</h6>
      <p class="card-text">Use RingCentral to send and receive SMS and MMS.</p>
      <ul class="pl-0 ml-4">
      <li><a href="https://developers.ringcentral.com/guide/messaging/sms/sending-sms" class="card-link">Send an SMS</a></li>
      <li><a href="https://developers.ringcentral.com/guide/messaging/sms/sending-images" class="card-link">Sending MMS</a></li>
      </ul>
    </div>
  </div>

  <div class="card" style="width: 18rem;">
    <div class="card-body pt-0 pb-0">
      <h5 class="card-title">Agent Group</h5>
      <h6 class="card-subtitle mb-2 text-muted">Messaging API</h6>
      <p class="card-text">Use RingCentral to manage the faxes your company sends and receives.</p>
      <ul class="pl-0 ml-4">
      <li><a href="https://developers.ringcentral.com/guide/messaging/fax/sending-faxes" class="card-link">Send a Fax</a></li>
      <li><a href="https://developers.ringcentral.com/guide/messaging/fax/receiving-faxes" class="card-link">Receive a Fax</a></li>
      </ul>
    </div>
  </div>

  <div class="card" style="width: 18rem;">
    <div class="card-body pt-0 pb-0">
      <h5 class="card-title">Making and Controlling Calls</h5>
      <h6 class="card-subtitle mb-2 text-muted">Voice API</h6>
      <p class="card-text">Use RingCentral to enable a "click-to-dial" experience, and to manage calls in progress.</p>
      <ul class="pl-0 ml-4">
      <li><a href="https://developers.ringcentral.com/guide/voice/ringout" class="card-link">RingOut</a></li>
      <li><a href="https://developers.ringcentral.com/guide/voice/call-control" class="card-link">Active Call Control</a></li>
      <li><a href="https://developers.ringcentral.com/guide/voice/call-log/recordings" class="card-link">Call Recordings</a></li>
      </ul>
    </div>
  </div>
</div>

<div class="card-deck">

  <div class="card" style="width: 18rem;">
    <div class="card-body pt-0 pb-0">
      <h5 class="card-title">Authentication</h5>
      <h6 class="card-subtitle mb-2 text-muted">Auth API</h6>
      <p class="card-text">The first step in making any API call is authenticating to the platform.</p>
      <ul class="pl-0 ml-4">
      <li><a href="https://developers.ringcentral.com/guide/authentication/auth-code-flow" class="card-link">OAuth, a.k.a. 3-legged auth</a></li>
      <li><a href="https://developers.ringcentral.com/guide/authentication/password-flow" class="card-link">Password Auth</a></li>
      </ul>
    </div>
  </div>

  <div class="card" style="width: 18rem;">
    <div class="card-body pt-0 pb-0">
      <h5 class="card-title">Subscribe to Notifications</h5>
      <h6 class="card-subtitle mb-2 text-muted">Subscription API</h6>
      <p class="card-text">Receive notifications when events of interest occur within your account to create more responsive applications.</p>
      <ul>
      <li><a href="https://developers.ringcentral.com/guide/notifications/manual/webhooks" class="card-link">Webhooks</a></li>
      <li><a href="https://developers.ringcentral.com/guide/notifications/manual/pubnub" class="card-link">Mobile Push Notifications</a></li>
      </ul>
    </div>
  </div>

</div>
