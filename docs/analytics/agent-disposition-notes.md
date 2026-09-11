# Agent Disposition Notes

Agent disposition notes capture the outcome and free-text notes an agent records for an interaction. Use these endpoints to set notes while a call is being dispositioned, read notes after a call is archived, or update notes for an outbound campaign pass.

## Choose an Endpoint

| Goal | Endpoint |
| --- | --- |
| Set disposition and notes for a live call | `POST /voice/api/v1/admin/accounts/{accountId}/activeCalls/{uii}/dispositionCall` |
| Read disposition and notes after a call is archived | `GET /voice/api/v1/admin/accounts/{accountId}/callHistory/{uii}` |
| List outbound campaign passes for a lead | `GET /voice/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns/{campaignId}/leads/{leadId}/passes` |
| Update disposition and notes for an outbound campaign pass | `PUT /voice/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns/{campaignId}/leads/{leadId}/passes/{passUii}/agentNotesAndDisposition` |

## Requirements

* Use a RingCX access token. For authentication details, see [RingCentral authentication](../authentication/auth-ringcentral.md).
* Use the RingCX sub-account ID as `accountId`.
* Obtain the UII from [Listing Active Calls](active-calls/index.md#listing-active-calls) while the call is active, and retain it for call-level updates and archived call-history retrieval.
* Disposition values must already exist in the account, queue, or campaign configuration that applies to the interaction.
* URL-encode query parameter values, especially free-text notes.

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

## Read Notes for an Archived Call

After a call is archived, use the call history endpoint to retrieve the disposition and notes associated with the UII.

=== "HTTP"

    ```http
    GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/callHistory/{uii}
    Authorization: Bearer <ringcxAccessToken>
    Accept: application/json
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
        "/api/v1/admin/accounts/{accountId}/callHistory/{uii}"
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

    response = ev.get("/api/v1/admin/accounts/{accountId}/callHistory/{uii}")
    print(response.json())
    ```

The response includes call-level fields such as `agentDisposition` and session-level history in `activeCallSessionHistories`. Session history records can include `agentNotes`.

??? example "Response example"

    ```json
    {
      "accountId": "12345678",
      "uii": "202605051013071101050000000902",
      "agentDisposition": "SALE",
      "activeCallSessionHistories": [
        {
          "sessionId": "1",
          "agentNotes": "Customer requested follow-up."
        }
      ]
    }
    ```

## Set Notes for a Live Call

Use `dispositionCall` when an active or pending-disposition call needs to be completed with an agent disposition and optional notes.

```http
POST https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/activeCalls/{uii}/dispositionCall?disposition=SALE&callback=false&notes=Customer%20requested%20follow-up
Authorization: Bearer <ringcxAccessToken>
Accept: application/json
```

| Parameter | Requirement | Description |
| --- | --- | --- |
| `disposition` | Required | Preconfigured disposition value to store on the call. |
| `callback` | Required | Use `true` when the disposition schedules a callback. |
| `callBackDTS` | Required when `callback=true` | Callback date and time in `yyyyMMddHHmmss` format. |
| `notes` | Optional | Free-text notes to store with the disposition record. |

The endpoint returns `true` when the update succeeds.

??? example "Response example"

    ```json
    true
    ```

## Read or Update Outbound Campaign Pass Notes

For outbound campaign leads, notes can also be stored on a campaign pass. List passes for the lead first, then update the target `passUii`.

```http
GET https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns/{campaignId}/leads/{leadId}/passes
Authorization: Bearer <ringcxAccessToken>
Accept: application/json
```

??? example "Response example"

    ```json
    [
      {
        "passUii": "202605051013071101050000000902",
        "agentDisposition": "SALE",
        "agentNotes": "Customer requested follow-up."
      }
    ]
    ```

To update a pass:

```http
PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns/{campaignId}/leads/{leadId}/passes/{passUii}/agentNotesAndDisposition?agentDisposition=SALE&agentNotes=Customer%20requested%20follow-up
Authorization: Bearer <ringcxAccessToken>
Accept: application/json
```

The response is the updated `CampaignPass`.

## Permissions

| Endpoint | Required RingCX permission |
| --- | --- |
| `POST /activeCalls/{uii}/dispositionCall` | `READ` on Account (Permission Override) |
| `GET /callHistory/{uii}` | `READ` on Account |
| `GET /passes` | `READ` on Campaign |
| `PUT /agentNotesAndDisposition` | `UPDATE` on Campaign |

## Examples

=== "HTTP"
    ```http
    PUT https://ringcx.ringcentral.com/voice/api/v1/admin/accounts/12345678/dialGroups/1001/campaigns/2002/leads/3003/passes/202605051013071101050000000902/agentNotesAndDisposition?agentDisposition=SALE&agentNotes=Customer%20requested%20follow-up
    Authorization: Bearer <ringcxAccessToken>
    Accept: application/json
    ```

=== "Python"
    ```python
    import os
    import requests

    base_url = "https://ringcx.ringcentral.com/voice/api/v1/admin/accounts"
    token = os.environ["RINGCX_ACCESS_TOKEN"]

    account_id = "12345678"
    dial_group_id = 1001
    campaign_id = 2002
    lead_id = 3003
    pass_uii = "202605051013071101050000000902"

    url = (
        f"{base_url}/{account_id}/dialGroups/{dial_group_id}"
        f"/campaigns/{campaign_id}/leads/{lead_id}"
        f"/passes/{pass_uii}/agentNotesAndDisposition"
    )
    params = {
        "agentDisposition": "SALE",
        "agentNotes": "Customer requested follow-up.",
    }
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    response = requests.put(url, params=params, headers=headers)
    response.raise_for_status()
    print(response.json())
    ```

=== "JavaScript"
    ```javascript
    const baseUrl = "https://ringcx.ringcentral.com/voice/api/v1/admin/accounts";
    const token = process.env.RINGCX_ACCESS_TOKEN;

    const accountId = "12345678";
    const dialGroupId = 1001;
    const campaignId = 2002;
    const leadId = 3003;
    const passUii = "202605051013071101050000000902";

    const url = new URL(
      `${baseUrl}/${accountId}/dialGroups/${dialGroupId}` +
        `/campaigns/${campaignId}/leads/${leadId}` +
        `/passes/${passUii}/agentNotesAndDisposition`
    );
    url.search = new URLSearchParams({
      agentDisposition: "SALE",
      agentNotes: "Customer requested follow-up.",
    });

    const response = await fetch(url, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`Request failed: ${response.status}`);
    }

    console.log(await response.json());
    ```
