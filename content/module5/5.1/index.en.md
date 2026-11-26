---
title: "5.1 Understanding Risk Register, Security Hub Findings, Workflow & Escalation Process"
weight: 1
---

> ⚠️ **Region Reminder:** Security Hub findings are in **us-west-2 (Oregon)**.

**Estimated Time:** 15 minutes

---

## Introduction

As a security professional, you need comprehensive visibility into security misconfigurations and compliance violations across your AWS infrastructure. This section explores how AWS Security Hub assists in identifying critical security findings across EC2, IAM, S3, and other AWS services through automated compliance checks against industry standards.

Security Hub provides continuous monitoring and compliance assessment across multiple AWS services, helping you identify security misconfigurations before they can be exploited by attackers.

---

## The CNAPP Challenge: The Ignored Alert

In enterprise cloud security, finding a vulnerability is only half the battle. The true bottleneck is **remediation**.

Consider the standard operational loop:
1. **The Alert:** AWS Security Hub detects a critical risk (e.g., database port open to `0.0.0.0/0` or a public S3 bucket).
2. **The Notification:** An automated email is dispatched to a SecOps engineer.
3. **The Silent Failure:** Due to alert fatigue, shifting priorities, or off-work hours, the engineer ignores the email.
4. **The Window of Exposure:** The vulnerability remains active on the live internet, creating an immediate breach window.

To close this window, enterprise security operations require an intelligent response workflow that guarantees remediation while preserving strict operational safety.

---

## Enterprise Escalation Expansion: Exception Handling & Deferral Loops

In real-world enterprise environments, security teams cannot always apply fixes blindly. For instance, if an engineer is running a critical database load test, shutting down access ports immediately will break business operations.

To address this, the agentic workflow can be upgraded to handle **exceptions** and **deferred remediations** using the following logical state machine:

### 1. The Business Exception Gate (Reject with Reason)
-   **The Scenario:** An engineer rejects an automated security fix because of an active testing exception.
-   **The Agentic Response:** Rather than failing silently, the bot prompts the engineer to provide a mandatory business justification.
-   **Compliance Logging:** The bot compiles this exception reason and writes it to a central **Risk Register Artifact**. This maintains a tamper-proof audit trail for external compliance officers.

### 2. The Deferral Tracker (Remediate Later Loop)
-   **The Scenario:** The engineer clicks "Defer Fix" and states: *"I will apply this patch tomorrow at 10:00 AM."*
-   **The Agentic Response:** The bot parses the date/time response and records the deferred deadline inside a persistent state artifact.
-   **Continuous Verification:** On every scheduled run, the bot reviews the active deferral artifacts. If the deadline passes and the vulnerability is still active:
    1.  **Stage 1 Reminder:** The bot sends an alert warning the engineer that the exception has expired.
    2.  **Stage 2 Manager Escalation:** If the engineer ignores this reminder or attempts to defer it again without clearance, the bot flags the policy breach and escalates the issue directly to their manager.

### 3. Distributed Risk Ownership (Preventing Inbox Bottlenecks)
-   **The Problem:** Traditional security alerts flood a single generic security inbox, leading to severe alert fatigue and missed actions.
-   **The Distributed Solution:** autobotAI parses metadata from Security Hub and AWS tags to identify the specific resource owner (the developer who created the resource).
-   **Targeted Routing:** Approval cards and reports are sent directly to that specific developer, and escalations are routed directly to *their* manager. This distributes the remediation workload across the organization, ensuring those with the most context handle the fixes.

---

## The Agentic Solution: Optimus & DeepAgent Collaboration

This module showcases the collaboration between autobotAI's two core agentic layers to safely automate this risk profile:

