# Getting Started with Call Streaming

!!!important
    Please work with your RingCentral representative to activate Call Streaming service for your organization.

**Call Streaming** runs alongside [Call Recording](./../../call-recording). It streams real-time stereo audio to your WebSocket Secure(WSS) server, which can then be used for services like Speech Analysis etc.

**Call Streaming** requires a WSS server built and hosted by you. The server is to receive audio streams for further processing. [Quick start guide](#quick-start-guide) and [sample code](#step3-host-local-server) are provided below.

## Workflow Overview

<img class="img-fluid" width="100%" src="../../../images/call-streaming.png">

## Quick Start Guide

The following guide helps you quickly setup your local WebSocket server to try out Call Streaming by doing live transcription.

Overall, we want to:

- <img class="img-fluid" width="18px" src="../../../images/icons/new_file_icon.svg"> Create a streaming profile so we know where to stream call audio data to
- <img class="img-fluid" width="18px" src="../../../images/icons/computer_icon.svg"> Host a WebSocket server locally
- <img class="img-fluid" width="18px" src="../../../images/icons/phone_icon.svg"> Test it with an actual call

### Prerequisites

There are many live transcribe service providers. Here we use [Google Cloud Speech To Text](https://cloud.google.com/speech-to-text/docs) service as an example.

- [Google Cloud Account](https://cloud.google.com/)
- [Enable Google Speech To Text Service](https://console.cloud.google.com/speech/overview)
- [Google Service Account](https://cloud.google.com/docs/authentication/getting-started)

### Step.1 Start local server

After above setup, you will get a JSON key file in your local drive. Copy the path(including file name) as `keyFilePath`.

#### Nodejs(recommended)

- Create a new folder and do `npm init`
- Install a simple test package `npm i ev-audio-streaming-transcription`
- Create a new file `server.js` as below

```
const { default: runServer } = require('ev-audio-streaming-transcription');

const port = 3333;
// fill in value with your keyFilePath
const keyFilePath = ;
runServer(port, keyFilePath);
```

- `node server.js`

And you will get a WSS address which will be used later as `{streamingUrl}`.

#### Python

- Create a new folder and install a simple test package `pip install ev_audio_streaming_transcription_py`
- Create a new file `server.py` as below

```
from ev_audio_streaming_transcription_py import server
import asyncio

port=3333
if __name__ == "__main__":  
    asyncio.run(server.main(port))
```

- `python server.py`
- Open another terminal and run `ngrok http 3333`. You will get a HTTPS address. Replace 'HTTPS' with 'WSS' and that is the address which will be used later as `{streamingUrl}`.

### Step.2 Create a streaming profile

For our server to know where to send audio streams to, we will need a streaming profile.

Let's test with a [Queue](../../../routing/queues/queues)(incoming call streams). Here we will need:

- `productId`: the id for your `Queue`
- `mainAccountId`: get it from Engage Voice Admin Console -> Settings -> Accounts -> main account id
- `subAccountId`: get it from Engage Voice Admin Console -> Settings -> Accounts -> expand main account -> sub account id
- `rcAccountId`: `RingCentral User ID` for admin user


Call Streaming operates per **Queue(inbound calls) or Campaign(outbound calls)**. The streaming service will be activated upon the creation of a streaming profile. As shown by the flow chart above, audio streams will be sent to your `{streamingUrl}` where your WebSocket server can do further processing.

To create a streaming profile, do `HTTP POST` request to `{PLATFORM_BASE_URL}/media-distributor/product` (be sure to set [PLATFORM_BASE_URL](../../../basics/uris/#current-host) with `Bearer Auth Token` from [authorizationToken](../../../authentication/auth-ringcentral)).

| API Property | Description |
|-|-|
| **`productType`** | QUEUE or CAMPAIGN |
| **`streamingUrl`** | The url for your WSS server which should start with `wss:` **NOT** `ws:` |
| **`secret`** | Optional. You can use it for your server side validation for incoming websocket messages. |

Sample request:

`POST https://{PLATFORM_ENDPOINT_PATH}/platform/api/media/product`

`Authorization: bearer {authorizationToken}`

```json
{
    "productType": "QUEUE",
    "productId": 1234,
    "subAccountId": "99990001",
    "mainAccountId": "99990000",
    "rcAccountId": "123456789",
    "streamingUrl": "wss://sample.com",
    "secret": "sampleSecret"
}
```

Sample response:

```json
{
    "productType": "QUEUE",
    "productId": 1234,
    "subAccountId": "99990001",
    "mainAccountId": "99990000",
    "rcAccountId": "123456789",
    "streamingUrl": "wss://sample.com",
    "secret": "sampleSecret"
}
```

!!!warning
    We don't validate your WebSocket server connectivity upon the creation or update of a streaming profile. Please make sure the uploaded `streamingUrl` is correct and the server is working.

#### Enable Streaming for Queue/Campaign

**Go to [Engage Voice admin console](https://engage.ringcentral.com/).**

- **For Queue: Go to Routing -> Voice queues & skills -> Select your Queue -> Recording settings**
- **For Campaign: Go to Dialing -> Campaigns -> Select your Campaign -> Recording settings**

<img class="img-fluid" width="997px" src="../../../images/agent-segment-streaming.png">

### Step.3 Make a call

Have an agent available in the `Queue` that you've created a streaming profile with and call the number of the `Queue`. Check local server's log. There should be logging for different types of messages. Upon the hangup of the call, the local server will wrap up audio file writing and you should be able to play the audio.

Call streaming will work alongside call recording.

<img class="img-fluid" width="300px" src="../../../images/call-streaming-agent-call.png">


## Audio Streaming Message Data

Let's have a quick review on what the WebSocket messages look like.

When an agent in the Queue/Campaign is connected to a call, Engage Voice server will start to send websocket messages to `streamingUrl`. There are 4 types of messages:

- [Connect](#connect-message)
- [Start](#start-message)
- [Media](#media-message)
- [Stop](#stop-message)

!!!note
    If the websocket initiation request is accepted, we will begin sending messages. If the websocket initiation is denied, we will receive a 4xx error and not proceed. If the websocket initiation fails with a 5xx error, we will attempt to retry up to 3 attempts.

#### Connect Message

!!!note
    Before sending Connect Message, there will be a HTTP request for websocket upgrade handshake, with the following query parameters that can be parsed and stored on your system as needed: `Call ID`, `Session ID`, `Caller ANI`, `DNIS`, `EV Account ID`, `EV Subaccount ID`, `RingCentral Office Account ID`, `Agent ID`, `Product Type(Queue|Campaign|Manual)`, `Product ID`

Connect Message will be sent once websocket connection is established.

```json
{ 
 "event": "Connected", 
 "protocol": "AgentSession", 
 "version": "1.0.0" 
}
```

#### Start Message

Start Message will be sent right after Connect Message. It contains the metadata of your stream.

```json
{ 
 "event": "Start", 
 "metadata": {
    "callId": "12345", 
    "sessionId": 2, 
    "ani": "2223334444", 
    "dnis": "2223334444", 
    "accountId": "99990000", 
    "subaccountId": "99990001", 
    "rcAccountId": "123456789", 
    "agentId": 123, 
    "productType": "Queue", 
    "productId": 1234, 
    "contentType": "audio/x-mulaw", 
    "sampleRateHertz": 8000, 
    }
}
```

#### Media Message

Media Message is the primary message type you will receive and it will sent continuously. It contains the audio data of your stream.

!!!note
    Media stream is encoded with ulaw algorithm, with sample rate 8000Hz and depth 8-bit

```json
{ 
    "event": "Media", 
    "perspective": "Participant" | "Conference", 
    "sequenceId": "1",   
    "media": "{base64_encoded_binary_data}" // media field will contain the binary data for about 20ms of audio.
}
```

!!!note
    Media Messages are generally in-sequence, hence you could simply ignore not-in-sequence message. However, to ensure all messages are in-sequence, you could also write additional logic to pause on not-in-sequence messages and wait for the in-sequence one, then continue.

!!!note
    In stereo channels, the left channel will be agent's audio, and the right channel will have audio for caller and all other existing legs from transfers/requeues.

#### Stop Message

Stop Message is sent at the end of the call and contains relevant metadata. We will send a stop message for each perspective of the call.

```json
{ 
    "event": "Stop", 
    "metadata": {
        "duration": 120, 
        "end_time": "2021-01-14T00:00:00Z" //RFC-3339 format timestamp 
    }
} 
```
