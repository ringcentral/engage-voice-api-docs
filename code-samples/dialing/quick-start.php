<?php
require('vendor/autoload.php');

$ev = new EngageVoiceSDKWrapper\RestClient(
    $_ENV['RC_CLIENT_ID'],
    $_ENV['RC_CLIENT_SECRET']
);

try{
    $ev->login( [ "jwt" => $_ENV['RC_JWT'] ], function($response){
      create_a_dial_group();
    });
}catch (Exception $e) {
    print $e->getMessage();
}

function create_a_dial_group(){
  global $ev;
  try{
    $endpoint = 'admin/accounts/~/dialGroups';
    $params = array (
      "dialGroupName" => "My Dial Group - Predictive",
      "dialGroupDesc" => "A test dial group with predictive dial mode",
      "dialMode" => "PREDICTIVE",
      "isActive" => true
    );
    $response = $ev->post($endpoint, $params);
    print ($response."\r\n");
  }catch (Exception $e) {
    print $e->getMessage();
  }
}
?>
