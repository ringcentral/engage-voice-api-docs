# Authentication

The RingCentral Engage Voice API is offered for both the current Engage Voice deployment or legacy systems.

## Current API

The current Engage Voice system makes the API accessible at:

* `https://engage.ringcentral.com/voice/api`

and uses the OAuth 2.0 Authorization header:

* `Authorization: Bearer <myAccessToken>`

Read more about [authorizing with the current system API](auth-ringcentral).

## Legacy API

The legacy system provides the same voice APIs with a different base URL and authorization header.

The base URL is either one of the following depending on your deployment:

* `https://portal.vacd.biz/api/`
* `https://portal.virtualacd.biz/api/`

The authorization header is the following:

* `X-Auth-Header: <myApiKey>`

Read more about [authorizing with the legacy system API](auth-legacy).
