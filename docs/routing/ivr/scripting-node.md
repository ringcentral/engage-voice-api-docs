# About Scripting Node

The Scripting node allows you to use custom JavaScript to add features to your IVR. Developers will be able to add extra power to their IVR with custom JavaScript. These JavaScript functions can access data from other nodes leading into this Scripting node or process data and store the data for use in other nodes. To learn more about Scripting node, following this link [here](https://support.ringcentral.com/engagevoice/admin/voice-admin-use-scripting-node.html).

## Example
Let's start with our example of using [WWW node](www-node.md). Let's say you use WWW node to authenticate with your RingCentral Office. You will receive a response to the WWW node request and you'll need to parse that response for the RingCentral access token. Using a JavaScript node makes it possible for you to develop a set of JavaScript commands to retrieve the access token.

!!! Note
    This example uses password flow from RingCentral Office. This flow is only available to private apps within your own organization.

Let's create a new node to our workflow by dragging a Scripting node from the dock on to your canvas.

<img class="img-fluid" width="150" src="../../../images/ivr-scripting-node.png">

Then you'll want to take the following code and paste it into your Script Properties

```javascript
var data = ivr.getData('AuthenticateRC');
var authResponseData = JSON.parse(data);
var responseBody = JSON.parse(authResponseData.response_body);
ivr.putData('$rcAccessToken', responseBody.access_token);
var rcAuthorization = responseBody.token_type + ' ' + responseBody.access_token;
ivr.putData('$rcAuthorization', rcAuthorization);
```

Your Script Properties should look like the following.

<img class="img-fluid" width="697" src="../../../images/ivr-scripting-properties.png">

Now let's dissect each of those lines.

When you use the WWW node, the response is stored in a local model object in the IVR. To retrieve this response, we need to reference the previous WWW node by its name, `AuthenticateRC`. Notice the way we do this is by using the method `getData` with the prefix `ivr.`

```javascript
var data = ivr.getData('AuthenticateRC');
```

What we just retrieved is just a string, but specifically, it's a JSON string. We need to convert this string into a JSON object.

```javascript
var authResponseData = JSON.parse(data);
```

This data is all the data including headers, and all we need is the response body so let's extract that out.

```javascript
var responseBody = JSON.parse(authResponseData.response_body);
```

Then we'll take the access token and store that access token in our IVR key/value store. Remember that IVR methods are prefixed wiht `ivr.`, but this time instead of getting the data, we are using `putData` to put the data into the IVR key/value store.

```javascript
ivr.putData('$rcAccessToken', responseBody.access_token);
```

The last step is to construct the authorization header. As we are using [Password Flow](https://developers.ringcentral.com/guide/authentication/password-flow), we'll need to construct an authorization string with the token type `Basic` concatenated with our access token. Then we'll store that string as our Authorization string.

```javascript
var rcAuthorization = responseBody.token_type + ' ' + responseBody.access_token;
ivr.putData('$rcAuthorization', rcAuthorization);
```

Now we are ready to start invoking RingCentral Office APIs with our valid authorization header. Give it a try!
