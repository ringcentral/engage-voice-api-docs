# Queue Events

Queue events define what callers experience while waiting in a queue. Use them for hold music, announcements, wait-time behavior, DTMF input, and priority handling for special caller scenarios.

## Core Concepts

Queue events belong to a specific queue. The API path uses `gateQueueEvents` because queues are represented as `gates` in the API.

Priority queue events can be used when specific conditions apply, such as a queue being closed, a queue reaching capacity, or a caller matching a special ANI rule. DTMF events can be attached to a queue event when callers need keypad options during the queue experience.

## Manage Queue Events

| Operation | Method and path |
| --- | --- |
| List queue events | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents` |
| Get queue event | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents/{eventId}` |
| Create queue events | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents` |
| Update queue events | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents` |
| Update one queue event | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents/{eventId}` |
| Delete queue event | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents/{eventId}` |

## Create or Update Queue Events

Create and batch-update queue events by sending an array of event objects.

```http
POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents
Authorization: Bearer <ringcxAccessToken>
Content-Type: application/json
```

```json
[
  {
    "eventRank": 0,
    "queueEvent": "PLAY-AUDIO-LOOP:holdmusic",
    "eventDuration": 120,
    "enableDtmf": 0
  },
  {
    "eventRank": 1,
    "queueEvent": "END-CALL:true",
    "eventDuration": 0,
    "enableDtmf": 0
  }
]
```

### Common Fields

| Field | Required | Description |
| --- | --- | --- |
| `eventId` | No | Queue event ID. Omit it when creating a new event. |
| `eventRank` | Yes | Order in which queue events are evaluated or played. |
| `queueEvent` | No | Event action or audio behavior. |
| `eventDuration` | No | Duration, in seconds, for time-based queue event behavior. |
| `enableDtmf` | No | Whether the event accepts DTMF input. |
| `active` | No | Whether the event is active. |

## Retrieve Queue Events

```http
GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents
Authorization: Bearer <ringcxAccessToken>
Accept: application/json
```

Use the returned `eventId` values when updating or deleting a single queue event.

## DTMF Events

DTMF events belong to a queue event and define keypad behavior for callers.

| Operation | Method and path |
| --- | --- |
| List DTMF events | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents/{eventId}/gateQueueDtmfEvents` |
| Create DTMF events | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents/{eventId}/gateQueueDtmfEvents` |
| Update DTMF events | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents/{eventId}/gateQueueDtmfEvents` |
| Update one DTMF event | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents/{eventId}/gateQueueDtmfEvents/{dtmfEventId}` |
| Delete DTMF event | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents/{eventId}/gateQueueDtmfEvents/{dtmfEventId}` |

Configure the parent queue event before adding DTMF options.
