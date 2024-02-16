# Using Postman to test RingCX APIs

For easy testing using [Postman](https://www.getpostman.com/), RingCentral provides a Postman 2.0 Collection for RingCX. It is based on the RingCentral RingCX OpenAPI 3.0 Specificaion. While Postman can import an OpenAPI 3.0 Specification directly, RingCentral recommends using the Collection as it provides better authorization handling using Postman variables and environments as recommended by Postman.

The files are available here:

* [Postman 2.0 Collection](https://raw.githubusercontent.com/ringcentral/engage-voice-api-docs/master/specs/engage-voice_postman2.json)
* [OpenAPI 3.0 Specification](https://raw.githubusercontent.com/ringcentral/engage-voice-api-docs/master/specs/engage-voice_openapi3.json)

This document describes how to install and use the Postman 2.0 Collection.

## Pre-Requisites

!!! primary "Note for Legacy Systems"
    Legacy systems [decribed here](authentication/index.md) and Legacy password authentication are not supported with
    this Postman Collection. If you have such a need, please [make a request here](https://github.com/ringcentral/engage-voice-api-docs/issues).

This Postman spec is designed for following environment:

* Current RingCentral RingCX account located at: https://engage.ringcentral.com. See [here for more information on current and legacy systems](authentication/index.md).
* RingCentral RingCX user linked to RingEX user for single-sign-on. RingEX users should be using RingCentral password authenticaiton, not SAML-based Single Sign-on.
* RingCentral app created at https://developers.ringcentral.com with OAuth 2.0 Password Credentials flow enabled.

## Using Postman

Using Postman once you have your pre-requisites consists of a few steps:

2. Importing the Postman Collection
1. Configuring Your Postman Environment
3. Making an API call

### Importing the Postman Collection

Use the following steps to import the RingCX Postman collection.

1. In the upper left corner of the Postman application click the "Import" button.
2. Click the "Import from Link" tab.
3. Paste in the following URL where it says "Enter a URL and press import": [`https://raw.githubusercontent.com/ringcentral/engage-voice-api-docs/master/specs/engage-voice_postman2.json`](https://raw.githubusercontent.com/ringcentral/engage-voice-api-docs/master/specs/engage-voice_postman2.json)
4. Click the "ImpContinueort" button

## Configuring Your Postman Environment

The Postman Collection uses environment variables for authentication and authorization. Fill out thes following for your environment:

1. In Postman, create an environment by clicking the Gear icon for "Management Environments" in the upper right corner. This will bring up a list of existing environments.
2. Click "Add" to create a new environment.
3. Choose a name of your choice.
4. Enter your enviroment variables as described below.
5. Click the "Add" button to finish adding this environment.

| Variable | Description |
|------|-------------|
| **`RINGCENTRAL_CLIENT_ID`** | App's OAuth 2.0 Client ID |
| **`RINGCENTRAL_CLIENT_SECRET`** | App's sOAuth 2.0 Client Secrets |
| **`RINGCENTRAL_USERNAME`** | RingCentral username |
| **`RINGCENTRAL_EXTENSION`** | RingCentral user's extension numbers |
| **`RINGCENTRAL_PASSWORD`** | RingCentral user's password. Note, this needs to be using the RingCentral passsword system and not SSO for this Postman spec. |

### Making an API call

To test the Postman collection, let's call the "Get Users" API.

1. In the Environments pick list in the upper right corner, select the environment you just created.
1. In the left hand navigation menu, select "Auth" > "Fetch access token"
1. Click the "Send" button which will load a otken in the window. You do not need to do anything with this token.
1. Navigate to "Users" > "Users" > "Get users" and click "Send".

## Feedback

If you have any feedback on using the Postman collection, please [post to the RingCX docs GitHub repo](https://github.com/ringcentral/engage-voice-api-docs/issues).
