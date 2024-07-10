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
    		"https://ringcx.ringcentral.com/api/auth/login/rc/accesstoken",
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