---
title: "Module 4: SOC Automation - Agentic Workflow for GuardDuty"
weight: 05
---

> ⚠️ **Region Reminder:** GuardDuty findings are generated in **us-west-2 (Oregon)**.

**Estimated Time:** 45 minutes

## Overview

This comprehensive module addresses security threats across both database (RDS) and compute (EC2) layers, along with IAM-related security incidents. You'll learn to detect threats using Amazon GuardDuty and implement automated remediation using autobotAI's agentic capabilities powered by **Amazon Bedrock** to achieve end-to-end autonomous protection.

---

## The Agentic SecOps Transformation

Traditional threat management requires security engineers to manually triage endless streams of GuardDuty findings across RDS, EC2, and IAM. With **autobotAI Agentic SecOps**, AI agents autonomously analyze threat findings, validate attacker IPs against threat intelligence, execute precise remediation actions, and notify your security team.

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
        <p><strong>Cluttered & Unresolved GuardDuty Findings</strong></p>
        <p>Endless security alerts across RDS, EC2, and IAM remain active without automated response.</p>
        <img src="../static/01.guardduty_findings.png" alt="Before Agentic SecOps - Cluttered GuardDuty Findings" style="width:100%; border-radius: 6px; margin-top: 10px;" />
      </td>
      <td style="padding: 15px; vertical-align: top; border: 1px solid #e9ecef; background-color: #f5fff5;">
        <p><strong>1) Remediated & Resolved Threat Status</strong></p>
        <img src="../static/module4/gd-rem-2.png" alt="After Agentic SecOps - Remediated GuardDuty Finding" style="width:100%; border-radius: 6px; margin-bottom: 15px;" />
        <p><strong>2) Workflow Execution & AI Agent UI</strong></p>
        <img src="../static/mod4-agent-view.png" alt="After Agentic SecOps - Workflow Execution UI" style="width:100%; border-radius: 6px;" />
      </td>
    </tr>
  </tbody>
</table>

---

## What You'll Learn

By the end of this module, you will be able to:

- Detect and respond to RDS-related security threats using GuardDuty
- Identify and mitigate EC2 security incidents including SSH brute force, Tor client activity, and credential exfiltration
- Understand GuardDuty RDS Protection and how it monitors database login activity
- Identify IAM-related security threats and anomalous behavior
- Implement AI-driven automated remediation for security findings
- Configure intelligent threat analysis and decision-making workflows
- Set up automated notification systems via Amazon SES for security incidents

## Module Structure

This module is divided into the following sections:

### 4.1 Detecting Security Threats Using GuardDuty

Learn how GuardDuty detects security threats across RDS, EC2, and IAM:

**RDS Protection Features:**
- Continuous monitoring of RDS login activity for Amazon Aurora and RDS databases
- Detection of suspicious login behavior and brute-force attacks
- Identification of access from Tor networks and known malicious IP addresses
- Analysis of both successful and failed login attempts

**EC2 Threat Detection:**
- SSH brute force attack identification
- Tor client activity detection
- Instance credential exfiltration monitoring
- Network anomaly detection

**IAM Threat Detection:**
- Monitoring of IAM entity activities and API calls
- Detection of reconnaissance activities from malicious sources
- Identification of credential misuse and unauthorized access attempts

**Finding Types Covered:**

*RDS & IAM Findings:*
- `CredentialAccess:RDS/TorIPCaller.FailedLogin`
- `Discovery:RDS/TorIPCaller`
- `Discovery:RDS/MaliciousIPCaller`
- `Recon:IAMUser/MaliciousIPCaller.Custom`
- `Recon:IAMUser/TorIPCaller`

*EC2 Findings:*
- `UnauthorizedAccess:EC2/SSHBruteForce`
- `Backdoor:EC2/C&CActivity.B!DNS` (Tor Client Detection)
- `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.OutsideAWS`

### 4.2 Implement Automated Remediation with autobotAI

Build AI-driven automated response mechanisms using autobotAI's agentic capabilities:

**Bot Overview:**
This bot leverages autobotAI's agentic capabilities powered by **Amazon Bedrock** to automate the analysis, decision-making, and remediation of Amazon GuardDuty findings across RDS and EC2 security incidents. By combining AI-driven intelligence from Bedrock's foundation models with AWS-native tools, it identifies real threats, validates attacker IPs, executes mitigation actions, and performs automated incident response — enabling end-to-end autonomous protection for both database and compute layers.

**Automated Remediation Components:**
- AI-powered threat assessment and validation using AbuseIPDB
- Automated IP blocking and network isolation
- Intelligent security group modification
- IAM credential rotation and scope reduction
- Forensic evidence collection
- Real-time notification via Amazon SES
- Comprehensive audit trail of all remediation actions

**Key Capabilities:**
- Real-time threat response without manual intervention
- Intelligent decision-making based on threat context
- Graduated response based on finding severity and validation
- Integration with external threat intelligence (AbuseIPDB)
- Comprehensive audit trail of all remediation actions
- Integration with notification systems for security team alerts

## Architecture Overview

The threat detection and automated remediation architecture includes:

1. **Detection Layer**:
   - GuardDuty continuously monitors RDS login activity, EC2 network traffic, and IAM operations
   - Analyzes patterns for anomalous behavior across all layers
   - Generates findings for potential security threats

2. **AI Analysis Layer (Powered by Amazon Bedrock)**:
   - autobotAI agent leverages Bedrock's foundation models to analyze GuardDuty findings
   - AI-driven threat validation using external intelligence (AbuseIPDB)
   - Intelligent decision-making on appropriate response actions using Bedrock's reasoning capabilities
   - Contextual severity assessment and mitigation planning

3. **Remediation Layer**:
   - Automated execution of response actions
   - Security group modifications and IP blocking
   - IAM credential rotation and scope reduction
   - Instance isolation when necessary

4. **Notification Layer**:
   - Amazon SES sends detailed email alerts to security teams
   - Includes AI analysis results and actions taken
   - Provides complete incident summary

5. **Audit Layer**:
   - CloudWatch Logs maintain comprehensive audit trails
   - CloudTrail logs all API activities
   - Complete visibility into all remediation actions

---

## ✅ Module Success Criteria

By the end of this module, you should have:
- [ ] Reviewed GuardDuty findings in the console
- [ ] Understood different finding types (RDS, EC2, IAM)
- [ ] Imported and configured the GuardDuty remediation bot
- [ ] Executed automated remediation workflow
- [ ] Received notification with remediation summary
- [ ] Verified security group modifications applied