```text
[Phase 1: Setup & Governance]
Optimus Chat (AI Orchestrator)
   ├── triages active findings
   ├── builds custom remediation tools (Actions)
   ├── User Governance Gate: User approves and enables actions
   └── deploys Bot & Escalation Skill (Clickable Bot Node Card redirect)

[Phase 2: Automated Run & Safety net]
DeepAgent Bot (Daily Scheduled, 10:00 AM)
   ├── resolves Safe findings automatically
   ├── emails redirect links pointing to the DeepAgent Chat Thread
   ├── presents interactive Approval Cards directly in the chat stream
   └── Safety Net: Escalates to manager via SES if timeouts (2m/5m) expire
```

### 1. Tool Governance (Phase 1)
To prevent rogue automation, **Optimus** first designs the remediation actions and pauses execution, forcing the operator to review, save, and enable the tools in the **Optimus Tools** panel. This ensures complete governance over the bot's capabilities.

### 2. Interactive Chat Thread Approvals (Phase 2)
For disruptive findings, the bot emails a secure redirect link pointing back to the **DeepAgent Chat Thread**. Instead of navigating complex external portals, the risk owner interacts with **Approval Cards directly in the chat bubble stream**, clicking **Approve** or **Reject** on individual findings.

### 3. Accelerated Manager Escalation Safety Net
If the engineer ignores the approval thread, the bot handles wait-state timeouts. Because this is a 2-hour lab, the timeout is accelerated (2 minutes for a reminder, 5 minutes for escalation). The bot queries SES organizational identities to locate their manager's email and escalates the pending approval cards to secure the environment before a breach can occur.

---

## Security Hub Compliance Monitoring

### Automated Security Checks

AWS Security Hub performs automated, continuous security best practice checks against your AWS resources. It aggregates findings from multiple AWS services and checks your resources against industry standards including:

- **AWS Foundational Security Best Practices (FSBP):** AWS-recommended security controls
- **CIS AWS Foundations Benchmark:** Industry-standard security configuration guidelines
- **PCI DSS:** Payment Card Industry Data Security Standard requirements
- **NIST frameworks:** National Institute of Standards and Technology guidelines

Security Hub continuously evaluates your resources and generates findings when misconfigurations are detected, providing a centralized view of your security posture across accounts and regions.

### Security Hub Finding Types

In this workshop, we will be reviewing and remediating the following types of Security Hub findings:

**Infrastructure Security Findings:**
- EC2 security group misconfigurations
- VPC default security group violations
- Instance metadata service vulnerabilities
- Public IP auto-assignment issues

**Identity & Access Management Findings:**
- Weak IAM password policies
- Suspicious IAM user activity (from GuardDuty)

**Data Protection Findings:**
- S3 bucket public access violations
- Unencrypted SNS topics and SQS queues
- DynamoDB tables without deletion protection

---

## Security Hub Finding Types Covered

This module focuses on twelve critical security findings that autobotAI can automatically remediate:

### 1. Infrastructure Security - EC2 & VPC

#### EC2 Security Groups - Remote Server Administration Ports

**Finding:** `EC2 security groups should not allow ingress from 0.0.0.0/0 to remote server administration ports`

**Description:** Security groups allow unrestricted inbound access (0.0.0.0/0) to remote administration ports like SSH (22), RDP (3389), and other management ports.

**Risk Level:** High

**Why This Matters:**
- Exposes administrative interfaces to the entire internet
- Primary target for automated scanning and brute force attacks
- Successful compromise grants full system access
- Common entry point for ransomware and data breaches

**Remediation:** Restrict security group rules to specific IP ranges or use AWS Systems Manager Session Manager for secure access

---

#### Security Groups - High Risk Ports

**Finding:** `Security groups should not allow unrestricted access to ports with high risk`

**Description:** Security groups allow unrestricted access (0.0.0.0/0 or ::/0) to ports commonly exploited by attackers.

**Risk Level:** High

**Why This Matters:**
- High-risk ports include database ports (3306, 5432, 1433), web admin panels (8080, 8443), and other services
- Unrestricted access increases attack surface significantly
- Automated scanners constantly probe these ports
- Can lead to data exfiltration, service disruption, or system compromise

