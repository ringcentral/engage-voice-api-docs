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
| Save queue events | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents` |
| Update one queue event | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents/{eventId}` |
| Delete queue event | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents/{eventId}` |

## SDK Setup

SDK examples in this article use JWT authentication and load credentials from environment variables.

=== "JavaScript"

    ```bash
    npm install ringcentral-engage-voice-client dotenv
    ```

=== "Python"

    ```bash
    pip3 install ringcentral_engage_voice python-dotenv
    ```

Create a `.env` file in the directory where you run the sample:

```text
RC_CLIENT_ID=<clientId>
RC_CLIENT_SECRET=<clientSecret>
RC_JWT=<jwt>
```

The SDK wrapper reads these values, signs in with RingCentral, and exchanges the RingCentral access token for a RingCX access token before calling RingCX APIs.

## Save Queue Events

Create and batch-update queue events by saving the queue's event list.

=== "HTTP"

    ```http
    PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents
    Authorization: Bearer <ringcxAccessToken>
    Content-Type: application/json

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

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    gate_group_id = "<gateGroupId>"
    gate_id = "<gateId>"
    access_token = "<ringcxAccessToken>"
    payload = [
        {
            "eventRank": 0,
            "queueEvent": "PLAY-AUDIO-LOOP:holdmusic",
            "eventDuration": 120,
            "enableDtmf": 0,
        },
        {
            "eventRank": 1,
            "queueEvent": "END-CALL:true",
            "eventDuration": 0,
            "enableDtmf": 0,
        },
    ]

    response = requests.put(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/gateGroups/{gate_group_id}/gates/{gate_id}/gateQueueEvents",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        json=payload,
    )
    response.raise_for_status()
    print(response.json())
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const gateGroupId = "<gateGroupId>";
    const gateId = "<gateId>";
    const accessToken = "<ringcxAccessToken>";
    const payload = [
      {
        eventRank: 0,
        queueEvent: "PLAY-AUDIO-LOOP:holdmusic",
        eventDuration: 120,
        enableDtmf: 0
      },
      {
        eventRank: 1,
        queueEvent: "END-CALL:true",
        eventDuration: 0,
        enableDtmf: 0
      }
    ];

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/gateGroups/${gateGroupId}/gates/${gateId}/gateQueueEvents`,
      {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      }
    );

    if (!response.ok) throw new Error(await response.text());
    console.log(await response.json());
    ```

=== "JavaScript SDK"

    ```javascript
    const EngageVoice = require("ringcentral-engage-voice-client").default;
    require("dotenv").config();

    async function main() {
      const ev = new EngageVoice({
        clientId: process.env.RC_CLIENT_ID,
        clientSecret: process.env.RC_CLIENT_SECRET
      });

      await ev.authorize({ jwt: process.env.RC_JWT });

      const payload = [
        {
          eventRank: 0,
          queueEvent: "PLAY-AUDIO-LOOP:holdmusic",
          eventDuration: 120,
          enableDtmf: 0
        },
        {
          eventRank: 1,
          queueEvent: "END-CALL:true",
          eventDuration: 0,
          enableDtmf: 0
        }
      ];

      const response = await ev.put(
        "/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents",
        payload
      );
      console.log(response.data);
    }

    main().catch(console.error);
    ```

=== "Python SDK"

    ```python
    import os
    from dotenv import load_dotenv
    from ringcentral_engage_voice import RingCentralEngageVoice

    load_dotenv()

    ev = RingCentralEngageVoice(
        os.environ["RC_CLIENT_ID"],
        os.environ["RC_CLIENT_SECRET"],
    )
    ev.authorize(jwt=os.environ["RC_JWT"])

    payload = [
        {
            "eventRank": 0,
            "queueEvent": "PLAY-AUDIO-LOOP:holdmusic",
            "eventDuration": 120,
            "enableDtmf": 0,
        },
        {
            "eventRank": 1,
            "queueEvent": "END-CALL:true",
            "eventDuration": 0,
            "enableDtmf": 0,
        },
    ]

    response = ev.put(
        "/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents",
        payload,
    ).json()
    print(response)
    ```

??? example "Response example"

    ```json
    [
      {
        "eventId": 67882,
        "eventRank": 0,
        "queueEvent": "PLAY-AUDIO-LOOP:holdmusic",
        "eventDuration": 120,
        "enableDtmf": 0
      },
      {
        "eventId": 67883,
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

=== "HTTP"

    ```http
    GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents
    Authorization: Bearer <ringcxAccessToken>
    Accept: application/json
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    gate_group_id = "<gateGroupId>"
    gate_id = "<gateId>"
    access_token = "<ringcxAccessToken>"

    response = requests.get(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/gateGroups/{gate_group_id}/gates/{gate_id}/gateQueueEvents",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        },
    )
    response.raise_for_status()
    print(response.json())
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const gateGroupId = "<gateGroupId>";
    const gateId = "<gateId>";
    const accessToken = "<ringcxAccessToken>";

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/gateGroups/${gateGroupId}/gates/${gateId}/gateQueueEvents`,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
          Accept: "application/json"
        }
      }
    );

    if (!response.ok) throw new Error(await response.text());
    console.log(await response.json());
    ```

=== "JavaScript SDK"

    ```javascript
    const EngageVoice = require("ringcentral-engage-voice-client").default;
    require("dotenv").config();

    async function main() {
      const ev = new EngageVoice({
        clientId: process.env.RC_CLIENT_ID,
        clientSecret: process.env.RC_CLIENT_SECRET
      });

      await ev.authorize({ jwt: process.env.RC_JWT });

      const response = await ev.get(
        "/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents"
      );
      console.log(response.data);
    }

    main().catch(console.error);
    ```

=== "Python SDK"

    ```python
    import os
    from dotenv import load_dotenv
    from ringcentral_engage_voice import RingCentralEngageVoice

    load_dotenv()

    ev = RingCentralEngageVoice(
        os.environ["RC_CLIENT_ID"],
        os.environ["RC_CLIENT_SECRET"],
    )
    ev.authorize(jwt=os.environ["RC_JWT"])

    response = ev.get(
        "/api/v1/admin/accounts/{accountId}/gateGroups/{gateGroupId}/gates/{gateId}/gateQueueEvents"
    ).json()
    print(response)
    ```

Use the returned `eventId` values when updating or deleting a single queue event.

??? example "Response example"

    ```json
    [
      {
        "eventId": 67882,
        "eventRank": 0,
        "queueEvent": "PLAY-AUDIO-LOOP:holdmusic",
        "eventDuration": 120,
        "enableDtmf": 0
      }
    ]
    ```

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
