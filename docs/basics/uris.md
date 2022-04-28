# Methods, Endpoints and Parameters of the Engage Voice API

This guide describes the fundamentals of the Engage Voice API and is a useful to developers wishing to understand its conventions and usage guidelines.

## Resources and Parameters

Every entity in the Engage Voice API is represented with a certain resource identified by a specific URI. The structure of a URI is similar to that of a web page's URL. The URI syntax is represented by the following scheme:

`<protocol> :// <hostname> [: <port>] / <path> [? <query>] [# <fragment>]`

| Name | Description |
|------|-------------|
| **protocol** | The networking protocol (http or https protocols are generally used in REST). |
| **hostname** | The server network address information. |
| **port** |  The TCP port where the server listens for incoming requests. If omitted, the default value is used for a given protocol. |
| **path** | A resource identification, typically hierarchical by nature, e.g. foo/bar/baz. |
| **query** | An optional part separated by a question mark (?) and contains additional identification information that is not hierarchical in nature. The query string syntax is organized as a sequence of key-value pairs separated by an ampersand. Not all API resources allow query parameters. |
| **fragment** | An optional part separated from the rest by a hash (`#`) and that contains additional information redirecting to a secondary resource; for example, a section heading of an article identified by the URI. The Engage Voice REST API does not use fragments. |

Protocol, host and port together constitute the main entry point to access the API.

### Protocol
There are two types or networking protocols typically available in REST: HTTP and HTTPS.  Note that for security reasons, connection is allowed using only HTTPS protocol to the default HTTPS port 443, so the port can be omitted in the URI.

### Current Host
Engage Voice is using a new host server, and is accessible on `https://engage.ringcentral.com`.

* Authentication path
  `/api/auth/login`
* API endpoint path
  `/voice/api/v1`
* Platform base url
  `/platform/api`

### Legacy Host
Engage Voice legacy host servers are also still accessible on `https://portal.vacd.biz` and `https://portal.virtualacd.biz`.

* Authentication path
  `/api/auth/login`
* API endpoint path
  `/api/v1`


All of Engage Voice's API resources are organized by either an authentication path or a API endpoint path. All API endpoint paths start with either `/voice/api` or just the legacy method of `/api` followed by the version number of the API you are accessing.  Currently only `/v1` is publicly available. Let's consider a typical API resource URI:

<code>https://engage.ringcentral.com/voice/api/v1/admin/accounts/<strong>15300002</strong>/agentGroups/<strong>2025</strong>/agents/<strong>1369310</strong></code>

Path parameters are commonly used in the Engage Voice's API to identify a particular entity belonging to a given type by its unique key. Most of the API resources represent some objects (i.e. agent) which are owned by a particular Engage Voice account (company) and a subsequent group (i.e. agent group). Three example path parameters are `accountId`, `agentGroupId`, and `agentId`. As you might expect, they identify the account, the group, and the object ID. In this example, the account, agent group, and specific agent, and are bolded in the example above.

!!! info "FYI"
    RingCentral users associate an account with the company main phone number and an extension with the short extension number, but users (agents) are uniquely identified by their account, agent group, and unique agent ID.

### Query Parameters

