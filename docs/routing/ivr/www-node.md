# About WWW Node

The WWW node can facilitate communication with external resources using the REST or SOAP protocols. This means you can use the WWW node if you want the IVR to do things like create, retrieve, update, or delete information by communicating with resources outside the platform. To learn more about WWW node, following this link [here](https://support.ringcentral.com/engagevoice/admin/voice-admin-use-www-node.html).

## Example
In this example, we are going to communicate with our RingCentral Office platform. We want to login to the RingCentral Office platform to utilize some of our features from that platform. To login to the RingCentral Office platform, we use the [Password Flow](https://developers.ringcentral.com/guide/authentication/password-flow).

!!! Note
    This example uses password flow from RingCentral Office. This flow is only available to private apps within your own organization.

First, create a node by dragging a WWW node from the dock on to your canvas.

<img class="img-fluid" width="149" src="../../../images/ivr-www-node.png">

In Password Flow, we need to `POST` to the following endpoint in our sandbox:

`https://platform.devtest.ringcentral.com/restapi/oauth/token`

<img class="img-fluid" width="796" src="../../../images/ivr-www-properties-post.png">

For the request body (shown as "Body Content" in the UI), we set the parameters for Password Flow:

`grant_type=password&username=18559100010&extension=101&password=121212`

<img class="img-fluid" width="798" src="../../../images/ivr-www-properties-body.png">

With the following headers:

`Content-Type: application/x-www-form-urlencoded`

`Authorization: Basic {yourEncodedClientIdandClientSecret}`

Where `yourEncodeClientIdandClientSecret` is a Base64 encoded string of your Client ID and Client Secret with a colon (`:`) delimiter in between.

`{clientId}:{clientSecret}`

<img class="img-fluid" width="799" src="../../../images/ivr-www-properties-headers.png">

Click "OK" and you've created your own POST request to authenticate with our RingCentral Office platform. The next step is to receive and process the response. For that, we'll need to use the [Scripting node](../scripting-node) to parse with JavaScript.
