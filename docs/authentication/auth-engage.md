# Obtaining an Engage access token without a RingCentral login

Use this authentication method only when your RingCX account is not linked to a RingCentral / RingEX login and you must sign in directly to the Engage platform.

!!! important "Use RingCentral authentication when available"
    For accounts with single sign-on to RingEX, use the default [RingCentral token exchange flow](auth-ringcentral.md). New integrations should use that flow whenever possible.

!!! note "If you do not know which platform your account resides on, contact your Customer Success Manager (CSM) and ask for your Platform ID."

## Generate an Engage access token

To sign in directly to Engage, provide your `username`, `password`, and `platformId`.

### Request

```http
POST https://engage.ringcentral.com/api/auth/login/admin?username={email}&password={password}&platformId={platformId}
```

Here is an example using cURL:

```bash
curl -X POST 'https://engage.ringcentral.com/api/auth/login/admin?username={email}&password={password}&platformId={platformId}'
```

The response contains an `accessToken` and a `refreshToken`. Use the `accessToken` for RingCX Voice API calls. Save the `refreshToken` so you can refresh the access token when it expires.

## Token lifetime and renewal

Engage access tokens used with the current RingCX Voice API expire after 5 minutes. RingCX does not automatically refresh the token for you.

Cache and reuse the access token until it is close to expiration. If an API call returns `401 Unauthorized` because the token expired, refresh the token before retrying the request.

### Refresh an Engage access token

```http
POST https://engage.ringcentral.com/api/auth/token/refresh
Content-Type: application/x-www-form-urlencoded

refresh_token=<engageRefreshToken>
```

The response contains a new `accessToken` and a new `refreshToken`. Save the new refresh token for the next refresh request.

## Generate a permanent API token

In specific cases, a permanent API token is useful, such as calling an API from an IVR flow. Every time you run the method below, a new API token is created and returned. You can also [retrieve a list](#list-all-personal-api-tokens) of permanent API tokens to see which tokens are still available.

### Request

```http
POST https://engage.ringcentral.com/voice/api/v1/admin/token

Authorization: Bearer {accessToken}
```

Here is an example using cURL:

```bash
curl -X POST 'https://engage.ringcentral.com/voice/api/v1/admin/token' \
  -H 'Authorization: Bearer <accessToken>'
```

The response is an API token that looks similar to:

```text
aws80:c2353445-bc74-af1a-2850-1d55a371c0a9
```

## List all personal API tokens

As you create new API tokens, those permanent API tokens persist. You can retrieve the list of personal API tokens using the following request.

### Request

```http
GET https://engage.ringcentral.com/voice/api/v1/admin/token

X-Auth-Token: {apiToken}
or
Authorization: Bearer <accessToken>
```

Here is an example using cURL:

```bash
curl -X GET 'https://engage.ringcentral.com/voice/api/v1/admin/token' \
  -H 'X-Auth-Token: {apiToken}'
```

You can authenticate this request with `X-Auth-Token` using a generated API token, or with `Authorization: Bearer <accessToken>` using a current Engage access token.

The response is an API token list that looks similar to:

```json
[
  "aws80:c2353445-bc74-af1a-2850-1d55a371c0a9",
  "aws80:dab26445-53ca-12c2-0185-4c33b642a023"
]
```

## Delete an API token

If you no longer need an API token, or you believe it may have been compromised, delete it.

=== "X-Auth-Token"

    ```http
    DELETE https://engage.ringcentral.com/voice/api/v1/admin/token/{apiToken}

    X-Auth-Token: {apiToken}
    ```

=== "Authorization header"

    ```http
    DELETE https://engage.ringcentral.com/voice/api/v1/admin/token/{apiToken}

    Authorization: Bearer <accessToken>
    ```

Here is an example cURL command:

```bash
curl -X DELETE 'https://engage.ringcentral.com/voice/api/v1/admin/token/{apiTokenForDelete}' \
  -H 'X-Auth-Token: {apiToken}'
```

## Get accounts

You can retrieve the accounts available to the authenticated user. The main account is the top-level account. Most operational API calls are performed against a sub-account.

```http
GET https://engage.ringcentral.com/voice/api/v1/admin/accounts
Authorization: Bearer <accessToken>
```

Here is an example cURL command:

```bash
curl -X GET 'https://engage.ringcentral.com/voice/api/v1/admin/accounts' \
  -H 'Authorization: Bearer {accessToken}'
```
