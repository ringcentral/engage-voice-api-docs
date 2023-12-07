# Obtaining an RingCX Access Token with a RingCentral Login

To access RingCX APIs, you need to create an RingCX App, and then with the client credentials, request an RingCX Access Token. Once you have created an App, request a RingCentral Access Token and then using an RingCX API to create an RingCX Access Token. Then the RingCX Access Token can be used to access RingCX APIs.

> Note: RingCX APIs for MVP customers are rooted at:
>
> `https://engage.ringcentral.com/voice/api/`

## Create an App

The first thing we need to do is create an app in the RingCentral Developer Portal. This can be done quickly by clicking the "Create RingCX App" button below. Just click the button, enter a name and description if you choose, and click the "Create" button. If you do not yet have a RingCentral account, you will be prompted to create one.

!!! important
    While you can create a RingCentral account through the Developer Portal, you will need a production account to use RingCX APIs at this time.  Make sure to login to your developer account using the same credentials as your production RingCentral account. The RingCentral account created via the Developer Portal will **not** work.

<a target="new" href="https://developer.ringcentral.com/new-app?name=Engage+Voice+Quick+Start+App&desc=A+simple+app+to+demo+engage+voice+apis+access&public=false&type=ServerOther&carriers=7710,7310,3420&permissions=ReadAccounts&redirectUri=" class="btn btn-primary">Create RingCX App</a>

<div class="expand" id="create-app-instructions">
<ol>
<li><a href="https://developers.ringcentral.com/login.html#/">Login or create an account</a> if you have not done so already.</li>
<li>Go to Console/Apps and click 'Create App' button.</li>
<li>Select the App Type, "REST API App (most common)," then click Next.</li>
<li>Give your app a name and description, then scroll to the "Auth" section.</li>
<li>In the "Auth" section:
  <ul>
  <li>Select 'JWT auth flow' for the authentication method.</li>
  <li>Under "Issue refresh tokens?" make sure the box for 'Yes' is highlighted.</li>
  </ul>
  </li>
<li>In the "Security" section, specify only the following "Application Scopes":
  <ul>
    <li>Read Accounts</li>
  </ul>
</li>
<li>In the same "Security" section, make sure to select:
  <ul>
    <li>This app is <b>private</b> and will only be callable using credentials from the same RingCentral account.</li>
  </ul>   
</li>
</ol>
</div>

When you are done, you will be taken to the app's dashboard. Make note of the Client ID. This is your Client ID for the App in the Sandbox. To start using RingCX APIs, you need to graduate your app to Production and use the Production Client ID and Client Secret in upcoming steps.  Make sure to have your RingCX account number ready for the next step. If you do not have an RingCX account, please reach out to our [Sales](https://www.ringcentral.com/feedback/sales-contact.html) team to sign up for an RingCX account.

<a target="new" href="https://docs.google.com/forms/d/e/1FAIpQLScyidt7WFb_CJrpn9yGbcZ8P_gQ42UvXz3oBBnjF0tRh7MVMw/viewform?usp=sf_link" class="btn btn-primary">Request Graduation of RingCX App</a>

## Retrieve RingCentral Access Token

Now retrieve a RingCentral access token using the following instructions:

