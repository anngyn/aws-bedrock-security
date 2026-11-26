---
title: "1.2 Creating AWS Integrations"
weight: 2
---

> ⚠️ **Region Reminder:** Deploy CloudFormation stack and configure all integrations in **us-west-2 (Oregon)**.

**Estimated Time:** 20 minutes

**Objective:** Set up AWS, Amazon Bedrock, Amazon Athena, and Amazon SES integrations to enable comprehensive security automation.

## Overview

We'll set up four key integrations to enable comprehensive security automation: AWS (infrastructure), Amazon Bedrock (AI), Amazon Athena (log analytics), and Amazon SES (notifications).

---

## Adding AWS Integration

### Purpose
The **AWS Integration** connects autobotAI with your AWS account, enabling it to securely access AWS services and resources for automation.  
It forms the foundation for all subsequent AWS-related integrations such as **Amazon Bedrock**, **Amazon SES**, and **Amazon Inspector**.

### Steps

1. After successfully signing up, open another browser tab and [**sign in to your AWS account**](https://console.aws.amazon.com/).
2. From the autobotAI home page, click on **Integrations**.

![Integrations Page](../../static/mod1-overview-page.png)

3. Click on **+ Add Integration**, search for **AWS**, and select **AWS**.

4. Provide the following details:

   ![AWS Integration Setup](../../static/mod1-aws-integration-setup.png)

   - **Account Name/Alias**: Enter any relevant name for this integration (e.g. AIOps).
   - **Permission Set**: Select **FullAccess** (or your preferred permission set: *FullAccess*, *AppSec*, *IAMOps*, or *SOC*).

   ![Select Additional AWS Integrations](../../static/mod1-select-additional-integrations.png)

   - **Additional AWS Integrations**: Select the checkboxes for **AWS Bedrock**, **AWS SES**, and **AWS Athena** so they are set up alongside your AWS integration, and set the region to **us-west-2 (Oregon)**.
   - **Acknowledgements**: Check the acknowledgement checkboxes before proceeding.

5. Click **Continue Setup**.  
6. Click on **Launch Stack**. This will redirect you to the AWS Console.

![Launch Stack](../../static/mod1-launch-stack.png)

7. Change the region to **Oregon - us-west-2**.  
8. Scroll down, check the confirmation boxes, and click **Create Stack**.  

> **Note:** Make sure to check the **"I acknowledge that AWS CloudFormation might create IAM resources with custom names."** box before submitting.

![Deploy Stack1](../../static/region.png)  
![Deploy Stack2](../../static/aws-launch-stack2.png)

9. Once the stack creation completes, go back to the autobotAI window and wait for **5-10 seconds**.  
    - A **Test Connection** button will automatically appear. Click it to proceed. This will redirect you to the **Integrations** tab, where you should see your AWS integration listed as **Active**.  

    ![Test Button Appearing](../../static/test-button-appearing-new.jpg)

> **Note:** If the 'Test' button does not appear automatically, you can manually activate the integration:  
> 1. Go to the **Integrations** listing page.  
> 2. Click on the **Filter** icon and select **Inactive** from the **State**.  
> 3. Locate your AWS integration from the filtered list.  
> 4. Click the **Play button (▶)** icon under **Actions** to test the integration.  
> 5. Once you see the "Successful" message, refresh the page to see the **Active** state.  

> **Troubleshooting Tip:** If the CloudFormation stack deploys successfully in `us-west-2` but autobotAI doesn't show the integration as active (even after testing), wait a few minutes and try refreshing the page or re-testing the integration. This sync issue occurs intermittently.

---

## Adding and Verifying Identities in Amazon SES

This step is required to send or receive notifications via Amazon SES.

> ⚠️ **SES Sandbox Mode:** Workshop accounts require **both sender AND recipient emails to be verified**.
>
> **Simplest approach:** Use the same email for both — verify it once and use it as both "From" and "To" in workflows.
>
> **If your corporate email blocks same From/To:** Verify a personal email (Gmail, etc.) as "From" and your work email as "To".

1. Go to the **SES service** in your AWS console (in the same region used for integration).
2. From the left panel, select **Identities**.  
3. Click **Create Identity**.  
4. Choose **Email Address**, enter the email address you used for autobotAI, and click **Create Identity**.
5. Repeat this process for an additional personal email address (preferably Gmail) to receive notifications.

![Create SES Identity](../../static/ses-verify1.png)

6. You will receive verification emails from AWS for each identity.  
7. Open each email and click on the **verification link**.

![Verify SES Email](../../static/ses-verify2.png)

---

## Setting Up Global Settings

### Configure Global AI Preference

This configuration allows the platform to automatically use your preferred **AI integration** and **model** for generating AI-driven insights, notifications, and automation across workflows.

### Prerequisites

To use the **Claude Opus 4.6** model, ensure that:  
- Your **Amazon Bedrock account** has **access enabled** to the Claude Opus 4.6 model.
- The model is available in your selected AWS region (`us-west-2`).  
- If you don't see the model in your dropdown, request access from the **Amazon Bedrock Console** under *Model Access*.

### Steps

1. From the **autobotAI** console, click on the **Slider bar (Settings)** icon (near the bell icon).
2. Navigate to **AI Configuration**.  
3. Select the following:  
   - **Integration Type:** Choose your AI provider (e.g., Amazon Bedrock).
   - **Integration:** Select the integrated AI account you configured earlier.  
   - **LLM Model:** Pick the model you want the platform to use globally (e.g., **Claude Opus 4.6**).  

![Step 1 – Configure Global AI Preferences](../../static/mod1-ai-configuration.png)

---

## (Optional) Manual Integration Creation

> ℹ️ **Manual Creation Note:** The individual integration sections below (Amazon Bedrock, Amazon Athena, and Amazon SES) are **optional**. Since you selected **AWS Bedrock**, **AWS SES**, and **AWS Athena** during the main AWS integration setup, autobotAI creates them automatically. Only follow these manual creation steps if autobotAI fails to create an integration automatically alongside AWS.

### (Optional) Adding Amazon Bedrock Integration

#### Purpose
The **Amazon Bedrock Integration** enables autobotAI to use **Generative AI models** (such as Claude, Titan, or Llama) from Amazon Bedrock.
This allows AI-powered agents and workflows to analyze, generate, and fix code, or make autonomous security decisions.

#### Prerequisites
Your AWS account must already be integrated with autobotAI.

#### Steps
1. From the autobotAI home page, click on **Integrations**.  
2. Click on **+ Add Integration**, scroll down to **AI Services**, and select **Amazon Bedrock**.
3. Provide the following details:
   - **Alias**: Name for the integration.
   - **Tag (optional)**: Select or enter an optional tag.
   - **Integration Id**: Select the AWS integration created in the previous step.
   - **Region (optional)**: Select the region **Oregon - us-west-2**.  
4. Click **Create**.

![Amazon Bedrock Integration](../../static/bedrock.png)

---

### (Optional) Adding Amazon Athena Integration

#### Purpose
The **Amazon Athena Integration** lets autobotAI run **SQL queries directly against your logs in Amazon S3** — without provisioning any database.
It is the engine behind the **WAF Log Threat Analysis** module (Module 2), where the AI agent creates an external table over your AWS WAF v2 logs and queries them to detect, classify, and remediate web attacks.

#### Prerequisites
Your AWS account must already be integrated with autobotAI.

#### Steps
1. From the autobotAI home page, click on **Integrations**.
2. Click on **+ Add Integration**, then **search for `Athena`** and select the **AWS Athena** card → **Add Integration**.

![Search for Athena](../../static/athena-search.png)

3. Provide the following details:
   - **Alias**: Name for the integration.
   - **Tag (optional)**: Select or enter an optional tag.
   - **Integration Id**: Select the AWS integration created in the first step.
   - **Region (optional)**: Select the region **Oregon - us-west-2** (the same region as your WAF logs).
4. Click **Create**.

![Amazon Athena Integration](../../static/athena.png)

> **Note:** Athena reads query results into an S3 output location. The workshop AWS account is pre-provisioned with the WAF log bucket and an Athena results bucket, so no extra configuration is required here.

---

### (Optional) Adding Amazon SES Integration

#### Purpose
The **Amazon SES (Simple Email Service) Integration** allows autobotAI to send **AI-generated notifications, alerts, and reports** through verified email addresses.

#### Prerequisites
AWS account integration must be completed before this step.

#### Steps
1. From the autobotAI home page, click on **Integrations**.  
2. Click on **+ Add Integration**, scroll down to **Notifications and Communications**, and select **Amazon SES**.  
3. Provide the following details:
   - **Alias**: Name for the integration.
   - **Tag (optional)**: Select or enter an optional tag.
   - **Integration Id**: Select the AWS integration created earlier.
   - **Region (optional)**: Select the region where your SES service is configured.
4. Click **Create**.

![Amazon SES Integration](../../static/ses.png)

---

**Next:** Proceed to Module 1.3 to set up GitHub integration.

---

## ✅ Success Criteria

You've completed this section when:
- [ ] AWS integration shows "Active" status in autobotAI
- [ ] Amazon Bedrock, Athena, and SES integrations created (automatically or manually)
- [ ] SES email identity verified (check for "Verified" status in SES console)
- [ ] If using different From/To emails: Both email addresses verified in SES

---

## Troubleshooting

### Issue: CloudFormation stack creation fails
**Solution:**
1. Ensure you're in us-west-2 region
2. Check that you acknowledged the IAM capabilities checkbox
3. Review the stack events for specific error messages

### Issue: AWS integration not showing as Active
**Solution:**
1. Wait 30-60 seconds after stack creation
2. Click "Test" manually from the Integrations page
3. Verify the CloudFormation stack completed successfully

### Issue: SES verification email not received
**Solution:**
1. Check spam/junk folder
2. Verify you entered the correct email address
3. Try creating a new identity if the email doesn't arrive within 5 minutes

### Issue: SES email sending fails with "Email address not verified"
**Solution:**
1. In SES Sandbox mode, **both sender AND recipient** must be verified
2. Verify the recipient email address in SES console (Identities → Create Identity)
3. If using same email for From/To and it fails, try using a different personal email as the "From" address

### Issue: Corporate email blocks same From/To address
**Solution:**
1. Some corporate email policies reject emails where sender = recipient
2. Verify a personal email (Gmail, Yahoo, etc.) as the "From" address
3. Keep your corporate email as the "To" (recipient) address
4. Both addresses must be verified in SES
