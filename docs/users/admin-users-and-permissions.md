# Admin User and Permission APIs

The Admin User and Permission APIs let you manage RingCX administrative users, role assignments, rights documents, API tokens, and account-level authentication checks. Use them when user and permission changes are driven by an external identity or governance process.

## Strategic Overview

Agents and administrators are related but not identical. Agent APIs manage contact-center users who handle interactions. Admin user and permission APIs manage access to the Admin portal and administrative API capabilities.

### Key Use Cases

* **User Governance:** List users and inspect effective permissions for audits.
* **Role Automation:** Add or remove platform roles during onboarding and offboarding.
* **Rights Document Management:** Create or update rights documents that define administrative access.
* **Auth Utilities:** Validate tokens and support password reset workflows.

### Required Permissions & Scopes

#### 1. Configure OAuth Scopes

Your application needs the `ReadAccounts` OAuth scope.

#### 2. Enable RingCX Admin Access

The authenticating user must have sufficient Admin portal permissions to read users and update roles or rights documents. User create/list operations require `MANAGE_USERS` or `SUPER_USER`; rights document assignment requires `MANAGE_RIGHTS` or `SUPER_USER`. Use least privilege for automation accounts, and separate read-only audit automation from onboarding/offboarding automation.

!!! warning "Common Authorization Errors"
    If the OAuth token is valid but the user cannot manage users, roles, or rights documents, the API returns an error similar to:
    ```json
    {
      "errorCode": "access.denied.exception",
      "generalMessage": "You do not have permission to access this resource",
      "timestamp": 1611847650696
    }
    ```

## Users

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List users | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/users` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/getUserList) |
| Create user | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/users` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/createUser) |
| Get user | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/users/{userId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/getUser) |
| Update user | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/users/{userId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/updateUser) |
| Delete user | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/users/{userId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/deleteUser) |

## Roles

Roles are coarse-grained access assignments. Use role endpoints for straightforward role membership changes.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List user roles | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/users/{userId}/roles` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/getRoles) |
| Add role | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/users/{userId}/roles/{roleType}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/addRole) |
| Remove role | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/users/{userId}/roles/{roleType}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/removeRole) |

## Rights Documents

Rights documents provide detailed administrative permissions. Use these endpoints for advanced permission management or audit tooling.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List rights docs | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/users/{userId}/rightsDocs` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/getRightsDocs) |
| Create rights doc | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/users/{userId}/rightsDocs` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/createRightsDoc) |
| Update rights doc | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/users/{userId}/rightsDocs/{rightsDocId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/updateRightsDoc) |
| Delete rights doc | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/users/{userId}/rightsDocs/{rightsDocId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/deleteRightsDoc) |
| Assign rights doc | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/rightsDocs/{rightsDocId}/assignments` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/assignRightsDoc) |
| Delete assignment | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/rightsDocs/{rightsDocId}/assignments/{assignedUserId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/deleteRightsDocAssignment) |

## Auth Utilities

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| Validate token | `GET https://ringcx.ringcentral.com/voice/api/v1/auth/isTokenValid` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/isTokenValid) |
| Reset password | `POST https://ringcx.ringcentral.com/voice/api/v1/auth/passwordReset` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/passwordReset) |
| Request password reset | `POST https://ringcx.ringcentral.com/voice/api/v1/auth/passwordResetRequest` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/passwordResetRequest) |

## Recommended Workflow

1. List or create the user.
2. Apply required roles for broad access.
3. Create or assign rights documents for detailed access.
4. Verify effective access by reading assigned and aggregated rights documents.
5. Remove roles and rights document assignments during offboarding.

!!! warning
    Permission changes can grant administrative access to customer data and configuration. Apply least privilege and log all automated changes for audit review.

!!! important "Rate Limiting & Stability"
    User and permission changes should be serialized per user. Avoid parallel role and rights document updates for the same user because the final effective permission set can be difficult to audit.

## Request Examples

### Create a User

