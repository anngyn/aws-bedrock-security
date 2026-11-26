---
title: "5.3 (Bonus) Remediating Posture Violations with Multi-Agent Multi-Model Workflow"
weight: 3
---

> ⚠️ **Region Reminder:** Select **us-west-2 (Oregon)** in AWS and review AWS Security Hub CSPM.

**Estimated Time:** 15 minutes

---

## Introduction

The previous section focused on how Optimus enables federated HIL (human-in-the-loop) remediation with highly autonomous operations. Sometimes these operations need a defined and controlled process. In this section, you'll implement automated remediation for AWS Security Hub CSPM findings using autobotAI's multi-agent multi-model agentic workflow capabilities. The bot will autonomously analyze findings, assess business impact, and execute appropriate remediation actions while maintaining comprehensive audit trails.

---

## Bot Overview

This bot leverages **autobotAI's Agentic AI framework** to autonomously analyze, evaluate, and remediate **AWS Security Hub findings**.  

By combining AWS native security data with AI reasoning via **Amazon Bedrock**, it performs intelligent triage, executes remediation tasks, and sends structured notifications — enabling a fully autonomous and explainable security response workflow.

### Key Capabilities

- **Intelligent Analysis:** Amazon Bedrock's Claude 3.5 Sonnet v2 analyzes finding context and business impact
- **Automated Remediation:** Direct fixes applied to non-compliant resources without human intervention
- **Risk Assessment:** AI-driven evaluation of remediation risks and operational impact
- **Approval Workflow:** Human-in-the-loop for high-risk changes
- **Audit Trail:** Complete documentation of all actions for compliance
- **Notification System:** Real-time alerts via Amazon SES

---

## Covered Findings

This module supports remediation for the following Security Hub controls:

- **EC2 security groups should not allow ingress from 0.0.0.0/0 to remote server administration ports**  
- **Security groups should not allow unrestricted access to ports with high risk**  
- **VPC default security groups should not allow inbound or outbound traffic**  
- **Security groups should only allow unrestricted incoming traffic for authorized ports**  
- **S3 general purpose buckets should block public access**  
- **SNS topics should be encrypted at rest using AWS KMS**  
- **Suspicious activity by an IAM user (product: GuardDuty)**  
- **EC2 instances should use Instance Metadata Service Version 2 (IMDSv2)**  
- **EC2 subnets should not automatically assign public IP addresses**  
- **DynamoDB tables should have deletion protection enabled**  
- **Password policies for IAM users should have strong configurations**  
- **Amazon SQS queues should be encrypted at rest**  

> 💡 *These are example finding types for demonstration. You can easily configure the bot to handle any Security Hub finding or resource type by simply dragging and dropping your desired tools or logic.*

---

## Importing and Running Workflow

> **Note:** The bot will run for approximately **10-15 minutes**. You can monitor the progress in the execution logs or via the chat interface during the session.

### Step 1: Import the Bot from Library

