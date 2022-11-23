# Save To Files Example and Walkthrough

!!!important
    It's assumed that you have gone through [Getting Started Guide](./../getting-started)

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

### Step.2 Setup streaming profile

Please refer to [Getting Started Guide](./../getting-started) Step.1.

### Step.3 Start Local Server

Let's start our local server which receives audio streaming segments and saves them into local files.

#### Sample Code

=== "Nodejs"
        ```javascript
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

            // Handle Web Socket Connection
            wss.on("connection", function connection(ws) {
                console.log("New Connection Initiated");

                const conferenceWav = new WaveFile();
                const agentWav = new WaveFile();
                let conferenceBuffer = Buffer.from('');
                let agentBuffer = Buffer.from('');
                let callId = '';


                ws.on("message", function incoming(message) {
                    const msg = JSON.parse(message);
                    switch (msg.event) {
                        case "Connected":
                            console.log(JSON.stringify(msg));
                            break;
                        case "Start":
                            callId = `${msg.metadata.callId}-${msg.metadata.sessionId}`;
                            console.log(`${callId}: START  ${JSON.stringify(msg)}`);
                            break;
                        case "Media":
                            switch (msg.perspective) {
                                case 'Conference':
                                    conferenceBuffer = Buffer.concat([conferenceBuffer, Buffer.from(msg.        media,  "base64")]);
                                    break;
                                case 'Participant':
                                    agentBuffer = Buffer.concat([agentBuffer, Buffer.from(msg.media,        "base64")] );
                                    break;
                            }
                            break;
                        case "Stop":
                            console.log(`${callId}: STOP ${JSON.stringify(msg)}`);

                            conferenceWav.fromScratch(1, 8000, '8m', conferenceBuffer);
                            agentWav.fromScratch(1, 8000, '8m', agentBuffer);
                            conferenceWav.fromMuLaw();
                            agentWav.fromMuLaw();
                            fs.writeFileSync(`${recordingDirectory}/${callId}_conference.wav`, conferenceWav.       toBuffer());
                            fs.writeFileSync(`${recordingDirectory}/${callId}_agent.wav`, agentWav.toBuffer     ());
                            console.log(`${callId}: Audio Files Created`);
                            break;
                    }
                });
            });

        ```
=== "Python"
        ```python
        # IMPORTANT!!! It requires ffmpeg(https://ffmpeg.org/download.html)
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
                    raise Exception('Failed to convert raw audio! Response: {response}'.format      (response=stderr))


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
            streaming_session["id"] = str(streaming_session["metadata"]["callId"]) + "-" + str      (streaming_session["metadata"]["sessionId"])

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
            parser = argparse.ArgumentParser(description='Starts up a SimpleWebSocket Server, will send         messages to all conencted consumers')
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
            async with websockets.serve(handle, args.hostname, args.port, ping_interval=1,      ping_timeout=500000):
                await asyncio.Future()  # run forever

        if __name__ == "__main__":  
            asyncio.run(main())
        ```
