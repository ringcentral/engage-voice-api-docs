# Audio Files APIs

The Audio Files APIs let you manage account-level audio files that can be used by RingCX routing experiences, such as queue prompts, hold music, IVR audio, and agent whisper audio.

This page covers customer-managed account audio files. It does not cover global audio file administration or deprecated audio streaming endpoints.

## Common Use Cases

* Upload prompt audio from an external content management workflow.
* List audio files before assigning them to queue, IVR, or routing configuration.
* Rename an audio asset while keeping account-level file management automated.
* Download an audio file as MP3 for preview or quality review.
* Remove unused account audio files after confirming they are no longer referenced.

## Authentication and Permissions

Use the standard RingCX authentication flow and send the RingCX access token in the `Authorization` header.

```http
Authorization: Bearer <ringcxAccessToken>
```

The authenticating user must have the RingCX administrative permissions required by the operation.

| Operation | Required permissions |
| --- | --- |
| List audio files | `READ` on Account, `READ` on Utilities |
| Upload audio file | `READ` on Account (permission override), `CREATE` on Utilities |
| Rename audio file | `READ` on Account (permission override), `UPDATE` on Utilities |
| Download audio file as MP3 | `READ` on Account, `READ` on Utilities |
| Delete audio file | `READ` on Account (permission override), `DELETE` on Utilities |

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

The SDK wrapper reads these values, signs in with RingCentral, and exchanges the RingCentral access token for a RingCX access token before calling RingCX APIs. For multipart upload and binary download, use the HTTP client examples to control file streams directly.

## Endpoints

| Operation | Method and Path | API Reference |
| --- | --- | --- |
| List audio files | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/utilities/audioFiles` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Audio-Files/getAccountAudioFiles) |
| Upload audio file | `POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/utilities/audioFiles` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Audio-Files/uploadAudioFile) |
| Rename audio file | `PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/utilities/audioFiles/{fileName}/rename` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Audio-Files/renameLocalAudioFile) |
| Download audio file as MP3 | `GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/utilities/audioFiles/{fileName}/mp3` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Audio-Files/listenToAudioFile) |
| Delete audio file | `DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/utilities/audioFiles/{fileName}/remove` | [Reference](https://developers.ringcentral.com/engage/voice/api-reference/Audio-Files/deleteLocalAudioFile) |

## File Names

The `AudioFileView` response returns `fileName` without the file extension. Use that returned `fileName` value when referencing the file in other RingCX configuration and when calling the rename, download, or delete endpoints.

When `fileName` is part of the URL path, URL-encode it. The `newFileName` value for rename is passed as a query parameter and should be the new base file name, without a file extension or path separators.

!!! warning
    Deleting or renaming an audio file can affect queue events, IVR scripts, workflows, or other routing configuration that references the file. Confirm references before changing files used in production.

## Recommended Workflow

1. List existing audio files to avoid duplicate names.
2. Upload the new audio file as `multipart/form-data`.
3. Store the returned `fileName`.
4. Reference that `fileName` in the RingCX routing configuration that uses the audio asset.
5. Preview the audio through the MP3 download endpoint when needed.
6. Rename or delete files only after confirming the file is not used by active routing configuration.

## List Audio Files

=== "HTTP"

    ```http
    GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/utilities/audioFiles
    Authorization: Bearer <ringcxAccessToken>
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    access_token = "<ringcxAccessToken>"

    response = requests.get(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/utilities/audioFiles",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response.raise_for_status()
    print(response.json())
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const accessToken = "<ringcxAccessToken>";

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/utilities/audioFiles`,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`
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
        "/api/v1/admin/accounts/{accountId}/utilities/audioFiles"
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

    response = ev.get("/api/v1/admin/accounts/{accountId}/utilities/audioFiles")
    print(response.json())
    ```

??? example "Response example"

    ```json
    [
      {
        "fileName": "support_hold_music",
        "fileSize": 184320,
        "lastModified": "2026-07-24T18:22:10Z"
      }
    ]
    ```

## Upload an Audio File

Send the audio file as `multipart/form-data`. Do not set the multipart `Content-Type` boundary manually; let your HTTP client set it.

Use the `uploadFileName` query parameter when the stored file name should differ from the local file name. Use `audioName` when the audio asset needs a display name for multilingual audio matching.

=== "HTTP"

    ```bash
    curl -X POST \
      "https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/utilities/audioFiles" \
      -H "Authorization: Bearer <ringcxAccessToken>" \
      -F "file=@support-hold-music.mp3"
    ```

=== "Python"

    ```python
    import requests

    account_id = "<accountId>"
    access_token = "<ringcxAccessToken>"

    with open("support-hold-music.mp3", "rb") as audio_file:
        response = requests.post(
            f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/utilities/audioFiles",
            headers={"Authorization": f"Bearer {access_token}"},
            files={"file": ("support-hold-music.mp3", audio_file, "audio/mpeg")},
        )

    response.raise_for_status()
    print(response.json())
    ```

=== "JavaScript"

    ```javascript
    import { readFile } from "node:fs/promises";

    const accountId = "<accountId>";
    const accessToken = "<ringcxAccessToken>";
    const bytes = await readFile("support-hold-music.mp3");
    const form = new FormData();
    form.append("file", new Blob([bytes], { type: "audio/mpeg" }), "support-hold-music.mp3");

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/utilities/audioFiles`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${accessToken}`
        },
        body: form
      }
    );

    if (!response.ok) throw new Error(await response.text());
    console.log(await response.json());
    ```

??? example "Response example"

    ```json
    {
      "fileName": "support-hold-music",
      "fileSize": 184320,
      "lastModified": "2026-07-24T18:22:10Z"
    }
    ```

## Rename an Audio File

The rename endpoint uses a query parameter for the new file name and does not require a request body.

=== "HTTP"

    ```http
    PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/utilities/audioFiles/{fileName}/rename?newFileName=support_hold_music_v2
    Authorization: Bearer <ringcxAccessToken>
    ```

=== "Python"

    ```python
    import requests
    from urllib.parse import quote

    account_id = "<accountId>"
    file_name = "support_hold_music"
    access_token = "<ringcxAccessToken>"

    response = requests.put(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/utilities/audioFiles/{quote(file_name, safe='')}/rename",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"newFileName": "support_hold_music_v2"},
    )
    response.raise_for_status()
    print(response.json())
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const fileName = "support_hold_music";
    const accessToken = "<ringcxAccessToken>";
    const params = new URLSearchParams({ newFileName: "support_hold_music_v2" });

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/utilities/audioFiles/${encodeURIComponent(fileName)}/rename?${params}`,
      {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      }
    );

    if (!response.ok) throw new Error(await response.text());
    console.log(await response.json());
    ```

