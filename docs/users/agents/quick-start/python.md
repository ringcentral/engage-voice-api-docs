no_breadcrumb:true

# Call Answering Rules Python Quick Start

Welcome to the RingCentral Platform. RingCentral is the leading unified communications platform. From one system developers can integrate with, or build products around all the ways people communicate today: SMS, voice, fax, chat and meetings.

In this Quick Start, we are going to read preset call answering rules of a user, so that you can see the rule's details and update the rule with new values if you want to. Let's get started.

## Create an App

The first thing we need to do is create an app in the RingCentral Developer Portal. This can be done quickly by clicking the "Create Call Management App" button below. Just click the button, enter a name and description if you choose, and click the "Create" button. If you do not yet have a RingCentral account, you will be prompted to create one.

<a target="_new" href="https://developer.ringcentral.com/new-app?name=Call+Management+Quick+Start+App&desc=A+simple+app+to+demo+call+answering+rules+on+RingCentral&public=false&type=ServerOther&carriers=7710,7310,3420&permissions=ReadAccounts&redirectUri=" class="btn btn-primary">Create Call Management App</a>
<a class="btn-link btn-collapse" data-toggle="collapse" href="#create-app-instructions" role="button" aria-expanded="false" aria-controls="create-app-instructions">Show detailed instructions</a>

<div class="collapse" id="create-app-instructions">
<ol>
<li><a href="https://developer.ringcentral.com/login.html#/">Login or create an account</a> if you have not done so already.</li>
<li>Go to Console/Apps and click 'Create App' button.</li>
<li>Give your app a name and description, then click Next.</li>
<li>On the second page of the create app wizard enter the following:
  <ul>
  <li>Select 'Private' for Application Type.</li>
  <li>Select 'Server-only (No UI)' for Platform Type.</li>
  </ul>
  </li>
<li>On the third page of the create app wizard, select the following permissions:
  <ul>
    <li>ReadAccounts</li>
  </ul>
</li>
<li>We are using Password Flow authentication, so leave "OAuth Redirect URI" blank.</li>
</ol>
</div>

When you are done, you will be taken to the app's dashboard. Make note of the Client ID and Client Secret. We will be using those momentarily.

## Read User Call Answering Rules

### Install EngageVoice SDK wrapper

```bash
pip3 install engagevoice-sdk-wrapper
```

### Create and Edit list-agent-groups.py

Create a file called <tt>list-agent-groups.py</tt>. Be sure to edit the variables in ALL CAPS with your app and user credentials.

```python
from engagevoice.sdk_wrapper import *

RC_CLIENT_ID= '<ENTER CLIENT ID>'
RC_CLIENT_SECRET= '<ENTER CLIENT SECRET>'

RC_USERNAME = '<YOUR ACCOUNT PHONE NUMBER>'
RC_PASSWORD = '<YOUR ACCOUNT PASSWORD>'
RC_EXTENSION = '<YOUR EXTENSION NUMBER>'

def list_account_agent_groups():
    try:
        endpoint = 'admin/accounts/~/agentGroups'
        response = ev.get(endpoint, None, None)
        print (response)
    except Exception as e:
        print (e)

evsdk = RestClient(RC_CLIENT_ID, RC_CLIENT_SECRET)
try:
    resp = evsdk.login(RC_USERNAME, RC_PASSWORD, RC_EXTENSION)
    if resp:
        list_account_agent_groups()

except Exception as e:
    print (e)
```

### Run Your Code

You are almost done. Now run your script.

```bash
$ python list-agent-groups.py
```

## Need Help?

Having difficulty? Feeling frustrated? Receiving an error you don't understand? Our community is here to help and may already have found an answer. Search our community forums, and if you don't find an answer please ask!

<a target="_new" href="https://forums.developers.ringcentral.com/search.html?c=11&includeChildren=false&f=&type=question+OR+kbentry+OR+answer+OR+topic&redirect=search%2Fsearch&sort=relevance&q=call+management">Search the forums &raquo;</a>

## What's Next?

When you have successfully made your first API call, it is time to take your next step towards building a more robust RingCentral application.

<a class="btn btn-success btn-lg" href="../../../basics/your-first-steps/">Take your next step &raquo;</a>
