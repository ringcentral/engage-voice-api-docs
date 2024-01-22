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
