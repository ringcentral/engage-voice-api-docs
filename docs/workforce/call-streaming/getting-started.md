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

### Step.3 Host Local Server for Live Transcribe

There are many live transcribe service providers. Here we use [Google Cloud Speech To Text](https://cloud.google.com/speech-to-text/docs) service as an example.

#### Prerequisites

- [Google Cloud Account](https://cloud.google.com/)
- [Enable Google Speech To Text Service](https://console.cloud.google.com/speech/overview)
- [Google Service Account](https://cloud.google.com/docs/authentication/getting-started)

Since we've already setup ngrok tunnel which will publicly open our server on local port `3333` to `wss://xxxxxx.ngrok.io`, let's now start our server with below sample code. It receives audio streaming segments and applies Google Cloud Speech To Text service to convert them into texts.

#### Sample Code

!!!note
    Please make sure all required packages in sample code are installed

WebSocket server sample code:

```javascript tab="Nodejs"
    // Note: It takes couple of seconds connecting to Google server, then the transcription will begin

    const WebSocket = require("ws");
    // Imports the Google Cloud client library
    const speech = require('@google-cloud/speech');

    const wss = new WebSocket.Server({
        port: 3333
        });

    // Creates a client
    const client = new speech.SpeechClient();
    const request = {
        config: {
            encoding: "MULAW",
            sampleRateHertz: 8000,
            languageCode: 'en-US',
        },
        interimResults: false, // If you want interim results, set this to true
        };

        console.log(`Server started on port: ${wss.address().port}`);

    // Handle Web Socket Connection
    wss.on("connection", function connection(ws) {
        console.log("New Connection Initiated");
        //Create a recognize stream
        const recognizeStream = client
          .streamingRecognize(request)
          .on('error', console.error)
          .on('data', data =>
            process.stdout.write(
              data.results[0] && data.results[0].alternatives[0]
                ? `========\n Transcription: ${data.results[0].alternatives[0].transcript}\n    Confidence: ${data.results[0].alternatives[0].confidence}\n`
                : '\n\nReached transcription time limit, press Ctrl+C\n'
            )
            );

        ws.on("message", function incoming(message) {
            const msg = JSON.parse(message);
            switch (msg.event) {
                case "Connected":
                    console.log(`A new call has connected.`);
                    console.log(msg);
                    break;
                case "Start":
                    console.log('Starting Media Stream');
                    callId = msg.metadata.callId;
                    break;
                case "Media":
                    switch (msg.perspective) {
                        // Here we only do client side transcription
                        case 'Conference':
                            recognizeStream.write(msg.media);
                            break;
                    }
                    break;
                case "Stop":
                    console.log(`Call Has Ended`);
                    recognizeStream.end()
                    break;
            }
        });
    });

```

```python tab="Python"
import argparse
import asyncio
import json
import logging
import websockets
import base64
import sys
import re
import threading
from google.cloud import speech
from six.moves import queue

logging.basicConfig(level=logging.INFO)

BUFFER_COUNT = 5 # to add up audio segments to 100ms as recommended by Google

def listen_print_loop(responses):
    """Iterates through server responses and prints them.
    The responses passed is a generator that will block until a response
        is provided by the server.
    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
        print only the transcription for the top alternative of the top result.
    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
                continue
        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
                continue
        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript
        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = " " * (num_chars_printed - len(transcript))
        if not result.is_final:
            sys.stdout.write(f'{transcript}{overwrite_chars}\r')
            sys.stdout.flush()
            num_chars_printed = len(transcript)
        else:
            print(transcript + overwrite_chars)
            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r"\b(exit|quit)\b", transcript, re.I):
                print("Exiting..")
                break
            num_chars_printed = 0

class Transcoder(object):
    """
    Converts audio chunks to text
    """
    def __init__(self):
        self.buff = queue.Queue()
        self.closed = False
        self.transcript = None
        self.client = speech.SpeechClient()
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MULAW,
            sample_rate_hertz=8000,
            language_code="en-US",
            max_alternatives=1,
            model='phone_call'
            )
        self.streaming_config = speech.StreamingRecognitionConfig(   
            config=self.config, interim_results=True,
        )
        """Start up streaming speech call"""
        t = threading.Thread(target=self.process)
        t.isDaemon = True
        t.start()

    
    def process(self):
        """
        Audio stream recognition and result parsing
        """
        audio_generator = self.stream_generator()
        requests = (speech.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = self.client.streaming_recognize(self.streaming_config, requests)
        listen_print_loop(responses)

    def stream_generator(self):
        while not self.closed:
            chunk = self.buff.get()
            if chunk is None:
                return
            data = [chunk]
            while True:
                try:
                    chunk = self.buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break
            yield b''.join(data)

    def write(self, data):
        """
        Writes data to the buffer
        """
        self.buff.put(data)
    
    def exit(self):
        self.closed = True

def log_message(message: str) -> None:
    logging.info(f"Message: {message}")

async def handle(websocket, path):
    logging.info(path) 
    transcoder = Transcoder()
    buffer_counter=0
    buffer = b""
    async for messageStr in websocket:
        # logging.info(messageStr)
        message = json.loads(messageStr)
        if message["event"] is not None and message["event"] == "Connected":
            logging.info("Consumed ACK")
        elif message["event"] is not None and message["event"] == "Start":
            print("start")
        elif message["event"] is not None and message["event"] == "Media":
            buffer_counter += 1
            media = message["media"]
            media_bytes = base64.b64decode(media)
            if buffer_counter > BUFFER_COUNT:
                transcoder.write(buffer)
                buffer_counter=0
                buffer = b""
            else:
                buffer = buffer + media_bytes
        elif message["event"] is not None and message["event"] == "Stop":
            transcoder.exit()
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

    logging.info("Server started on host: " + args.hostname + ":" + str(args.port))
    async with websockets.serve(handle, args.hostname, args.port, ping_interval=1, ping_timeout=500000):
        await asyncio.Future()  # run forever

if __name__ == "__main__":  
    asyncio.run(main())
```

Start the server and make a phone call. It then will take couple of seconds to connect to Google service. After that, transcribed texts will start to show in your console like in below.

- NodeJs

<img class="img-fluid" width="300px" src="../../../images/call-streaming-live-transcribe-console-nodejs.png">

- Python

<img class="img-fluid" width="600px" src="../../../images/call-streaming-live-transcribe-console-python.png">

#### Additional Notes

To achieve better performance overall, you might want to look into the details on:

- [Recognition Config](https://cloud.google.com/speech-to-text/docs/reference/rpc/google.cloud.speech.v1#recognitionconfig)
- [Best Practices](https://cloud.google.com/speech-to-text/docs/best-practices)

### Audio Streaming

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


### Step.4 Make a call

Have an agent available in the `Queue` that you've created a streaming profile with and call the number of the `Queue`. Check local server's log. There should be logging for different types of messages. Upon the hangup of the call, the local server will wrap up audio file writing and you should be able to play the audio.

Call streaming will work alongside call recording.

<img class="img-fluid" width="300px" src="../../../images/call-streaming-agent-call.png">