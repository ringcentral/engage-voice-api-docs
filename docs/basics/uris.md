# Methods, Endpoints and Parameters of the RingCX API

This guide explains how RingCX API URLs are structured, which base URLs to use, and how HTTP methods, path parameters, query parameters, request bodies, and headers work across the API.

## Resources and Parameters

RingCX API requests are made to a base URL plus a resource path. Most current public examples should use `https://ringcx.ringcentral.com` as the host.

### Current Host

Use the following base URLs for current RingCX APIs.

| API area | Base URL | Use for |
| --- | --- | --- |
| Current Voice API | `https://ringcx.ringcentral.com/voice/api` | General RingCX Voice API requests. |
| Versioned admin API | `https://ringcx.ringcentral.com/voice/api/v1` | Most admin, routing, dialing, user, and real-time voice resources. |
| CX integration APIs | `https://ringcx.ringcentral.com/voice/api/cx/integration/v1` | CX integration-style endpoints that use RingCentral account and sub-account context. |
| Platform/media APIs | `https://ringcx.ringcentral.com/platform/api` | Platform-level media resources, such as streaming profile configuration. |
| Authentication APIs | See [Authentication](../authentication/index.md) | Token generation, token exchange, refresh, and legacy authentication. |

The base URL depends on the API family. Each API guide and API Reference entry includes the endpoint path for that resource. Use the table above as a map of the common base paths, and follow the specific endpoint shown in the documentation for the API you are calling.

Some older specs and examples may show `https://engage.ringcentral.com` for current API paths. For new public documentation and integrations, use `https://ringcx.ringcentral.com` unless a specific authentication article or endpoint example says otherwise.

### Legacy Host

Legacy RingCX deployments use one of the following hosts:

* `https://portal.vacd.biz/api/`
* `https://portal.virtualacd.biz/api/`

Legacy APIs use `X-Auth-Token` authentication instead of the current bearer-token flow. See [Legacy authentication](../authentication/auth-legacy.md) for details.

## URL Structure

A full API URL follows the same structure as a standard web URL:

```text
<protocol>://<hostname>[:<port>]/<path>[?<query>][#<fragment>]
```

| Name | Description |
| --- | --- |
| `protocol` | The network protocol. RingCX APIs require HTTPS. |
| `hostname` | The server host, such as `ringcx.ringcentral.com`. |
| `port` | The TCP port. For HTTPS, omit the port and use the default port `443`. |
| `path` | The resource path that identifies the API operation. |
| `query` | Optional key-value parameters after `?`, separated by `&`. |
| `fragment` | Optional browser fragment after `#`. RingCX REST APIs do not use fragments. |

For example:

```http
GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}
```

In this URL:

* `https://ringcx.ringcentral.com` is the host.
* `/voice/api/v1` is the versioned Voice API base path.
* `/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}` is the resource path.
* `{accountId}`, `{agentGroupId}`, and `{agentId}` are path parameters.

## Path Parameters

Path parameters are required values embedded in the resource path. They identify the resource being read, changed, or deleted.

For example:

```http
GET /voice/api/v1/admin/accounts/{accountId}/agentGroups/{agentGroupId}/agents/{agentId}
```

| Parameter | Meaning |
| --- | --- |
| `accountId` | The RingCX sub-account that owns the resource. |
| `agentGroupId` | The agent group that contains the agent. |
| `agentId` | The individual agent resource. |

Path parameter values must be URL-safe. If a value contains reserved URL characters, encode it before sending the request.

## Account Identifiers

RingCX APIs use more than one account identifier, depending on the API area.

| Identifier | Where it appears | Meaning |
| --- | --- | --- |
| `accountId` | `/voice/api/v1/admin/accounts/{accountId}/...` | The RingCX sub-account ID. Most versioned admin APIs use this value. |
| `subAccountId` | `/voice/api/cx/integration/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/...` | The RingCX sub-account ID in CX integration APIs. |
| `rcAccountId` | `/voice/api/cx/integration/v1/accounts/{rcAccountId}/...` | The RingCentral account context used by CX integration APIs. |

