# Remote HTTP Service APIs

The Remote HTTP Service APIs let you configure outbound HTTP integrations used by RingCX routing and scripting flows. Use them to maintain service groups, services, service inputs, activation state, and external authentication configurations from code.

## Strategic Overview

Remote HTTP services define reusable external endpoints that RingCX can call from IVR, scripting, or integration workflows. They are useful when the same CRM, middleware, or data-enrichment service must be configured consistently across many queues, scripts, or sub-accounts.

### Key Use Cases

* **Integration Provisioning:** Create service definitions during customer onboarding.
* **Credential Rotation:** Update OAuth or external auth configurations without rebuilding scripts.
* **Environment Promotion:** Clone or update service definitions as configurations move from test to production.
* **Operational Control:** Activate or deactivate a remote service during outages or endpoint migrations.

### Required Permissions & Scopes

Your application needs the `ReadAccounts` OAuth scope. The authenticating user must have platform permissions to read and update remote HTTP service groups, HTTP services, service inputs, and external auth configurations.

## Manage Service Groups

Service groups organize related remote HTTP services.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List groups | `GET /voice/api/v1/admin/accounts/{accountId}/httpServiceGroups` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/getHttpServiceGroupList) |
| Create group | `POST /voice/api/v1/admin/accounts/{accountId}/httpServiceGroups` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/createHttpServiceGroup) |
| List groups with services | `GET /voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/withChildren` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/getHttpServiceGroupListWithChildren) |
| Get group | `GET /voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/getHttpServiceGroup) |
| Update group | `PUT /voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/updateHttpServiceGroup) |

## Manage HTTP Services

HTTP service records describe the external endpoint and how RingCX calls it.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List services | `GET /voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}/httpServices` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/getHttpServiceList) |
| Create service | `POST /voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}/httpServices` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/createHttpService) |
| Get service | `GET /voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}/httpServices/{serviceId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/getHttpService) |
| Update service | `PUT /voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}/httpServices/{serviceId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/updateHttpService) |
| Clone service | `POST /voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}/httpServices/{serviceId}/clone` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/cloneHttpService) |
| Set active state | `PUT /voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}/httpServices/{serviceId}/setIsActive` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/setHttpServiceIsActive) |

## Configure Service Inputs

Inputs define the values RingCX passes into the remote service request. Keep these in sync with the service contract expected by your external endpoint.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List inputs | `GET /voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}/httpServices/{serviceId}/inputs` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/getHttpServiceInputList) |
| Create input | `POST /voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}/httpServices/{serviceId}/inputs` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/createHttpServiceInput) |
| Get input | `GET /voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}/httpServices/{serviceId}/inputs/{inputId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/getHttpServiceInput) |
| Delete input | `DELETE /voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}/httpServices/{serviceId}/inputs/{inputId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/deleteHttpServiceInput) |

## External Auth Configurations

External auth configurations store reusable authentication settings for remote services. Use these APIs when integrations require OAuth or other reusable credentials.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List auth configs | `GET /voice/api/cx/admin/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/external/authConfigs` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/getAccountAuthConfigs) |
| Create auth config | `POST /voice/api/cx/admin/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/external/authConfigs` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/createAccountAuthConfig) |
| Update auth config | `PUT /voice/api/cx/admin/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/external/authConfigs/{configId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/updateAccountAuthConfig) |
| Delete auth config | `DELETE /voice/api/cx/admin/v1/accounts/{rcAccountId}/sub-accounts/{subAccountId}/external/authConfigs/{configId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/deleteAccountAuthConfig) |

## Recommended Workflow

1. Create or select a service group.
2. Create the remote HTTP service with the external endpoint details.
3. Add service inputs that map RingCX values into the outbound request.
4. Attach or update external auth configuration when the service requires credentials.
5. Activate the service after validation.
6. Clone the service when creating a similar integration for another environment or workflow.

!!! important
    Treat remote service changes like production integration changes. Validate the external endpoint, authentication, and expected response shape before activating the service in a live routing flow.
