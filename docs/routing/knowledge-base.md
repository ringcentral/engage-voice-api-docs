# Knowledge Base APIs

The Knowledge Base APIs let you maintain RingCX knowledge base groups, categories, and articles from an external content system. Use them when help content must be synchronized from another source of truth.

## Strategic Overview

Knowledge base content is organized into groups, categories, and articles. These APIs are configuration APIs for content management, not analytics APIs. They are most useful when an organization already manages support content in a CMS and needs RingCX content to follow the same lifecycle.

### Key Use Cases

* **Content Synchronization:** Publish approved support articles from an external CMS into RingCX.
* **Category Management:** Keep category structure aligned across sub-accounts or environments.
* **Bulk Maintenance:** Update article text, metadata, or grouping without manual portal edits.
* **Audit Support:** Compare RingCX knowledge content against a source repository.

### Required Permissions & Scopes

#### 1. Configure OAuth Scopes

To authenticate, your application must be configured with the following permission in the [Developer Portal](https://developers.ringcentral.com/my-account.html#/applications):

* **`ReadAccounts`**: Required to validate account context and access RingCX administrative APIs.

#### 2. Enable RingCX Admin Access

The authenticating user must have RingCX permissions that match the action being performed. Category creation requires `CREATE` on Knowledge Base Group, while article creation requires `CREATE` on Scripting.

!!! warning "Common Authorization Errors"
    If the application has the right OAuth scope but the user lacks knowledge base management permissions, the API returns an error similar to:
    ```json
    {
      "errorCode": "access.denied.exception",
      "generalMessage": "You do not have permission to access this resource",
      "timestamp": 1611847650696
    }
    ```

## Knowledge Base Groups

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List groups with children | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/withChildren` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/getKnowledgeBaseGroupListWithChildren) |
| Get group | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/getKnowledgeBaseGroup) |
| Update group | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/updateKnowledgeBaseGroup) |
| Delete group | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/deleteKnowledgeBaseGroup) |

## Categories

Categories organize articles within a knowledge base group.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List categories | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}/knowledgeBaseCategories` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/getKnowledgeBaseCategoryList) |
| Create category | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}/knowledgeBaseCategories` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/createKnowledgeBaseCategory) |
| List categories with articles | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}/knowledgeBaseCategories/withChildren` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/getKnowledgeBaseCategoryListWithChildren) |
| Get category | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}/knowledgeBaseCategories/{knowledgeBaseCategoryId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/getKnowledgeBaseCategory) |
| Update category | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}/knowledgeBaseCategories/{knowledgeBaseCategoryId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/updateKnowledgeBaseCategory) |
| Delete category | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}/knowledgeBaseCategories/{knowledgeBaseCategoryId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/deleteKnowledgeBaseCategory) |

## Articles

Articles are managed within a category.

Article permissions are tied to Scripting because knowledge articles can be used in agent and routing workflows. See the [IVR Scripting node](ivr/scripting-node.md) documentation when content changes are part of a scripting workflow.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List articles | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}/knowledgeBaseCategories/{knowledgeBaseCategoryId}/knowledgeBaseArticles` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/getKnowledgeBaseArticleList) |
| Create article | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}/knowledgeBaseCategories/{knowledgeBaseCategoryId}/knowledgeBaseArticles` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/createKnowledgeBaseArticle) |
| Get article | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}/knowledgeBaseCategories/{knowledgeBaseCategoryId}/knowledgeBaseArticles/{knowledgeBaseArticleId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/getKnowledgeBaseArticle) |
| Update article | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}/knowledgeBaseCategories/{knowledgeBaseCategoryId}/knowledgeBaseArticles/{knowledgeBaseArticleId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/updateKnowledgeBaseArticle) |
| Delete article | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}/knowledgeBaseCategories/{knowledgeBaseCategoryId}/knowledgeBaseArticles/{knowledgeBaseArticleId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/deleteKnowledgeBaseArticle) |

## Recommended Workflow

1. Read the group and category tree with the `withChildren` endpoints.
2. Create missing categories before creating articles.
3. Upsert articles from the external content source.
4. Update categories or articles when content metadata changes.
5. Delete only after confirming no downstream workflow depends on the content.

!!! important
    Keep an external content identifier in article metadata when available. That makes synchronization idempotent and helps prevent duplicate articles.

!!! important "Rate Limiting & Stability"
    Synchronize knowledge base content in batches, especially when importing from an external CMS. Read the group/category tree first, update only changed articles, and use exponential backoff on `429 Too Many Requests` responses.

## Identifiers and Parameters

| Parameter | Type | Requirement | Description |
| --- | --- | --- | --- |
| `accountId` | String | **Required** | RingCX account that owns the knowledge base. |
| `knowledgeBaseGroupId` | Integer | **Required** | Group that contains categories. |
| `knowledgeBaseCategoryId` | Integer | **Required for category/article operations** | Category that contains articles. |
| `knowledgeBaseArticleId` | Integer | **Required for article read/update/delete** | Article identifier. |

