# Engage Voice SDKs

The following SDKs provide developers with libraries that make interfacing with Engage Voice APIs easier in your language of choice.

## Client SDKs

Client SDKs provide a native language interface to Engage Voice REST APIs

* [JavaScript Client SDK](https://github.com/ringcentral/engage-voice-js)
* [Python Client SDK](https://github.com/ringcentral/engage-voice-python)
* [EngageVoice.Net Client SDK](https://github.com/ringcentral/EngageVoice.Net)
* [Java Client SDK](https://github.com/ringcentral/engage-voice-java)

## Mobile Framework

The following Mobile Framework was built to show how a developer could build an agent experience on a mobile device to integrate with Engage Voice. This example utilizes the [Engage Voice Embeddable](https://github.com/ringcentral/engage-voice-embeddable) within Cordova, a mobile development framework. Since the Embeddable uses standard web technologies, this makes Cordova a great fit for packaging the Embeddable for distribution across iOS and Android app stores. A separate Web Server is expected to host the static web components including the HTML page and JavaScript code. That JavaScript code then communicates to the Engage Voice platform in the cloud.

<img class="img-fluid" width="732" src="../../../images/sdk-mobile-framework-diagram.png">

To keep things local to a single development environment, Ngrok is used to tunnel web requests (to the Embeddable page) to a local web server. This way, your Embeddable's interface is presented by Cordova. We also deploy Cordova on a local simulator that can communicate to your local web server (running Embeddable) which then communicates to Engage Voice. Now you can customize your app to use Engage Voice services either by creating a different web technology experience via you web server or by customizing the Embeddable to integrate with other applications like CRMs.

* [Engage Voice Embeddable for Mobile](https://github.com/ringcentral/ringcentral-engage-voice-embeddable-mobile)

## Community SDKs

There are currently a set of unofficial client SDK libraries built the developer community. The list below includes SDK wrappers for Engage Voice Platform APIs.

If you’ve built your own Engage Voice library, plugin, or open source app, please [get in touch](mailto:devsupport@ringcentral.com) and we’ll add it to this list.

Some of these integrations may be incomplete. Feedback and bugs should be directed to their representative authors.

### Node JS

* [engagevoice-sdk-wrapper](https://github.com/pacovu/engagevoice-sdk-wrapper-node) - A simple SDK wrapper to login RingCentral platform (using Password Flow authentication) and exchange for an Engage Voice access token.

### PHP

* [engagevoice-sdk-wrapper](https://github.com/pacovu/engagevoice-sdk-wrapper-php) - A simple SDK wrapper to login RingCentral platform (using Password Flow authentication) and exchange for an Engage Voice access token.

### Python

* [engagevoice-sdk-wrapper](https://github.com/pacovu/engagevoice-sdk-wrapper-python) - A simple SDK wrapper to login RingCentral platform (using Password Flow authentication) and exchange for an Engage Voice access token.


!!! warning "Disclaimer"
    RingCentral provides the above list solely on an "as is" basis and makes no representation, warranty, assurance, guarantee or inducement of any kind with respect to the items on this list, including without limitation, any warranty of accuracy or completeness, merchantability or fitness for a particular purpose, or with respect to the non-infringement of trademarks, copyrights, patents, or any other intellectual property rights, or rights of third persons. Moreover, inclusion in the above list is not intended to imply, directly or indirectly, that these entities endorse, are endorsed by, or have any affiliation with RingCentral, and notice of any bugs or feedback should be directed to the representative author, not RingCentral.
