# Obtaining a permanent access token using legacy credentials

Use this authentication method only for legacy deployments that use the legacy portal hosts. For current RingCX accounts with RingCentral / RingEX login, use the default [RingCentral token exchange flow](auth-ringcentral.md).

To generate an API token, use your own login or create an "API User" specifically to own the API tokens your integration needs. If multiple integrations require different rights, create separate API users with the correct permissions. If multiple integrations require the same rights, you can create one or more API tokens for the same user and distribute a unique token to each service.

!!! info "What URLs to use when accessing the legacy RingCX API"
    Legacy RingCX APIs are rooted at either:
    
    * `https://portal.vacd.biz/api/`
    * `https://portal.virtualacd.biz/api/`

## Generate an auth token

Get an auth token for the user that will own the API token. This is a temporary login token.

```http
POST https://portal.vacd.biz/api/v1/auth/login
or
POST https://portal.virtualacd.biz/api/v1/auth/login

Content-Type: application/x-www-form-urlencoded

username={email}&password={password}
```

Here is an example using cURL:

```bash
curl -X POST 'https://portal.vacd.biz/api/v1/auth/login' \
  -d 'username={email}' \
  -d 'password={password}'
```

In the result, you will see an `authToken` property. Copy this value for the next step.

The auth token expires after 1 hour. You can use `stayLoggedIn` to extend the auth token to 2 weeks. Anytime an auth token is used in an API request, the auth token expiration is extended by 1 hour or 2 weeks depending on the token type.

## Generate an API token for a user

Generate a permanent API token using the following API call. Every time you run this method, another API token is created and returned.

```http
POST https://portal.vacd.biz/api/v1/admin/token
or
POST https://portal.virtualacd.biz/api/v1/admin/token

X-Auth-Token: {authTokenOrApiToken}
```

Here is an example cURL command:

```bash
curl -X POST 'https://portal.vacd.biz/api/v1/admin/token' \
  -H 'X-Auth-Token: {authTokenOrApiToken}'
```

The token in the `X-Auth-Token` header can be the temporary auth token generated in the previous step or an existing API token for the same user.

The response is an API token that looks similar to:

```text
aws80:c2353445-bc74-af1a-2850-1d55a371c0a9
```

You now have a permanent API token. Use this token in the `X-Auth-Token` header for legacy API calls.

## List all API tokens for a user

To list all existing API tokens for a user:

```http
GET https://portal.vacd.biz/api/v1/admin/token
or
GET https://portal.virtualacd.biz/api/v1/admin/token

X-Auth-Token: {authTokenOrApiToken}
```

## Delete an API token

If you no longer need an API token, or you believe it may have been compromised, delete it.

```http
DELETE https://portal.vacd.biz/api/v1/admin/token/{apiToken}
or
DELETE https://portal.virtualacd.biz/api/v1/admin/token/{apiToken}

X-Auth-Token: {authTokenOrApiToken}
```

Here is an example cURL command:

```bash
curl -X DELETE 'https://portal.vacd.biz/api/v1/admin/token/{apiTokenForDelete}' \
  -H 'X-Auth-Token: {authTokenOrApiToken}'
```

In the request above, you may use the auth token or API token for the user whose token is being deleted, including the token being deleted itself. A parent user token may also be used when it has permission to manage the user's API tokens.

## Get users

Test your auth token or API token using the request below.

```http
GET https://portal.vacd.biz/api/v1/admin/users
or
GET https://portal.virtualacd.biz/api/v1/admin/users

X-Auth-Token: {authTokenOrApiToken}
```

Here is an example cURL command:

```bash
curl -X GET 'https://portal.vacd.biz/api/v1/admin/users' \
  -H 'X-Auth-Token: {authTokenOrApiToken}'
```
