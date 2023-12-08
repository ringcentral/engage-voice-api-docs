<?php
require('vendor/autoload.php');

// Instantiate the SDK wrapper object with your RingCentral app credentials
$ev = new EngageVoiceSDKWrapper\RestClient("RC_APP_CLIENT_ID", "RC_APP_CLIENT_SECRET");
try{
  // Login your account with your RingCentral Office user credentials
  $ev->login("RC_USERNAME", "RC_PASSWORD", "RC_EXTENSION_NUMBER");
  $endpoint = "admin/accounts/~/gateGroups";
  // get a list of Queue Groups and find the "Platform" queue group for this user
  $response = $ev->get($endpoint);
  $jsonObj = json_decode($response);
  foreach ($jsonObj as $group){
      if ($group->groupName == "Platform"){
          // get a list of Queues from this "Platform" Queue Group
          $endpoint = 'admin/accounts/~/gateGroups/' . $group->gateGroupId . "/gates";
          $response = $ev->post($endpoint);
          $jsonObj = json_decode($response);
          foreach ($jsonObj as $queue) {
              if ($queue->gateName == "My PHP Queue"){
                $endpoint .= '/' . $queue->gateId;
                $queue->gateDesc = "An *edited* queue description for this Queue"
                $queueInfo = $ev->put($endpoint, $queue);
                print ($queueInfo);
                break;
              }
          }
          break;
      }
  }
}catch (Exception $e) {
  print $e->getMessage();
}
