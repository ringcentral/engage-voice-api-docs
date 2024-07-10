var https = require('https')

var RC_ACCESS_TOKEN = "VALID-RINGCENTRAL-ACCESS-TOKEN"

var url = "ringcx.ringcentral.com"
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