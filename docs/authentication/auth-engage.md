# Obtaining a RingCX access token without a RingEX Login

To access RingCX APIs without a corresponding RingEX account, you can directly login to the RingCX platform by specifying the platform you reside on.

!!! hint "All new accounts start with RingEX"
    For accounts with single-sign-on to RingEX, the method to [exchange access tokens](auth-ringcentral.md#retrieve-ringcentral-access-token) is the default.

!!! alert "If you do not know which platform your account resides on, please contact your Customer Success Manager (CSM) and ask for your Platform ID."

## Generate an RingCX Access Token

The first step to login to RingCX without a RingEX login is to provide your `username`, `password` and `platformId`.

### Request
```http
POST https://ringcx.ringcentral.com/api/auth/login/admin?username={email}&password={password}&platformId={platform ID}
```

Here is an example using cURL:

`curl -X POST 'https://ringcx.ringcentral.com/api/auth/login/admin?username={email}&password={password}&platformId={platform ID}'`

In the response, you will see a very long string for an `accessToken`. You'll want to copy and save this for your next call.  You will also see a shorter string for a `refreshToken`. Save this token as well to [refresh your access token](#refresh-ringcentral-engage-access-token) when the access token expires.

## Generate a Permanent API Token

In specific instances, a permanent API token is desired (for example, calling an API from the IVR). You can create permanent API tokens for this instance. Every time you run the method below, a new API token will be created and returned. You can also [retrieve a list](#list-all-personal-api-tokens) of permanent API tokens to see which tokens are still working.

### Request
```http
POST https://ringcx.ringcentral.com/voice/api/v1/admin/token

Authorization: Bearer {accessToken}
```

Here is an example using cURL:

`curl -X POST https://ringcx.ringcentral.com/voice/api/v1/admin/token -H "Authorization: Bearer <accessToken>"`

The response will be an API token that looks something like:

`aws80:c2353445-bc74-af1a-2850-1d55a371c0a9`

## List all Personal API Tokens

As you create new API tokens, those permanent API tokens will persist and you can see a list of your personal API tokens using the following command.

### Request
```http
GET https://ringcx.ringcentral.com/voice/api/v1/admin/token

X-Auth-Token: {apiToken}
or
Authorization: Bearer <accessToken>
```

Here is an example using cURL:

`curl -X GET https://ringcx.ringcentral.com/voice/api/v1/admin/token -H "X-Auth-Token: {apiToken}"`

The `apiToken` in the `X-Auth-Token` header can be a token generated using the user credentials in the [step above](#generate-a-permanent-api-token) or an existing API token for the user, or even a new access token from just logging in.

The response will be an API token list that looks something like:

### JSON

```json
{
  "aws80:c2353445-bc74-af1a-2850-1d55a371c0a9",
  "aws80:dab26445-53ca-12c2-0185-4c33b642a023"
}
```

## Delete an API Token

If you are done with an API Token and no longer need it, or you feel it may have been compromised, you can delete an existing token as follows.

=== "X-Auth-Token"

    ```http
    DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/token/{apiToken}

    X-Auth-Token: {apiToken}
    ```

=== "Authorization header"

    ```http
    DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/token/{apiToken}

    Authorization: Bearer <accessToken>
    ```


Here is an example cURL command:

`curl -X DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/token/{API-TOKEN-FOR-DELETE} -H "X-Auth-Token: {apiToken}"`

## Get Accounts

A method to try is to retrieve the accounts this user has access to. The main account is the top level account and is considered a container for the sub-accounts that most operations are performed on.

```http
GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts
Authorization: Bearer <accessToken>
```

Here is an example cURL command:

`curl -X GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts -H "Authorization: Bearer {accessToken}"`
