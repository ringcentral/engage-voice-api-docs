# About Bulk Lead Import

The RingCX API allows you to load one or multiple leads at a time. You can also load leads for immediate dialing at the top of the dialer cache or in normal priority.

!!! alert "Please Note"
    To enumerate a list of Campaigns for the `campaignId` path property, please review section [Enumerating Campaigns](./#enumerating-campaigns) below.

The JSON body consists of a set of options along with an array of leads in the `uploadLeads` property

## Primary parameters

Some key options for the request body include:

| Property | Description |
|-|-|
| **dialPriority** | set this value to `IMMEDIATE` to add leads to the top of the dialer queue, `NORMAL` otherwise. |
| **duplicateHandling** | Duplicates are determined by the lead's `leadPhone` property.<ul><li>`REMOVE_ALL_EXISTING` means to remove the new lead in this batch in favor of the existing lead in any list in the campaign (as long as that lead in the existing lead list was already added with this same property). This means that the lead was already loaded into one of the lists within the campaign using `REMOVE_ALL_EXISTING` previously.</li><li>`REMOVE_FROM_LIST` looks for duplicate leads in the list being uploaded. It does not remove duplicates in the lead list that has already been imported previously.</li><li>`RETAIN_ALL` means to keep all duplicates.</li></ul> |
| **timeZoneOption** | this field tells the Engage how to set the timezone for the user. Use `NPA_NXX` to set the timezone via the lead's phone number. Use `ZIPCODE` to set the timezone via the lead's zipcode. Use `EXPLICIT` to set the timezone via the `CampaignLead` object's `leadTimezone` property. Finally, use `NOT_APPLICABLE` if there is no timezone desired. |

Each load in the `uploadLeads` array consists of a lead with the following notable options:

| Property | Description |
|-|-|
| **externId** | this is a required string property. |
| **leadPhone** | this can be a single phone number or a pipe-deliminted field of multiple phone numbers. For US numbers, this is a 10 digit format including area code. |

## Enumerating Campaigns

Leads are uploaded per Campaign which requires a `campaignId`. The following two API calls will enable enumerating the account's campaign list.

1. Call the Get Dial Groups API to get a list of dial groups. Each dial group will have a `dialGroupId` property.

     `GET /api/v1/admin/accounts/{accountId}/dialGroups`

2. For the Dial Group of interest, call the Get Dial Group Campaigns API:

     `GET /api/v1/admin/accounts/{accountId}/dialGroups/{dialGroupId}/campaigns`

## Upload Leads for a campaign

To upload leads for a campaign, we will need a campaign Id. As campaigns are members of a dialing group.

## Enumerating Campaigns and Import Leads

### Request
Be sure to set the proper [BASE_URL](../../../basics/uris/#resources-and-parameters) and [authorization header](../../../authentication/auth-ringcentral) for your deployment.

=== "HTTP"
    ```http
    POST {baseURL}/api/v1/admin/accounts/{accountId}/campaigns/{campaignId}/leadLoader/direct
    Authorization: Bearer <yourAccessToken>

    {
        "description": "Prospect customers",
        "dialPriority": "IMMEDIATE",
        "duplicateHandling": "REMOVE_FROM_LIST",
        "listState": "ACTIVE",
        "timeZoneOption": "NOT_APPLICABLE",
        "uploadLeads": [
          {
             "leadPhone":"1111111111",
             "externId":"1",
             "title":"Dr.",
             "firstName":"Jeff",
             "midName":"John",
             "lastName":"Malfetti",
             "suffix":"Jr.",
             "address1":"3101 Fake St.",
             "address2":"Suite 120",
             "city":"Rock",
             "state":"CO",
             "zip":"80500",
             "email":"test@test.com",
             "gateKeeper":"Some one",
             "auxData1":30,
             "auxData2":"a",
             "auxData3":100,
             "auxData4":"aa",
             "auxData5":1000,
             "auxPhone":"1111111110",
             "extendedLeadData":{
                "important":"data",
                "interested":true
             }
          },{
             "leadPhone":"2222222222",
             "externId":"222",
             "firstName":"Jason",
             "midName":"",
             "lastName":"Black",
             "address1":"1514 Bernardo Ave",
             "city":"New York",
             "state":"NY",
             "zip":"10001",
          },{
             "leadPhone":"3333333333",
             "externId":"333",
             "firstName":"Rich",
             "lastName":"Dunbard"
          }
        ],
       "dncTags":[
      
       ]
    }
    ```
=== "Node JS"
    ```javascript
    /****** Install Node JS SDK wrapper *******
    $ npm install ringcentral-engage-voice-client
    *******************************************/

    const RunRequest = async function () {
        const EngageVoice = require('ringcentral-engage-voice-client').default

        // Instantiate the SDK wrapper object with your RingCentral app credentials
        const ev = new EngageVoice({
            clientId: "RINGCENTRAL_CLIENTID",
            clientSecret: "RINGCENTRAL_CLIENTSECRET"
        })

        try {
            // Authorize with your RingCentral Office user credentials
            await ev.authorize({
                username: "RINGCENTRAL_USERNAME",
                extension: "RINGCENTRAL_EXTENSION",
                password: "RINGCENTRAL_PASSWORD"
            })

            // Get Dial Groups data
            const groupsEndpoint = "/api/v1/admin/accounts/{accountId}/dialGroups"
            const groupsResponse = await ev.get(groupsEndpoint)
            for (var group of groupsResponse.data) {
                // Select your Dial Group
                if (group.dialGroupName == "My New Dial Group") {
                    const campaignsEndpoint = groupsEndpoint + "/" + group.dialGroupId + "/campaigns"
                    const campaignsResponse = await ev.get(campaignsEndpoint)
                    for (var campaign of campaignsResponse.data) {
                        // Select your Campaign and import Leads
                        if (campaign.campaignName == "My Predictive Campaign") {
                            const leadsEndpoint = "/api/v1/admin/accounts/{accountId}/campaigns/" +     campaign.campaignId + "/leadLoader/direct"
                            const postData = {
                                "listState": "ACTIVE",
                                "duplicateHandling": "RETAIN_ALL",
                                "timeZoneOption": "NPA_NXX",
                                "description": "Lead Search Test",
                                "dialPriority": "IMMEDIATE",
                                "uploadLeads": [{
                                    "leadPhone": "8888888888",
                                    "externId": "222",
                                    "firstName": "Jason",
                                    "midName": "",
                                    "lastName": "Black",
                                    "address1": "1514 Bernardo Ave",
                                    "city": "New York",
                                    "state": "NY",
                                    "zip": "10001",
                                }, {
                                    "leadPhone": "3323333333",
                                    "externId": "333",
                                    "firstName": "Rich",
                                    "lastName": "Dunbard"
                                }
                                ]
                            }
                            const leadsResponse = await ev.post(leadsEndpoint, postData)
                            console.log(leadsResponse.data)
                        }
                    }
                }
            }
        }
        catch (err) {
            console.log(err.message)
        }
    }

    RunRequest();
    ```
=== "Python"  
    ```python
    #### Install Python SDK wrapper ####
    # $ pip3 install ringcentral_engage_voice
    #  or
    # $ pip install ringcentral_engage_voice
    #####################################

    from ringcentral_engage_voice import RingCentralEngageVoice

    def import_leads():
        try:
            dialGroupsEndpoint = "/api/v1/admin/accounts/{accountId}/dialGroups"
            dialGroupsResponse = ev.get(dialGroupsEndpoint).json()
            for group in dialGroupsResponse:
                # Select your Dial Group
                if group['dialGroupName'] == "My New Dial Group":
                    campaignsEndpoint = f"{dialGroupsEndpoint}/{group['dialGroupId']}/campaigns"    #   f   string:https://www.python.org/dev/peps/pep-0498/
                    campaignsResponse = ev.get(campaignsEndpoint).json()
                    for campaign in campaignsResponse:
                        # Select your Campaign and import Leads
                        if campaign['campaignName'] == "My Predictive Campaign":
                            leadsEndpoint = f"/api/v1/admin/accounts/{accountId}/campaigns/{campaign    ['campaignId']}/leadLoader/direct"
                            postBody = {
                              "description": "Prospect customers",
                              "dialPriority": "IMMEDIATE",
                              "duplicateHandling": "REMOVE_FROM_LIST",
                              "listState": "ACTIVE",
                              "timeZoneOption": "NPA_NXX",
                              "uploadLeads": [{
                                   "leadPhone":"8888888888",
                                   "externId":"222",
                                   "firstName":"Jason",
                                   "midName":"",
                                   "lastName":"Black",
                                   "address1":"1514 Bernardo Ave",
                                   "city":"New York",
                                   "state":"NY",
                                   "zip":"10001",
                                },{
                                   "leadPhone":"3323333333",
                                   "externId":"333",
                                   "firstName":"Rich",
                                   "lastName":"Dunbard"
                                }
                              ]
                            }
                            leadsResponse = ev.post(leadsEndpoint, postBody).json()
                            print(leadsResponse)
                            break
        except Exception as e:
            print(e)


    # Instantiate the SDK wrapper object with your RingCentral app credentials
    ev = RingCentralEngageVoice(
        "RINGCENTRAL_CLIENTID",
        "RINGCENTRAL_CLIENTSECRET")

    try:
        # Authorize with your RingCentral Office user credentials
        ev.authorize(
            username="RINGCENTRAL_USERNAME",
            password="RINGCENTRAL_PASSWORD",
            extension="RINGCENTRAL_EXTENSION"
        )

        import_leads()
    except Exception as e:
        print(e)
    ```
=== "PHP"
    ```php
    /************ Install PHP SDK wrapper **************
    $ composer require engagevoice-sdk-wrapper:dev-master
    *****************************************************/
    
    <?php
    require('vendor/autoload.php');
    
    require('vendor/autoload.php');
    
    // Instantiate the SDK wrapper object with your RingCentral app credentials
    $ev = new EngageVoiceSDKWrapper\RestClient("RC_APP_CLIENT_ID", "RC_APP_CLIENT_SECRET");
    try{
      // Login your account with your RingCentral Office user credentials
      $ev->login("RC_USERNAME", "RC_PASSWORD", "RC_EXTENSION_NUMBER");
        read_dial_groups();
    }catch (Exception $e) {
        print $e->getMessage();
    }
    
    function read_dial_groups(){
      global $ev;
      $endpoint = 'admin/accounts/~/dialGroups';
      try{
        $resp = $ev->get($endpoint);
        $jsonObj = json_decode($resp);
        foreach ($jsonObj as $group){
          if ($group->dialGroupName == "My Dial Group - Predictive"){
            read_group_campaigns($group->dialGroupId);
            break;
          }
        }
      }catch (Exception $e) {
          print $e->getMessage();
      }
    }
    
    function read_group_campaigns($dialGroupId){
      global $ev;
      $endpoint = 'admin/accounts/~/dialGroups/' . $dialGroupId . "/campaigns";
      try{
        $resp = $ev->get($endpoint);
        $jsonObj = json_decode($resp);
        foreach ($jsonObj as $campaign){
          if ($campaign->campaignName == "API Test"){
              load_campaign_leads($campaign->campaignId)
              break;
          }
        }
      }catch(Exception $e) {
          print $e->getMessage();
      }
    }
    
    function load_campaign_leads($campaignId){
      global $ev;
      $endpoint = 'admin/accounts/~/campaigns/' . $campaignId . "/leadLoader/direct";
      $params = array (
        "description" => "Prospect customers",
        "dialPriority" => "IMMEDIATE",
        "duplicateHandling" => "REMOVE_FROM_LIST",
        "listState" => "ACTIVE",
        "timeZoneOption" => "NOT_APPLICABLE",
        "uploadLeads" => array (
          array (
             "leadPhone" => "1111111111",
             "externId" => "1",
             "title" => "Dr.",
             "firstName" => "Jeff",
             "midName" => "John",
             "lastName" => "Malfetti",
             "suffix" => "Jr.",
             "address1" => "3101 Fake St.",
             "address2" => "Suite 120",
             "city" => "Rock",
             "state" => "CO",
             "zip" => "80500",
             "email" => "test@test.com",
             "gateKeeper" => "Some one",
             "auxData1" => 30,
             "auxData2" => "a",
             "auxData3" => 100,
             "auxData4" => "aa",
             "auxData5" => 1000,
             "auxPhone" => "1111111110",
             "extendedLeadData" => array (
                "important" => "data",
                "interested" => true
             )
          ),
          array (
             "leadPhone" => "2222222222",
             "externId" => "222",
             "firstName" => "Jason",
             "midName" => "",
             "lastName" => "Black",
             "address1" => "1514 Bernardo Ave",
             "city" => "New York",
             "state" => "NY",
             "zip" => "10001",
          ),
          array (
             "leadPhone" => "3333333333",
             "externId" => "333",
             "firstName" => "Rich",
             "lastName" => "Dunbard"
          )
        )
      );
      try{
        $resp = $ev->post($endpoint, $params);
        print ($resp);
      }catch(Exception $e) {
          print $e->getMessage();
      }
    }
    ```
