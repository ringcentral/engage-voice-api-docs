#!/usr/bin/env python3
"""Generate the public RingCX Postman collection from the OpenAPI spec."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "specs" / "engage-voice_openapi3.json"
COLLECTION_PATH = ROOT / "specs" / "engage-voice_postman2.json"
ENVIRONMENT_PATH = ROOT / "specs" / "ringcx_postman_environment.json"
LEGACY_COLLECTION_PATH = ROOT / "specs" / "engage-voice_legacy_auth_postman2.json"
LEGACY_ENVIRONMENT_PATH = ROOT / "specs" / "ringcx_legacy_postman_environment.json"

HTTP_METHODS = ("get", "post", "put", "patch", "delete", "head", "options")
MAX_EXAMPLE_PROPERTIES = 10
MAX_EXAMPLE_DEPTH = 4

RINGCX_BASE_URL = "{{ringcx_base_url}}"
RINGCENTRAL_BASE_URL = "{{ringcentral_base_url}}"
LEGACY_BASE_URL = "{{legacy_base_url}}"

PATH_VARIABLE_ALIASES = {
    "accountId": "rcx_sub_account_id",
    "subAccountId": "rcx_sub_account_id",
    "mainAccountId": "rcx_main_account_id",
    "rcAccountId": "rc_account_uid",
}

HELPER_OPERATIONS = {
    ("POST", "/api/auth/login/rc/accesstoken"),
    ("GET", "/voice/api/v1/admin/accounts"),
}

LEGACY_ONLY_OPERATIONS = {
    ("POST", "/voice/api/v1/auth/login"),
}

COMMON_VARIABLES = [
    {
        "key": "ringcx_base_url",
        "value": "https://ringcx.ringcentral.com",
        "type": "default",
    },
    {
        "key": "ringcentral_base_url",
        "value": "https://platform.ringcentral.com",
        "type": "default",
    },
    {"key": "RINGCENTRAL_CLIENT_ID", "value": "", "type": "secret"},
    {"key": "RINGCENTRAL_CLIENT_SECRET", "value": "", "type": "secret"},
    {"key": "RINGCENTRAL_JWT", "value": "", "type": "secret"},
    {"key": "rco_access_token", "value": "", "type": "secret"},
    {"key": "ringcx_bearer_token", "value": "", "type": "secret"},
    {"key": "rcev_access_token", "value": "", "type": "secret"},
    {"key": "ringcx_token_expires_at", "value": "", "type": "default"},
    {"key": "rcx_sub_account_id", "value": "", "type": "default"},
    {"key": "rcx_main_account_id", "value": "", "type": "default"},
    {"key": "rc_account_uid", "value": "", "type": "default"},
]

SECRET_VARIABLE_KEYS = {
    "RINGCENTRAL_CLIENT_ID",
    "RINGCENTRAL_CLIENT_SECRET",
    "RINGCENTRAL_JWT",
    "rco_access_token",
    "ringcx_bearer_token",
    "rcev_access_token",
}

LEGACY_VARIABLES = [
    {
        "key": "legacy_base_url",
        "value": "https://portal.vacd.biz/api",
        "type": "default",
    },
    {"key": "legacy_username", "value": "", "type": "secret"},
    {"key": "legacy_password", "value": "", "type": "secret"},
    {"key": "legacy_auth_token", "value": "", "type": "secret"},
    {"key": "legacy_api_token", "value": "", "type": "secret"},
    {"key": "legacy_api_token_to_delete", "value": "", "type": "secret"},
]

LEGACY_SECRET_VARIABLE_KEYS = {
    "legacy_username",
    "legacy_password",
    "legacy_auth_token",
    "legacy_api_token",
    "legacy_api_token_to_delete",
}


def load_json(path: Path) -> Dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def resolve_pointer(document: Dict[str, Any], ref: str) -> Any:
    if not ref.startswith("#/"):
        raise ValueError(f"Only local OpenAPI references are supported: {ref}")

    value: Any = document
    for part in ref[2:].split("/"):
        key = part.replace("~1", "/").replace("~0", "~")
        value = value[key]
    return value


def dereference(document: Dict[str, Any], value: Any) -> Any:
    if not isinstance(value, dict) or "$ref" not in value:
        return value

    resolved = copy.deepcopy(resolve_pointer(document, value["$ref"]))
    siblings = {key: copy.deepcopy(item) for key, item in value.items() if key != "$ref"}
    if siblings and isinstance(resolved, dict):
        resolved.update(siblings)
    return resolved


def first_example(examples: Any) -> Any:
    if not isinstance(examples, dict):
        return None
    for example in examples.values():
        if isinstance(example, dict) and "value" in example:
            return copy.deepcopy(example["value"])
    return None


def schema_example(
    document: Dict[str, Any],
    schema: Any,
    name: str = "value",
    depth: int = 0,
    seen_refs: Sequence[str] = (),
) -> Any:
    if not isinstance(schema, dict):
        return None

    ref = schema.get("$ref")
    if ref:
        if ref in seen_refs or depth >= MAX_EXAMPLE_DEPTH:
            return {}
        resolved = dereference(document, schema)
        return schema_example(document, resolved, name, depth + 1, (*seen_refs, ref))

    if "example" in schema:
        return copy.deepcopy(schema["example"])
    if "default" in schema:
        return copy.deepcopy(schema["default"])
    if "const" in schema:
        return copy.deepcopy(schema["const"])

    enum = schema.get("enum")
    if isinstance(enum, list) and enum:
        return copy.deepcopy(next((item for item in enum if item is not None), enum[0]))

    if isinstance(schema.get("allOf"), list):
        merged: Dict[str, Any] = {}
        fallback: Any = None
        for child in schema["allOf"]:
            example = schema_example(document, child, name, depth + 1, seen_refs)
            if isinstance(example, dict):
                merged.update(example)
            elif fallback is None:
                fallback = example
        return merged if merged else fallback

    for keyword in ("oneOf", "anyOf"):
        choices = schema.get(keyword)
        if isinstance(choices, list) and choices:
            return schema_example(document, choices[0], name, depth + 1, seen_refs)

    schema_type = schema.get("type")
    if not schema_type:
        if "properties" in schema or "additionalProperties" in schema:
            schema_type = "object"
        elif "items" in schema:
            schema_type = "array"

    if schema_type == "object":
        properties = schema.get("properties") or {}
        required = set(schema.get("required") or [])
        selected: List[Tuple[str, Any]] = []

        for property_name, property_schema in properties.items():
            resolved_property = dereference(document, property_schema)
            if isinstance(resolved_property, dict) and resolved_property.get("readOnly"):
                continue
            if property_name in required:
                selected.append((property_name, property_schema))

        for property_name, property_schema in properties.items():
            if property_name in required:
                continue
            if len(selected) >= MAX_EXAMPLE_PROPERTIES:
                break
            resolved_property = dereference(document, property_schema)
            if isinstance(resolved_property, dict) and resolved_property.get("readOnly"):
                continue
            selected.append((property_name, property_schema))

        return {
            property_name: schema_example(
                document,
                property_schema,
                property_name,
                depth + 1,
                seen_refs,
            )
            for property_name, property_schema in selected
        }

    if schema_type == "array":
        item = schema_example(document, schema.get("items") or {}, name, depth + 1, seen_refs)
        return [item]

    if schema_type == "boolean":
        return False

    if schema_type in ("integer", "number"):
        minimum = schema.get("minimum")
        return minimum if minimum is not None else 0

    if schema_type == "string" or schema_type is None:
        value_format = schema.get("format")
        if value_format == "date-time":
            return "2026-01-15T12:00:00Z"
        if value_format == "date":
            return "2026-01-15"
        if value_format == "uuid":
            return "00000000-0000-4000-8000-000000000000"
        if value_format in ("uri", "url"):
            return "https://example.com/resource"
        if value_format in ("binary", "byte"):
            return "<binary>"
        return f"<{name}>"

    return None


def scalar_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list)):
        return json.dumps(value, separators=(",", ":"))
    return str(value)


def parameter_example(document: Dict[str, Any], parameter: Dict[str, Any]) -> str:
    if "example" in parameter:
        return scalar_text(parameter["example"])
    example = first_example(parameter.get("examples"))
    if example is not None:
        return scalar_text(example)
    schema = dereference(document, parameter.get("schema") or {})
    return scalar_text(schema_example(document, schema, parameter.get("name") or "value"))


def merged_parameters(
    document: Dict[str, Any],
    path_item: Dict[str, Any],
    operation: Dict[str, Any],
) -> List[Dict[str, Any]]:
    merged: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for parameter in [*(path_item.get("parameters") or []), *(operation.get("parameters") or [])]:
        resolved = dereference(document, parameter)
        if not isinstance(resolved, dict):
            continue
        key = (resolved.get("in", ""), resolved.get("name", ""))
        merged[key] = resolved
    return list(merged.values())


def choose_media(content: Dict[str, Any]) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
    if not isinstance(content, dict) or not content:
        return None, None

    preferences = (
        "application/json",
        "application/x-www-form-urlencoded",
        "multipart/form-data",
    )
    for media_type in preferences:
        if media_type in content:
            return media_type, content[media_type]
    for media_type, media in content.items():
        if media_type.endswith("+json"):
            return media_type, media
    return next(iter(content.items()))


def media_example(document: Dict[str, Any], media: Dict[str, Any], request: bool) -> Any:
    if "example" in media:
        return copy.deepcopy(media["example"])
    example = first_example(media.get("examples"))
    if example is not None:
        return example
    if not request:
        return None
    return schema_example(document, media.get("schema") or {})


def build_body(
    document: Dict[str, Any], request_body: Any
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    resolved = dereference(document, request_body)
    if not isinstance(resolved, dict):
        return None, None

    media_type, media = choose_media(resolved.get("content") or {})
    if not media_type or not isinstance(media, dict):
        return None, None

    example = media_example(document, media, request=True)
    schema = dereference(document, media.get("schema") or {})

    if media_type == "application/x-www-form-urlencoded":
        properties = schema.get("properties") if isinstance(schema, dict) else {}
        required = set(schema.get("required") or []) if isinstance(schema, dict) else set()
        fields = []
        for key, value_schema in (properties or {}).items():
            fields.append(
                {
                    "key": key,
                    "value": scalar_text(schema_example(document, value_schema, key)),
                    "type": "text",
                    "disabled": key not in required,
                }
            )
        return {"mode": "urlencoded", "urlencoded": fields}, media_type

    if media_type == "multipart/form-data":
        properties = schema.get("properties") if isinstance(schema, dict) else {}
        required = set(schema.get("required") or []) if isinstance(schema, dict) else set()
        fields = []
        for key, value_schema in (properties or {}).items():
            resolved_schema = dereference(document, value_schema)
            is_file = isinstance(resolved_schema, dict) and resolved_schema.get("format") == "binary"
            field: Dict[str, Any] = {
                "key": key,
                "type": "file" if is_file else "text",
                "disabled": key not in required,
            }
            if is_file:
                field["src"] = []
            else:
                field["value"] = scalar_text(schema_example(document, value_schema, key))
            fields.append(field)
        return {"mode": "formdata", "formdata": fields}, media_type

    if isinstance(example, str) and not media_type.endswith("json"):
        raw = example
        language = "text"
    else:
        raw = json.dumps(example if example is not None else {}, indent=2, ensure_ascii=True)
        language = "json" if media_type == "application/json" or media_type.endswith("+json") else "text"

    return {
        "mode": "raw",
        "raw": raw,
        "options": {"raw": {"language": language}},
    }, media_type


def path_variable_name(parameter_name: str) -> str:
    return PATH_VARIABLE_ALIASES.get(parameter_name, parameter_name)


def build_url(
    document: Dict[str, Any],
    path: str,
    parameters: Iterable[Dict[str, Any]],
) -> Tuple[Dict[str, Any], List[str]]:
    rendered_path = path
    variables: List[str] = []
    query: List[Dict[str, Any]] = []

    for parameter in parameters:
        location = parameter.get("in")
        name = parameter.get("name")
        if not name:
            continue

        if location == "path":
            variable_name = path_variable_name(name)
            rendered_path = rendered_path.replace("{" + name + "}", "{{" + variable_name + "}}")
            variables.append(variable_name)
        elif location == "query":
            query_parameter: Dict[str, Any] = {
                "key": name,
                "value": parameter_example(document, parameter),
                "disabled": not bool(parameter.get("required")),
            }
            description = parameter.get("description")
            if description:
                query_parameter["description"] = description
            query.append(query_parameter)

    raw = RINGCX_BASE_URL + rendered_path
    if query:
        raw += "?" + "&".join(f"{item['key']}={item['value']}" for item in query)

    url: Dict[str, Any] = {
        "raw": raw,
        "host": [RINGCX_BASE_URL],
        "path": [part for part in rendered_path.lstrip("/").split("/") if part],
    }
    if query:
        url["query"] = query
    return url, variables


def auth_event(lines: List[str]) -> Dict[str, Any]:
    return {
        "listen": "test",
        "script": {"type": "text/javascript", "exec": lines},
    }


def request_id(method: str, path: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"ringcx:{method}:{path}"))


def make_url(base_url: str, path: str) -> Dict[str, Any]:
    return {
        "raw": base_url + path,
        "host": [base_url],
        "path": [part for part in path.lstrip("/").split("/") if part],
    }


def build_auth_folder() -> Dict[str, Any]:
    ringcentral_token = {
        "name": "1. Get RingCentral access token",
        "id": request_id("POST", "/restapi/oauth/token"),
        "request": {
            "method": "POST",
            "auth": {
                "type": "basic",
                "basic": [
                    {"key": "username", "value": "{{RINGCENTRAL_CLIENT_ID}}", "type": "string"},
                    {"key": "password", "value": "{{RINGCENTRAL_CLIENT_SECRET}}", "type": "string"},
                ],
            },
            "header": [
                {"key": "Accept", "value": "application/json", "type": "text"},
                {
                    "key": "Content-Type",
                    "value": "application/x-www-form-urlencoded",
                    "type": "text",
                },
            ],
            "body": {
                "mode": "urlencoded",
                "urlencoded": [
                    {
                        "key": "grant_type",
                        "value": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                        "type": "text",
                    },
                    {"key": "assertion", "value": "{{RINGCENTRAL_JWT}}", "type": "text"},
                ],
            },
            "url": make_url(RINGCENTRAL_BASE_URL, "/restapi/oauth/token"),
            "description": (
                "Uses the app client credentials and JWT from the selected environment to obtain "
                "a RingCentral access token. This token is used for the RingCX token exchange and "
                "RingCentral account UID lookup."
            ),
        },
        "event": [
            auth_event(
                [
                    "pm.test('RingCentral token request succeeds', function () {",
                    "  pm.response.to.have.status(200);",
                    "});",
                    "const body = pm.response.json();",
                    "pm.expect(body).to.have.property('access_token');",
                    "pm.environment.set('rco_access_token', body.access_token);",
                ]
            )
        ],
        "response": [],
    }

    exchange = {
        "name": "2. Exchange for RingCX access token",
        "id": request_id("POST", "/api/auth/login/rc/accesstoken"),
        "request": {
            "method": "POST",
            "auth": {"type": "noauth"},
            "header": [
                {"key": "Accept", "value": "application/json", "type": "text"},
                {
                    "key": "Content-Type",
                    "value": "application/x-www-form-urlencoded",
                    "type": "text",
                },
            ],
            "body": {
                "mode": "urlencoded",
                "urlencoded": [
                    {"key": "rcTokenType", "value": "Bearer", "type": "text"},
                    {"key": "rcAccessToken", "value": "{{rco_access_token}}", "type": "text"},
                ],
            },
            "url": make_url(RINGCX_BASE_URL, "/api/auth/login/rc/accesstoken"),
            "description": (
                "Exchanges the RingCentral access token for a RingCX access token. The exchange "
                "is limited to five requests per minute, and the returned RingCX token is valid "
                "for five minutes."
            ),
        },
        "event": [
            auth_event(
                [
                    "pm.test('RingCX token exchange succeeds', function () {",
                    "  pm.response.to.have.status(200);",
                    "});",
                    "const body = pm.response.json();",
                    "pm.expect(body).to.have.property('accessToken');",
                    "pm.environment.set('ringcx_bearer_token', body.accessToken);",
                    "pm.environment.set('rcev_access_token', body.accessToken);",
                    "pm.environment.set('ringcx_token_expires_at', String(Date.now() + (5 * 60 * 1000)));",
                ]
            )
        ],
        "response": [],
    }

    accounts = {
        "name": "3. Get RingCX account IDs",
        "id": request_id("GET", "/voice/api/v1/admin/accounts"),
        "request": {
            "method": "GET",
            "header": [{"key": "Accept", "value": "application/json", "type": "text"}],
            "url": make_url(RINGCX_BASE_URL, "/voice/api/v1/admin/accounts"),
            "description": (
                "Returns the RingCX accounts available to the authenticated user. The test script "
                "stores the first accountId as rcx_sub_account_id and its mainAccountId as "
                "rcx_main_account_id."
            ),
        },
        "event": [
            auth_event(
                [
                    "pm.test('RingCX accounts request succeeds', function () {",
                    "  pm.response.to.have.status(200);",
                    "});",
                    "const accounts = pm.response.json();",
                    "pm.expect(accounts).to.be.an('array').that.is.not.empty;",
                    "const account = accounts[0];",
                    "pm.expect(account).to.have.property('accountId');",
                    "pm.environment.set('rcx_sub_account_id', String(account.accountId));",
                    "if (account.mainAccountId !== undefined && account.mainAccountId !== null) {",
                    "  pm.environment.set('rcx_main_account_id', String(account.mainAccountId));",
                    "}",
                ]
            )
        ],
        "response": [],
    }

    ringcentral_uid = {
        "name": "4. Get RingCentral account UID",
        "id": request_id("GET", "/restapi/v1.0/account/~"),
        "request": {
            "method": "GET",
            "auth": {
                "type": "bearer",
                "bearer": [
                    {"key": "token", "value": "{{rco_access_token}}", "type": "string"}
                ],
            },
            "header": [{"key": "Accept", "value": "application/json", "type": "text"}],
            "url": make_url(RINGCENTRAL_BASE_URL, "/restapi/v1.0/account/~"),
            "description": (
                "Uses the RingCentral access token from step 1 to retrieve the RingCentral account "
                "UID used by RingCX CX integration paths."
            ),
        },
        "event": [
            auth_event(
                [
                    "pm.test('RingCentral account request succeeds', function () {",
                    "  pm.response.to.have.status(200);",
                    "});",
                    "const account = pm.response.json();",
                    "pm.expect(account).to.have.property('id');",
                    "pm.environment.set('rc_account_uid', String(account.id));",
                ]
            )
        ],
        "response": [],
    }

    return {
        "name": "Auth and setup",
        "description": (
            "Run these requests in order. They use environment variables and save only short-lived "
            "tokens and account identifiers to the selected Postman environment."
        ),
        "item": [ringcentral_token, exchange, accounts, ringcentral_uid],
    }


def success_response_example(
    document: Dict[str, Any],
    responses: Dict[str, Any],
    request: Dict[str, Any],
) -> List[Dict[str, Any]]:
    for code in sorted(responses, key=lambda item: (not item.isdigit(), item)):
        if not code.isdigit() or not 200 <= int(code) < 300:
            continue

        response = dereference(document, responses[code])
        if not isinstance(response, dict):
            continue
        media_type, media = choose_media(response.get("content") or {})
        if not media_type or not isinstance(media, dict):
            continue
        example = media_example(document, media, request=False)
        if example is None:
            continue

        body = example if isinstance(example, str) else json.dumps(example, indent=2, ensure_ascii=True)
        headers = [{"key": "Content-Type", "value": media_type}]
        return [
            {
                "name": f"{code} {response.get('description', 'Success')}",
                "originalRequest": copy.deepcopy(request),
                "status": response.get("description") or "Success",
                "code": int(code),
                "_postman_previewlanguage": "json" if media_type.endswith("json") else "text",
                "header": headers,
                "cookie": [],
                "body": body,
            }
        ]
    return []


def build_operation_item(
    document: Dict[str, Any],
    path: str,
    path_item: Dict[str, Any],
    method: str,
    operation: Dict[str, Any],
) -> Tuple[Dict[str, Any], List[str]]:
    parameters = merged_parameters(document, path_item, operation)
    url, path_variables = build_url(document, path, parameters)

    headers: List[Dict[str, Any]] = [
        {"key": "Accept", "value": "application/json", "type": "text"}
    ]
    for parameter in parameters:
        if parameter.get("in") != "header":
            continue
        name = parameter.get("name")
        if not name or name.lower() in ("authorization", "content-type"):
            continue
        header: Dict[str, Any] = {
            "key": name,
            "value": parameter_example(document, parameter),
            "type": "text",
            "disabled": not bool(parameter.get("required")),
        }
        if parameter.get("description"):
            header["description"] = parameter["description"]
        if name.lower() == "cookie" and header["value"].startswith("access_token="):
            header["value"] = "access_token={{ringcx_bearer_token}}"
        headers.append(header)

    request: Dict[str, Any] = {
        "method": method.upper(),
        "header": headers,
        "url": url,
        "description": operation.get("description") or operation.get("summary") or "",
    }

    if path == "/voice/api/v1/auth/login" or path.startswith("/voice/api/v1/summary/"):
        request["auth"] = {"type": "noauth"}

    request_body = operation.get("requestBody")
    if request_body is not None:
        body, media_type = build_body(document, request_body)
        if body is not None:
            request["body"] = body
        if media_type:
            headers.append({"key": "Content-Type", "value": media_type, "type": "text"})

    name = operation.get("summary") or operation.get("operationId") or f"{method.upper()} {path}"
    if operation.get("deprecated"):
        name = f"[Deprecated] {name}"
        request["description"] = (
            "Deprecated operation. " + (request.get("description") or "")
        ).strip()

    item: Dict[str, Any] = {
        "name": name,
        "id": request_id(method.upper(), path),
        "request": request,
        "response": success_response_example(document, operation.get("responses") or {}, request),
    }
    return item, path_variables


def add_unique_names(items: List[Dict[str, Any]]) -> None:
    counts: Dict[str, int] = {}
    for item in items:
        counts[item["name"]] = counts.get(item["name"], 0) + 1
    for item in items:
        if counts[item["name"]] > 1:
            item["name"] = f"{item['name']} [{item['request']['method']}]"


def build_collection(document: Dict[str, Any]) -> Tuple[Dict[str, Any], int, List[str]]:
    tag_descriptions = {
        tag["name"]: tag.get("description", "")
        for tag in document.get("tags") or []
        if isinstance(tag, dict) and tag.get("name")
    }
    tag_items: Dict[str, List[Dict[str, Any]]] = {}
    path_variables = set()
    operation_count = 0

    for path, path_item in (document.get("paths") or {}).items():
        for method in HTTP_METHODS:
            operation = path_item.get(method)
            if not isinstance(operation, dict):
                continue
            operation_count += 1
            if (method.upper(), path) in HELPER_OPERATIONS | LEGACY_ONLY_OPERATIONS:
                continue
            item, item_variables = build_operation_item(
                document, path, path_item, method, operation
            )
            path_variables.update(item_variables)
            tag = (operation.get("tags") or ["Other"])[0]
            tag_items.setdefault(tag, []).append(item)

    for items in tag_items.values():
        add_unique_names(items)

    groups = []
    used_tags = set()
    for group in document.get("x-tag-groups") or []:
        folders = []
        for tag in group.get("tags") or []:
            items = tag_items.get(tag)
            if not items:
                continue
            used_tags.add(tag)
            folder: Dict[str, Any] = {"name": tag, "item": items}
            if tag_descriptions.get(tag):
                folder["description"] = tag_descriptions[tag]
            folders.append(folder)
        if folders:
            groups.append({"name": group.get("name") or "Other", "item": folders})

    remaining_folders = []
    for tag in sorted(set(tag_items) - used_tags):
        folder = {"name": tag, "item": tag_items[tag]}
        if tag_descriptions.get(tag):
            folder["description"] = tag_descriptions[tag]
        remaining_folders.append(folder)
    if remaining_folders:
        groups.append({"name": "Other", "item": remaining_folders})

    variables = copy.deepcopy(COMMON_VARIABLES)
    existing_keys = {variable["key"] for variable in variables}
    for variable_name in sorted(path_variables):
        if variable_name not in existing_keys:
            variables.append({"key": variable_name, "value": "", "type": "default"})

    collection = {
        "info": {
            "name": "RingCentral RingCX Voice API",
            "description": (
                "Requests for the public RingCX Voice APIs. Import the companion environment "
                "template, configure JWT credentials, and run Auth and setup before calling API "
                "requests. Select requests individually; running the entire collection would "
                "invoke operations that create, update, or delete RingCX resources."
            ),
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "auth": {
            "type": "bearer",
            "bearer": [
                {"key": "token", "value": "{{ringcx_bearer_token}}", "type": "string"}
            ],
        },
        "variable": variables,
        "item": [build_auth_folder(), *groups],
    }
    return collection, operation_count, sorted(path_variables)


def build_environment() -> Dict[str, Any]:
    return {
        "name": "RingCX Voice API Environment",
        "values": [
            {**copy.deepcopy(variable), "enabled": True}
            for variable in COMMON_VARIABLES
        ],
        "_postman_variable_scope": "environment",
    }


def legacy_api_key_auth(token_variable: str = "legacy_auth_token") -> Dict[str, Any]:
    return {
        "type": "apikey",
        "apikey": [
            {"key": "key", "value": "X-Auth-Token", "type": "string"},
            {"key": "value", "value": "{{" + token_variable + "}}", "type": "string"},
            {"key": "in", "value": "header", "type": "string"},
        ],
    }


def build_legacy_collection() -> Dict[str, Any]:
    login = {
        "name": "1. Get temporary legacy auth token",
        "id": request_id("POST", "/legacy/v1/auth/login"),
        "request": {
            "method": "POST",
            "auth": {"type": "noauth"},
            "header": [
                {"key": "Accept", "value": "application/json", "type": "text"},
                {
                    "key": "Content-Type",
                    "value": "application/x-www-form-urlencoded",
                    "type": "text",
                },
            ],
            "body": {
                "mode": "urlencoded",
                "urlencoded": [
                    {"key": "username", "value": "{{legacy_username}}", "type": "text"},
                    {"key": "password", "value": "{{legacy_password}}", "type": "text"},
                    {"key": "stayLoggedIn", "value": "false", "type": "text"},
                ],
            },
            "url": make_url(LEGACY_BASE_URL, "/v1/auth/login"),
            "description": (
                "Authenticates a user on a legacy RingCX portal and stores the returned temporary "
                "authToken as legacy_auth_token. This request does not use bearer authentication."
            ),
        },
        "event": [
            auth_event(
                [
                    "pm.test('Legacy login succeeds', function () {",
                    "  pm.response.to.have.status(200);",
                    "});",
                    "const body = pm.response.json();",
                    "pm.expect(body).to.have.property('authToken');",
                    "pm.environment.set('legacy_auth_token', String(body.authToken));",
                ]
            )
        ],
        "response": [],
    }

    create_token = {
        "name": "2. Create permanent legacy API token",
        "id": request_id("POST", "/legacy/v1/admin/token"),
        "request": {
            "method": "POST",
            "header": [{"key": "Accept", "value": "text/plain", "type": "text"}],
            "url": make_url(LEGACY_BASE_URL, "/v1/admin/token"),
            "description": (
                "Creates a permanent API token for the authenticated legacy user and stores it as "
                "legacy_api_token. Each successful run creates another token."
            ),
        },
        "event": [
            auth_event(
                [
                    "pm.test('Legacy API token creation succeeds', function () {",
                    "  pm.response.to.have.status(200);",
                    "});",
                    "const token = pm.response.text().trim();",
                    "pm.expect(token).to.not.equal('');",
                    "pm.environment.set('legacy_api_token', token);",
                ]
            )
        ],
        "response": [],
    }

    list_tokens = {
        "name": "3. List legacy API tokens",
        "id": request_id("GET", "/legacy/v1/admin/token"),
        "request": {
            "method": "GET",
            "header": [{"key": "Accept", "value": "application/json", "type": "text"}],
            "url": make_url(LEGACY_BASE_URL, "/v1/admin/token"),
            "description": "Lists permanent API tokens owned by the authenticated legacy user.",
        },
        "event": [
            auth_event(
                [
                    "pm.test('Legacy API token list succeeds', function () {",
                    "  pm.response.to.have.status(200);",
                    "});",
                ]
            )
        ],
        "response": [],
    }

    test_token = {
        "name": "4. Test permanent legacy API token",
        "id": request_id("GET", "/legacy/v1/admin/users"),
        "request": {
            "method": "GET",
            "auth": legacy_api_key_auth("legacy_api_token"),
            "header": [{"key": "Accept", "value": "application/json", "type": "text"}],
            "url": make_url(LEGACY_BASE_URL, "/v1/admin/users"),
            "description": (
                "Calls a legacy API with legacy_api_token in the X-Auth-Token header. The user must "
                "have permission to retrieve users."
            ),
        },
        "event": [
            auth_event(
                [
                    "pm.test('Permanent legacy API token is accepted', function () {",
                    "  pm.response.to.have.status(200);",
                    "});",
                ]
            )
        ],
        "response": [],
    }

    delete_token = {
        "name": "5. Delete selected legacy API token",
        "id": request_id("DELETE", "/legacy/v1/admin/token/{token}"),
        "request": {
            "method": "DELETE",
            "header": [{"key": "Accept", "value": "application/json", "type": "text"}],
            "url": make_url(
                LEGACY_BASE_URL,
                "/v1/admin/token/{{legacy_api_token_to_delete}}",
            ),
            "description": (
                "Deletes only the token entered in legacy_api_token_to_delete. The value is blank "
                "by default to prevent an unintended deletion."
            ),
        },
        "event": [
            auth_event(
                [
                    "pm.test('Legacy API token deletion succeeds', function () {",
                    "  pm.expect(pm.response.code).to.be.oneOf([200, 204]);",
                    "});",
                ]
            )
        ],
        "response": [],
    }

    return {
        "info": {
            "name": "RingCentral RingCX Legacy Authentication",
            "description": (
                "Authentication helpers for RingCX deployments that use a legacy portal host and "
                "X-Auth-Token. Use the main RingCX Voice API collection for current deployments."
            ),
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "auth": legacy_api_key_auth(),
        "item": [
            {
                "name": "Legacy authentication",
                "description": (
                    "Choose the legacy portal host in the companion environment, configure the "
                    "legacy username and password, and run requests individually in order."
                ),
                "item": [login, create_token, list_tokens, test_token, delete_token],
            }
        ],
    }


def build_legacy_environment() -> Dict[str, Any]:
    return {
        "name": "RingCX Legacy Authentication Environment",
        "values": [
            {**copy.deepcopy(variable), "enabled": True}
            for variable in LEGACY_VARIABLES
        ],
        "_postman_variable_scope": "environment",
    }


def walk_items(items: Iterable[Dict[str, Any]]) -> Iterable[Dict[str, Any]]:
    for item in items:
        if "request" in item:
            yield item
        yield from walk_items(item.get("item") or [])


def validate_generated(
    document: Dict[str, Any],
    collection: Dict[str, Any],
    environment: Dict[str, Any],
    operation_count: int,
) -> List[str]:
    errors: List[str] = []
    requests = list(walk_items(collection.get("item") or []))
    expected_request_count = (
        operation_count - len(HELPER_OPERATIONS) - len(LEGACY_ONLY_OPERATIONS) + 4
    )
    if len(requests) != expected_request_count:
        errors.append(
            f"Expected {expected_request_count} requests, generated {len(requests)}"
        )

    request_ids = [item.get("id") for item in requests]
    if len(request_ids) != len(set(request_ids)):
        errors.append("Generated duplicate Postman request IDs")

    expected_operation_ids = {
        request_id(method.upper(), path)
        for path, path_item in (document.get("paths") or {}).items()
        for method in HTTP_METHODS
        if isinstance(path_item.get(method), dict)
    }
    actual_request_ids = set(request_ids)
    legacy_operation_ids = {
        request_id(method, path) for method, path in LEGACY_ONLY_OPERATIONS
    }
    missing_operation_ids = expected_operation_ids - actual_request_ids - legacy_operation_ids
    if missing_operation_ids:
        errors.append(
            f"Generated collection is missing {len(missing_operation_ids)} OpenAPI operations"
        )

    extra_request_ids = actual_request_ids - expected_operation_ids
    if len(extra_request_ids) != 2:
        errors.append(
            "Generated collection must contain exactly two non-OpenAPI RingCentral setup requests"
        )

    requests_by_id = {item["id"]: item for item in requests}
    for path, path_item in (document.get("paths") or {}).items():
        referenced_parameters = set(re.findall(r"\{([^{}]+)\}", path))
        rendered_path = path
        for parameter_name in referenced_parameters:
            rendered_path = rendered_path.replace(
                "{" + parameter_name + "}",
                "{{" + path_variable_name(parameter_name) + "}}",
            )

        for method in HTTP_METHODS:
            if not isinstance(path_item.get(method), dict):
                continue
            declared_parameters = {
                parameter.get("name")
                for parameter in merged_parameters(document, path_item, path_item[method])
                if parameter.get("in") == "path"
            }
            missing_parameters = referenced_parameters - declared_parameters
            if missing_parameters:
                errors.append(
                    f"{method.upper()} {path}: missing path parameter definitions for "
                    + ", ".join(sorted(missing_parameters))
                )
            item = requests_by_id.get(request_id(method.upper(), path))
            if not item:
                continue
            request = item["request"]
            if request.get("method") != method.upper():
                errors.append(f"{method.upper()} {path}: generated method does not match")
            generated_url = (request.get("url") or {}).get("raw", "").split("?", 1)[0]
            expected_url = RINGCX_BASE_URL + rendered_path
            if generated_url != expected_url:
                errors.append(
                    f"{method.upper()} {path}: generated URL does not match OpenAPI path"
                )

    serialized = json.dumps(collection, ensure_ascii=True)
    forbidden_fragments = (
        "https://engage.ringcentral.com",
        ".lab.engage.",
        ".int.ringcentral.com",
        "<Error: Too many levels of nesting",
    )
    for fragment in forbidden_fragments:
        if fragment in serialized:
            errors.append(f"Generated collection contains forbidden fragment: {fragment}")

    for item in requests:
        request = item["request"]
        body = request.get("body") or {}
        if body.get("mode") == "raw":
            options = body.get("options") or {}
            language = (options.get("raw") or {}).get("language")
            if language == "json":
                try:
                    json.loads(body.get("raw") or "")
                except json.JSONDecodeError as error:
                    errors.append(f"{item.get('name')}: invalid JSON body: {error}")

    environment_values = {
        value.get("key"): value.get("value") for value in environment.get("values") or []
    }
    for key in SECRET_VARIABLE_KEYS:
        if environment_values.get(key):
            errors.append(f"Environment secret variable {key} must be blank")

    spec_operation_count = sum(
        1
        for path_item in (document.get("paths") or {}).values()
        for method in HTTP_METHODS
        if isinstance(path_item.get(method), dict)
    )
    if spec_operation_count != operation_count:
        errors.append("OpenAPI operation count changed while generating the collection")

    return errors


def validate_legacy_generated(
    collection: Dict[str, Any], environment: Dict[str, Any]
) -> List[str]:
    errors: List[str] = []
    requests = list(walk_items(collection.get("item") or []))

    if len(requests) != 5:
        errors.append(f"Expected 5 legacy auth requests, generated {len(requests)}")

    request_ids = [item.get("id") for item in requests]
    if len(request_ids) != len(set(request_ids)):
        errors.append("Generated duplicate legacy Postman request IDs")

    collection_auth = collection.get("auth") or {}
    if collection_auth.get("type") != "apikey":
        errors.append("Legacy collection must use API key authentication")
    auth_values = {
        item.get("key"): item.get("value")
        for item in collection_auth.get("apikey") or []
    }
    if auth_values.get("key") != "X-Auth-Token":
        errors.append("Legacy collection must send X-Auth-Token")

    for item in requests:
        request = item.get("request") or {}
        raw_url = (request.get("url") or {}).get("raw", "")
        if not raw_url.startswith(LEGACY_BASE_URL + "/v1/"):
            errors.append(f"{item.get('name')}: legacy URL is not rooted at legacy_base_url")

        auth = request.get("auth") or {}
        if auth.get("type") == "bearer":
            errors.append(f"{item.get('name')}: legacy request must not use bearer auth")
        for header in request.get("header") or []:
            if str(header.get("key", "")).lower() == "authorization":
                errors.append(
                    f"{item.get('name')}: legacy request must not send Authorization"
                )

    login_request = next(
        (item for item in requests if item.get("name", "").startswith("1.")), None
    )
    if not login_request or (login_request.get("request") or {}).get("auth") != {
        "type": "noauth"
    }:
        errors.append("Legacy login request must explicitly disable authentication")

    serialized = json.dumps(collection, ensure_ascii=True)
    for fragment in (
        "https://ringcx.ringcentral.com",
        "https://engage.ringcentral.com",
        "/voice/api/",
    ):
        if fragment in serialized:
            errors.append(f"Legacy collection contains current-host fragment: {fragment}")

    environment_values = {
        value.get("key"): value.get("value") for value in environment.get("values") or []
    }
    for key in LEGACY_SECRET_VARIABLE_KEYS:
        if environment_values.get(key):
            errors.append(f"Legacy environment secret variable {key} must be blank")

    return errors


def compare_file(path: Path, expected: Dict[str, Any]) -> bool:
    if not path.exists():
        print(f"Missing generated file: {path.relative_to(ROOT)}", file=sys.stderr)
        return False
    actual = load_json(path)
    if actual != expected:
        print(
            f"Generated file is stale: {path.relative_to(ROOT)}. "
            "Run python3 scripts/generate_postman.py.",
            file=sys.stderr,
        )
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify that checked-in Postman artifacts match the generator output.",
    )
    args = parser.parse_args()

    document = load_json(SPEC_PATH)
    collection, operation_count, path_variables = build_collection(document)
    environment = build_environment()
    legacy_collection = build_legacy_collection()
    legacy_environment = build_legacy_environment()

    errors = validate_generated(document, collection, environment, operation_count)
    errors.extend(validate_legacy_generated(legacy_collection, legacy_environment))
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    if args.check:
        current = compare_file(COLLECTION_PATH, collection)
        current = compare_file(ENVIRONMENT_PATH, environment) and current
        current = compare_file(LEGACY_COLLECTION_PATH, legacy_collection) and current
        current = compare_file(LEGACY_ENVIRONMENT_PATH, legacy_environment) and current
        if not current:
            return 1
    else:
        write_json(COLLECTION_PATH, collection)
        write_json(ENVIRONMENT_PATH, environment)
        write_json(LEGACY_COLLECTION_PATH, legacy_collection)
        write_json(LEGACY_ENVIRONMENT_PATH, legacy_environment)

    request_count = (
        operation_count - len(HELPER_OPERATIONS) - len(LEGACY_ONLY_OPERATIONS) + 4
    )
    print(
        f"Postman collections are current: {operation_count} OpenAPI operations, "
        f"{request_count} current requests, 5 legacy auth requests, "
        f"{len(path_variables)} path variables."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
