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
            // Create a new Queue for this queue group
            $endpoint = 'admin/accounts/~/gateGroups/' . $group->gateGroupId . "/gates";
            $params = array (
              "isActive" => true,
              "gateName" => "My PHP Queue",
              "gateDesc" => "An initial queue for this Queue Group"
            );
            $response = $ev->post($endpoint, $params);
            print ($response);
        }
    }
  }catch (Exception $e) {
    print $e->getMessage();
  }
