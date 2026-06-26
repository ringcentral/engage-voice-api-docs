# Authentication

RingCX Voice APIs support several authentication methods. For most current RingCX customers, use the RingCentral login flow. The Engage and legacy flows remain available for accounts that were provisioned for those authentication models, but new integrations should use RingCentral authentication whenever possible.

## Which auth method should I use?

| Auth method | Use when | API host | Authorization header |
| --- | --- | --- | --- |
| [RingCX with RingCentral Token](auth-ringcentral.md) | Your RingCX user is linked to RingEX / RingCentral login. This is the default for current integrations. | `https://engage.ringcentral.com/voice/api/` | `Authorization: Bearer <ringcxAccessToken>` |
| [Engage Access Token](auth-engage.md) | Your account does not use a linked RingCentral login and must sign in directly to the Engage platform. | `https://engage.ringcentral.com/voice/api/` | `Authorization: Bearer <engageAccessToken>` |
| [Legacy](auth-legacy.md) | Your deployment uses the legacy portal hosts. | `https://portal.vacd.biz/api/` or `https://portal.virtualacd.biz/api/` | `X-Auth-Token: <authTokenOrApiToken>` |

## Current RingCX API

The current RingCX Voice API is rooted at:

* `https://engage.ringcentral.com/voice/api/`

Current API calls use an OAuth 2.0 bearer-style authorization header:

* `Authorization: Bearer <accessToken>`

For RingCentral-linked accounts, the `accessToken` in this header must be a RingCX access token. Your application first obtains a RingCentral access token, then exchanges it for a RingCX access token before calling RingCX Voice APIs.

Read more about [authorizing with the default RingCentral login flow](auth-ringcentral.md).

If your account does not have a RingCentral login linked to RingCX, read more about [authorizing with a direct Engage login](auth-engage.md).

## Legacy API

The legacy system provides the same voice APIs with different base URLs and a different authorization header.

The base URL is either one of the following depending on your deployment:

* `https://portal.vacd.biz/api/`
* `https://portal.virtualacd.biz/api/`

The authorization header is:

* `X-Auth-Token: <authTokenOrApiToken>`

Read more about [authorizing with the legacy system API](auth-legacy.md).