1. Visit the [autobotAI Library](https://autobot.live/app#/library).  
2. Search for **"AWS Security Hub Agentic Remediation"**.  
3. Click on the bot card and select **Import**.

---

### Step 2: Configure the Bot

> **Note:** Ensure AWS integrations and Bedrock models (Anthropic Claude 3.5 Sonnet v2 and Meta Llama 3.1 70B) are configured before proceeding.  
> Refer to: **Module 1.2: Adding Amazon Bedrock Integration**

---

### Step 3: Configure "Get All Security Hub Findings" Node

1. Select the node **"Get All Security Hub Findings"**.  
2. Click **Integration**, then configure the following:
   - **Integration (Optional):**  
     If you have multiple AWS integrations, select the specific one added previously. Otherwise, leave it blank.
   - **Region (Required):**  
     Select the AWS region where **Security Hub** is enabled and actively analyzing findings.  

![Configure Get All Security Hub Findings Node](../../static/sh-1.png)

---

### Step 4: Configure "Threat Analyzer Agent" Node

This node uses **Amazon Bedrock (Anthropic Claude 3.5 Sonnet v2)** for contextual analysis of findings.

1. Under **Integration**, set:
   - **Integration Type:** `Amazon Bedrock`
   - **Integration Account:** Select your previously added Amazon Bedrock integration.

![Configure Threat Analyzer Agent Node](../../static/sh-2.png)

2. Under **AI**, set:
   - **AI Model:** Choose `Claude 3.5 Sonnet v2`
   - *Note:* Ensure model access is available in your Bedrock account.

3. **Agent Tools:**
   - If you have multiple AWS or GitHub integrations, select the specific ones required for this workflow.
   - Otherwise, leave them as defaults.

---

### Step 5: Configure "Approval" Node

This node manages **human or automated approvals** before executing critical actions.

> **Note:**  
> Similar to the **AI Notification** nodes in other workflows, this node can send structured messages to notify or request approval from operators.

1. **Recipients:** Under the **Approvers** section, select the verified Amazon SES email identity. This is available as a **Static** option in the dropdown list, from which the appropriate verified SES email identity should be chosen.
2. **Service:** Choose **AWS SES**.  
3. **Connection:** Select the Amazon SES integration configured earlier.

![Configure Approval Node](../../static/sh-3.png)

---

### Step 6: Configure "Remediation Agent" Node

This node performs the actual remediation actions based on the analyzed findings and approval outcome.

1. Under **Integration**, set:
   - **Integration Type:** `Amazon Bedrock`
   - **Integration Account:** Choose the Amazon Bedrock account.
   - **AI Model:** Select `Claude 3.5 Sonnet v2`
   - *Note:* Ensure required model access.

2. **Agent Tools:**
   - If multiple integrations exist, assign the correct AWS integration to each tool.
   - If only one integration is present, no changes are needed.

---

### Step 7: Configure "Notification" Nodes

This workflow includes **multiple notification nodes** to provide updates on analysis and remediation progress.

Configure each notification node with:
1. **Recipients:** Verified Amazon SES email identity
2. **Service:** `Amazon SES`
3. **Connection:** Your Amazon SES integration

---

### Step 8: Save and Run the Bot

1. Click **Save** to apply all configuration changes.  
2. Click **Run** to start execution of the bot.
3. The bot will:
   - Retrieve all Security Hub findings
   - Analyze each finding for criticality and impact
   - Request approval for remediation actions
   - Execute approved remediations
   - Send notifications with results

---

## Understanding the Remediation Workflow

### Phase 1: Finding Collection (< 2 minutes)

The bot retrieves all active Security Hub findings from the specified region, filtering for:
- Findings with "FAILED" compliance status
- Supported finding types configured in the workflow
- Resources that can be automatically remediated

### Phase 2: AI Analysis (2-5 minutes)

Amazon Bedrock's Claude 3.5 Sonnet v2 analyzes each finding to:
- Assess severity and business impact
- Evaluate remediation complexity
- Identify potential risks of applying fixes
- Prioritize findings based on risk and impact
- Generate remediation recommendations

### Phase 3: Approval Request (Variable)

For high-risk changes, the bot:
- Sends detailed analysis via Amazon SES
- Includes finding details, proposed fix, and risk assessment
- Waits for human approval before proceeding
- Logs approval decisions for audit trail

### Phase 4: Automated Remediation (1-3 minutes)

The Remediation Agent executes approved fixes:
- Applies changes using AWS APIs
- Validates successful remediation
- Updates Security Hub finding status
- Handles errors and rollback if needed

### Phase 5: Validation & Notification (1-2 minutes)

The bot verifies remediation success:
- Confirms finding status changed to "PASSED"
- Sends completion notification with results
- Updates compliance scores
- Generates audit documentation

---

## Summary

In this section, you learned:

- ✅ How to import and configure the Security Hub remediation bot
- ✅ How Amazon Bedrock powers intelligent finding analysis
- ✅ The complete remediation workflow from detection to validation
- ✅ How to monitor and verify remediation effectiveness
- ✅ Best practices for operating automated security remediation

You've now completed the implementation of AI-driven automated remediation for AWS Security Hub findings, achieving continuous compliance through intelligent automation.

---

## Additional Resources

- [autobotAI Documentation](https://autobot.live/docs) - Complete platform documentation
- [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/) - Foundation models platform
- [Security Hub Automated Response](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-cloudwatch-events.html) - Event-driven automation
- [AWS Security Best Practices](https://docs.aws.amazon.com/security/) - Comprehensive security guidance

---

## ✅ Success Criteria

You've completed this section when:
- [ ] Imported the Security Hub remediation bot from the public library
- [ ] Configured the AWS Bedrock and SES nodes
- [ ] Saved and executed the workflow
- [ ] Verified finding remediation in Security Hub

---

## Troubleshooting

### Issue: Bot fails to fetch Security Hub findings
**Solution:** Verify your AWS integration permissions and ensure the AWS region in the Security Hub node is set to us-west-2.

### Issue: SES notification email not delivered
**Solution:** Ensure the recipient email address is verified in Amazon SES in us-west-2.
