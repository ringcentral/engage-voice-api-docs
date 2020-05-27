# About Searching for Leads

You can search for leads using Primary Search Fields and Extended Search Fields. The Primary Search Fields can be used for performing basic searches on leads such as the campaign or list they are found in, while the Extended Search Fields provide search parameters that you can use to get more granular with your lead search.

```http tab="HTTP"

    POST /api/v1/admin/accounts/{accountId}/campaignLeads/leadSearch
    Authorization: bearer <myAccessToken>
    Content-Type: application/json;charset=UTF-8
    Accept: application/json

    {"firstName":"Jon"}
```

```bash tab="cURLs"

    curl -XPOST 'https://engage.ringcentral.com/voice/api/v1/admin/accounts/{accountId}/campaignLeads/leadSearch' \
       -H 'Authorization: Bearer {myAccessToken}' \
       -d '{"firstName":"John"}' \
       -H 'Content-Type: application/json'
```

```javascript tab="Node JS"
/****** Install Node JS SDK wrapper *******
$ npm install engagevoice-sdk-wrapper --save
*******************************************/

const EngageVoice = require('engagevoice-sdk-wrapper')

// Instantiate the SDK wrapper object with your RingCentral app credentials
var ev = new EngageVoice.RestClient("RC_CLIENT_ID", "RC_CLIENT_SECRET")

// Login your account with your RingCentral Office user credentials
ev.login("RC_USERNAME", "RC_PASSWORD", "RC_EXTENSION_NUMBER", function(err, response){
  if (!err){
    var endpoint = 'admin/accounts/~/campaignLeads/leadSearch'
    var params = { firstName: "John" }
    ev.post(endpoint, params, function(err, response){
        if (!err){
            console.log(response)
        }
    })
  }
})
```

```python tab="Python"
/****** Install Python SDK wrapper **
$ pip install engagevoice-sdk-wrapper
*************************************/

from engagevoice.sdk_wrapper import *

# Instantiate the SDK wrapper object with your RingCentral app credentials
ev = RestClient("RC_APP_CLIENT_ID", "RC_APP_CLIENT_SECRET")

# Login your account with your RingCentral Office user credentials
try:
    ev.login("RC_USERNAME", "RC_PASSWORD", "RC_EXTENSION_NUMBER")
    endpoint = 'admin/accounts/~/campaignLeads/leadSearch'
    params = { "firstName" : "John" }
    response = ev.post(endpoint, params)
    print (response)        
except Exception as e:
    print (e)
```

```php tab="PHP"
/****** Install PHP SDK wrapper **
$ composer require engagevoice-sdk-wrapper:dev-master
*************************************/

<?php
require('vendor/autoload.php');

// Instantiate the SDK wrapper object with your RingCentral app credentials
$ev = new EngageVoiceSDKWrapper\RestClient("RC_APP_CLIENT_ID", "RC_APP_CLIENT_SECRET");
try{
  // Login your account with your RingCentral Office user credentials
  $ev->login("RC_USERNAME", "RC_PASSWORD", "RC_EXTENSION_NUMBER");
  $endpoint = "admin/accounts/~/campaignLeads/leadSearch";
  $params = array ( "firstName" => "John" );
  $response = $ev->post($endpoint, $params);
  print ($response."\r\n");
}catch (Exception $e) {
  print $e->getMessage();
}
```
## References

* [Web console documentation: Using the Leads search](https://docs.ringcentral.com/engage/article/voice-admin-use-lead-search)
