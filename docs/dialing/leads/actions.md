# About Lead Actions

Have a lead or multiple leads you want to do something with? Lead actions are a set of operations you can perform on a single lead or several leads.  Actions include suppressing leads, deleting leads, or even moving leads from one campaign to another. You can perform these actions on a single lead or multiple leads. The following describes such actions and guides you to different ways to programmatically work with leads.

## List of Lead Actions

| Lead Action | Description |
|-|-|
| `RESET_LEADS` | This action resets your lead pass count to zero, sets the lead status to READY, and changes the next dial time to right now. |
| `CANCEL_LEADS` | When you apply this action to your leads, they will not be dialed until you reverse the action. This action changes the lead status from whatever it was prior to the action to CANCELLED. Please note that once you cancel a lead, there is no way to revert to (or access information about) the lead’s status prior to being cancelled. |
| `DELETE_LEADS` | This action completely removes leads from the system. **Please note**, when you delete a lead from the system, the system deletes all lead data (including lead name, address, and any data provided in the Leads search). The system will, however, retain call data related to the lead (including UII, the agent who spoke with the lead, agent and system dispositions, talk time, etc.) |
| `PAUSE_LEADS` | This action functions exactly as the Cancel Leads action does — the only difference is in the name, which exists for differentiation purposes. You can categorize a lead as PAUSED if you don’t wish to dial them right now, but you would like to indicate that you might wish to dial them at some point in the future. |
| `DIALER_REFRESH` | |
| `READY_LEADS` | This action changes the lead’s current status to READY, making the lead available to dial. This action will not change the lead’s pass count or the lead’s next scheduled dial time. |
| `MANUAL_LEADS` | This action adds one manual pass count and agent disposition update to the selected lead(s). |
| `EMAIL_LEADS` | This action allows you to email a downloadable ZIP file of the lead list results to one or more email addresses (for multiple addresses, separate each with a comma). Please note that the email will contain a download link that expires within 24 hours. |
| `CALLBACK_LEADS` | This action allows you to set or cancel scheduled callback for the selected leads. |
| `MOVE_TO_CAMPAIGN` | This action moves your leads to a campaign and lead list of your choice. |
| `AGENT_RESERVATION` | This action allows you to set or cancel agent-specific callbacks for the selected leads. |
| `SUPPRESS_LEADS` | When you apply this action to your leads, they will not be dialed until you reverse the action. This action does not change a lead’s status from whatever it was prior to the suppressing action. This simply allows you to stop a lead from being dialed while maintaining their current lead status. |
| `UNSUPPRESS_LEADS` | Apply this action to your leads to reverse the Suppress Leads action discussed above. This action will simply revert a lead’s status back to whatever it was before it was suppressed. |

## Moving Leads to Another Campaign

Let's say we have a list of leads in a campaign and we want to move all those leads to another campaign. We will need to do the following:

* Find the campaign ID of the campaign you wish to move from and to.
* Find an existing list to move leads to (optional).
* Move the leads to the new campaign with some options.

### Find the Campaign IDs

To move leads from one campaign to another, you first must find the source campaign ID and the target campaign ID. To find the campaign ID, iterate through each dial group, in each account, and find the campaign that matches the one you are looking for.

#### Javascript Example
```javascript
async function findCampaignByName (
  engageVoice,
  name
) {
  let r = await engageVoice.get('/api/v1/admin/accounts');
  for (const account of r.data) {
    r = await engageVoice.get(
      `/api/v1/admin/accounts/${account.accountId}/dialGroups`
    );
    for (const dialGroup of r.data) {
      r = await engageVoice.get(
        `/api/v1/admin/accounts/${account.accountId}/dialGroups/${dialGroup.dialGroupId}/campaigns`
      );
      for (const campaign of r.data) {
        if (campaign.campaignName === name) {
          return {account, dialGroup, campaign};
        }
      }
    }
  }
  throw new Error(`Cannot find the campaign by name "${name}".`);
};
```

### Find Exisiting Lists to Move Leads to (Optional)

Using the above function, we can also find the new campaign for our leads. With this new campaign ID, we can check if there is an existing list we can move our leads to. This step is not necessary as we can just create a new list, but here is how you use existing lists on your target campaign.

#### Javascript Example
```javascript
let leadList = await ev.get(
    '/api/v1/admin/accounts/'+thisCampaign.account.accountId+'/dialGroups/'+thisCampaign.dialGroup.dialGroupId+'/campaigns/'+thisCampaign.campaign.campaignId+'/lists'
  );
```

### Move Leads into new Campaign

