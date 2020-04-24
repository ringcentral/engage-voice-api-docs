# Obtaining an Engage Access Token

To access Engage Voice APIs, you need to request an Engage Access Token. This is by first requesting a RingCentral Access Token and then using an Engage API to create an Engage Access Token. Then the Engage Access Token can be used to access Engage Voice APIs.

> Note: Engage Voice APIs for Office customers are rooted at:
> 
> `https://engage.ringcentral.com/voice/api/`

## Retrieve RingCentral Access Token

First retrieve a RingCentral access token using the following instructions:

https://developers.ringcentral.com/guide/authentication

## Retrieve RingCentral Engage Access Token

Once you have a RingCentral Access Token, call the following Engage API to receive an Engage Bearer access token.

```http tab="Request"
POST https://engage.ringcentral.com/api/auth/login/rc/accesstoken
Content-Type: application/x-www-form-urlencoded

rcAccessToken=<rcAccessToken>&rcTokenType=Bearer
```

```bash tab="cURL"
$ curl -XPOST https://engage.ringcentral.com/api/auth/login/rc/accesstoken \
-d 'rcAccessToken=<rcAccessToken>'  -d 'rcTokenType=Bearer'
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

```
GET https://engage.ringcentral.com/voice/api/v1/admin/users
Authorization: Bearer <rcEngageAccessToken>
```