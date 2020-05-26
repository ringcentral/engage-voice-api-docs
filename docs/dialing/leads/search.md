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

    var ev = new EngageVoice.RestClient()

    ev.login("legacy-username", "legacy-password", "", function(err, response){
        if (err)
          console.log(err)
        else{
          search_account_campaign_leads()
        }
    })

    function search_account_campaign_leads(){
        var endpoint = 'admin/accounts/~/campaignLeads/leadSearch'
        var params = {
            firstName: "John"
        }
        ev.post(endpoint, params, function(err, response){
            if (err){
                console.log(err)
            }else {
                var jsonObj = JSON.parse(response)
                console.log(jsonObj)
            }
        })
    }
```

```python tab="Python"
    /****** Install Python SDK wrapper **
    $ pip install engagevoice-sdk-wrapper
    *************************************/

    from engagevoice.sdk_wrapper import *

    def search_account_campaign_leads():
    try:
        endpoint = 'admin/accounts/~/campaignLeads/leadSearch'
        params = { "firstName" : "John" }
        response = ev.post(endpoint, params)
        jsonObj = json.loads(response)
        print (jsonObj)
    except Exception as e:
        print (e)

    ev = RestClient()
    try:
        resp = ev.login("legacy-username", "legacy-password")
        if resp:
            search_account_campaign_leads()
    except Exception as e:
        print (e)
```

```php tab="PHP"
    /****** Install PHP SDK wrapper **
    $ composer require engagevoice-sdk-wrapper:dev-master
    *************************************/

    <?php
    require('vendor/autoload.php');

    $ev = new EngageVoiceSDKWrapper\RestClient();
    try{
        $ev->login("legacy-username", "legacy-password", null, function($response){
          search_account_campaign_leads();
        });
    }catch (Exception $e) {
        print $e->getMessage();
    }

    function search_account_campaign_leads(){
        global $ev;
        $endpoint = "admin/accounts/~/campaignLeads/leadSearch";
        $params = array ( "firstName" => "John" );
        try{
            $resp = $ev->post($endpoint, $params);
            print ($resp);
        }catch (Exception $e) {
            print $e->getMessage();
        }
    }
```
## References

* [Web console documentation: Using the Leads search](https://docs.ringcentral.com/engage/article/voice-admin-use-lead-search)
