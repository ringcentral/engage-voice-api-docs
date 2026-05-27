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

Your application needs the `ReadAccounts` OAuth scope. The authenticating user must also have platform permissions to read and update knowledge base groups, categories, and articles.

## Knowledge Base Groups

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List groups with children | `GET /voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/withChildren` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/getKnowledgeBaseGroupListWithChildren) |
| Get group | `GET /voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/getKnowledgeBaseGroup) |
| Update group | `PUT /voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/updateKnowledgeBaseGroup) |
| Delete group | `DELETE /voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/deleteKnowledgeBaseGroup) |

## Categories

Categories organize articles within a knowledge base group.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List categories | `GET /voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}/knowledgeBaseCategories` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/getKnowledgeBaseCategoryList) |
| Create category | `POST /voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}/knowledgeBaseCategories` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/createKnowledgeBaseCategory) |
| List categories with articles | `GET /voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}/knowledgeBaseCategories/withChildren` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/getKnowledgeBaseCategoryListWithChildren) |
| Get category | `GET /voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}/knowledgeBaseCategories/{knowledgeBaseCategoryId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/getKnowledgeBaseCategory) |
| Update category | `PUT /voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}/knowledgeBaseCategories/{knowledgeBaseCategoryId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/updateKnowledgeBaseCategory) |
| Delete category | `DELETE /voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}/knowledgeBaseCategories/{knowledgeBaseCategoryId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/deleteKnowledgeBaseCategory) |

## Articles

Articles are managed within a category.

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List articles | `GET /voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}/knowledgeBaseCategories/{knowledgeBaseCategoryId}/knowledgeBaseArticles` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/getKnowledgeBaseArticleList) |
| Create article | `POST /voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}/knowledgeBaseCategories/{knowledgeBaseCategoryId}/knowledgeBaseArticles` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/createKnowledgeBaseArticle) |
| Get article | `GET /voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}/knowledgeBaseCategories/{knowledgeBaseCategoryId}/knowledgeBaseArticles/{knowledgeBaseArticleId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/getKnowledgeBaseArticle) |
| Update article | `PUT /voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}/knowledgeBaseCategories/{knowledgeBaseCategoryId}/knowledgeBaseArticles/{knowledgeBaseArticleId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/updateKnowledgeBaseArticle) |
| Delete article | `DELETE /voice/api/v1/admin/accounts/{accountId}/knowledgeBaseGroups/{knowledgeBaseGroupId}/knowledgeBaseCategories/{knowledgeBaseCategoryId}/knowledgeBaseArticles/{knowledgeBaseArticleId}` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Knowledge-Base/deleteKnowledgeBaseArticle) |

## Recommended Workflow

1. Read the group and category tree with the `withChildren` endpoints.
2. Create missing categories before creating articles.
3. Upsert articles from the external content source.
4. Update categories or articles when content metadata changes.
5. Delete only after confirming no downstream workflow depends on the content.

!!! important
    Keep an external content identifier in article metadata when available. That makes synchronization idempotent and helps prevent duplicate articles.