## Request Examples

### Create a Category

`POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}/knowledgeBaseCategories`

The category display name is `title`, not `name`. `KnowledgeBaseGroup` is the resource whose display name is `name`; categories and articles both use `title`.

```json
{
  "title": "Billing",
  "description": "Billing and invoice support articles",
  "active": true,
  "order": 10
}
```

### Create an Article

`POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}/knowledgeBaseCategories/{knowledgeBaseCategoryId}/knowledgeBaseArticles`

```json
{
  "title": "Update invoice contact",
  "content": "<p>Open Billing, select the account, and update the invoice contact.</p>",
  "labels": "billing,invoice",
  "active": true,
  "showSend": true,
  "order": 20
}
```

### Update an Article

```json
{
  "knowledgeBaseArticleId": 9876,
  "title": "Update invoice contact",
  "content": "<p>Open Billing, select the account, and update the invoice contact.</p><p>Save your changes.</p>",
  "labels": "billing,invoice,admin",
  "active": true,
  "showSend": true,
  "order": 20
}
```

### Example Article Response

```json
{
  "knowledgeBaseArticleId": 9876,
  "title": "Update invoice contact",
  "content": "<p>Open Billing, select the account, and update the invoice contact.</p>",
  "contentPlain": "Open Billing, select the account, and update the invoice contact.",
  "labels": "billing,invoice",
  "active": true,
  "showSend": true,
  "order": 20,
  "knowledgeBaseCategory": {
    "knowledgeBaseCategoryId": 1234,
    "title": "Billing"
  }
}
```

## Article and Category Schema Notes

Knowledge base article content is stored in the `content` field as HTML. The service also exposes a plain-text projection as `contentPlain` in list/detail views where supported.

### `KnowledgeBaseArticle`

| Field | Type | Description |
| --- | --- | --- |
| `knowledgeBaseArticleId` | Integer | Article identifier. |
| `title` | String | Article title. |
| `content` | String | HTML article body. |
| `contentPlain` | String | HTML-stripped article content returned by the service. |
| `labels` | String | Label text used for filtering or categorization. |
| `active` | Boolean | Whether the article is available. |
| `showSend` | Boolean | Whether agents can send the article where supported by the UI. |
| `order` | Integer | Sort order within the category. |
| `knowledgeBaseCategory` | Object | Parent category reference (`KnowledgeBaseCategory`). |

### `KnowledgeBaseCategory`

| Field | Type | Description |
| --- | --- | --- |
| `knowledgeBaseCategoryId` | Integer | Category identifier. |
| `title` | String | Category title. The group display name is `name`; categories and articles both use `title`. |
| `description` | String | Free-form description. |
| `active` | Boolean | Whether the category is available. |
| `order` | Integer | Sort order within the group. |
| `groupId` | Integer | Parent group identifier. |
| `knowledgeBaseGroup` | Object | Parent group reference (`KnowledgeBaseGroup`). |
| `knowledgeBaseArticles` | Array | Articles in the category, returned by the `withChildren` list endpoint. |
| `permissions` | Array | Per-resource CRUD permissions for the authenticated user. |

!!! info "Content Format"
    The implementation cleans saved HTML content, including link handling. Avoid sending unsupported scripts or raw external markup; sanitize CMS content before synchronizing it into RingCX.

## Common Errors

| Status | Cause | Resolution |
| --- | --- | --- |
| `400 Bad Request` | Missing category/article fields or invalid content. | Validate HTML and required fields before submitting. |
| `403 Forbidden` | Caller lacks knowledge base permissions. | Grant Admin portal permission for knowledge base management. |
| `404 Not Found` | Group, category, or article ID is not under the account. | Read the tree with `withChildren` before updating nested resources. |
| `409 Conflict` | Duplicate content or deletion blocked by downstream dependencies. | Use an external CMS identifier in labels or metadata and confirm before deletion. |

## Sample Implementation (Python)

```python
import requests

BASE_URL = "https://ringcx.ringcentral.com/voice/api"

def sync_cms_article(token, account_id, group_id, category_id, cms_article):
    headers = {"Authorization": f"Bearer {token}"}
    body = {
        "title": cms_article["title"],
        "content": cms_article["html"],
        "labels": f"cms,{cms_article['id']}",
        "active": True,
        "showSend": True,
        "order": cms_article.get("order", 0),
    }
    response = requests.post(
        f"{BASE_URL}/v1/admin/accounts/{account_id}/knowledgeBaseGroups/{group_id}"
        f"/knowledgeBaseCategories/{category_id}/knowledgeBaseArticles",
        headers=headers,
        json=body,
    )
    response.raise_for_status()
    return response.json()
```