Another kind of parameter you will come across in the Engage Voice API is a *query parameter*. Query parameters are generally used in object retrieval operations and let the consumer specify the filtering criteria, the desired level of details, etc. Query parameter values in the URL have to be encoded according to [RFC-1738: Uniform Resource Locators](https://tools.ietf.org/html/rfc1738). Query parameters support setting multiple values. It is possible to specify several values for a single query parameter, and filtering results will cover all of them. For example, this functionality is applied to retrieve or remove lists of messages and records.

### Examples

Let's consider the examples below to illustrate the API resources and parameters. For simplicity reasons, we will exclude protocol and host values from the URIs in the examples.

* Get call details for an agent under a specific account (accountId and userId must be predetermined):

    `/{accountId}/users/{userId}/reports/inputControls?accountIds={accountId}&products=CLOUD_PROFILE`

* Get a list of *active* **calls** under a specific account:

    `/api/v1/admin/accounts/{accountId}/activeCalls/list?product=ACCOUNT&productId=12440001`

* Get a list of *active* **agents** under a specific account:

    `/api/v1/admin/accounts/{accountId}/auxStates/?activeOnly=true`

## Methods

In the Engage Voice API, as in any REST API, the resources are accessible by standard HTTP methods: GET, POST, PUT and DELETE. These methods form a uniform CRUD interface expanded as "create, retrieve, update and delete".

| Method | Description |
|--------|-------------|
| `GET` | Retrieves the object represented by the resource that is specified in the request body. It may be the call log information for an extension, the address book with contacts, etc. |
| `POST` | Creates a new object represented by the resource that is specified in the request. In the response body the server sends the representation of the created object, as if there is an immediate `GET` request for it.
| `PUT` | Modifies the already existing object represented by the resource that is specified in the request body. If the object was successfully modified, the server responds with the representation of the changed resource in the response body. The request body may contain only the modified properties of the resource. The response returns the entire resource representation with all of the properties, as in case of the `GET` request. |
| `DELETE` | Removes the object represented by the resource that is specified in the request body. |

### Example

Let's consider a simple example of a `GET` method — retrieving details of the user you are currently logged in as from the Engage Voice REST API.

```http tab="Request"
GET /api/v1/userDetail/self
Accept: application/json
Authorization: Bearer {authToken}
```

```http tab="Response"
HTTP/1.1 200 OK
Content-Type: application/json

{
    "adminId": 2537,
    "rcUserId": 3361292020,
    "rcAccountId": "3058829020",
    "evMainAccountId": null,
    "digitalAccountId": null,
    "digitalAccountApiUrl": null,
    "digitalAccountEmbedUrl": null,
    "agentDetails": [
        {
            "agentId": 1369310,
            "firstName": "John",
            "lastName": "Smith",
            "email": "rc.guest@gmail.com",
            "username": "rc.guest+15300002_1791@gmail.com",
            "agentType": "AGENT",
            "rcUserId": 3361292020,
            "accountId": "15300002",
            "accountName": "RC Platform Internal",
            "agentGroupId": null,
            "externalAgentId": null,
            "location": null,
            "team": null,
            "allowLoginControl": true,
            "allowLoginUpdates": true,
            "password": null,
            "agentRank": null,
            "initLoginBaseState": null,
            "ghostRnaAction": null,
            "enableSoftphone": null,
            "altDefaultLoginDest": null,
            "phoneLoginPin": null,
            "manualOutboundDefaultCallerId": null,
            "directAgentExtension": null,
            "maxChats": null
        }
    ],
    "inboxModeEnabled": false,
    "taskModeEnabled": false,
    "digitalAdminEnabled": false,
    "digitalAnalyticsEnabled": false
}
```

!!! alert "FYI"
    Not all Engage Voice API resources support all of the four methods. In order to find out which resources support a particular method, please refer to the API Reference.

## Object Representation

Whenever you need to send or retrieve a particular piece of data — for example, a call log record, information on an extension, etc. — it will be embedded in the HTTP request or response.

The RingCentral API allows you to explicitly define a representation format by using the following HTTP headers:

* The `Content-Type` header defines the MIME type of the request body. The server will expect the request body to contain data in the specified format.

* The `Accept` header indicates the desired MIME type of the response body. The server will return response data in this format (if possible) and will set the `Content-Type` response header accordingly.

!!! info "FYI"
    The API server accepts and returns all string values in UTF-8 encoding and does not support other character sets. It is not required to explicitly specify charset in Content-Type and Accept HTTP headers. But a client has to implement proper encoding/decoding of character strings passed in HTTP requests/responses.

## User Agent Identification

It is strongly recommended that client applications provide the `User-Agent` HTTP header with every request, which should contain the key information about the requesting application, including application name, version, OS/platform name and version, etc. For browser-based (JavaScript) applications it is usually not possible to override the user agent string which is sent by browser. But other types of applications (desktop, mobile and server-side) can easily follow this recommendation.

There are three primary rules when setting the User Agent:

1. Clients should send the `User-Agent` header and value with each request.
2. A particular application instance should send the exact same user agent string in all API requests.
3. The format of user agent value should follow the convention described below.

We recommend using a short application name and version delimited by forward slash character and optionally followed by additional details about this client instance in parentheses (e.g. operating system name, version, revision number, etc.).

For example:

* `RCMobile/3.6.1 (OfficeAtHand; iOS/6.0; rev.987654)`
* `PostmanRuntime/7.25.0`
* `Softphone/6.2.0.11632`

The `User-Agent` string format is described in <a target="_new" href="https://tools.ietf.org/html/rfc1945">RFC 1945</a> and <a target="_new" href="https://tools.ietf.org/html/rfc2068">RFC 2068</a>.
