<?php
require('vendor/autoload.php');

// Instantiate the SDK wrapper object with your RingCentral app credentials
$ev = new EngageVoiceSDKWrapper\RestClient("RC_APP_CLIENT_ID", "RC_APP_CLIENT_SECRET");
try{
  // Login your account with your RingCentral Office user credentials
  $ev->login("RC_USERNAME", "RC_PASSWORD", "RC_EXTENSION_NUMBER");
  $endpoint = "admin/accounts/~/gateGroups";
  $response = $ev->get($endpoint);
  $jsonObj = json_decode($response);
  foreach ($jsonObj as $group){
    print ("Queue group name: ".$group->groupName."\r\n");
    print ("Queue group id: ".$group->gateGroupId."\r\n");
  }
}catch (Exception $e) {
  print $e->getMessage();
}
