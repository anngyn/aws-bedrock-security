---
title: "Preparation"
weight: 1
---

> ⚠️ **Region Reminder:** All workshop activities should be performed in the **us-west-2 (Oregon)** region.

**Estimated Time:** 10-15 minutes (Option A) | 30-35 minutes (Option B)

## Choose Your Setup Path

This workshop can be completed in two ways. Select the option that matches your situation:

| Option | Best For | Time | Cost |
|--------|----------|------|------|
| **Option A: AWS Event** | Attending an AWS-hosted workshop event | 5 min | Free |
| **Option B: Self-Paced** | Learning on your own, in your own AWS account | 30 min | ~$10-15/day |

---

## Option A: AWS Event (Workshop Studio)

> **Use this option if:** You are attending an AWS-hosted event and received a sign-in URL from the event organizer.

### Step 1: Sign In to Workshop Studio

1. Obtain the sign-in URL from the event organizer. Click **Email One-Time Password (OTP)**.

   ![Workshop Studio Sign In](../static/preparation/1-sign-in.png)

2. Enter your email address and click **Send passcode**.

   ![Enter Email for OTP](../static/preparation/2-otp-email.png)

3. Check your inbox for the email with subject **Your one-time passcode**.

   ![Email Passcode](../static/preparation/3-outlook-screenshot.jpg)

4. Enter the passcode and click **Sign in**.

   ![Enter Passcode](../static/preparation/4-otp-passcode.png)

5. The event access code should be pre-filled. Click **Next**.

   ![Event Access Code](../static/preparation/5-event-access-code.png)

6. Check **I agree with the Terms and Conditions** and click **Join event**.

   ![Terms and Conditions](../static/preparation/6-terms-and-conditions.png)

7. Click **Open AWS Console** in the left menu.

   ![Open AWS Console](../static/preparation/consolelogin.png)

### ✅ Option A Complete

Your AWS environment is ready. Proceed to **Module 1** to begin the workshop.

---

## Option B: Self-Paced (Your Own AWS Account)

> **Use this option if:** You want to run this workshop independently in your own AWS account.

### Prerequisites

Before you begin, ensure you have:

- [ ] AWS account with **Administrator access**
- [ ] Credit card attached to AWS account (for resource costs)
- [ ] Valid email address (for SES verification)
- [ ] GitHub account (for code security module)
- [ ] ~30 minutes for initial setup

### Cost Warning

⚠️ **Important:** Running this workshop in your own account will incur AWS charges.

| Resource Type | Estimated Cost |
|--------------|----------------|
| EC2 Instances (2x t3.micro) | ~$0.50/day |
| RDS PostgreSQL (db.t3.micro) | ~$0.50/day |
| Aurora MySQL Serverless v2 | ~$2-5/day |
| NAT Gateway | ~$1.50/day |
| Other services | ~$1-2/day |
| **Total Estimate** | **~$10-15/day** |

> 💡 **Tip:** Delete the CloudFormation stack immediately after completing the workshop to stop charges.

---

### What Gets Deployed

The CloudFormation template creates a complete security workshop environment:

```text
┌─────────────────────────────────────────────────────────────────┐
│                    SECURITY SERVICES                            │
│  GuardDuty │ Security Hub │ Inspector │ AWS Config │ Detective  │
└─────────────────────────────────────────────────────────────────┘
        │                                           │
        ▼                                           ▼
┌───────────────────────┐         ┌───────────────────────────────┐
│     MAIN VPC          │         │         RDS VPC               │
│  ┌─────────────────┐  │         │  ┌─────────────────────────┐  │
│  │ Attacker EC2    │  │         │  │ PostgreSQL (GuardDuty)  │  │
│  │ (Red Team)      │──┼────────▶│  │ MySQL (Security Hub)    │  │
│  ├─────────────────┤  │         │  └─────────────────────────┘  │
│  │ Vulnerable EC2  │  │         └───────────────────────────────┘
│  │ (SSH Target)    │  │
│  └─────────────────┘  │         ┌───────────────────────────────┐
└───────────────────────┘         │       JIT VPC (Module 2)      │
                                  │  ┌─────────────────────────┐  │
                                  │  │ Aurora MySQL Serverless │  │
                                  │  │ (JIT Access Demo)       │  │
                                  │  └─────────────────────────┘  │
                                  └───────────────────────────────┘
```

