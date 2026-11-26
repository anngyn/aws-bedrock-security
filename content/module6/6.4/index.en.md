---
title: "6.4 (Bonus) Remediating SCA and IaC with Multi-Agent Multi-Model Workflow"
weight: 4
---

> ⚠️ **Region Reminder:** Configure all AWS resources in **us-west-2 (Oregon)**.

**Estimated Time:** 10 minutes

## Introduction

Now that you have experienced how to create and execute a complex, agentic AppSec workflow autonomously with Optimus, let's explore another way to set up these bots.

As an alternative to building the AppSec Inspector bots interactively with Optimus, you can directly import the pre-built remediation workflow from the autobotAI library and configure the nodes for a high degree of flexible process control. This approach allows you to quickly deploy the remediation bot using a standardized template if you prefer a more hands-on configuration experience.

---

## Importing the Workflow

> **Note:** The bot will run for approximately **10 minutes**. You can monitor the progress in the execution logs or via the chat interface during the session.

### Step 1: Import the Bot from Library

1. Visit the [autobotAI Library](https://autobot.live/app#/library).  
2. Search for **"AWS Inspector Code Security With Agentic AI Fixes"**.  
3. Click on the bot card and select **Import**.

---

### Step 2: Configure the Bot Integration

> **Note:** Ensure AWS integrations and Bedrock models (Anthropic Claude 4.5 Sonnet) are configured before proceeding.  
> Refer to: **Module 1.2: Adding Amazon Bedrock Integration**

---

### Step 3: Configure "Inspector Scanning" Node

1. Select the **Inspector Scanning** node.
2. Click **Integration**, then configure the following:
   - **Integration (Optional):** Select your specific AWS integration if you have multiple.
   - **Region (Required):** Select the AWS region where **Amazon Inspector** is enabled (e.g., `us-west-2`).

---

### Step 4: Configure "AI Agent" Node

This node uses **Amazon Bedrock** for intelligent analysis of the findings and generating remediation code.

1. Under **Integration**, set:
   - **Integration Type:** `Amazon Bedrock`
   - **Integration Account:** Select your previously added Amazon Bedrock integration.
   - **AI Model:** Choose `global.anthropic.claude-sonnet-4-5-20250929-v1:0` or `Claude 3.5 Sonnet v2`.

---

### Step 5: Configure "Notification" Nodes

The workflow includes nodes for notifying the reviewer and escalating if the SLA is breached.

1. **Recipients:** Under the **Approvers** section, select the verified Amazon SES email identity.
2. **Service:** Choose **AWS SES**.  
3. **Connection:** Select the Amazon SES integration configured earlier.

---

### Step 6: Save and Run the Bot

1. Click **Save** to apply all configuration changes.  
2. Click **Run** to start execution of the bot.
3. The bot will:
   - Retrieve Inspector vulnerabilities
   - Analyze and clone the vulnerable repository
   - Push code fixes and create a Pull Request
   - Send SLA-enforced notifications to ensure the PR is reviewed

---

## Validation

After the bot runs, you can verify its actions exactly as you did in the Optimus-built workflow:
1. Navigate to your GitHub repository and review the newly created Pull Request.
2. Check the **Tasks** dashboard in autobotAI to see the tracking status.
3. Check your email for the notification and escalation messages.

---

## ✅ Success Criteria

You've completed this section when:
- [ ] The AppSec Inspector Remediation Workflow is successfully imported
- [ ] Inspector Scanning node is configured with the correct region
- [ ] AI Agent node is configured with the correct Bedrock model
- [ ] Notification nodes are configured with the verified SES identity
- [ ] The bot executes successfully and creates a remediation PR

---

## Troubleshooting

### Issue: The workflow fails to import
**Solution:** Ensure you are searching for the exact name in the library. If the library is empty, refresh your session.

### Issue: The bot stops running without creating a PR
**Solution:** Check the AI Agent node to ensure you selected the correct Bedrock model (Claude 3.5 Sonnet v2) and that model access is enabled in your AWS account.
