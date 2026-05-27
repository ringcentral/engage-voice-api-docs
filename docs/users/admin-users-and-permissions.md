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

Your application needs the `ReadAccounts` OAuth scope. The authenticating user must have sufficient platform permissions to read users and update roles or rights documents.

## Users

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List users | `GET /voice/api/v1/admin/users` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/getUserList) |
| Create user | `POST /voice/api/v1/admin/users` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/createUser) |
| Get user | `GET /voice/api/v1/admin/users/{userId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/getUser) |
| Update user | `PUT /voice/api/v1/admin/users/{userId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/updateUser) |
| Delete user | `DELETE /voice/api/v1/admin/users/{userId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/deleteUser) |

## Roles

Roles are coarse-grained access assignments. Use role endpoints for straightforward role membership changes.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List user roles | `GET /voice/api/v1/admin/users/{userId}/roles` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/getRoles) |
| Add role | `POST /voice/api/v1/admin/users/{userId}/roles/{roleType}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/addRole) |
| Remove role | `DELETE /voice/api/v1/admin/users/{userId}/roles/{roleType}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/removeRole) |

## Rights Documents

Rights documents provide detailed administrative permissions. Use these endpoints for advanced permission management or audit tooling.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List rights docs | `GET /voice/api/v1/admin/users/{userId}/rightsDocs` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/getRightsDocs) |
| Create rights doc | `POST /voice/api/v1/admin/users/{userId}/rightsDocs` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/createRightsDoc) |
| Update rights doc | `PUT /voice/api/v1/admin/users/{userId}/rightsDocs/{rightsDocId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/updateRightsDoc) |
| Delete rights doc | `DELETE /voice/api/v1/admin/users/{userId}/rightsDocs/{rightsDocId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/deleteRightsDoc) |
| Assign rights doc | `POST /voice/api/v1/admin/rightsDocs/{rightsDocId}/assignments` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/assignRightsDoc) |
| Delete assignment | `DELETE /voice/api/v1/admin/rightsDocs/{rightsDocId}/assignments/{assignedUserId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/deleteRightsDocAssignment) |

## Auth Utilities

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| Validate token | `GET /voice/api/v1/auth/isTokenValid` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/isTokenValid) |
| Reset password | `POST /voice/api/v1/auth/passwordReset` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/passwordReset) |
| Request password reset | `POST /voice/api/v1/auth/passwordResetRequest` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Admin-Users-and-Permissions/passwordResetRequest) |

## Recommended Workflow

1. List or create the user.
2. Apply required roles for broad access.
3. Create or assign rights documents for detailed access.
4. Verify effective access by reading assigned and aggregated rights documents.
5. Remove roles and rights document assignments during offboarding.

!!! warning
    Permission changes can grant administrative access to customer data and configuration. Apply least privilege and log all automated changes for audit review.
