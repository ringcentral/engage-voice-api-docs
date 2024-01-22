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