**Remediation:** Restrict access to specific IP ranges or use VPN/bastion hosts for administrative access

---

#### Security Groups - Authorized Ports Only

**Finding:** `Security groups should only allow unrestricted incoming traffic for authorized ports`

**Description:** Security groups allow unrestricted inbound traffic on ports that haven't been explicitly authorized for public access.

**Risk Level:** Medium to High

**Why This Matters:**
- Only specific ports (like 80, 443 for web services) should be publicly accessible
- Other ports should be restricted to known IP ranges
- Reduces attack surface and limits exposure
- Helps maintain principle of least privilege

**Remediation:** Review and restrict security group rules to only allow public access on explicitly authorized ports

---

#### EC2.2 - VPC Default Security Groups

**Finding:** `[EC2.2] VPC default security groups should not allow inbound or outbound traffic`

**Description:** Default security groups in your VPCs allow unrestricted inbound and outbound traffic, violating the principle of least privilege.

**Risk Level:** Medium to High

**Why This Matters:**
- Default security groups are automatically attached to resources if no specific security group is specified
- Unrestricted rules create unintended access paths
- Attackers can exploit these overly permissive rules for lateral movement
- Compliance frameworks (CIS, PCI DSS) require restricting default security groups

**Remediation:** Remove all inbound and outbound rules from default security groups

---

#### EC2.8 - Instance Metadata Service v2

**Finding:** `[EC2.8] EC2 instances should use Instance Metadata Service Version 2 (IMDSv2)`

**Description:** EC2 instances are using IMDSv1, which is vulnerable to Server-Side Request Forgery (SSRF) attacks.

**Risk Level:** High

**Why This Matters:**
- IMDSv1 allows any process on the instance to access metadata without authentication
- SSRF vulnerabilities in applications can be exploited to steal IAM credentials
- IMDSv2 requires session tokens, preventing SSRF-based credential theft
- Critical for protecting temporary security credentials

**Remediation:** Enforce IMDSv2 by setting `HttpTokens=required` on all EC2 instances

---

#### EC2.15 - Public IP Auto-Assignment

**Finding:** `[EC2.15] EC2 subnets should not automatically assign public IP addresses`

**Description:** Subnets are configured to automatically assign public IP addresses to instances launched within them.

**Risk Level:** Medium

**Why This Matters:**
- Unintended internet exposure of resources meant to be private
- Increases attack surface by making instances directly accessible from the internet
- Violates network segmentation best practices
- Can lead to data exfiltration or unauthorized access

**Remediation:** Disable automatic public IP assignment on subnet configurations

---

### 2. Identity & Access Management

#### Suspicious IAM Activity (GuardDuty)

**Finding:** `Suspicious activity by an IAM user (product: GuardDuty)`

**Description:** GuardDuty has detected suspicious or anomalous behavior by an IAM user, such as API calls from unusual locations, reconnaissance activities, or credential misuse.

**Risk Level:** Medium to High

**Why This Matters:**
- Indicates potential account compromise or insider threat
- Unusual API patterns may signal reconnaissance before an attack
- Credential theft or misuse can lead to data breaches
- Early detection is critical for preventing escalation
- May indicate lateral movement within your environment

**Common Suspicious Activities:**
- API calls from Tor exit nodes or known malicious IPs
- Reconnaissance activities (listing resources, permissions)
- Unusual geographic locations or access patterns
- High-volume API calls inconsistent with normal behavior
- Access to resources outside normal scope

**Remediation:** Investigate the activity, rotate credentials if compromised, restrict IAM permissions, and enable MFA

---

#### IAM Password Policies

**Finding:** `[IAM.7] Password policies for IAM users should have strong AWS configurations`

**Description:** IAM password policy doesn't meet security best practices for complexity and rotation.

**Risk Level:** Medium

**Why This Matters:**
- Weak passwords are vulnerable to brute force attacks
- Lack of password rotation increases risk of credential compromise
- Compliance requirements mandate strong password policies
- Human users are often the weakest link in security

