# Live Transcribe

!!!important
    It's assumed that you have gone through [Getting Started Guide](./../getting-started)

There are many live transcribe service providers. Here we use [Google Cloud Speech To Text](https://cloud.google.com/speech-to-text/docs) service as an example.

## Google Cloud Speed To Text

### Prerequisites

- [Google Cloud Account](https://cloud.google.com/)
- [Enable Google Speech To Text Service](https://console.cloud.google.com/speech/overview)
- [Google Service Account](https://cloud.google.com/docs/authentication/getting-started)

### Step.1 Setup ngrok and streaming profile

Please refer to [Getting Started Guide](./../getting-started) Step.1 and Step.2.

### Step.2 Start local server

#### Nodejs

Start a project and install npm libraries:

```bash
npm init

npm i ws @google-cloud/speech
```

WebSocket server sample code:

```javascript
    // Note: It takes couple of seconds connecting to Google server, then the transcription will begin

    const WebSocket = require("ws");
    const wss = new WebSocket.Server({
        port: 3333
    });

    // Imports the Google Cloud client library
    const speech = require('@google-cloud/speech');
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
                ? `Transcription: ${data.results[0].alternatives[0].transcript}\n`
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
                    console.log(`Session metadata: ${JSON.stringify(msg, null, 2)}`);
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

Start the server and make a phone call. It then will take couple of seconds to connect to Google service. After that, transcribed texts will start to show in your console like in below.

<img class="img-fluid" width="400px" src="../../../images/call-streaming-live-transcribe-console.png">
