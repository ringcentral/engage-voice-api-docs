# Reports

The Reports APIs provide workforce management (WFM) tools to retrieve detailed agent interaction records and aggregated performance statistics across queues and agents. These endpoints are designed to feed external systems with raw data necessary for scheduling, compliance, and performance analysis.

## Strategic Overview

These tools allow developers to synchronize RingCX interaction data with third-party WFM platforms. By providing both granular segment metadata and high-level interval statistics, the API supports reporting requirements and forensic interaction tracking.

### Key Use Cases

* **WFM Synchronization:** Exporting agent activity and queue metrics to workforce management software for staffing optimization.
* **Compliance Archiving:** Maintaining a metadata trail of all interactions, including links to recordings and transcripts.
* **Performance Analysis:** Reviewing aggregated queue and agent data to identify trends in talk time and wrap-up durations.

### Real-Time vs. Latency Expectations

Data availability is subject to a propagation delay while interactions are finalized and indexed.

* **Data Availability:** Data must be fetched **at least 5 minutes** before the current time to avoid API errors.
* **Processing Buffer:** For interaction metadata and recordings, it is recommended to allow a 15-minute window for all media processing to complete.

!!! important "Rate Limiting & Stability"
    * **Limit:** Requests are limited to **2 calls per minute**.
    * **Strategy:** If the API returns a `429 Too Many Requests` status code, implement an **exponential backoff** strategy for subsequent retry attempts. This strategy involves doubling the delay after each consecutive 429 error (e.g., 1s, 2s, 4s...) rather than retrying at fixed intervals.

### Required Permissions & Scopes

For detailed instructions on obtaining your access token, please refer to the [RingCentral Authentication Guide](https://developers.ringcentral.com/engage/voice/guide/authentication/auth-ringcentral).

To successfully call the API, your RingCX account must be configured with **WEM Access**. If you lack the necessary permissions or receive an error when calling the API, please contact your Customer Success Manager (CSM)

---

## Interaction Metadata & Media

### Agent Segment Metadata

**Purpose:** Granular Interaction Auditing and Quality Management.

The **Interaction Metadata** API is used to reconstruct the complete "story" of a customer journey. While a standard report might show a single call, this API breaks that call down into specific **Segments**, representing every participant (Agent, IVR, or Bot) involved.

A user would use this to perform forensic tracking or quality assurance. For example, if a customer was transferred three times, this API provides the metadata for all three segments, including specific timestamps for when each agent joined or left, and the direct URL to the audio recording for that specific portion of the call.

* **Reference:** [Interaction Metadata API Details](https://developers.ringcentral.com/engage/voice/api-reference/Public-Integration-API/getInteractionMetadata)

### Retrieving Agent Segment Recordings & Transcripts

Once metadata is retrieved, users can access the specific media files.

* **Recordings:** Used for compliance archiving and quality evaluations. To account for processing time, allow at least 10 minutes after an interaction completes before retrieval.
* **Transcripts:** Used for text-based sentiment analysis and quick review of conversations without listening to audio. Like recordings, these should be accessed after the 10-15 minute processing window.

For more details on how to retrieve these files refer to the [Call Transcripts API](../analytics/reports/call-transcripts.md)

---

## Aggregated Statistics

### Queue Statistics (`agg-queue-stats`)

**Purpose:** Service Level Monitoring and Operational Health.

The **Queue Statistics** API provides a high-level view of how specific contact center queues are performing over defined time intervals (15, 30, 45, or 60 minutes). It aggregates data across the entire queue rather than focusing on individual agents.

Operations managers use this data to ensure the center is meeting its Service Level Agreements (SLAs). It is the primary tool for identifying volume trends, such as spikes in abandoned calls or excessive wait times, allowing for real-time or historical staffing adjustments.

* **Reference:** [Queue Statistics API Details](https://developers.ringcentral.com/engage/voice/api-reference/Public-Integration-API/buildAggQueueStats)

### Agent Statistics (`agg-agent-stats`)

**Purpose:** Workforce Productivity and Attendance Tracking.

The **Agent Statistics** API is designed to measure the general output and availability of the workforce. It focuses on how agents are spending their time across broad categories like "talking," "wrap-up," or "idle".

A user would use this API to generate daily or weekly productivity reports. It is commonly used for payroll verification and ensuring that agents are adhering to their scheduled shifts by comparing their active time against their expected hours.

* **Reference:** [Agent Statistics API Details](https://developers.ringcentral.com/engage/voice/api-reference/Public-Integration-API/buildAggAgentStats)

### Agent Extended Statistics (`agg-agent-extended-stats`)

**Purpose:** Deep-Dive Performance and Behavioral Analysis.

The **Agent Extended Statistics** API provides a more granular breakdown of performance metrics for agents across their assigned queues. It builds upon basic stats by adding specific handling details, such as transfer counts and precise handling times per queue.

This is the preferred tool for workforce planners and supervisors performing root-cause analysis. If a supervisor notices a drop in efficiency, they can use this API to determine if the issue is tied to a specific queue or if an agent is transferring a disproportionate number of interactions, indicating a potential need for further training.

* **Reference:** [Agent Extended Statistics API Details](https://developers.ringcentral.com/engage/voice/api-reference/Public-Integration-API/buildExtendedAggAgentStats)

---