---

### Step 1: Enable Amazon Bedrock Model Access (Do This First!)

> 💡 **Why first?** Bedrock access is instant for most accounts, but doing this first lets you proceed while CloudFormation deploys.

1. Open [Amazon Bedrock Console](https://us-west-2.console.aws.amazon.com/bedrock/home?region=us-west-2#/modelaccess)

2. Click **Manage model access**

3. Enable the following models:
   - ✅ **Anthropic - Claude 3.5 Sonnet v2**
   - ✅ **Meta - Llama 3.1 70B Instruct**

4. Click **Request model access**

5. Wait for status to change to **Access granted** (usually instant)

> **Note:** Some models may require acceptance of end-user license agreements (EULA).

---

### Step 2: Deploy CloudFormation Stack

The CloudFormation template creates all required AWS resources for this workshop.

#### Get the Template

:button[Download cfn-self-paced.yaml]{href="https://static.us-east-1.prod.workshops.aws/public/1ff65006-cc4a-48fd-99c9-3ef1e3d7a5ef/static/cfn-self-paced.yaml" action=download}

> 💡 **Alternative:** Right-click the button above → "Save Link As..." → Save as `cfn-self-paced.yaml`

#### Deploy via AWS Console

1. Download the template using the button above

2. Open the [AWS CloudFormation Console](https://us-west-2.console.aws.amazon.com/cloudformation/home?region=us-west-2)

3. Click **Create stack** → **With new resources (standard)**

4. Select **Upload a template file**, choose the downloaded file, and click **Next**

5. Enter stack name: `autobotai-security-workshop`

6. Click **Next** through the options page

7. On the Review page, scroll to the bottom and check:
   - ✅ **I acknowledge that AWS CloudFormation might create IAM resources with custom names**
   - ✅ **I acknowledge that AWS CloudFormation might require the following capability: CAPABILITY_AUTO_EXPAND**

8. Click **Create stack**

---

### Step 3: Wait for Deployment (~25-30 minutes)

The stack creates the following resources:

| Category | Resources Created |
|----------|-------------------|
| **Networking** | 3 VPCs, Subnets, NAT Gateway, Internet Gateways, Route Tables |
| **Security Services** | GuardDuty, Security Hub, Inspector, AWS Config, Detective |
| **Compute** | 2 EC2 instances (attack simulation + vulnerable target) |
| **Database** | PostgreSQL RDS, Aurora MySQL Serverless v2 (for JIT access) |
| **Storage** | S3 buckets for GuardDuty logs and Config |
| **IAM** | Roles and policies for workshop resources |
| **Vulnerable Resources** | Intentionally misconfigured resources for Security Hub findings |

Monitor the deployment:
1. Go to [CloudFormation Console](https://us-west-2.console.aws.amazon.com/cloudformation/home?region=us-west-2)
2. Select your stack (`autobotai-security-workshop`)
3. Click the **Events** tab to monitor progress
4. Wait until status shows **CREATE_COMPLETE**

---

### Step 4: Verify Deployment

After the stack completes, verify the resources:

#### Check CloudFormation Outputs

1. In CloudFormation Console, select your stack
2. Click the **Outputs** tab
3. Note these important values:
   - `JITDBClusterEndpoint` - Aurora MySQL endpoint for Module 2
   - `RedTeamAttackerIP` - Attacker instance IP (for GuardDuty findings)

#### Verify Security Services

| Service | Verification |
|---------|--------------|
| **GuardDuty** | [Console](https://us-west-2.console.aws.amazon.com/guardduty/home?region=us-west-2) → Should show "Enabled" |
| **Security Hub** | [Console](https://us-west-2.console.aws.amazon.com/securityhub/home?region=us-west-2) → Should show dashboard |
| **Inspector** | [Console](https://us-west-2.console.aws.amazon.com/inspector/v2/home?region=us-west-2) → Should show "Activated" |
| **Config** | [Console](https://us-west-2.console.aws.amazon.com/config/home?region=us-west-2) → Should show recorder running |

---

### Step 5: Wait for Security Findings (~15-30 minutes)

The deployed resources automatically generate security findings:

- **GuardDuty:** Attack simulations run automatically and generate findings within 15-30 minutes
- **Security Hub:** Compliance checks run immediately and show FAILED findings
- **Inspector:** EC2 vulnerability scans complete within 10-15 minutes

> 💡 **Tip:** You can proceed to Module 1 while waiting for findings to generate.

---

### ✅ Option B Complete

Your self-paced environment is ready. Proceed to **Module 1** to begin the workshop.

---

## Cleanup Instructions (Self-Paced Only)

> ⚠️ **Important:** Delete resources after completing the workshop to avoid ongoing charges.

### Delete CloudFormation Stack

1. Open [CloudFormation Console](https://us-west-2.console.aws.amazon.com/cloudformation/home?region=us-west-2)
2. Select `autobotai-security-workshop` stack
3. Click **Delete**
4. Confirm deletion
5. Wait for stack deletion to complete (~15-20 minutes)

### ⚠️ If Stack Deletion Fails

Stack deletion commonly fails due to non-empty S3 buckets. Follow these steps:

**Step 1: Empty S3 Buckets**
1. Go to [S3 Console](https://s3.console.aws.amazon.com/s3/home?region=us-west-2)
2. Find buckets starting with `autobotai-workshop-`
3. For each bucket:
   - Select the bucket → Click **Empty** → Confirm
4. Retry stack deletion

**Step 2: Manual Cleanup (if still failing)**

If the stack still fails to delete, manually remove these resources:

| Resource Type | How to Find | Action |
|--------------|-------------|--------|
| **S3 Buckets** | Search `autobotai-workshop` | Empty, then delete |
| **RDS Snapshots** | RDS Console → Snapshots | Delete manual snapshots |
| **GuardDuty** | GuardDuty Console | Disable if needed |
| **Security Hub** | Security Hub Console | Disable if needed |
| **Config Recorder** | Config Console | Stop recorder |

---

## Troubleshooting

### Issue: CloudFormation stack fails to create
**Solution:**
1. Check the **Events** tab for the specific error
2. Common issues:
   - Service limits exceeded → Request limit increase
   - IAM permissions → Ensure you have Administrator access
   - Region not supported → Use us-west-2

### Issue: "GuardDuty detector already exists" error
**Solution:**
This should no longer occur - the template automatically detects and uses existing GuardDuty detectors. If you still see this error, please report it.

### Issue: "BlockPublicPolicy" error for S3 bucket
**Solution:**
Your account has S3 Block Public Access enabled at the account level (security best practice). This is fine - the S3 bucket will still be created and Security Hub will still generate findings for the misconfigured bucket settings.

### Issue: Bedrock models show "Access denied"
**Solution:**
1. Verify you requested access in Step 1
2. Check that access status shows "Access granted"
3. Some models require EULA acceptance

### Issue: No GuardDuty findings after 30 minutes
**Solution:**
1. Verify GuardDuty is enabled in us-west-2
2. Check that EC2 instances are running
3. Findings may take up to 1 hour in some cases

### Issue: Security Hub shows no findings
**Solution:**
1. Verify Security Hub is enabled
2. Wait 15-30 minutes for initial compliance checks
3. Check that AWS Config recorder is running

### Issue: Stack deletion fails
**Solution:**
1. Check CloudFormation Events tab for the failing resource
2. Most common: S3 buckets not empty - empty them first
3. See "If Stack Deletion Fails" section above

---

## ✅ Success Criteria

You've completed this section when:
- [ ] You can access the AWS Console (via Workshop Studio OR your own account)
- [ ] The AWS Console shows **us-west-2** as the selected region
- [ ] (Self-Paced) Amazon Bedrock models show "Access granted"
- [ ] (Self-Paced) CloudFormation stack shows **CREATE_COMPLETE**
