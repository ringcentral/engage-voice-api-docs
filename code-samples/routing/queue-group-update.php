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
        if ($group->groupName == "My New Queue Group"){
            $endpoint = 'admin/accounts/~/gateGroups/' . $group->gateGroupId;
            $params = array ( "groupName" => $group->groupName . " - Updated" );
            $response = $ev.put($endpoint, $params);
            print ($response);
        }
    }
}catch (Exception $e) {
    print $e->getMessage();
}

