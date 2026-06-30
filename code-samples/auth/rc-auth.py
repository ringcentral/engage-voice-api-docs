import json
import requests

RC_ACCESS_TOKEN = "VALID-RINGCENTRAL-ACCESS-TOKEN"
url = "https://engage.ringcentral.com/api/auth/login/rc/accesstoken?includeRefresh=true"
body = {
    "rcAccessToken": RC_ACCESS_TOKEN,
    "rcTokenType": "Bearer"
}
headers = {
              'Content-Type': 'application/x-www-form-urlencoded'
          }
try:
    res = requests.post(url, headers=headers, data=body)
    if res.status_code == 200:
        jsonObj = json.loads(res.content)
        print (jsonObj['accessToken'])
    else:
        print (res.content)
except Exception as e:
    raise ValueError(e)