Using the same JavaScript function above, you can also find the target campaign ID by name. With that campaign ID, move the leads to a new list in the new campaign.

#### Javascript Example
```javascript tab="Node JS"
await ev.put(
    '/voice/api/v1/admin/accounts/'+thisCampaign.account.accountId+'/campaignLeads/actions?leadAction=MOVE_TO_CAMPAIGN',    
    {
      "campaignLeadSearchCriteria":
      {
        "campaignId":thisCampaign.campaign.campaignId,
        "listIds":[],
        "agentDispositions":[],
        "systemDispositions":[],
        "leadStates":[],
        "physicalStates":[],
        "leadTimezones":[],
        "campaignIds":[thisCampaign.campaign.campaignId]
      },
      "leadActionParams":
      {
        "paramMap":
        {
          "CAMPAIGN_ID":newCampaign.campaign.campaignId,
          "LIST_ID":"0",
          "LIST_NAME":"New Leads List",
          "CREATE_COPY_SETTING":"false",
          "DUPLICATE_ACTION_SETTING":"MOVE"
        }
      }
    }
  );
```

```python tab="Python"
#### Install Python SDK wrapper ####
# $ pip3 install ringcentral_engage_voice
#  or
# $ pip install ringcentral_engage_voice
#####################################

from ringcentral_engage_voice import RingCentralEngageVoice

def move_leads_to_campaign():
    try:
        # Leads are to be moved from one campaign to another
        fromCampaignId = 0
        toCampaignId = 0

        dialGroupsEndpoint = "/api/v1/admin/accounts/{accountId}/dialGroups"
        dialGroupsResponse = ev.get(dialGroupsEndpoint).json()
        for group in dialGroupsResponse:
            # Find your Dial Group
            if group['dialGroupName'] == "My New Dial Group":
                campaignsEndpoint = f"{dialGroupsEndpoint}/{group['dialGroupId']}/campaigns"    # f string:https://www.python.org/dev/peps/pep-0498/
                campaignsResponse = ev.get(campaignsEndpoint).json()
                for campaign in campaignsResponse:
                    # Find From-Campaign and To-Campaign
                    if campaign['campaignName'] == "My Predictive Campaign":
                        fromCampaignId = campaign['campaignId']
                    if campaign['campaignName'] == "My New Predictive Campaign Python":
                        toCampaignId = campaign['campaignId']
                        
                # Validate and move Leads
                if fromCampaignId !=0 and toCampaignId !=0:
                    params = "leadAction=MOVE_TO_CAMPAIGN"
                    moveLeadsEndpoint = "/api/v1/admin/accounts/{accountId}/campaignLeads/actions"
                    putBody = {
                        "campaignLeadSearchCriteria":
                        {
                            "campaignId": fromCampaignId,
                            "listIds": [],
                            "agentDispositions": [],
                            "systemDispositions": [],
                            "leadStates": [],
                            "physicalStates": [],
                            "leadTimezones": [],
                            "campaignIds": [fromCampaignId]
                        },
                        "leadActionParams":
                        {
                            "paramMap":
                            {
                                "CAMPAIGN_ID": toCampaignId,
                                "LIST_ID": "0",
                                "LIST_NAME": "New Leads List",
                                "CREATE_COPY_SETTING": "false",
                                "DUPLICATE_ACTION_SETTING": "MOVE"
                            }
                        }
                    }
                    moveLeadsResponse = ev.put(moveLeadsEndpoint, putBody, params).json()
                    print(moveLeadsResponse)
                else:
                    print("Unable to find target campaigns")
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

    move_leads_to_campaign()
except Exception as e:
    print(e)
```

#### Move Parameters
| Parameter | Description |
|-|-|
| `CAMPAIGN_ID` | The ID of the campaign you want to move to. |
| `LIST_ID` | Identified of the list you want to move to. If you are creating a new list, set this to `0`. |
| `LIST_NAME` | If you are creating a new list on the new campaign, enter it here. Otherwise, you can leave this parameter out. |
| `CREATE_COPY_SETTING` | To move the original leads, set this to `false`. However, you can also make a copy of the leads so they exist in both places by setting this to `true`. A special setting will create a copy of the leads in the new campaign, but will also set the lead state to TRANSITION. Set this parameter to `TRANSITION` so the copied lead's state become TRANSITION. |
| `DUPLICATE_ACTION_SETTING` | The target lead list may already have the lead you are trying to move/copy over. You can choose to move the lead over anyway by setting this to `MOVE`, or to not move duplicates, set this to `IGNORE`. |