[RingCentral Authentication](https://developers.ringcentral.com/guide/authentication)

## Retrieve RingCentral RingCX Access Token

Once you have a RingCentral Access Token, call the following RingCX API to receive an RingCX Bearer access token.

### Request

```http
POST https://engage.ringcentral.com/api/auth/login/rc/accesstoken
Content-Type: application/x-www-form-urlencoded

rcAccessToken=<rcAccessToken>&rcTokenType=Bearer
```

It's also a good idea to use a refresh token as the access token expires in 5 minutes.  
```http
POST https://engage.ringcentral.com/api/auth/login/rc/accesstoken?includeRefresh=true
Content-Type: application/x-www-form-urlencoded

rcAccessToken=<rcAccessToken>&rcTokenType=Bearer
```

Where:

-   **`<rcAccessToken>`** is the RingCentral Access Token you received from RingCentral MVP authentication flow.

=== "cURL"
    ```bash
    $ curl -XPOST https://engage.ringcentral.com/api/auth/login/rc/accesstoken \
          -d 'rcAccessToken=<rcAccessToken>' \
          -d 'rcTokenType=Bearer'
    ```
    
=== "Go"
    ```go
    package main

    import(
          "fmt"
          "encoding/json"
          "io/ioutil"
          "net/url"
        )

    // RingCXToken is an example and does not cover all the
    // properties in the API response.
    type RingCXToken struct {
        	AccessToken string `json:"accessToken"`
        	TokenType   string `json:"tokenType"`
    }

    func RcToEvToken(rctoken string) (string, error) {
      	res, err := http.PostForm(
        		"https://engage.ringcentral.com/api/auth/login/rc/accesstoken",
        		url.Values{"rcAccessToken": {rctoken}, "rcTokenType": {"Bearer"}})
        if err != nil {
        		return "", err
        }
        if res.StatusCode >= 300 {
        		return "", fmt.Errorf("Invalid Token Response [%v]", res.StatusCode)
        }
        ringCXToken := RingCXToken{}
        bytes, err := ioutil.ReadAll(res.Body)
        if err != nil {
        		return "", err
        }
        err = json.Unmarshal(bytes, &ringCXToken)
        return ringCXToken.AccessToken, err
    }

    func main() {
      	rctoken := "myRcToken"

      	evtoken, err := RcToEvToken(rctoken)
      	if err != nil {
        		log.Fatal(err)
        }
        fmt.Println(evtoken)
    }
    ```
=== "Node JS"
    ```javascript
    var https = require('https')

    var RC_ACCESS_TOKEN = "VALID-RINGCENTRAL-ACCESS-TOKEN"

    var url = "engage.ringcentral.com"
    var path = '/api/auth/login/rc/accesstoken'
    var body = 'rcAccessToken=' + RC_ACCESS_TOKEN + "&rcTokenType=Bearer"
    var headers = { 'Content-Type': 'application/x-www-form-urlencoded' }

    var options = {host: url, path: path, method: 'POST', headers: headers};
    var post_req = https.request(options, function(res) {
          var response = ""
          res.on('data', function (chunk) {
              response += chunk
          }).on("end", function(){
              if (res.statusCode == 200){
                  var tokensObj = JSON.parse(response)
                  console.log(tokensObj.accessToken)
              }else{
                  console.log(response)
              }
          });
        }).on('error', function (e) {
            console.log(e)
        })
    post_req.write(body);
    post_req.end();
    ```

=== "Python"
    ```python 
    import requests

    RC_ACCESS_TOKEN = "VALID-RINGCENTRAL-ACCESS-TOKEN"
    url = "https://engage.ringcentral.com/api/auth/login/rc/accesstoken"
    body = "rcAccessToken=%s&rcTokenType=Bearer" % (RC_ACCESS_TOKEN)
    headers = {
                  'Content-Type': 'application/x-www-form-urlencoded'
              }
    try:
        res = requests.post(url, headers=headers, data=body)
        if res.status_code == 200:
            jsonObj = json.loads(res._content)
            print (jsonObj['accessToken'])
        else:
            print (res._content)
    except Exception as e:
        raise ValueError(e)
    ```

=== "PHP"
    ```php
    <?php
    $RC_ACCESS_TOKEN = "VALID-RINGCENTRAL-ACCESS-TOKEN";

    $url = "https://engage.ringcentral.com/api/auth/login/rc/accesstoken";
    $body = 'rcAccessToken=' . $RC_ACCESS_TOKEN . "&rcTokenType=Bearer";
    $headers = array ('Content-Type: application/x-www-form-urlencoded');

    try{
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        curl_setopt($ch, CURLOPT_POST, TRUE);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
        curl_setopt($ch, CURLOPT_TIMEOUT, 600);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
        $strResponse = curl_exec($ch);
        $curlErrno = curl_errno($ch);
        if ($curlErrno) {
            throw new Exception($curlErrno);
        } else {
            $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
            curl_close($ch);
            if ($httpCode == 200) {
                $tokensObj = json_decode($strResponse);
                print ($tokensObj->accessToken);
            }else{
                print ($strResponse);
            }
        }
    }catch (Exception $e) {
        throw $e;
    }
    ```

### Response

The response will contain the `accessToken` property that can be used in an API call, as well as the `refreshToken` property that can be used to refresh the access token when the access token expires. Make sure to save both the `accessToken` and `refreshToken` for future API calls. Take note of the `accountId` property as that will be used to make future API calls.

The following is an abbreviated response.

```json
{
  "refreshToken":"<rcRingCXRefreshToken>",
  "accessToken":"<rcRingCXAccessToken>",
  "tokenType":"Bearer",
  "agentDetails":[
    {
      "agentId":111111,
      "firstName":"John",
      "lastName":"Wang",
      "email":"john.wang@example.com",
      "username":"john.wang@example.com",
      "agentType":"AGENT",
      "rcUserId":222222,
      "accountId":"333333",
      "accountName":"RingForce",
      "agentGroupId":null,
      "allowLoginControl":true,
      "allowLoginUpdates":true
    }
  ],
  "adminId":1111,
  "adminUrl":"/voice/admin/",
  "agentUrl":"/voice/agent/",
  "ssoLogin":true
}
```

## Example RingCX API Call

The following is an example RingCX API Call using a RingCentral RingCX Access Token.

```http
GET https://engage.ringcentral.com/voice/api/v1/admin/users
Authorization: Bearer <rcRingCXAccessToken>
```

## Get Accounts

Another method to try is to retrieve the accounts this user has access to. The main account is the top level account and is consider a container for the sub-accounts that most operations are performed on.

```http
GET https://engage.ringcentral.com/voice/api/v1/admin/accounts
Authorization: Bearer <rcRingCXAccessToken>
```

Here is an example cURL command:

`curl -X GET https://engage.ringcentral.com/voice/api/v1/admin/accounts -H "Authorization: Bearer {rcRingCXAccessToken}"`

## Refresh RingCentral RingCX Access Token

The RingCentral RingCX Access Token will only live for a few minutes (currently 5 minutes) before needing to be refreshed. If the access token is expired, the API request will respond with:

```http
401 Unauthorized

Jwt is expired
```

Use the `refreshToken` to refresh the RingCentral RingCX access token, by calling the following RingCX API.

### Request

```http
POST https://engage.ringcentral.com/api/auth/token/refresh
Content-Type: application/x-www-form-urlencoded

refresh_token=<rcRingCXRefreshToken>&rcTokenType=Bearer
```

Where:

-   **`<rcRingCXRefreshToken>`** is the RingCentral Refresh Token you received from RingCentral RingCX authentication flow.

### Response

The response will contain the same `accessToken` property that can be used in an API call, but the `refreshToken` property will be a new refresh token that can be used to refresh the access token when the access token expires. Make sure to save the new `refreshToken` for future refresh token API calls.

The following is an abbreviated response.

```json
{
  "refreshToken":"<rcRingCXRefreshToken>", //Save this as it will be new.
  "accessToken":"<rcRingCXAccessToken>",
  "tokenType":"Bearer",
  "agentDetails":[
    {
      "agentId":111111,
      "firstName":"John",
      "lastName":"Wang",
      "email":"john.wang@example.com",
      "username":"john.wang@example.com",
      "agentType":"AGENT",
      "rcUserId":222222,
      "accountId":"333333",
      "accountName":"RingForce",
      "agentGroupId":null,
      "allowLoginControl":true,
      "allowLoginUpdates":true
    }
  ],
  "adminId":1111,
  "adminUrl":"/voice/admin/",
  "agentUrl":"/voice/agent/",
  "ssoLogin":true
}
```
