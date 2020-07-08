# Engage Voice SDKs

The following SDKs provide developers with libraries that make interfacing with Engage Voice APIs easier in your language of choice.

## Client SDKs

Client SDKs provide a native language interface to Engage Voice REST APIs

* [JavaScript Client SDK](https://github.com/ringcentral/engage-voice-js)
* [Python Client SDK](https://github.com/ringcentral/engage-voice-python)

## Agent SDKs

The Agent SDK is a library to link client agent controls to the Engage Voice system. The Agent SDK also connects to a single point of entry authentication flow (also known as [Engage Access Token](../../authentication/auth-ringcentral)) and is responsible for connecting the WebSocket used for client messaging after authentication. The Agent SDK is found in npm.

* [Agent SDK](https://www.npmjs.com/package/@ringcentral/engage-voice-agent)

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
