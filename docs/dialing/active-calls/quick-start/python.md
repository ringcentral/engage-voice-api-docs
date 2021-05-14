no_breadcrumb:true

# List Active Calls Python Quick Start

Welcome to the Engage Voice Platform. In this Quick Start, we are going to read a list of active calls from an account. Let's get started.

## Create an App

The first thing we need to do is create an app in the RingCentral Developer Portal. This can be done quickly by clicking the "Create Engage Voice App" button below. Just click the button, enter a name and description if you choose, and click the "Create" button. If you do not yet have a RingCentral account, you will be prompted to create one.

<a target="_new" href="https://developer.ringcentral.com/new-app?name=Engage+Voice+Quick+Start+App&desc=A+simple+app+to+demo+engage+voice+apis+access&public=false&type=ServerOther&carriers=7710,7310,3420&permissions=ReadAccounts&redirectUri=" class="btn btn-primary">Create Engage Voice App</a>
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

## Read Dial Groups for an Engage Voice Account

### Install Engage Voice SDK Wrapper for Python

```bash
$ pip install engagevoice-sdk-wrapper
```

### Create and Edit list-active-calls.py

Create a file called <tt>list-active-calls.py</tt>. Be sure to edit the variables in ALL CAPS with your app and user credentials.

```python
#### Install Python SDK wrapper ####
# $ pip3 install ringcentral_engage_voice
#  or
# $ pip install ringcentral_engage_voice
#####################################
from ringcentral_engage_voice import RingCentralEngageVoice

def list_active_calls():
    try:
        params = "product=ACCOUNT&productId={accountId}"
        response = ev.get("/api/v1/admin/accounts/{accountId}/activeCalls/list", params).json()
        print(response)
    except Exception as e:
        print(e)


# Instantiate the SDK wrapper object with your RingCentral app credentials
ev = RingCentralEngageVoice(
    "RINGCENTRAL_CLIENTID",
    "RINGCENTRAL_CLIENTSECRET")

try:
    # Authorize with your RingCentral Office user credentials
    ev.authorize(
        username="RINGCENTRAL_USERNAME",
        password="RINGCENTRAL_PASSWORD",
        extension="RINGCENTRAL_EXTENSION"
    )

    list_active_calls()
except Exception as e:
    print(e)
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