Use the [Get accounts](../authentication/auth-ringcentral.md#get-accounts) request, or account details returned during authentication, to identify the account IDs available to the authenticated user.

## Query Parameters

Query parameters appear after `?` and are commonly used to filter, page, or otherwise modify a request.

```http
GET /voice/api/v1/admin/accounts/{accountId}/activeCalls/list?product=ACCOUNT&productId={accountId}&maxRows=50
```

In this example:

* `product=ACCOUNT` scopes the request to account-level calls.
* `productId={accountId}` identifies the account product.
* `maxRows=50` limits the number of returned rows.

Always URL-encode query parameter values. For example, spaces should be encoded as `%20` or `+`, depending on the client library and endpoint requirements.

Some endpoints allow repeated query parameters or comma-separated values. Follow the endpoint-specific reference when a parameter accepts multiple values.

## Request Bodies

Request bodies are used mainly with `POST` and `PUT` requests. Unless an endpoint says otherwise, send request bodies as JSON.

```http
POST /voice/api/v1/admin/accounts/{accountId}/activeCalls/createManualAgentCall
Content-Type: application/json
Authorization: Bearer <ringcxAccessToken>
```

Some authentication endpoints use `application/x-www-form-urlencoded` instead of JSON. Follow the request format shown in the endpoint documentation.

## Examples

The examples below omit the host for readability. Add the appropriate base URL from [Current Host](#current-host).

| Task | Example path |
| --- | --- |
| List active calls for a sub-account | `GET /voice/api/v1/admin/accounts/{accountId}/activeCalls/list?product=ACCOUNT&productId={accountId}` |
| Get a transcript segment | `GET /voice/api/cx/integration/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/transcripts/dialogs/{dialogId}/segments/{segmentId}` |
| Create a streaming profile | `POST /platform/api/media/product` |
| Get a user list | `GET /voice/api/v1/admin/users` |

## Methods

RingCX APIs use standard HTTP methods. Not every resource supports every method; check the endpoint-specific documentation before assuming that a related create, read, update, or delete operation exists.

| Method | Description |
| --- | --- |
| `GET` | Retrieves a resource or list of resources. GET requests normally use path and query parameters, not a request body. |
| `POST` | Creates a resource or starts an action. POST requests often include a JSON request body. |
| `PUT` | Updates an existing resource. PUT requests usually include the changed resource fields in the request body. |
| `DELETE` | Deletes or removes a resource identified by the request path. |

### Example

The following request retrieves the accounts available to the authenticated user:

=== "Request"

    ```http
    GET /voice/api/v1/admin/accounts
    Accept: application/json
    Authorization: Bearer <ringcxAccessToken>
    ```

=== "Response"

    ```http
    HTTP/1.1 200 OK
    Content-Type: application/json

    [
      {
        "accountId": "99990001",
        "accountName": "Example Sub-Account",
        "mainAccountId": "99990000"
      }
    ]
    ```

## Object Representation

RingCX APIs generally send and receive JSON objects.

Use these headers when sending JSON:

* `Content-Type: application/json` tells the server that the request body is JSON.
* `Accept: application/json` tells the server that the client expects a JSON response.
* `Authorization: Bearer <ringcxAccessToken>` authenticates current RingCX API calls. See [Authentication](../authentication/index.md) for token details.

The API accepts and returns string values in UTF-8 encoding.

## User Agent Identification

For server-side, desktop, and mobile integrations, include a stable `User-Agent` header with each request. A useful value includes the application name and version, and optionally the platform.

Examples:

* `MyRingCXIntegration/1.0`
* `PostmanRuntime/7.25.0`
* `CustomerSync/2.4 (Linux)`

Browser-based JavaScript applications may not be able to override the browser's default user-agent string.
