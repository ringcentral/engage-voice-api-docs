# About Redshift Database Access

!!! danger "Critcal Notice!!"
    The Redshift Database Access only operates on Prebuilt Reports. Since Prebuilt Reports have been [discontinued](https://support.ringcentral.com/engagevoice/analytics/voice-analytics-intro-scheduled-reports.html), the use of the Redshift Database Access will be for legacy reporting only. 

!!! info "Purchasing Redshift Database Access"
    The Redshift Database Access is a chargeable item and must be granted by your account manager. Please reach out to your account manager to purchase and activate the Redshift Database Access.

!!! warning "Not for Engage Omni"
    The Redshift Database Access is not suitable for Engage Omni. If you are a new Engage Omni user, please use the [Historical reports and dashboards](https://support.ringcentral.com/engagevoice/analytics/historical-reports-dashboards.html) instead for your reporting purposes.

When accessing the Redshift Historical Database you will be provided with a username, password, schema name and JDBC connection URL. The credentials will only enable a user to read/query from the database. There are also limitations as to the number of connections (5) and time that a query can run (5 minutes) before they are refused or terminated respectfully.

With the aforementioned credentials you can create a connection to the historical database with your choice of client. This client will need to support either a Postgres or preferably the Redshift JDBC driver.

The Redshift JDBC driver and generic connection information can be found [here](https://docs.aws.amazon.com/redshift/latest/mgmt/configure-jdbc-connection.html#download-jdbc-driver).

The AWS tutorial and help pages for Redshift can be found [here](https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html).

Once connected the user will have read permissions to all schemas on the database. However, you will only be able to query your provided schema. Underneath each schema is a Redshift View. These views mirror all of the tables in the production schema and contain all of the same columns.

The following query is useful as it will provide you with a list of views that your user has access to.

```sql
SELECT
table_schema as schema_name,
table_name as view_name
FROM information_schema.views
WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
ORDER BY schema_name, view_name;
```

## Views (Tables)
You can also view this through each client GUI. The \_XXXXXXXX schema names are visible and from there you can list the views under each schema. The available views are listed below.

* agent_block_monitor
* agent_login_gates
* agent_logins
* agent_states
* call_events
* call_sessions
* calls
* dnc_list
* internal_chats
* international_calls
* reverse_match_results
* scripting_studio_result
* survey_response_details (Legacy Surveys - no longer supported)
* survey_responses (Legacy Surveys - no longer supported)
* visual_ivr_results
* whitelist_entries

From the list of available views, there are 4 main tables that are generally of most interest when creating KPIs.

* calls
* call_sessions
* agent_logins
* agent_states

## Tables

A brief description of the four core tables are below.

### CALLS
By far the largest table with the most information. It is also the largest table in terms of data stored and number of columns, which as of this documentation is 165. This creates a challenge at times when querying because you must be very specific about the information that you want to return or the performance of your query will suffer.

This Calls table contains a unique record per call. In most scenarios this will mean one record per uii. A uii is a unique 30 character call identifier with the first 14 digits representing the time that the call initiated on the Engage Voice platform. An example uii might look like this.

UII - 202001010011550131070000000400

We also use a shortened version of the uii which is titled the uii_table_key. The uii_table_key is 28 characters in length. This allowed us to change the data type from a varchar to a bigint which enabled slightly faster query performance while searching for specific uiis. Using the example uii above the uii_table_key would be…

UII_TABLE_KEY - 2001010011550131070000000400

The only difference being the _first two characters_ have been removed.

On the calls table and any other table related to call data, we use the uii_table_key as a distribution key. This is because the uii_table_key has a very high cardinality. We also create a compound sort key with uii_table_key and account_id. This keeps the data organized chronologically and makes for faster querying. A table with the sort and distribution keys is located at the bottom of this document.

The Calls table contains information on any product ID the call was associated with. These columns are gate_id, campaign_id, visual_ivr_id, trac_id, cloud_destination_id, etc. The products all have a product name column, that may make them easier to identify. An example is “campaign_name” or “gate_name”. The majority of calls will be related to either Gates (now titled as Queues in the application), Campaigns, or IVRs. It can be the case that a call contains more than one product, if that is the case all products related to that call will populate the respective column with a product_id and product name. These can be used to group calls by products, search for calls on a specific product, etc. Lastly, the calls table also contains basic information as of the final call state and agent information who may have handled the call. This includes agent_id, agent_username, agent_login_id, and agent_disposition.

### CALL_SESSIONS
The call sessions table is similar to the calls table however each record is broken down by session_id. Most calls will have more than one session_id, one for each leg of the call. Records with a session_id of 1 can be thought of as the entire encapsulated call. All subsequent session_ids are an individual leg of the call. For example, an agent may dial out to a lead, then once connected the agent may determine that another agent might be better able to handle that call and then transfer to an inbound Queue (gate_id). The call would have three sessions, one for the entire call, one for the outbound leg to the lead, and one on the transfer to the Queue. The call_sessions table also uses the uii_table_key and account_id distribution and sort keys.

### AGENT_LOGINS
The agent_logins table gives a summed up version of specific agent login sessions. A login session is the time period between when an agent logs into the platform and when they logout. This table contains statistics about the specific state duration for each agent session, as well as metadata related to each agent like username, agent_id, agent_group_id, agent_name, agent_team, etc. Each agent login session is given an agent_login_id which is a unique identifier that can be filtered by to determine the number of calls that an agent fielded in one login session. There are several timestamps on this table including login_dts, and logout_dts. The agent_logins table is distributed evenly across all nodes in the Redshift cluster so there is not a distribution key, however there is a compound sort key that utilizes the login_dts, and account_id columns.

### AGENT_STATES
The agent_states table is a detailed breakdown of agent state information. There are only 13 columns in the table. All records are sorted by account_id and agent_login_id with agent_login_id being the distribution key for the table. This table contains state_label which is the custom label assigned to a base working state if any. It also contains the base_state and the duration in seconds for how long the agent was in that particular state. It also contains the uii_table_key for any call that may have been tied to that state.

There are also two columns on each table that are titled etl_job_timestamp and etl_job_guid. These are internal columns used to track the progress of data loading into the Redshift cluster and can be ignored.

## Sample Queries

We highly advise against writing any SELECT * query especially against the CALLS table. It is not performant and may cause us to cancel any long running query.

### GENERIC CALLS SELECT

```sql
SELECT
uii_table_key,
account_id,
call_timestamp,
enqueue_time,
dequeue_time,
dequeue_attempts,
dial_type,
call_type,
agent_notes,
gate_id,
gate_name,
is_presented,
is_accepted,
agent_disposition,
campaign_id,
campaign_name,
visual_ivr_id,
visual_ivr_name,
lead_id,
list_id,
pass_number,
agent_login_id,
agent_id
FROM _xxxxxxxx.calls
WHERE account_id = xxxxxxxx AND uii_table_key BETWEEN 2001010011550131070000000400 AND 2001020011550131070000000400;
```

### GENERIC AGENT LOGINS

```sql
SELECT
account_id,
agent_id,
agent_login_id,
username,
last_name,
fist_name,
email,
login_dts,
logout_dts,
login_time,
available_time,
engaged_time,
lunch_time,
work_time,
train_time,
rna_time,
pending_disp_time,
agent_phone,
team
FROM _xxxxxxxx.agent_logins
WHERE account_id = xxxxxxxx AND login_dts BETWEEN ‘2020-01-01 00:00:00’ AND ‘2020-01-02 00:00:00’;
```

## Sort and Distribution Keys
The table below contains a list of distribution and sort keys for each table. If the distkey column is true, then that column is the distribution key for the table. For the sort key column, the number corresponds to the position of the column in the compound sort. We encourage you to use both the distribution key and sort keys when writing queries. To do this include them in your WHERE clause and include them on any joins.

| Table | Column | Data Type | Distribution Key | Sort Key|
|-|-|-|-|-|
| agent_block_monitor | agent_login_id | bigint | false | 2 |
| agent_login_gates | agent_login_id | bigint | false | 2 |
| agent_states | agent_login_id | bigint | true | 1 |
| internal_chats | log_id | bigint | true | 0 |
| agent_block_monitor | account_id | integer | false | 1 |
| agent_login_gates | account_id | integer | false | 1 |
| agent_logins | account_id | integer | false | 2 |
| agent_states | account_id | integer | false | 2 |
| call_events | account_id | integer | false | 1 |
| call_sessions | account_id | integer | false | 2 |
| calls | account_id | integer | false | 2 |
| chats | account_id | integer | false | 1 |
| dnc_list | account_id | integer | false | 1 |
| internal_chats | account_id | integer | false | 2 |
| international_calls | account_id | integer | false | 2 |
| reverse_match_results | account_id | integer | false | 2 |
| scripting_studio_result | account_id | integer | false | 2 |
| survey_response_details | account_id | integer | false | 2 |
| survey_response_details | response_id | integer | true | 1 |
| survey_responses | account_id | integer | false | 2 |
| visual_ivr_results | account_id | integer | false | 2 |
| whitelist_entries | account_id | integer | false | 1 |
| call_events | uii_table_key | numeric(28,0) | true | 2 |
| call_sessions | uii_table_key | numeric(28,0) | true | 1 |
| calls | uii_table_key | numeric(28,0) | true | 1 |
| chats | uii_table_key | numeric(28,0) | true | 2 |
| international_calls | uii_table_key | numeric(28,0) | true | 1 |
| reverse_match_results | uii_table_key | numeric(28,0) | true | 1 |
| scripting_studio_result | uii_table_key | numeric(28,0) | true | 1 |
| survey_responses | uii_table_key | numeric(28,0) | true | 1 |
| visual_ivr_results | uii_table_key | numeric(28,0) | true | 1 |
| agent_logins | login_dts | timestamp without time zone | false | 1 |
| dnc_list | added_date | timestamp without time zone | false | 2 |
| internal_chats | message_dts | timestamp without time zone | false | 1 |
| whitelist_entries | added_dts | timestamp without time zone | false | 2 |

## Table Descriptions
Below are tables containing the columns their position in the tables they belong to. They also list their data type, max length, and whether that column is nullable or not.

### CALLS
| Position | Column | Data Type | Max Length | Nullable |
|-|-|-|-|-|
| 1 | uii_table_key | numeric | 28 | NO |
| 2 | uii | character | 30 | NO |
| 3 | account_id | integer | 32 | NO |
| 4 | account_name | character varying | 126 | YES |
| 5 | call_timestamp | timestamp without time zone | | YES |
| 6 | call_date | date | | YES |
| 7 | visual_ivr_id | integer | 32 | YES |
| 8 | trac_id | integer | 32 | YES |
| 9 | cloud_profile_id | integer | 32 | YES |
| 10 | campaign_id | integer | 32 | YES |
| 11 | campaign_name | character varying | 150 | YES |
| 12 | campaign_desc | character varying | 255 | YES |
| 13 | gate_id | integer | 32 | YES |
| 14 | gate_name | character varying | 100 | YES |
| 15 | gate_desc | character varying | 200 | YES |
| 16 | source_type | character | 20 | YES |
| 17 | lead_id | integer | 32 | YES |
| 18 | outbound_disposition | character | 25 | YES |
| 19 | source_app_id | character varying | 20 | YES |
| 20 | ani | character varying | 20 | YES |
| 21 | dnis | character varying | 20 | YES |
| 22 | originating_dnis | character varying | 20 | YES |
| 23 | aux_phone | character varying | 30 | YES |
| 24 | enqueue_time | timestamp without time zone | | YES |
| 25 | dequeue_time | timestamp without time zone | | YES |
| 26 | call_state | character | 20 | YES |
| 27 | priority_queue_event | character varying | 255 | YES |
| 28 | skill_override | character varying | 255 | YES |
| 29 | next_dequeue_time | timestamp without time zone | | YES |
| 30 | dequeue_attempts | integer | 32 | YES |
| 31 | curr_dequeue_event_id | integer | 32 | YES |
| 32 | next_session_id | integer | 32 | YES |
| 33 | recording_deleted | integer | 32 | YES |
| 34 | opt_out | boolean | | YES |
| 35 | sla_qualified | boolean | | YES |
| 36 | sla_passed | boolean | | YES |
| 37 | is_short_call | boolean | | YES |
| 38 | is_long_call | boolean | | YES |
| 39 | is_short_abandon | boolean | | YES |
| 40 | dial_type | integer | 32 | YES |
| 41 | call_type | character | 20 | YES |
| 42 | agent_notes | character varying | 65535 | YES |
| 43 | pci_compliant | boolean | | YES |
| 44 | recording_url | character varying | 555 | YES |
| 45 | call_result | character | 20 | YES |
| 46 | is_presented | boolean | | YES |
| 47 | agent_id | integer | 32 | YES |
| 48 | agent_first_name | character varying | 160 | YES |
| 49 | agent_last_name | character varying | 160 | YES |
| 50 | agent_username | character varying | 260 | YES |
| 51 | agent_externid | character varying | 255 | YES |
| 52 | is_agent_disposition_complete | boolean | | YES |
| 53 | gate_group_id | integer | 32 | YES |
| 54 | group_name | character varying | 100 | YES |
| 55 | trac_description | character varying | 255 | YES |
| 56 | trac_rule_destination | character varying | 255 | YES |
| 57 | callback_requested | boolean | | YES |
| 58 | is_callback | boolean | | YES |
| 59 | callback_uii | character varying | 30 | YES |
| 60 | callback_result | character varying | 255 | YES |
| 61 | profile_name | character varying | 255 | YES |
| 62 | profile_desc | character varying | 255 | YES |
| 63 | cloud_destination_id | integer | 32 | YES |
| 64 | destination_name | character varying | 255 | YES |
| 65 | destination_desc | character varying | 255 | YES |
| 66 | media_isci | character varying | 255 | YES |
| 67 | media_network | character varying | 255 | YES |
| 68 | media_market | character varying | 255 | YES |
| 69 | media_code | character varying | 255 | YES |
| 70 | media_format | character varying | 255 | YES |
| 71 | media_version | character varying | 255 | YES |
| 72 | media_length | character varying | 255 | YES |
| 73 | sla_time | integer | 32 | YES |
| 74 | etl_job_timestamp | timestamp without time zone | | YES |
| 75 | etl_job_guid | character varying | 256 | YES |
| 76 | latitude | numeric | 10 | YES |
| 77 | longitude | numeric | 10 | YES |
| 78 | ani_country_code | character | 5 | YES |
| 79 | ani_state | character | 5 | YES |
| 80 | agent_disposition | character varying | 180 | YES |
| 81 | outbound_externid | character varying | 180 | YES |
| 82 | main_account_name | character varying | 125 | YES |
| 83 | main_account_id | integer | 32 | YES |
| 84 | ani_is_cell | smallint | 16 | YES |
| 85 | trac_open_rule | boolean | | YES |
| 86 | trac_locater_description | character varying | 255 | YES |
| 87 | trac_location_description | character varying | 255 | YES |
| 88 | ani_city | character varying | 264 | YES |
| 89 | trac_dest_description | character varying | 255 | YES |
| 90 | dial_group_id | integer | 32 | YES |
| 91 | dial_group_name | character varying | 125 | YES |
| 92 | dial_group_desc | character varying | 125 | YES |
| 93 | billing_code | character varying | 256 | YES |
| 94 | dnis_description | character varying | 256 | YES |
| 95 | caller_id | character varying | 20 | YES |
| 96 | live_answer_message | character varying | 256 | YES |
| 97 | mach_answer_message | character varying | 256 | YES |
| 98 | list_id | bigint | 64 | YES |
| 99 | pass_number | integer | 32 | YES |
| 100 | is_complete | smallint | 16 | YES |
| 101 | uploaded_list_description | character varying | 400 | YES |
| 102 | reserved_agent_id | integer | 32 | YES |
| 103 | lead_state | character varying | 50 | YES |
| 104 | next_dial_time | timestamp without time zone | | YES |
| 105 | lead_timezone | character varying | 5 | YES |
| 106 | title | character varying | 100 | YES |
| 107 | mid_name | character varying | 100 | YES |
| 108 | suffix | character varying | 100 | YES |
| 109 | city | character varying | 50 | YES |
| 110 | state | character varying | 50 | YES |
| 111 | zip | character varying | 50 | YES |
| 112 | gate_keeper | character varying | 325 | YES |
| 113 | email | character varying | 325 | YES |
| 114 | aux_data1 | character varying | 325 | YES |
| 115 | aux_data2 | character varying | 325 | YES |
| 116 | aux_data3 | character varying | 325 | YES |
| 117 | aux_data4 | character varying | 325 | YES |
| 118 | aux_data5 | character varying | 325 | YES |
| 119 | aux_external_url | character varying | 325 | YES |
| 120 | aux_greeting | character varying | 65535 | YES |
| 121 | loaded_dts | timestamp without time zone | | YES |
| 122 | list_desc | character varying | 400 | YES |
| 123 | reserved_agent_firstname | character varying | 100 | YES |
| 124 | reserved_agent_lastname | character varying | 100 | YES |
| 125 | reserved_agent_username | character varying | 200 | YES |
| 126 | address1 | character varying | 325 | YES |
| 127 | address2 | character varying | 325 | YES |
| 128 | first_name | character varying | 200 | YES |
| 129 | last_name | character varying | 200 | YES |
| 130 | is_contact | boolean | | YES |
| 131 | is_success | boolean | | YES |
| 132 | is_xfer | boolean | | YES |
| 133 | xfer_dest | character varying | 50 | YES |
| 134 | dial_mode | character varying | 30 | YES |
| 135 | country_id | character | 10 | YES |
| 136 | country_name | character varying | 75 | YES |
| 137 | country_code | character | 10 | YES |
| 138 | list_state | character varying | 265 | YES |
| 139 | int_cost | numeric | 14 | YES |
| 140 | international_prefix | character varying | 30 | YES |
| 141 | international_destination | character varying | 256 | YES |
| 142 | speed_to_lead_first_pass | integer | 32 | YES |
| 143 | speed_to_lead_agent_conn | integer | 32 | YES |
| 144 | external_agent_id | character varying | 284 | YES |
| 145 | agent_login_id | bigint | 64 | YES |
| 146 | session_id | smallint | 16 | YES |
| 147 | dial_duration | integer | 32 | YES |
| 148 | is_abandoned | boolean | | YES |
| 149 | is_accepted | boolean | | YES |
| 150 | is_deflected | boolean | | YES |
| 151 | is_manual_no_connect | boolean | | YES |
| 152 | exclude_abandon | smallint | 16 | YES |
| 153 | agent_group_id | integer | 32 | YES |
| 154 | agent_group_name | character varying | 255 | YES |
| 155 | script_group_id | integer | 32 | YES |
| 156 | script_group_name | character varying | 255 | YES |
| 157 | track_group_id | integer | 32 | YES |
| 158 | track_group_name | character varying | 255 | YES |
| 159 | visual_ivr_group_id | integer | 32 | YES |
| 160 | visual_ivr_group_name | character varying | 255 | YES |
| 161 | cloud_group_id | integer | 32 | YES |
| 162 | cloud_group_name | character varying | 255 | YES |
| 163 | lead_extra_data | character varying | 65535 | YES |
| 164 | pass_disposition | character varying | 30 | YES |
| 165 | outbound_disposition_tracker | character varying | 30 | YES |

### CALL SESSIONS
| Position | Column | Data Type | Max Length | Nullable |
|-|-|-|-|-|
| 1 | uii_table_key | numeric | 28 | NO |
| 2 | account_id | integer | 32 | NO |
| 3 | uii | character | 30 | NO |
| 4 | the_date | timestamp without time zone | | YES |
| 5 | session_id | smallint | 16 | NO |
| 6 | session_type | character varying | 20 | YES |
| 7 | recording_url | character varying | 255 | YES |
| 8 | is_monitoring | integer | 32 | YES |
| 9 | on_hold | integer | 32 | YES |
| 10 | call_dts | timestamp without time zone | | YES |
| 11 | duration | integer | 32 | YES |
| 12 | term_party | character varying | 140 | YES |
| 13 | term_reason | character varying | 130 | YES |
| 14 | agent_login_id | bigint | 64 | YES |
| 15 | cloud_destination_id | integer | 32 | YES |
| 16 | is_dequeue_agent | smallint | 16 | YES |
| 17 | transfer_flag | integer | 32 | YES |
| 18 | skill_profile_id | integer | 32 | YES |
| 19 | dial_dts | timestamp without time zone | | YES |
| 20 | dial_duration | integer | 32 | YES |
| 21 | dial_disposition | character varying | 50 | YES |
| 22 | carrier | character varying | 50 | YES |
| 23 | wrap_time | integer | 32 | YES |
| 24 | gate_id | integer | 32 | YES |
| 25 | gate_name | character varying | 150 | YES |
| 26 | agent_id | integer | 32 | YES |
| 27 | first_name | character varying | 150 | YES |
| 28 | last_name | character varying | 150 | YES |
| 29 | username | character varying | 270 | YES |
| 30 | team | character varying | 150 | YES |
| 31 | dial_result | character varying | 20 | YES |
| 32 | source_type | character | 10 | YES |
| 33 | source_id | bigint | 64 | YES |
| 34 | source_name | character varying | 255 | YES |
| 35 | etl_job_timestamp | timestamp without time zone | | YES |
| 36 | etl_job_guid | character | 38 | YES |
| 37 | agent_notes | character varying | 65535 | YES |
| 38 | agent_disposition | character varying | 150 | YES |
| 39 | phone | character varying | 90 | YES |
| 40 | cloud_destination_name | character varying | 312 | YES |
| 41 | cloud_destination_desc | character varying | 312 | YES |
| 42 | wait_time | integer | 32 | YES |

### AGENT LOGINS
| Position | Column | Data Type | Max Length | Nullable |
|-|-|-|-|-|
| 1 | account_id | integer | 32 | NO |
| 2 | agent_login_id | bigint | 64 | NO |
| 3 | agent_id | integer | 32 | YES |
| 4 | parent_agent_id | integer | 32 | YES |
| 5 | skill_profile_id | integer | 32 | YES |
| 6 | login_dial_group_id | integer | 32 | YES |
| 7 | monitor_agent_id | integer | 32 | YES |
| 8 | agent_team | character varying | 65 | YES |
| 9 | first_name | character varying | 65 | YES |
| 10 | last_name | character varying | 65 | YES |
| 11 | username | character varying | 65 | YES |
| 12 | email | character varying | 150 | YES |
| 13 | team | character varying | 65 | YES |
| 14 | agent_name | character varying | 65 | YES |
| 15 | external_agent_id | character varying | 65 | YES |
| 16 | agent_phone | character varying | 255 | YES |
| 17 | agent_state | character varying | 32 | YES |
| 18 | agent_aux_state | character varying | 50 | YES |
| 19 | agent_login_type | character varying | 16 | YES |
| 20 | state_dts | timestamp without time zone | | YES |
| 21 | login_dts | timestamp without time zone | | NO |
| 22 | logout_dts | timestamp without time zone | | YES |
| 23 | login_time | bigint | 64 | YES |
| 24 | calls_handled | integer | 32 | YES |
| 25 | preview_dials | integer | 32 | YES |
| 26 | manual_dials | integer | 32 | YES |
| 27 | rna_count | integer | 32 | YES |
| 28 | reserved_uii | character varying | 30 | YES |
| 29 | reserved_dts | timestamp without time zone | | YES |
| 30 | last_call_dts | timestamp without time zone | | YES |
| 31 | next_call_time | timestamp without time zone | | YES |
| 32 | pending_disposition | smallint | 16 | YES |
| 33 | pending_disp_time | integer | 32 | YES |
| 34 | ip_map_key | character varying | 32 | YES |
| 35 | current_chat_count | integer | 32 | YES |
| 36 | last_archive_state_dts | timestamp without time zone | | YES |
| 37 | agent_rank | integer | 32 | YES |
| 38 | available_time | integer | 32 | YES |
| 39 | ring_time | integer | 32 | YES |
| 40 | engaged_time | integer | 32 | YES |
| 41 | hold_time | integer | 32 | YES |
| 42 | break_time | integer | 32 | YES |
| 43 | away_time | integer | 32 | YES |
| 44 | lunch_time | integer | 32 | YES |
| 45 | train_time | integer | 32 | YES |
| 46 | rna_time | integer | 32 | YES |
| 47 | work_time | integer | 32 | YES |
| 48 | dial_group_id | integer | 32 | YES |
| 49 | dial_group_name | character varying | 100 | YES |
| 50 | off_hook_time | numeric | 20 | YES |
| 51 | etl_job_timestamp | timestamp without time zone | | YES |
| 52 | etl_job_guid | character varying | 36 | YES |
| 53 | rounded_off_hook_time | numeric | 20 | YES |
| 54 | account_name | character varying | 65 | YES |
| 55 | location | character varying | 48 | YES |
| 56 | main_account_name | character varying | 65 | YES |
| 57 | main_account_id | character varying | 8 | YES |
| 58 | agent_group_id | integer | 32 | YES |
| 59 | agent_group_name | character varying | 256 | YES |
| 60 | chat_engaged_time | integer | 32 | YES |
| 61 | chat_rna_time | integer | 32 | YES |
| 62 | chat_available_time | integer | 32 | YES |
| 63 | chat_presented_time | integer | 32 | YES |

### AGENT STATES

| Position | Column | Data Type | Max Length | Nullable |
|-|-|-|-|-|
| 1 | account_id | integer | 32 | NO |
| 2 | agent_login_id | bigint | 64 | NO |
| 3 | state_dts | timestamp without time zone | | YES |
| 4 | base_state | character varying | 24 | YES |
| 5 | state_label | character varying | 50 | YES |
| 6 | duration | integer | 32 | YES |
| 7 | etl_job_timestamp | timestamp without time zone | | YES |
| 8 | etl_job_guid | character varying | 36 | YES |
| 9 | pending_disp | boolean | | YES |
| 10 | uii | character | 30 | YES |
| 11 | uii_table_key | numeric | 28 | YES |
| 12 | chat_base_state | character varying | 50 | YES |
| 13 | chat_duration | integer | 32 | YES |
