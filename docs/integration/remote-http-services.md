# Remote HTTP Service APIs

The Remote HTTP Service APIs let you configure outbound HTTP integrations used by RingCX routing and scripting flows. Use them to maintain service groups, services, service inputs, activation state, and external authentication configurations from code.

## Strategic Overview

Remote HTTP services define reusable external endpoints that RingCX can call from IVR, scripting, or integration workflows. They are useful when the same CRM, middleware, or data-enrichment service must be configured consistently across many queues, scripts, or sub-accounts.

IVR WWW nodes, scripting nodes, and other workflow steps reference these service definitions so the workflow does not need to duplicate endpoint URLs, headers, credentials, and input mappings.

### Key Use Cases

* **Integration Provisioning:** Create service definitions during customer onboarding.
* **Credential Rotation:** Update OAuth or external auth configurations without rebuilding scripts.
* **Environment Promotion:** Clone or update service definitions as configurations move from test to production.
* **Operational Control:** Activate or deactivate a remote service during outages or endpoint migrations.

### Required Permissions & Scopes

#### 1. Configure OAuth Scopes

To authenticate, your application must be configured with the following permission in the [Developer Portal](https://developers.ringcentral.com/my-account.html#/applications):

* **`ReadAccounts`**: Required to validate account context and access RingCX integration configuration APIs.

#### 2. Enable RingCX Admin Access

In the RingCX Admin portal, the authenticating user must have permission to read and update remote HTTP service groups, HTTP services, service inputs, and external auth configurations.

!!! warning "Common Authorization Errors"
    If the OAuth token is valid but the RingCX user lacks integration configuration access, the API returns an error similar to:
    ```json
    {
      "errorCode": "access.denied.exception",
      "generalMessage": "You do not have permission to access this resource",
      "timestamp": 1611847650696
    }
    ```

## Manage Service Groups

Service groups organize related remote HTTP services.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List groups | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/httpServiceGroups` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/getHttpServiceGroupList) |
| Create group | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/httpServiceGroups` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/createHttpServiceGroup) |
| List groups with services | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/withChildren` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/getHttpServiceGroupListWithChildren) |
| Get group | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/getHttpServiceGroup) |
| Update group | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/updateHttpServiceGroup) |

## Manage HTTP Services

HTTP service records describe the external endpoint and how RingCX calls it.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List services | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}/httpServices` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/getHttpServiceList) |
| Create service | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}/httpServices` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/createHttpService) |
| Get service | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}/httpServices/{serviceId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/getHttpService) |
| Update service | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}/httpServices/{serviceId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/updateHttpService) |
| Clone service | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}/httpServices/{serviceId}/clone` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/cloneHttpService) |
| Set active state | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}/httpServices/{serviceId}/setIsActive` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/setHttpServiceIsActive) |

## Configure Service Inputs

Inputs define the values RingCX passes into the remote service request. Keep these in sync with the service contract expected by your external endpoint.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List inputs | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}/httpServices/{serviceId}/inputs` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/getHttpServiceInputList) |
| Create input | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}/httpServices/{serviceId}/inputs` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/createHttpServiceInput) |
| Get input | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}/httpServices/{serviceId}/inputs/{inputId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/getHttpServiceInput) |
| Delete input | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}/httpServices/{serviceId}/inputs/{inputId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/deleteHttpServiceInput) |

## External Auth Configurations

External auth configurations store reusable authentication settings for remote services. Use these APIs when integrations require OAuth or other reusable credentials.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List auth configs | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/external/authConfigs` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/getExternalAuthConfigsList) |
| Get auth config | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/external/authConfigs/{authConfigId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/getExternalAuthConfigById) |
| Delete auth config | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/external/authConfigs/{authConfigId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/deleteExternalAuthConfigById) |
| Create API key auth | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/external/authConfigs/{authConfigId}/apiKey` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/createExternalAccountAuthConfigApiKey) |
| Create basic auth | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/external/authConfigs/{authConfigId}/basic` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/createExternalAccountAuthConfigBasic) |
| Create OAuth auth | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/external/authConfigs/{authConfigId}/oauth` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Remote-HTTP-Services/createExternalAccountAuthConfigOAuth) |

## Recommended Workflow

1. Create or select a service group.
2. Create the remote HTTP service with the external endpoint details.
3. Add service inputs that map RingCX values into the outbound request.
4. Attach or update external auth configuration when the service requires credentials.
5. Activate the service after validation.
6. Clone the service when creating a similar integration for another environment or workflow.

!!! important
    Treat remote service changes like production integration changes. Validate the external endpoint, authentication, and expected response shape before activating the service in a live routing flow.

!!! important "Rate Limiting & Stability"
    Remote HTTP service changes can affect live IVR and scripting flows. Batch provisioning updates, activate services only after validation, and use exponential backoff on `429 Too Many Requests` responses.

## Request Examples

### Create a Service Group

`POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/httpServiceGroups`

```json
{
  "groupName": "CRM enrichment",
  "description": "Services used by inbound IVR and scripts",
  "active": true
}
```

### Create an HTTP Service

`POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}/httpServices`

```json
{
  "serviceName": "Lookup customer by ANI",
  "description": "Returns CRM profile data for the caller",
  "url": "https://api.example.com/customers/lookup",
  "method": "POST",
  "contentType": "application/json",
  "active": false
}
```

### Create a Service Input

`POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/httpServiceGroups/{serviceGroupId}/httpServices/{serviceId}/inputs`

```json
{
  "inputName": "ani",
  "source": "CALL",
  "required": true,
  "description": "Caller phone number passed to the CRM lookup"
}
```

### Create API Key Auth

`POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/external/authConfigs/{authConfigId}/apiKey`

```json
{
  "name": "CRM API key",
  "apiKey": "secret-value",
  "headerName": "X-API-Key"
}
```

### Create Basic Auth

`POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/external/authConfigs/{authConfigId}/basic`

```json
{
  "name": "CRM basic auth",
  "username": "ringcx-service",
  "password": "secret-value"
}
```

### Create OAuth Auth

`POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/external/authConfigs/{authConfigId}/oauth`

```json
{
  "name": "CRM OAuth",
  "tokenUrl": "https://auth.example.com/oauth/token",
  "clientId": "ringcx-client",
  "clientSecret": "secret-value",
  "grantType": "client_credentials"
}
```

### Example HTTP Service Response

```json
{
  "serviceId": 4567,
  "serviceGroupId": 1234,
  "serviceName": "Lookup customer by ANI",
  "description": "Returns CRM profile data for the caller",
  "url": "https://api.example.com/customers/lookup",
  "method": "POST",
  "contentType": "application/json",
  "active": false
}
```

## Resource Notes

| Resource | Key Fields | Notes |
| --- | --- | --- |
| Service group | `serviceGroupId`, `groupName`, `description`, `active` | Logical container for related services. |
| HTTP service | `serviceId`, `serviceName`, `url`, `method`, `contentType`, `active` | Defines the external endpoint RingCX workflows call. |
| Service input | `inputId`, `inputName`, `source`, `required` | Maps RingCX runtime values into the request. |
| Auth config | `authConfigId`, `authType`, `name` | Stores reusable credentials for outbound calls. |

## Common Errors

| Status | Cause | Resolution |
| --- | --- | --- |
| `400 Bad Request` | Malformed URL, method, auth payload, or input mapping. | Validate service definitions before activating them. |
| `403 Forbidden` | User lacks integration configuration permissions. | Grant remote service and external auth permissions in the Admin portal. |
| `404 Not Found` | Service group, service, input, or auth config is not under the account. | Re-list parent resources and use IDs from the same account. |
| `409 Conflict` | Service is inactive, duplicated, or referenced by a workflow that prevents deletion. | Clone/update safely and activate only after validation. |

## Sample Implementation (Python)

```python
import requests

BASE_URL = "https://ringcx.ringcentral.com/voice/api"

def provision_remote_service(token, account_id):
    headers = {"Authorization": f"Bearer {token}"}
    group = requests.post(
        f"{BASE_URL}/v1/admin/accounts/{account_id}/httpServiceGroups",
        headers=headers,
        json={"groupName": "CRM enrichment", "active": True},
    )
    group.raise_for_status()
    group_id = group.json()["serviceGroupId"]

    service = requests.post(
        f"{BASE_URL}/v1/admin/accounts/{account_id}/httpServiceGroups/{group_id}/httpServices",
        headers=headers,
        json={
            "serviceName": "Lookup customer by ANI",
            "url": "https://api.example.com/customers/lookup",
            "method": "POST",
            "contentType": "application/json",
            "active": False,
        },
    )
    service.raise_for_status()
    service_id = service.json()["serviceId"]

    input_response = requests.post(
        f"{BASE_URL}/v1/admin/accounts/{account_id}/httpServiceGroups/{group_id}/httpServices/{service_id}/inputs",
        headers=headers,
        json={"inputName": "ani", "source": "CALL", "required": True},
    )
    input_response.raise_for_status()
    return {"group": group.json(), "service": service.json(), "input": input_response.json()}
```
