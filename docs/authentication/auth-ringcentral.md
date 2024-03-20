# Obtaining a RingCX access token with a RingCentral Login

To access RingCX APIs, you need to create a RingCX App, and then with the client credentials, request a RingCX access token. Once you have created an app, request a RingEX access token and then using a RingCX API to create a RingCX access token. Then the RingCX Access Token can be used to access RingCX APIs.

!!! info "RingCX APIs for RingEX customers are rooted at: https://engage.ringcentral.com/voice/api/"

## Create an app

The first thing we need to do is create an app in the RingCentral Developer Portal. This can be done quickly by clicking the "Create RingCX App" button below. Just click the button, enter a name and description if you choose, and click the "Create" button. If you do not yet have a RingCentral account, you will be prompted to create one.

!!! important
    While you can create a RingCentral account through the Developer Portal, you will need a production account to use RingCX APIs at this time.  Make sure to login to your developer account using the same credentials as your production RingCentral account. The RingCentral account created via the Developer Portal will **not** work.

<a target="new" href="https://developer.ringcentral.com/new-app?name=Engage+Voice+Quick+Start+App&desc=A+simple+app+to+demo+engage+voice+apis+access&public=false&type=ServerOther&carriers=7710,7310,3420&permissions=ReadAccounts&redirectUri=" class="btn btn-primary">Create RingCX App</a>

<div class="expand" id="create-app-instructions">
<ol>
<li><a href="https://developers.ringcentral.com/login.html#/">Login or create an account</a> if you have not done so already.</li>
<li>Go to Console/Apps and click 'Create App' button.</li>
<li>Select the App Type, "REST API App (most common)," then click Next.</li>
<li>Give your app a name and description, then scroll to the "Auth" section.</li>
<li>In the "Auth" section:
  <ul>
  <li>Select 'JWT auth flow' for the authentication method.</li>
  <li>Under "Issue refresh tokens?" make sure the box for 'Yes' is highlighted.</li>
  </ul>
  </li>
<li>In the "Security" section, specify only the following "Application Scopes":
  <ul>
    <li>Read Accounts</li>
  </ul>
</li>
<li>In the same "Security" section, make sure to select:
  <ul>
    <li>This app is <b>private</b> and will only be callable using credentials from the same RingCentral account.</li>
  </ul>
</li>
</ol>
</div>

When you are done, you will be taken to the app's dashboard. Make note of the Client ID. You will use this credential when authenticating your application in upcoming steps.  Next, make sure to have your RingCX account number ready. If you do not have an RingCX account, please reach out to our [Sales](https://www.ringcentral.com/feedback/sales-contact.html) team to sign up for an RingCX account.

## Retrieve RingCentral access token

Now retrieve a RingCentral access token using the following instructions:

[RingCentral Authentication](https://developers.ringcentral.com/guide/authentication)

## Retrieve RingCentral RingCX access token

Once you have a RingCentral Access Token, call the following RingCX API to receive an RingCX Bearer access token.

### Request

```http
POST https://engage.ringcentral.com/api/auth/login/rc/accesstoken
Content-Type: application/x-www-form-urlencoded

rcAccessToken=<rcAccessToken>&rcTokenType=Bearer
```

It's also a good idea to use a refresh token as the access token expires in 5 minutes.

```http
POST https://engage.ringcentral.com/api/auth/login/rc/accesstoken?includeRefresh=true
Content-Type: application/x-www-form-urlencoded

rcAccessToken=<rcAccessToken>&rcTokenType=Bearer
```

Where:

-   **`<rcAccessToken>`** is the RingCentral access token you received from the RingEX authentication flow.

=== "cURL"

    ```bash
    $ curl -XPOST https://engage.ringcentral.com/api/auth/login/rc/accesstoken \
          -d 'rcAccessToken=<rcAccessToken>' \
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

The response will contain the `accessToken` property that can be used in an API call, as well as the `refreshToken` property that can be used to refresh the access token when the access token expires. Make sure to save both the `accessToken` and `refreshToken` for future API calls. Take note of the `accountId` property as that will be used to make future API calls.

The following is an abbreviated response.

```json
{!> code-samples/auth/rc-auth-response.json !}
```

## Example RingCX API Call

The following is an example RingCX API Call using a RingCentral RingCX Access Token.

```http
GET https://engage.ringcentral.com/voice/api/v1/admin/users
Authorization: Bearer <rcRingCXAccessToken>
```

## Get Accounts

Another method to try is to retrieve the accounts this user has access to. The main account is the top level account and is consider a container for the sub-accounts that most operations are performed on.

```http
GET https://engage.ringcentral.com/voice/api/v1/admin/accounts
Authorization: Bearer <rcRingCXAccessToken>
```

Here is an example cURL command:

`curl -X GET https://engage.ringcentral.com/voice/api/v1/admin/accounts -H "Authorization: Bearer {rcRingCXAccessToken}"`

## Refresh RingCentral RingCX Access Token

The RingCentral RingCX Access Token will only live for a few minutes (currently 5 minutes) before needing to be refreshed. If the access token is expired, the API request will respond with:

```http
401 Unauthorized

Jwt is expired
```

Use the `refreshToken` to refresh the RingCentral RingCX access token, by calling the following RingCX API.

### Request

```http
POST https://engage.ringcentral.com/api/auth/token/refresh
Content-Type: application/x-www-form-urlencoded

refresh_token=<rcRingCXRefreshToken>&rcTokenType=Bearer
```

Where:

-   **`<rcRingCXRefreshToken>`** is the RingCentral Refresh Token you received from RingCentral RingCX authentication flow.

### Response

The response will contain the same `accessToken` property that can be used in an API call, but the `refreshToken` property will be a new refresh token that can be used to refresh the access token when the access token expires. Make sure to save the new `refreshToken` for future refresh token API calls.

The following is an abbreviated response.

```json
{!> code-samples/auth/rc-auth-refresh-response.json !}
```
