# Admininstration APIs

The following set of APIs are for admins that need to manage their sub accounts, along with the queues and agents within those sub accounts.

## User List

The user list returns a list of admins on the account. For a list of agents, please use the [Agents](https://developers.ringcentral.com/engage/voice/api-reference/Integration-Agent-Controller/getAgentList) API. The [public user list](https://developers.ringcentral.com/engage/voice/api-reference/Users/listAllUsers) most developers will use has many details including creation date, enabled status, and roles. However, for integrations, a smaller set of user data may be all that is needed, but with the added ability to distinguish the RingCX user name from the RingEX user name and the environment ID. For this purpose, there's an [integration user list](https://developers.ringcentral.com/engage/voice/api-reference/Integration-User-Controller/getUserList) that can be used instead.

## Sub-Accounts

Each main account has a sub-account where most customers reside. However, for partners, more sub-accounts may exist and retrieving [sub-accounts](https://developers.ringcentral.com/engage/voice/api-reference/Integration-Account-Controller/getSubAccountsByMainAccountId) may be useful for determining which account is being used by the customer.

## Agents

Most developers will want a list of agents and agent groups, but for workforce management, there are additional details that are important to know about agents.  [Agents](https://developers.ringcentral.com/engage/voice/api-reference/Integration-Agent-Controller/getAgentList) are derived from RingEX users and the RingCentral User ID will map to an agent ID in RingCX and include the agent's true email address. Along with this detail, you can also retrieve the agent's supervisors as an array of agent IDs, or if the agent is a supervisor, a list of agents that the agent supervises (`whereSupervisee`).

## Queue Groups with Agents

Once known as gates, queues are inbound routing rules for customers calling in to a number. Typically, queues have agents assigned to them and each queue would have to be iterated through to find all the agents assigned to a queue group. However, the [gate group with agents](https://developers.ringcentral.com/engage/voice/api-reference/Integration-Gate-Group-Controller/getGateGroupsWithAgents) integration API allows you to get a complete list of all queues in a queue group and the agents contained in that queue in a single call.

!!! info "This is not active agents in a queue"
    This API only returns a list of agents assigned to the queue. It does not return a list of agents actively receivng calls and chats from a queue.
