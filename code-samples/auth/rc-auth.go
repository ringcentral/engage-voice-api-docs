package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
)

// RingCXToken is an example and does not cover all the
// properties in the API response.
type RingCXToken struct {
	AccessToken string `json:"accessToken"`
	TokenType   string `json:"tokenType"`
}

func RcToRingCXToken(rctoken string) (string, error) {
	res, err := http.PostForm(
		"https://engage.ringcentral.com/api/auth/login/rc/accesstoken?includeRefresh=true",
		url.Values{"rcAccessToken": {rctoken}, "rcTokenType": {"Bearer"}})
	if err != nil {
		return "", err
	}
	defer res.Body.Close()
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
	rctoken := "VALID-RINGCENTRAL-ACCESS-TOKEN"

	ringcxToken, err := RcToRingCXToken(rctoken)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(ringcxToken)
}
