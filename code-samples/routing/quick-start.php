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
    $ev->login( [ "jwt" => $_ENV['RC_JWT'] ], function($response){
      create_a_queue_group();
    });
} catch (Exception $e) {
    print $e->getMessage();
}

function create_a_queue_group(){
  global $ev;
  try{
    $endpoint = "admin/accounts/~/gateGroups";
    $params = array ( 'groupName' => "My New Queue Group" );
    $response = $ev->post($endpoint, $params);
    print ($response."\r\n");
  }catch (Exception $e) {
    print $e->getMessage();
  }
}
?>
