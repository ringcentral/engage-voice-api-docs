<?php
// Remember to modify the path to where you installed the RingCentral SDK and saved your .env file!
require('./../vendor/autoload.php');
$dotenv = Dotenv\Dotenv::createImmutable(__DIR__ . '/../');
$dotenv->load();

$ev = new EngageVoiceSDKWrapper\RestClient(
    $_ENV['RC_CLIENT_ID'],
    $_ENV['RC_CLIENT_SECRET']
);

try{
    $resp = $ev->login( [ "jwt" => $_ENV['RC_JWT'] ], function($response){
      list_account_active_calls($resp->agentDetails[0]->accountId);
    });
}catch (Exception $e) {
    print $e->getMessage();
}

function list_account_active_calls($accountId){
    global $ev;
    $endpoint = "admin/accounts/~/activeCalls/list";
    $params = array (
      'product' => "ACCOUNT",
      'productId' => $accountId
    );
    try{
        $resp = $ev->get($endpoint, $params);
        print ($resp."\r\n");
    }catch (Exception $e) {
        print ($e->getMessage());
    }
}
