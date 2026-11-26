---
title: "3.1 Importing and Configuring the DAM Agentic App"
weight: 1
---

> ⚠️ **Region Reminder:** Configure all AWS nodes to use **us-west-2 (Oregon)**.

**Estimated Time:** 20 minutes

---

> 🔴 **YOU ARE THE DAM BUILDER ADMIN**
>
> For this entire section, you are acting as the **Security Administrator**. Your role is to build the Database Access Management system, configure AI models, set up integrations, and prepare the system for database access requests from DBAs, developers, and the DevOps team.

---

## Overview

In this section, you'll import the Just-in-Time DAM (database access management) multi-agent workflow from the autobotAI library and configure it with AI models, integrations, and notifications. The infrastructure (RDS database, VPC, security groups) has already been deployed for this workshop.

## Prerequisites

The following infrastructure has been pre-deployed:
- Amazon RDS MySQL database cluster
- VPC with appropriate networking configuration
- Security groups for database access
- Amazon Bedrock models enabled in your AWS account
- Amazon SES verified email addresses (from Module 1.2)
- AbuseIPDB integration configured (from Module 1.3)
- AWS integration configured in autobotAI (from Module 1.3)

---

> **Note:** The bot will run for approximately **10-15 minutes**. You can monitor the progress in the execution logs or via the chat interface during the session.

---

## 🔴 Step 1: Import the Bot from Library

> 🔴 **Security Admin Task:** Import the pre-built JIT access bot from the autobotAI library.

1. Visit [https://autobot.live/app#/library](https://autobot.live/app#/library)
2. Search for **"Just In Time RDS Access Control"**
3. Select the bot and click **Import**

---

## 🔴 Step 2: Configure AI Model for All Agent Nodes

> 🔴 **Security Admin Task:** Configure the AI models that power each agent in the workflow.

Configure the following agent nodes with consistent AI model settings:
- User Validation
- Risk Evaluator
- Access Granting Agent
- Access Revocation Agent
- Activity Analysis Agent

**For each agent node:**
1. Click on the agent node in the workflow canvas
2. In the right panel, under **Integration**, select **AWS Bedrock** integration

   ![Bedrock Integration](../../static/model_configuration.png)

3. Under **AI**, set model to: **us.anthropic.claude-sonnet-4-6**

   ![Model Configuration](../../static/ai_model.png)

> ⚠️ **Important:** For the Risk Evaluator node and tasks requiring large context windows, select a larger model - it provides deeper comprehension of risk factors across extensive data. For Notification, Approval, and other communication-related workflow nodes, a smaller model selection can be given, as these tasks are straightforward and don't require heavy reasoning., e.g. use **us.anthropic.claude-sonnet-4-6** for all workflow nodes.

   ![Model Configuration](../../static/update-model-in-Risk-eval-node.jpg)

> **Note:** The workflow canvas is the main area showing the bot's flow diagram. Click on each circular agent node to see its configuration panel on the right side of the screen.

---

## 🔴 Step 3: Configure Email Notifications

> 🔴 **Security Admin Task:** Set up email notifications so you'll receive alerts for access requests and security events.

Configure Amazon SES for the following notification nodes:
1. **Notify RDS Access Initiated for a User**
2. **Notify RDS Access Approved for a High Risk User**
3. **Notify User Activity and Revocation Status**
4. **Approval Action**

**For each notification node:**
1. Click on the notification node in the workflow canvas
2. In the right panel, configure:
   - **Recipients:** Select **Events** from the top-right corner of the field, then manually enter the personal email address you verified in SES and press **Enter**.
   - **Service:** Select **SES**
   - **Connection:**  Select your SES integration
   - **Action:** Select **Send Message using AWS SES**
3. For the **Approval Action** node specifically, set:
   - **Number of required approvers:** `1`
   - Similar to Module 5.3, please select the **Static** option under the **Approvers** section, and then choose the verified Amazon SES email identity from the dropdown list.

![Email Notification Setup](../../static/notification_node_configuration.png)

> **Note:** If you receive a delivery failure email, check your domain's SPF, DKIM, and DMARC records. These notifications keep you informed about access requests, approvals, and security events. Make sure to use the email address you verified in Module 1.2.

---

## 🔴 Step 4: Save and Publish Agentic App to Service Portal

> 🔴 **Security Admin Task:** Save your configuration and publish the bot to the Service Portal to make it available for self-service DBA access requests.

1. Click **Save** at the top right of the canvas to apply all configuration changes.
2. From the top navigation menu, click on **Bots** to go to the Bots management page.

   ![Navigate to Bots Page](../../static/rds-nav-to-bots-page.png)

3. Locate the **Just In Time RDS Access Control** bot card, click the **three dots (...)** menu icon on the right-most column of the card, and select **Publish to Service Portal**.

   ![Publish Bot to Service Portal](../../static/rds-publish-to-service-portal.png)

---

## Configuration Summary

As the **Security Admin**, you have successfully configured:

| Component | Configuration | Purpose |
|-----------|---------------|---------|
| **AI Agents** | All 5 agents using Claude Sonnet 4.5 via Amazon Bedrock | Powers intelligent decision-making |
| **IP Validation** | AbuseIPDB integration for threat detection | Validates requester IP reputation |
| **AWS Services** | AWS integration in us-west-2 region for 8 action nodes | Enables credential provisioning |
| **Notifications** | Email alerts via Amazon SES for 4 notification points | Keeps you informed of access events |
| **Approvals** | Manual approval workflow configured with 1 required approver | Allows you to review high-risk requests |
| **Publishing** | Published to Service Portal | Enables DBA self-service request workflow |

---

## What Happens Next?

> 🔄 **Persona Switch Coming**
>
> In the next section (3.2), you'll switch between personas:
> -  **As a DBA, Developer, DevOps:** You'll launch the Agentic App from the Self Service Portal and request database access.
> -  **As Security Admin:** You'll review and approve high-risk requests.

**Workshop Tip**: Once published, DBAs can access the bot anytime via the Self Service Portal.

---

## ✅ Success Criteria

As the **Security Admin**, you've completed this section when:

| Task | Status |
|------|--------|
| 🔴 Agentic Workflow imported from library successfully | ☐ |
| 🔴 All 5 AI agent nodes configured with Claude Sonnet 4.5 (Risk Evaluator uses Llama 70B) | ☐ |
| 🔴 AbuseIPDB integration configured for IP validation | ☐ |
| 🔴 All 8 AWS action nodes configured with us-west-2 region | ☐ |
| 🔴 All 4 notification nodes configured with SES | ☐ |
| 🔴 Approval node configured with 1 required approver | ☐ |
| 🔴 Bot saved and published to Service Portal | ☐ |

---

## Troubleshooting

### Issue: Bot not found in library
**Solution:** Search for "Just In Time RDS" or "JIT RDS" instead.

### Issue: AI model not available in dropdown
**Solution:** Verify Amazon Bedrock integration is active and model access is enabled.

### Issue: "Publish to Service Portal" option missing
**Solution:** Ensure you have saved all workflow changes before navigating to the Bots page.
