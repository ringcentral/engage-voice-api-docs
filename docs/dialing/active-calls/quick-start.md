# Engage Voice List Active Calls Quick Start

Welcome to the Engage Voice Platform. In this Quick Start, we are going to read a list of active calls from an account. Let's get started.

## Create an App

The first thing we need to do is create an app in the RingCentral Developer Portal. This can be done quickly by clicking the "Create App" button below. Just click the button, enter a name and description if you choose, and click the "Create" button. If you do not yet have a RingCentral account, you will be prompted to create one.

<a target="_new" href="https://developer.ringcentral.com/new-app?name=Engage+Voice+Quick+Start+App&desc=A+simple+app+to+demo+creating+a+queue+group&grantType=PersonalJWT&public=false&type=ServerOther&carriers=7710,7310,3420&permissions=ReadAccounts&redirectUri=&utm_source=devguide&utm_medium=button&utm_campaign=quickstart" class="btn btn-primary">Create App</a>
<a class="btn-link btn-collapse" data-toggle="collapse" href="#create-app-instructions" role="button" aria-expanded="false" aria-controls="create-app-instructions">Show detailed instructions</a>

<div class="collapse" id="create-app-instructions">
<ol>
<li><a href="https://developer.ringcentral.com/login.html#/">Login or create an account</a> if you have not done so already.</li>
<li>Go to Console/Apps and click 'Create App' button.</li>
<li>Select "REST API App" under "What type of app are you creating?" Click "Next."</li>
<li>Under "Auth" select "JWT auth flow"
<li>Under "Security" add the following permissions:
  <ul>
    <li>SMS</li>
    <li>ReadAccounts</li>
  </ul>
</li>
<li>Under "Security" select "This app is private and will only be callable using credentials from the same RingCentral account."</li>
</ol>
</div>

When you are done, you will be taken to the app's dashboard. Make note of the Client ID and Client Secret. We will be using those momentarily.

## Read Agent Groups for an Engage Voice Account

=== "JavaScript"

    ### Install Engage Voice SDK Wrapper for Node JS

    ```bash
    $ npm install ringcentral-engage-voice-client
    ```

    ### Create and Edit list-active-calls.js

    Create a file called <tt>list-active-calls.js</tt>. Be sure to edit the variables in ALL CAPS with your app and user credentials.

    ```javascript
    {!> code-samples/active-calls/quick-start.js !}
    ```

    ### Run Your Code

    You are almost done. Now run your script.

    ```bash
    $ node list-active-calls.js
    ```

=== "PHP"

    ### Install Engage Voice SDK Wrapper for Node JS

    ```bash
    $ npm install engagevoice-sdk-wrapper --save
    ```

    ### Create and Edit list-active-calls.js

    Create a file called <tt>list-active-calls.js</tt>. Be sure to edit the variables in ALL CAPS with your app and user credentials.

    ```php
    {!> code-samples/active-calls/quick-start.php !}
    ```

    ### Run Your Code

    You are almost done. Now run your script.

    ```bash
    $ node list-active-calls.php
    ```

=== "Python"

    ### Install Engage Voice SDK Wrapper for Python

    ```bash
    $ pip install engagevoice-sdk-wrapper
    ```

    ### Create and Edit list-active-calls.py

    Create a file called <tt>list-active-calls.py</tt>. Be sure to edit the variables in ALL CAPS with your app and user credentials.

    ```python
    {!> code-samples/active-calls/quick-start.py !}
    ```

    ### Run Your Code

    You are almost done. Now run your script.

    ```bash
    $ python list-active-calls.py
    ```

## Need Help?

Having difficulty? Feeling frustrated? Receiving an error you don't understand? Our community is here to help and may already have found an answer. Search our community forums, and if you don't find an answer please ask!

<a target="_new" href="https://forums.developers.ringcentral.com/search.html?c=11&includeChildren=false&f=&type=question+OR+kbentry+OR+answer+OR+topic&redirect=search%2Fsearch&sort=relevance&q=call+management">Search the forums &raquo;</a>

## What's Next?

When you have successfully made your first API call, it is time to take your next step towards building a more robust Engage Voice application.