**Remediation:** Configure IAM password policy with:
- Minimum length of 14 characters
- Require uppercase, lowercase, numbers, and symbols
- Password expiration and prevention of reuse
- Account lockout after failed attempts

---

### 3. Data Protection

#### S3 Public Access

**Finding:** `[S3.1] S3 general purpose buckets should block public access`

**Description:** S3 buckets have public access enabled, potentially exposing sensitive data.

**Risk Level:** Critical

**Why This Matters:**
- Public S3 buckets are a leading cause of data breaches
- Accidental exposure of sensitive customer data, credentials, or intellectual property
- Compliance violations (GDPR, HIPAA, PCI DSS)
- Reputational damage and financial penalties

**Remediation:** Enable S3 Block Public Access at bucket level

---

#### SNS Encryption

**Finding:** `[SNS.2] SNS topics should be encrypted at rest using AWS KMS`

**Description:** SNS topics are not encrypted, exposing message content at rest.

**Risk Level:** Medium

**Why This Matters:**
- Unencrypted messages can be accessed if AWS infrastructure is compromised
- Compliance requirements mandate encryption of sensitive data
- Messages may contain PII, credentials, or business-critical information
- Defense in depth requires encryption at rest

**Remediation:** Enable KMS encryption on SNS topics

---

#### SQS Encryption

**Finding:** `[SQS.1] Amazon SQS queues should be encrypted at rest`

**Description:** SQS queues lack server-side encryption, leaving messages vulnerable.

**Risk Level:** Medium

**Why This Matters:**
- Queue messages may contain sensitive application data
- Unencrypted queues violate data protection best practices
- Compliance frameworks require encryption of data at rest
- Minimal performance impact with significant security benefit

**Remediation:** Enable SQS server-side encryption using AWS KMS

---

#### DynamoDB Protection

**Finding:** `[DynamoDB.6] DynamoDB tables should have deletion protection enabled`

**Description:** DynamoDB tables lack deletion protection, risking accidental data loss.

**Risk Level:** Medium

**Why This Matters:**
- Accidental table deletion can cause catastrophic data loss
- No recovery mechanism for deleted tables without backups
- Business continuity and disaster recovery requirements
- Compliance requirements for data retention

**Remediation:** Enable deletion protection on DynamoDB tables

---

## Checking Findings in Security Hub Console

### Step 1: Navigate to Security Hub Console

1. In your AWS account, browse to [**Security Hub CSPM**](https://console.aws.amazon.com/securityhub/home)
2. Security Hub is already enabled in your account and you will land on the Summary page

### Step 2: View Findings

1. On the left side, click on **Findings**
2. Here you'll find all security findings aggregated from various AWS services

![Security Hub Findings](../../static/securityhubfindings.png)

### Step 3: Filter by Severity

Use the severity filter to focus on critical and high-severity findings that require immediate attention:
- **Critical:** Immediate action required
- **High:** Prompt attention needed
- **Medium:** Should be addressed in near term
- **Low:** Address as part of regular maintenance

### Step 4: Review Finding Details

Click on any finding to see detailed information:
- **Resource Details:** Which AWS resource is affected
- **Compliance Status:** Which security standards are violated
- **Remediation Steps:** AWS-recommended fixes
- **Related Findings:** Other findings affecting the same resource

### Step 5: Understand Compliance Scores

Security Hub provides compliance scores for each enabled standard:
- **AWS Foundational Security Best Practices**
- **CIS AWS Foundations Benchmark**
- **PCI DSS**
- **NIST frameworks**

---

**Next:** Proceed to [Module 5.2: Hands-On: Seeding & Executing the Bot via Optimus](../5.2/)

---

## ✅ Success Criteria

You've completed this section when:
- [ ] Understood Security Hub compliance checks and severity levels
- [ ] Reviewed the enterprise escalation architecture and timeout lifecycle
- [ ] Navigated to the Security Hub console and inspected findings
