---
title: "1.3 Adding GitHub and AbuseIPDB Integrations"
weight: 3
---

> ⚠️ **Region Reminder:** Ensure all integrations and Bedrock models are configured in **us-west-2 (Oregon)**.

**Estimated Time:** 15 minutes

**Objective:** Connect autobotAI with GitHub repositories and threat intelligence services to enable AI-driven code analysis and intelligent threat response.

---

## Adding GitHub Integration

### Purpose
The **GitHub Integration** connects autobotAI with your code repositories to enable **AI-driven code analysis, automated fixes, and pull request creation**.  
It's required for bots like *Amazon Inspector Code Security With Agentic AI Fixes*.

### Prerequisites
You'll need to generate a GitHub Personal Access Token (Classic) to authenticate autobotAI with your GitHub account. Follow the steps below to create your token.

### Step 1: Sign in to GitHub

1. Visit [https://github.com/settings/tokens](https://github.com/settings/tokens).
2. If you're not already signed in, you'll be redirected to the GitHub sign-in page:
   - **If you have a GitHub account:** Enter your username/email and password, then click **Sign in**.
   - **If you don't have a GitHub account:** Click **Sign up** and follow these steps:
     - Enter your email address
     - Create a password
     - Choose a username
     - Complete the verification puzzle
     - Click **Create account**
     - Verify your email address by clicking the link sent to your inbox
3. Once signed in, you'll be taken to the Personal Access Tokens page.

### Step 2: Generate GitHub Token

1. Click **Generate new token**, then select **Generate new token (classic)**.
   - If you have MFA enabled, enter the verification code to continue.  
2. Provide a name for your token.  
3. Under **Select scopes**, check the **repo** permission.  

![Generate GitHub Token](../../static/github-1.png)

4. Scroll down and click **Generate token**.  
5. Copy the generated token and store it safely — you won't be able to view it again later.

![Copy GitHub Token](../../static/github-2.png)

### Step 3: Add GitHub Integration in autobotAI

1. From the autobotAI home page, click on **Integrations**.  
2. Click on **+ Add Integration**, search for **GitHub**, and click **Add Integration (GitHub)**.
3. Provide the following:
   - **Alias**: Name for the integration.  
   - **Tag (optional)**: Select or enter an optional tag.  
   - **GitHub Token**: Paste the generated GitHub token.  
4. Click **Create**.

![GitHub Integration Setup](../../static/mod1-github-setup.png)

---

## Adding AbuseIPDB Integration

### Purpose
The **AbuseIPDB Integration** allows autobotAI agents to automatically check, validate, and respond to potentially malicious IPs detected in your environment — especially when used alongside **GuardDuty remediation workflows**.

### Sign up and Create AbuseIPDB API Key

1. **Sign Up for AbuseIPDB**  
   Go to [https://www.abuseipdb.com/register?plan=free](https://www.abuseipdb.com/register?plan=free) and **sign up for a free account**.  
   Fill in the required details:
   - **First Name**
   - **Last Name**
   - **Email Address**
   - **Password**

   > **Note:** Make sure to check the **"I'm not a robot"** box before submitting.  

   ![AbuseIPDB Integration](../../static/abdb.png)

2. **Verify Your Account**  
   After signing up, you will receive a verification email.  
   Open your inbox (check your spam folder if the email isn't there), locate the email, and click the verification link provided.

   ![AbuseIPDB Integration2](../../static/abdb-verify.png)

   Once verified, you will see the message:  
   *"Your email address has been successfully verified."*

3. **Access the API Key Section**  
   Click on your **Username** (top-right corner) and select **My API** under **Quick Links**.  
   Click **Create Key**, give your key a name, and click **Create**.

4. **Copy the API Key**  
   Locate and copy the generated **API Key** from this section.  

   ![AbuseIPDB Integration3](../../static/abdb-apikey.png)

5. **Add the API Key in autobotAI**  
   - Open the **autobotAI** platform.  
   - Navigate to **Integrations → + Add Integration → search AbuseIPDB → Add Integration (AbuseIPDB)**.  
   - Provide the following details:  
     - **Alias:** A recognizable name for this integration.  
     - **Tag (optional):** Select or enter an optional tag.  
     - **API Key:** Paste the copied AbuseIPDB API Key here.  
   - Click **Create** to complete the setup.

---

## Integration Summary

You have successfully set up all core integrations for your autobotAI security automation platform:

| Integration | Purpose | Status |
|-------------|---------|--------|
| **AWS** | Infrastructure access and security service integration | ✅ Connected |
| **Amazon Bedrock** | AI-powered threat analysis and response generation | ✅ Connected |
| **Amazon Athena** | SQL query engine for log analytics (WAF, CloudTrail, etc.) | ✅ Connected |
| **Amazon SES** | Automated security notifications and alerts | ✅ Connected |
| **GitHub** | AI-driven code analysis and automated security fixes | ✅ Connected |
| **AbuseIPDB** | Threat intelligence for malicious IP validation | ✅ Connected |

---

**Next:** With your integrations complete, you're ready to move to **Module 2: WAF Log Threat Analysis & Rule Building with Optimus**, where Optimus uses your Athena and AWS integrations to surface and remediate web attacks straight from the WAF logs.

---

## ✅ Success Criteria

You've completed this section when:
- [ ] GitHub integration shows "Active" status
- [ ] AbuseIPDB integration configured with API key
- [ ] Global AI preferences set (Amazon Bedrock + Claude Opus 4.6)
- [ ] All 5 integrations visible in the Integrations page

---

## Troubleshooting

### Issue: GitHub token not working
**Solution:**
1. Ensure you selected "repo" scope when creating the token
2. Verify the token hasn't expired
3. Try generating a new token if issues persist

### Issue: AbuseIPDB verification email not received
**Solution:** Check spam folder. The email comes from AbuseIPDB, not AWS.

### Issue: Claude Opus 4.6 not available in model dropdown
**Solution:**
1. Go to Amazon Bedrock console → Model access
2. Request access to Anthropic Claude models
3. Wait for approval (usually instant for workshop accounts)
