# RingCX Queue Group Quick Start

Welcome to the RingCX Platform. In this quick start, we are going to create a queue group for an account. Let's get started.

## Create an App

The first thing we need to do is create an app in the RingCentral Developer Portal. This can be done quickly by clicking the "Create App" button below. Just click the button, enter a name and description if you choose, and click the "Create" button. If you do not yet have a RingCentral account, you will be prompted to create one.

<a target="_new" href="https://developer.ringcentral.com/new-app?name=RingCX+Quick+Start+App&desc=A+simple+app+to+demo+creating+a+queue+group&grantType=PersonalJWT&public=false&type=ServerOther&carriers=7710,7310,3420&permissions=ReadAccounts&redirectUri=&utm_source=devguide&utm_medium=button&utm_campaign=quickstart" class="btn btn-primary">Create App</a>
<a class="btn-link btn-collapse" data-toggle="collapse" href="#create-app-instructions" role="button" aria-expanded="false" aria-controls="create-app-instructions">Show detailed instructions</a>

<div class="collapse" id="create-app-instructions">
<ol>
<li><a href="https://developer.ringcentral.com/login.html#/">Login or create an account</a> if you have not done so already.</li>
<li>Go to Console/Apps and click 'Create App' button.</li>
<li>Select "REST API App" under "What type of app are you creating?" Click "Next."</li>
<li>Under "Auth" select "JWT auth flow"
<li>Under "Security" add the following permissions:
  <ul>
    <li>ReadAccounts</li>
  </ul>
</li>
<li>Under "Security" select "This app is private and will only be callable using credentials from the same RingCentral account."</li>
</ol>
</div>

When you are done, you will be taken to the app's dashboard. Make note of the Client ID and Client Secret. We will be using those momentarily.

## Create a queue group for a RingCX account

=== "JavaScript"

    ### Install RingCX SDK wrapper for Node JS

    ```bash
    $ npm install ringcentral-engage-voice-client
    ```

    ### Create and edit create-queue-group.js

    Create a file called <tt>create-queue-group.js</tt>. Be sure to edit the variables in ALL CAPS with your app and user credentials.

    ```javascript
    {!> code-samples/routing/quick-start.js !}
    ```

    ### Run Your Code

    You are almost done. Now run your script.

    ```bash
    $ node create-queue-group.js
    ```

=== "PHP"

    ### Install RingCX SDK Wrapper for PHP

    ```bash
    $ composer require engagevoice-sdk-wrapper
    ```

    ### Create and Edit create-queue-group.php

    Create a file called <tt>create-queue-group.php</tt>. Be sure to edit the variables in ALL CAPS with your app and user credentials.

    ```php
    {!> code-samples/routing/quick-start.php !}
    ```

    ### Run Your Code

    You are almost done. Now run your script.

    ```bash
    $ php create-dial-group.php
    ```

=== "Python"

    ### Install RingCX SDK Wrapper for Python

    ```bash
    pip install ringcentral_engage_voice
    ```

    ### Create and Edit create-queue-group.py

    Create a file called <tt>create-queue-group.py</tt>. Be sure to edit the variables in ALL CAPS with your app and user credentials.

    ```python
    {!> code-samples/routing/quick-start.py !}
    ```

    ### Run Your Code

    You are almost done. Now run your script.

    ```bash
    $ python create-queue-group.py
    ```

## Need Help?

Having difficulty? Feeling frustrated? Receiving an error you don't understand? Our community is here to help and may already have found an answer. Search our community forums, and if you don't find an answer please ask!

<a target="_new" href="https://forums.developers.ringcentral.com/search.html?c=11&includeChildren=false&f=&type=question+OR+kbentry+OR+answer+OR+topic&redirect=search%2Fsearch&sort=relevance&q=call+management">Search the forums &raquo;</a>

## What's Next?

When you have successfully made your first API call, it is time to take your next step towards building a more robust RingCX application.