??? example "Response example"

    ```json
    {
      "fileName": "support_hold_music_v2",
      "fileSize": 184320,
      "lastModified": "2026-07-24T18:25:40Z"
    }
    ```

## Download an Audio File as MP3

Use this endpoint to preview or retrieve an account audio file as an MP3 stream.

=== "HTTP"

    ```bash
    curl -X GET \
      "https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/utilities/audioFiles/{fileName}/mp3" \
      -H "Authorization: Bearer <ringcxAccessToken>" \
      --output support-hold-music.mp3
    ```

=== "Python"

    ```python
    import requests
    from urllib.parse import quote

    account_id = "<accountId>"
    file_name = "support_hold_music"
    access_token = "<ringcxAccessToken>"

    response = requests.get(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/utilities/audioFiles/{quote(file_name, safe='')}/mp3",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response.raise_for_status()

    with open("support-hold-music.mp3", "wb") as audio_file:
        audio_file.write(response.content)
    ```

=== "JavaScript"

    ```javascript
    import { writeFile } from "node:fs/promises";

    const accountId = "<accountId>";
    const fileName = "support_hold_music";
    const accessToken = "<ringcxAccessToken>";

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/utilities/audioFiles/${encodeURIComponent(fileName)}/mp3`,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      }
    );

    if (!response.ok) throw new Error(await response.text());
    await writeFile("support-hold-music.mp3", Buffer.from(await response.arrayBuffer()));
    ```

## Delete an Audio File

=== "HTTP"

    ```http
    DELETE https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/utilities/audioFiles/{fileName}/remove
    Authorization: Bearer <ringcxAccessToken>
    ```

=== "Python"

    ```python
    import requests
    from urllib.parse import quote

    account_id = "<accountId>"
    file_name = "support_hold_music_v2"
    access_token = "<ringcxAccessToken>"

    response = requests.delete(
        f"https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{account_id}/utilities/audioFiles/{quote(file_name, safe='')}/remove",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response.raise_for_status()
    print(response.json())
    ```

=== "JavaScript"

    ```javascript
    const accountId = "<accountId>";
    const fileName = "support_hold_music_v2";
    const accessToken = "<ringcxAccessToken>";

    const response = await fetch(
      `https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/${accountId}/utilities/audioFiles/${encodeURIComponent(fileName)}/remove`,
      {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${accessToken}`
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

      const response = await ev.delete(
        "/api/v1/admin/accounts/{accountId}/utilities/audioFiles/support_hold_music_v2/remove"
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

    response = ev.delete(
        "/api/v1/admin/accounts/{accountId}/utilities/audioFiles/support_hold_music_v2/remove"
    )
    print(response.json())
    ```

??? example "Response example"

    ```json
    true
    ```

## Resource Schema

| Field | Type | Description |
| --- | --- | --- |
| `fileName` | String | Stored audio file name without the file extension. |
| `fileSize` | Integer | File size in bytes. |
| `lastModified` | Date-time | Timestamp when the audio file was last modified. |
| `auditMetadata` | Object | Audit metadata associated with the audio file, when present. |

## Common Errors

| Status | Cause | Resolution |
| --- | --- | --- |
| `400 Bad Request` | The uploaded file type or rename value is invalid. | Use a supported audio file and a simple base file name. |
| `403 Forbidden` | The authenticated user does not have the required Utilities permission. | Grant the matching Utilities permission for the operation. |
| `404 Not Found` | The account or audio file does not exist. | List audio files first and use the returned `fileName`. |
