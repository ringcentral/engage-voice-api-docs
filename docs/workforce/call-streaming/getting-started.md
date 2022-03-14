# Getting Started with Call Streaming

!!!important
    Please work with your RingCentral representative to activate Call Streaming service for your organization.

**Call Streaming** runs alongside [Call Recording](./../../call-recording). It streams real-time stereo audio to your WebSocket Secure(WSS) server, which can then be used for services like Speech Analysis etc.

**Call Streaming** requires a WSS server built and hosted by you. The server is to receive audio streams for further processing. [Quick start guide](#quick-start-guide) and [sample code](#step3-host-local-server) are provided below.

## Workflow Overview

<img class="img-fluid" width="100%" src="../../../images/call-streaming.png">

## Quick Start Guide

The following guide helps you quickly setup your local debugging environment to try out simplest Call Streaming implementation.

Overall, we want to:

- <img class="img-fluid" width="18px" src="../../../images/icons/connection_icon.svg"> Use `ngrok` for web tunneling to open your local server to public
- <img class="img-fluid" width="18px" src="../../../images/icons/new_file_icon.svg"> Create a streaming profile so we know where to stream call audio data to
- <img class="img-fluid" width="18px" src="../../../images/icons/computer_icon.svg"> Host a WebSocket server locally
- <img class="img-fluid" width="18px" src="../../../images/icons/phone_icon.svg"> Test it with an actual call

### Prerequisites

This guide expects you have ngrok installed and ready to run. If you need to learn more about ngrok, click the link.

- [ngrok](https://ngrok.com/)

### Step.1 Start ngrok

In command line, run:

```bash
ngrok http 3333
```

This will start a server with an `http` and `https` server URL. In this instance, we want to use the secure connection so look for:

```http
https://xxxxxx.ngrok.io
```

Replace `https` with `wss` so we have 

```http
wss://xxxxxx.ngrok.io
```

This will be our `streamingUrl`.

### Step.2 Create a streaming profile

For our server to know where to send audio streams to, we will need a streaming profile.

Let's test with a [Queue](../../../routing/queues)(incoming call streams). Here we will need:

- `productId`: the id for your `Queue`
- `mainAccountId`: get it from Engage Voice Admin Console -> Settings -> Accounts -> main account id
- `subAccountId`: get it from Engage Voice Admin Console -> Settings -> Accounts -> expand main account -> sub account id
- `rcAccountId`: `RingCentral User ID` for admin user


Call Streaming operates per **Queue(inbound calls) or Campaign(outbound calls)**. The streaming service will be activated upon the creation of a streaming profile. As shown by the flow chart above, audio streams will be sent to your `{streamingUrl}` where your WebSocket server can do further processing.

To create a streaming profile, do `HTTP POST` request to `{BASE_URL}/media-distributor/product`. (
be sure to set the proper [BASE_URL](../../../basics/uris/#resources-and-parameters) and [authorizationToken](../../../authentication/auth-ringcentral))

| API Property | Description |
|-|-|
| **`productType`** | QUEUE or CAMPAIGN |
| **`streamingUrl`** | The url for your WSS server which should start with `wss:` **NOT** `ws:` |
| **`secret`** | Optional. You can use it for your server side validation for incoming websocket messages. |

Sample request:

`POST {BASE_URL}/media-distributor/product`

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

Go to [Engage Voice admin console](https://engage.ringcentral.com/).

- For Queue: Go to Routing -> Voice queues & skills -> Select your Queue -> Recording settings
- For Campaign: Go to Dialing -> Campaigns -> Select your Campaign -> Recording settings

<img class="img-fluid" width="997px" src="../../../images/agent-segment-streaming.png">

### Step.3 Host local server

Since we've already setup ngrok tunnel which will publicly open our server on local port `3333` to `wss://xxxxxx.ngrok.io`, let's now start our server with below sample code. It receives audio streaming segments and write them into files under `recordings` folder.

```javascript tab="Nodejs"
    // Step.1 in console, do `npm init`
    // Step.2 `npm i wavefile ws`
    // Step.3 `node {thisFileName}.js` to start server
    
    const { resolve } = require('path');
    const fs = require('fs');
    const WaveFile = require('wavefile').WaveFile;

    const WebSocket = require("ws");
    const wss = new WebSocket.Server({
        port: 3333
    });

    const recordingDirectory = resolve(__dirname, 'recordings');

    fs.mkdir(recordingDirectory, { recursive: true }, (err) => {
        if (err) {
            return console.error(err);
        }
    });

    console.log(`Server started on port: ${wss.address().port}`);

    const conferenceWav = new WaveFile();
    const agentWav = new WaveFile();
    let conferenceBuffer = Buffer.from('');
    let agentBuffer = Buffer.from('');
    let callId = '';

    // Handle Web Socket Connection
    wss.on("connection", function connection(ws) {
        console.log("New Connection Initiated");
        ws.on("message", function incoming(message) {
            const msg = JSON.parse(message);
            switch (msg.event) {
                case "Connected":
                    console.log(`A new call has connected.`);
                    console.log(msg);
                    break;
                case "Start":
                    console.log('Starting Media Stream and Recording');
                    callId = msg.metadata.callId;
                    break;
                case "Media":
                    switch (msg.perspective) {
                        case 'Conference':
                            conferenceBuffer = Buffer.concat([conferenceBuffer, Buffer.from(msg.media,  "base64")]);
                            break;
                        case 'Participant':
                            agentBuffer = Buffer.concat([agentBuffer, Buffer.from(msg.media, "base64")] );
                            break;
                    }
                    break;
                case "Stop":
                    console.log(`Call Has Ended`);
                    conferenceWav.fromScratch(1, 8000, '8m', conferenceBuffer);
                    agentWav.fromScratch(1, 8000, '8m', agentBuffer);
                    conferenceWav.fromMuLaw();
                    agentWav.fromMuLaw();
                    fs.writeFileSync(`${recordingDirectory}/${callId}_conference.wav`, conferenceWav.   toBuffer());
                    fs.writeFileSync(`${recordingDirectory}/${callId}_agent.wav`, agentWav.toBuffer());
                    console.log(`Audio Files Created`);
                    break;
            }
        });
    });

```

```python tab="Python"
# requires ffmpeg(https://ffmpeg.org/download.html)
import argparse
import asyncio
import json
import logging
import websockets
import base64
import subprocess
from pathlib import Path

logging.basicConfig(level=logging.INFO)

streaming_sessions = {}

receive = ""
transmit = ""
recording_directory = "./recordings/"

class RecordingFile:
    def __init__(self, metadata, participant_type):
        self.filename = recording_directory + str(metadata["callId"]) + "-" + str(
            metadata["sessionId"]) + "_" + participant_type + ".raw"
        self.channels = 1
        self.sample_width = 1  # sample size for EMD stream is always 1 byte
        self.framerate = metadata["sampleRateHertz"]
        if metadata["audioContentType"] != "audio/x-mulaw":
            raise TypeError("Only 'audio/x-mulaw' is supported at this time!")

    def write(self, data):
        with open(self.filename, "ab") as file:
            file.write(data)

    def get_filename(self):
        return self.filename

    def get_channels(self):
        return self.channels

    def get_sample_width(self):
        return self.sample_width

    def get_framerate(self):
        return self.framerate

    def convert_raw_to_mulaw(self):
        proc = subprocess.Popen(
            args=[
                'ffmpeg',
                '-f', 'mulaw',
                '-ar', str(self.framerate),
                '-ac', str(self.channels),
                '-i', self.filename,
                '-c:a', 'pcm_mulaw',
                self.filename.replace(".raw", ".wav")],
            stdout=subprocess.PIPE)
        stdout, stderr = proc.communicate()

        if stderr:
            raise Exception('Failed to convert raw audio! Response: {response}'.format(response=stderr))


def log_message(message: str) -> None:
    logging.info(f"Message: {message}")

def consume_start_message(message, streaming_session) -> None:
    logging.info("Received a START Message for session_id " + streaming_session["id"])
    global transmit
    transmit = RecordingFile(message["metadata"], "agent")
    global receive
    receive = RecordingFile(message["metadata"], "conference")
    log_message(message)

def consume_media_message(message, streaming_session) -> None:
    # logging.info("Received MEDIA Message for session_id " + streaming_session["id"])
    media = message["media"]
    media_bytes = base64.b64decode(media)
    # logging.info(type(media_bytes))
    if message["perspective"] == "Participant":
        transmit.write(media_bytes)
    if message["perspective"] == "Conference":
        receive.write(media_bytes)
    # log_message(message)
    
def consume_stop_message(message, streaming_session) -> None:
    logging.info("Received STOP Message for session_id " + streaming_session["id"])
    transmit.convert_raw_to_mulaw()
    receive.convert_raw_to_mulaw()
    log_message(message)


def build_session(message, websocket) -> None:
    streaming_session = {"metadata": {}, "id": ""}
    streaming_sessions[websocket] = streaming_session
    streaming_session["metadata"] = message["metadata"]
    streaming_session["id"] = str(streaming_session["metadata"]["callId"]) + "-" + str(streaming_session["metadata"]["sessionId"])

async def handle(websocket, path):
    logging.info("we got a message")
    logging.info(path) 
    async for messageStr in websocket:
        # logging.info(messageStr)
        message = json.loads(messageStr)
        if message["event"] is not None and message["event"] == "Connected":
            logging.info("Consumed ACK")
        elif message["event"] is not None and message["event"] == "Start":
            build_session(message=message, websocket=websocket)
            consume_start_message(message, streaming_session=streaming_sessions[websocket])
        elif message["event"] is not None and message["event"] == "Media":
            consume_media_message(message, streaming_session=streaming_sessions[websocket])
        elif message["event"] is not None and message["event"] == "Stop":
            consume_stop_message(message, streaming_session=streaming_sessions[websocket])
            break

async def main():
    parser = argparse.ArgumentParser(description='Starts up a SimpleWebSocket Server, will send messages to all conencted consumers')
    parser.add_argument('--port',"-p", help='port number of the producer sending websocket data')
    parser.add_argument('--hostname',"-n", help='hostname of the producer websocket')

    args = parser.parse_args()

    if args.hostname is None:
        logging.info('No Hostname was supplied, defaulting to 127.0.0.1')
        args.hostname = '127.0.0.1'

    if args.port is None:
        logging.info('No port was supplied, defaulting to 3333')
        args.port = 3333

    Path(recording_directory).mkdir(parents=True, exist_ok=True)    
    logging.info("Server started on host: " + args.hostname + ":" + str(args.port))
    async with websockets.serve(handle, args.hostname, args.port, ping_interval=1, ping_timeout=500000):
        await asyncio.Future()  # run forever

if __name__ == "__main__":  
    asyncio.run(main())
```

### Audio Streaming

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


### Step.4 Make a call

Have an agent available in the `Queue` that you've created a streaming profile with and call the number of the `Queue`. Check local server's log. There should be logging for different types of messages. Upon the hangup of the call, the local server will wrap up audio file writing and you should be able to play the audio.

Call streaming will work alongside call recording.

<img class="img-fluid" width="300px" src="../../../images/call-streaming-agent-call.png">