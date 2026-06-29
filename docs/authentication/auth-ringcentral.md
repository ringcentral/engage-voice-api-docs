# Obtaining a RingCX access token with a RingCentral Login

This is the default authentication flow for current RingCX Voice API integrations. It applies when the RingCX user signs in with a linked RingCentral / RingEX login.

The flow has two steps:

1. Obtain a RingCentral access token from the RingCentral platform.
2. Exchange that RingCentral access token for a RingCX access token.

Use the RingCX access token, not the original RingCentral access token, when you call RingCX Voice APIs.

!!! info "RingCX Voice APIs are rooted at: https://engage.ringcentral.com/voice/api/"

## Create an app

Create an app in the RingCentral Developer Portal. You can use the "Create RingCX App" button below, enter a name and description if needed, and click "Create". If you do not have a RingCentral account, you will be prompted to create one.

!!! important
    You need a production RingCentral account that is linked to your RingCX account. A RingCentral account created only in the Developer Portal will not provide access to production RingCX Voice APIs.

<a target="new" href="https://developer.ringcentral.com/new-app?name=Engage+Voice+Quick+Start+App&desc=A+simple+app+to+demo+engage+voice+apis+access&public=false&type=ServerOther&carriers=7710,7310,3420&permissions=ReadAccounts&redirectUri=" class="btn btn-primary">Create RingCX App</a>

<div class="expand" id="create-app-instructions">
<ol>
<li><a href="https://developers.ringcentral.com/login.html#/">Log in or create an account</a> if you have not done so already.</li>
<li>Go to Console/Apps and click the "Create App" button.</li>
<li>Select the app type, "REST API App (most common)," then click Next.</li>
<li>Give your app a name and description, then scroll to the "Auth" section.</li>
<li>In the "Auth" section:
  <ul>
  <li>Select "JWT auth flow" for the authentication method.</li>
  <li>Under "Issue refresh tokens?", make sure "Yes" is selected.</li>
  </ul>
  </li>
<li>In the "Security" section, specify the following application scope:
  <ul>
    <li>Read Accounts</li>
  </ul>
</li>
<li>In the same "Security" section, make sure the app is private and can only be called using credentials from the same RingCentral account.</li>
</ol>
</div>

When you are done, you will be taken to the app's dashboard. Save the Client ID and Client Secret. You will use them to authenticate with RingCentral in the next step.

## Retrieve a RingCentral access token

Use the RingCentral authentication flow configured for your app to retrieve a RingCentral access token. For server-side RingCX integrations, JWT auth is the recommended RingCentral auth flow.

