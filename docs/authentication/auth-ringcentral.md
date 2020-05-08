# Obtaining an Engage Access Token

To access Engage Voice APIs, you need to request an Engage Access Token. This is by first requesting a RingCentral Access Token and then using an Engage API to create an Engage Access Token. Then the Engage Access Token can be used to access Engage Voice APIs.

> Note: Engage Voice APIs for Office customers are rooted at:
>
> `https://engage.ringcentral.com/voice/api/`

## Retrieve RingCentral Access Token

First retrieve a RingCentral access token using the following instructions:

[RingCentral Authenticaion](https://developers.ringcentral.com/guide/authentication)

## Retrieve RingCentral Engage Access Token

Once you have a RingCentral Access Token, call the following Engage API to receive an Engage Bearer access token.

```http tab="Request"
POST https://engage.ringcentral.com/api/auth/login/rc/accesstoken
Content-Type: application/x-www-form-urlencoded

rcAccessToken=<rcAccessToken>&rcTokenType=Bearer
```

```bash tab="cURL"
$ curl -XPOST https://engage.ringcentral.com/api/auth/login/rc/accesstoken \
      -d 'rcAccessToken=<rcAccessToken>' \
      -d 'rcTokenType=Bearer'
```

```go tab="Go"
package main

import(
      "fmt"
      "encoding/json"
      "io/ioutil"
      "net/url"
    )

// EngageToken is an example and does not cover all the
// properties in the API response.
type EngageToken struct {
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
    engageToken := EngageToken{}
    bytes, err := ioutil.ReadAll(res.Body)
    if err != nil {
    		return "", err
    }
    err = json.Unmarshal(bytes, &engageToken)
    return engageToken.AccessToken, err
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

```javascript tab="Node JS"
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

```python tab="Python"
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

```PHP tab="PHP"
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
        throw new \Exception($curlErrno);
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
}catch (\Exception $e) {
    throw $e;
}
```

### Response

The response will contain the `accessToken` property that can be used in an API call. Take note of the `accountId` property as that will be used to make future API calls.

The following is an abbreviated reponse.

```json
{
  "refreshToken":null,
  "accessToken":"<rcEngageOfficeToken>",
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

## Example Engage Voice API Call

The following is an example Engage Voice API Call using a RingCentral Engage Access Token.

```http
GET https://engage.ringcentral.com/voice/api/v1/admin/users
Authorization: Bearer <rcEngageAccessToken>
```