```json
{
  "userName": "alex.admin@example.com",
  "firstName": "Alex",
  "lastName": "Admin",
  "enabled": true,
  "roles": [
    "USER",
    "MANAGE_USERS"
  ],
  "regionalSettings": {
    "timezoneName": "America/Denver"
  }
}
```

### Assign a Role

`POST https://ringcx.ringcentral.com/voice/api/v1/admin/users/{userId}/roles/{roleType}`

Use the `roleType` path parameter for the role being assigned.

### Create a Rights Document

```json
{
  "rightsDocName": "Reporting audit access",
  "description": "Read-only analytics and reporting permissions",
  "active": true
}
```

### Assign a Rights Document

`POST https://ringcx.ringcentral.com/voice/api/v1/admin/rightsDocs/{rightsDocId}/assignments?userIds=987654&userIds=987655`

The assignment endpoint takes one or more `userIds` query parameters. It does not accept a JSON request body.

### Example User Response

```json
{
  "userId": 987654,
  "userName": "alex.admin@example.com",
  "firstName": "Alex",
  "lastName": "Admin",
  "enabled": true,
  "roles": [
    "USER",
    "MANAGE_USERS"
  ],
  "regionalSettings": {
    "timezoneName": "America/Denver"
  }
}
```

## Response and Schema Notes

| Resource | Key Fields | Notes |
| --- | --- | --- |
| User | `userId`, `userName`, `firstName`, `lastName`, `enabled`, `regionalSettings`, `roles` | Admin portal identity and lifecycle state. |
| Role | `roleType`, `userId`, `createdOn` | Coarse access grant. Supported role values include `SUPER_USER`, `USER`, `MANAGE_USERS`, `MANAGE_RIGHTS`, `ACCESS_SIBLINGS`, `ACCESS_AUDIT_LOG`, `ASSUME_USERS`, `REPORT_ADMINISTRATIVE_USER`, `WFO_ACCESS`, `ACCESS_GOODDATA_EDITOR`, `ACCESS_GOODDATA_ANALYST`, `ACCESS_GOODDATA_VIEWER`, and `NO_ACCESS`. |
| Rights document | `rightsDocId`, `rightsDocName`, `description`, `active`, `permissions` | Fine-grained administrative permissions. |
| Assignment | `rightsDocId`, `userIds`, `rightsDocIds` | Grants rights document access to one or more users. Assignment create operations use query parameters rather than a JSON body. |

## Common Errors

| Status | Cause | Resolution |
| --- | --- | --- |
| `400 Bad Request` | Missing user fields, invalid role type, or malformed rights document. | Validate against the generated API reference before submitting. |
| `403 Forbidden` | Caller cannot manage users, roles, or rights docs. | Grant appropriate Admin portal permission to the automation user. |
| `404 Not Found` | User, role, or rights document ID does not exist. | List the target resource before updating or deleting. |
| `409 Conflict` | Username, role, or assignment already exists. | Treat create operations as idempotent by reading current state first. |

## Sample Implementation (Python)

```python
import requests

BASE_URL = "https://ringcx.ringcentral.com/voice/api"

def onboard_admin_user(token, user_name, role_type, rights_doc_id=None):
    headers = {"Authorization": f"Bearer {token}"}
    user = requests.post(
        f"{BASE_URL}/v1/admin/users",
        headers=headers,
        json={
            "userName": user_name,
            "firstName": "Alex",
            "lastName": "Admin",
            "enabled": True,
            "roles": ["USER"],
            "regionalSettings": {"timezoneName": "America/Denver"},
        },
    )
    user.raise_for_status()
    user_id = user.json()["userId"]

    role = requests.post(
        f"{BASE_URL}/v1/admin/users/{user_id}/roles/{role_type}",
        headers=headers,
    )
    role.raise_for_status()

    if rights_doc_id is not None:
        assignment = requests.post(
            f"{BASE_URL}/v1/admin/rightsDocs/{rights_doc_id}/assignments",
            headers=headers,
            params={"userIds": [user_id]},
        )
        assignment.raise_for_status()

    return user.json()
```