See the [RingCentral authentication guide](https://developers.ringcentral.com/guide/authentication) for the current RingCentral OAuth instructions.

The RingCentral access token proves the RingCentral user/app identity. It is not the token you send to RingCX Voice API endpoints. After you retrieve it, exchange it for a RingCX access token.

## Retrieve a RingCX access token

Call the RingCX token exchange endpoint with the RingCentral access token.

The token exchange and refresh endpoints are authentication endpoints. The examples below use the Engage auth host. After you have a RingCX access token, use the RingCX Voice API host for API calls.

### Request

```http
POST https://engage.ringcentral.com/api/auth/login/rc/accesstoken?includeRefresh=true
Content-Type: application/x-www-form-urlencoded

rcAccessToken=<ringCentralAccessToken>&rcTokenType=Bearer
```

Where:

* **`<ringCentralAccessToken>`** is the RingCentral access token returned by the RingCentral authentication flow.
* **`rcTokenType`** must be `Bearer`.
* **`includeRefresh=true`** includes a RingCX `refreshToken` in the response.

=== "cURL"

    ```bash
    curl -X POST 'https://engage.ringcentral.com/api/auth/login/rc/accesstoken?includeRefresh=true' \
      -H 'Content-Type: application/x-www-form-urlencoded' \
      -d 'rcAccessToken=<ringCentralAccessToken>' \
      -d 'rcTokenType=Bearer'
    ```
    
=== "Go"

    ```go
    {!> code-samples/auth/rc-auth.go !}
    ```

=== "Javascript"

    ```javascript
    {!> code-samples/auth/rc-auth.js !}
    ```

=== "Python"

    ```python 
    {!> code-samples/auth/rc-auth.py !}
    ```

=== "PHP"

    ```php
    {!> code-samples/auth/rc-auth.php !}
    ```

### Response

The response contains the RingCX `accessToken` that you use for RingCX Voice API calls. If you include `includeRefresh=true`, the response also contains a `refreshToken` that can be used to obtain a new RingCX access token.

Save the following values:

* **`accessToken`**: The RingCX bearer token for API requests.
* **`refreshToken`**: The RingCX refresh token, returned when `includeRefresh=true`.
* **`mainAccountId`** and account IDs in `agentDetails`: Useful when choosing the account or sub-account for API calls.

The following is an abbreviated response.

```json
{!> code-samples/auth/rc-auth-response.json !}
```

## Token lifetime and rate limits

RingCX access tokens expire after 5 minutes. The token exchange endpoint is limited to 5 requests per minute.

Do not request a new RingCX access token before every API call. Cache and reuse the token until it is close to expiration, then obtain a new token. If your application has multiple workers or servers, coordinate token renewal so they do not all try to re-authenticate at the same time.

RingCX does not automatically refresh the token for you. If an API call returns `401 Unauthorized` because the token expired, your application must obtain a new valid RingCX token before retrying the request.

## Example RingCX API call

Use the RingCX access token in the `Authorization` header.

```http
GET https://engage.ringcentral.com/voice/api/v1/admin/users
Authorization: Bearer <ringcxAccessToken>
```

## Get accounts

You can retrieve the RingCX accounts available to the authenticated user. This request uses the RingCX access token returned by the token exchange.

```http
GET https://engage.ringcentral.com/voice/api/v1/admin/accounts
Authorization: Bearer <ringcxAccessToken>
```

Here is an example cURL command:

```bash
curl -X GET 'https://engage.ringcentral.com/voice/api/v1/admin/accounts' \
  -H 'Authorization: Bearer <ringcxAccessToken>'
```

The response includes the RingCX account IDs you need for RingCX Voice API requests:

* **`accountId`** is the RingCX sub-account ID. Most operational API calls are performed against a sub-account.
* **`mainAccountId`** is the RingCX main account ID. The main account is the top-level account.

Some RingCX APIs also require the RingCentral account UID. To retrieve that value, call the RingCentral account endpoint with the RingCentral/RingEX access token from [Retrieve a RingCentral access token](#retrieve-a-ringcentral-access-token).

```http
GET https://platform.ringcentral.com/restapi/v1.0/account/~
Authorization: Bearer <ringCentralAccessToken>
```

In that response, the `id` value is the RingCentral account UID. Use the RingCentral/RingEX access token for this request, not the RingCX access token.

## Refresh a RingCX access token

If you requested a refresh token with `includeRefresh=true`, call the refresh endpoint to obtain a new RingCX access token.

### Request

```http
POST https://engage.ringcentral.com/api/auth/token/refresh
Content-Type: application/x-www-form-urlencoded

refresh_token=<ringcxRefreshToken>
```

Where:

* **`<ringcxRefreshToken>`** is the RingCX refresh token returned by the token exchange or previous refresh response.

### Response

The response contains a new `accessToken` and a new `refreshToken`. Save the new refresh token for the next refresh request.

The following is an abbreviated response.

```json
{!> code-samples/auth/rc-auth-refresh-response.json !}
```

If you did not request or store a refresh token, repeat the RingCentral-token-to-RingCX-token exchange with a valid RingCentral access token.

If the RingCX access token is expired, API requests may return:

```http
401 Unauthorized

Jwt is expired
```
