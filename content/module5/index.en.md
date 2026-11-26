---
title: "Module 5: Agentic Remediation for Posture Violations with Federated Human-in-loop at Scale"
weight: 06
---

> ⚠️ **Region Reminder:** Security Hub findings are in **us-west-2 (Oregon)**.

**Estimated Time:** 45 minutes

## Overview

In this module, you'll transform from reactive security management to proactive, automated defense using agentic workflows. This module focuses on automated compliance remediation for AWS Security Hub findings. You'll learn to identify critical security misconfigurations through Security Hub and implement intelligent automated fixes that maintain continuous compliance across your AWS environment.

---

## ⚡ The Agentic SecOps Transformation

Before Agentic SecOps, posture management meant manually reviewing hundreds of non-compliant findings in AWS Security Hub and coordinating manual fixes across multiple team owners. With **autobotAI Agentic SecOps**, non-compliant findings automatically trigger intelligent remediation, interactive human-in-the-loop approval cards, and automated manager escalations when SLAs expire.

<table style="width:100%; border-collapse: collapse; margin: 20px 0;">
  <thead>
    <tr style="background-color: #f8f9fa;">
      <th style="width:50%; padding: 12px; text-align: center; border: 2px solid #dc3545; color: #dc3545;">
        <h3>❌ Before Agentic SecOps</h3>
      </th>
      <th style="width:50%; padding: 12px; text-align: center; border: 2px solid #28a745; color: #28a745;">
        <h3>✅ After Agentic SecOps</h3>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 15px; vertical-align: top; border: 1px solid #e9ecef; background-color: #fff5f5;">
        <p><strong>Cluttered & Unresolved Security Hub Findings</strong></p>
        <p>A backlogged list of non-compliant security posture findings sitting unresolved in your console.</p>
        <img src="../static/mod5-before-secops.png" alt="Before Agentic SecOps - Cluttered Security Hub Findings" style="width:100%; border-radius: 6px; margin-top: 10px;" />
      </td>
      <td style="padding: 15px; vertical-align: top; border: 1px solid #e9ecef; background-color: #f5fff5;">
        <p><strong>1) Remediated & Resolved Compliance Status</strong></p>
        <img src="../static/mod5-after-secops.png" alt="After Agentic SecOps - Remediated Security Hub Finding" style="width:100%; border-radius: 6px; margin-bottom: 15px;" />
        <p><strong>2) DeepAgent Autonomous Execution Thread</strong></p>
        <img src="../static/mod5-resolver-deepagent-thread.png" alt="After Agentic SecOps - DeepAgent Execution Thread" style="width:100%; border-radius: 6px;" />
      </td>
    </tr>
  </tbody>
</table>

---

## What You'll Learn

By the end of this module, you will be able to:

- Navigate Security Hub findings to identify critical misconfigurations
- Understand the business impact and risk level of common security findings
- Execute autobotAI remediation workflows that automatically fix security issues at scale
- Configure intelligent remediation powered by Amazon Bedrock foundation models
- Validate remediation effectiveness by confirming compliance score improvements
- Monitor compliance trends to identify systemic security issues
- Generate compliance reports for audit and regulatory requirements
- Implement preventive controls to avoid future misconfigurations

---

## Why Agentic Remediation Matters
- **Speed**: Reduce remediation time from hours to seconds
- **Consistency**: Eliminate human error through standardized workflows
- **Scale**: Apply fixes across hundreds of resources simultaneously
- **Intelligence**: Context-aware remediation that understands your environment

---

## CSPM vs. Security Hub v2 Findings

AWS Security Hub findings are split into two categories:

| Dimension | CSPM (Cloud Security Posture Management) | Security Hub v2 (Active Threats) |
|---|---|---|
| **Definition** | Static configuration checks against compliance standards (FSBP, CIS). | Dynamic runtime alerts, behavioral anomalies, and active threat reports. |
| **Examples** | Unencrypted S3 buckets, exposed database ports, default VPC security groups. | Suspicious API calls (GuardDuty), active compromise, malware detections. |
| **Mitigation** | Can be automatically resolved using pre-configured static workflows. | Requires dynamic context-aware analysis and human approval gating. |

---

## Two Approaches to Remediation

This module covers two different methods of executing agentic security operations:

-   **Approach 1: Seeding & Executing via Optimus (Dynamic):** Start from Optimus chat, authorize tools dynamically for governance, compile a daily scheduled Bot, and set up an interactive Approval Loop inside the chat thread (via a distributed risk owner focused chat interface) with fast-tracked escalation if ignored.
-   **Approach 2: Remediation via Library Bot Import (Static):** Import a pre-configured template from the Library, connect AWS SES and Bedrock nodes on the visual canvas, and execute the automated compliance flow.

---

## Module Structure

This module is divided into the following sections:

### 5.1 Understanding Security Hub Findings & Escalation Architecture
Learn about AWS Security Hub compliance checks, review the twelve findings covered, and understand the conceptual architecture of the Optimus-driven bot and manager escalation timeout loop.

### 5.2 Seeding & Executing the Bot via Optimus
Step-by-step setup using Optimus chat, setting tool governance, checking the Bot Node card, managing interactive approval cards in the chat thread, and manager escalation. *(Screenshots included)*

### 5.3 (Bonus) Remediation via Library Bot Import
Importing the static remediation bot from the Library, configuring AWS SES/Bedrock nodes on the canvas, and running the flow. *(Screenshots included)*

---

## Architecture Overview

The Security Hub remediation architecture includes:

1. **Detection Layer**:
   - Security Hub continuously monitors AWS resources against security standards
   - Aggregates findings from GuardDuty, Inspector, Config, and other services
   - Generates findings for non-compliant resources

2. **AI Analysis Layer (Powered by Amazon Bedrock)**:
   - autobotAI agent leverages Bedrock's foundation models to analyze Security Hub findings
   - AI-driven assessment of finding criticality and business impact
   - Intelligent decision-making on appropriate remediation actions using Bedrock's reasoning capabilities
   - Contextual risk evaluation before applying fixes

3. **Remediation Layer**:
   - Automated execution of compliance fixes
   - Security group modifications and access control updates
   - Encryption enablement for data services
   - Configuration changes for EC2, IAM, and other services

4. **Approval & Governance Layer**:
   - Human-in-the-loop approvals for high-risk changes
   - Approvals are routed through either interactive Approval Cards in the DeepAgent chat thread (Optimus approach) or Amazon SES notifications (Library bot approach).
   - Tool Governance ensures operators approve and enable generated mutation tools before they run.

5. **Notification & Escalation Layer**:
   - Amazon SES sends detailed alerts to security teams
   - DeepAgent bot automatically escalates ignored approvals to managers by resolving organization contacts from SES identities.

6. **Audit & Validation Layer**:
   - CloudWatch Logs maintain comprehensive audit trails
   - CloudTrail logs all API activities
   - Complete validation of compliance scoring improvements in the AWS Security Hub console

---

**Ready to begin?** Start with [Module 5.1: Understanding Security Hub Findings & Escalation Architecture](./5.1/)
