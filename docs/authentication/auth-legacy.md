# Obtaining a Permanent Access Token using Legacy Credentials

To generate the API token, you would either use your own login, or create an "API User" specifically to host the API tokens you need to call into our system. If you needed to integrate multiple services and each service needed a different level of permissions, you could create multiple API users, each with different Rights. If you had multiple services and they each required the same rights, you could create one or more API tokens for the same user and distribute a unique token around to each service (best practice).

> Note: RingCX APIs for MVP customers are rooted at either:
>
> * `https://portal.vacd.biz/api/`
> * `https://portal.virtualacd.biz/api/`

## Generating an Auth Token

Get AuthToken for the user you would like to generate API token for (one time operation)

```http
POST https://portal.vacd.biz/api/v1/auth/login
or
POST https://portal.virtualacd.biz/api/v1/auth/login

Content-Type: application/x-www-form-urlencoded

username={email}&password={password}
```

Here is an example using cURL:

`curl -X POST https://portal.vacd.biz/api/v1/auth/login -d "username={email}&password={password}"`

In the result, you will see an authToken property. This is what you will use to manually generate the API tokens in the next step. You want to copy this, it will look something like:

`baf522ee-5d42-457a-a18d-7b8500eeb573`

The AuthToken will expire after 1 hour. By using `stayLoggedIn`, you can extend the AuthToken to last 2 weeks. However, anytime an AuthToken is used in an API request, the AuthToken is automatically extended by 1 hour or 2 weeks depending on which AuthToken type you are using.

## Generate an API Token for a user

Generate a permanent API token using the following API call. Every time you run the method below, another API token will be created and returned.

```http
POST https://portal.vacd.biz/api/v1/admin/token
or
POST https://portal.virtualacd.biz/api/v1/admin/token

X-Auth-Token: {authTokenOrApiToken}
```

Here is an example cURL command:

`curl -X POST https://portal.vacd.biz/api/v1/admin/token -H "X-Auth-Token: {token}"`

The token in the `X-Auth-Token` header can be a token generated using the user credentials in the step above or an existing API token for the user.

The response will be an API token that looks something like:

`aws80:c2353445-bc74-af1a-2850-1d55a371c0a9`

You now have your permanent API token(s). The value returned from each of the POST requests above will be permanent and look very much like the authToken from Step 1.

If you lose track, you can always retrieve all of the permanent API tokens for a user by calling the following method with one of the API Tokens you know about, or by logging in with the user who's tokens you're interested in, and pulling the authToken from that user (as in Step 1). In other words, the temporary authToken is 100% interchangeable with the permanent API tokens for the same user.

## List all API Tokens for a user

To list all existing API Tokens for a user:

```http
GET https://portal.vacd.biz/api/v1/admin/token
or
GET https://portal.virtualacd.biz/api/v1/admin/token

X-Auth-Token: {authTokenOrApiToken}
```

## Delete an API Token

If you are done with an API Token and no longer need it, or you feel it may have been compromised, you can delete an existing token as follows.

```http
DELETE https://portal.vacd.biz/api/v1/admin/token/{apiToken}
or
DELETE https://portal.virtualacd.biz/api/v1/admin/token/{apiToken}

X-Auth-Token: {authTokenOrApiToken}
```
Here is an example cURL command:

`curl -X DELETE https://portal.vacd.biz/api/v1/admin/token/{API-TOKEN-FOR-DELETE} -H "X-Auth-Token: {authTokenOrApiToken}"`

In the above request, you may use the auth token or API token in the `X-Auth-Token` header for the user who's token is getting deleted (including the token for delete itself), or that of any parent user of the user who owns the API token for delete.

## Get Users

Now test your auth token or API token using the below request to get a list of users:

```http
GET https://portal.vacd.biz/api/v1/admin/users
or
GET https://portal.virtualacd.biz/api/v1/admin/users

X-Auth-Token: {authTokenOrApiToken}
```

Here is an example cURL command:

`curl -X GET https://portal.vacd.biz/api/v1/admin/users -H "X-Auth-Token: {authTokenOrApiToken}"`
