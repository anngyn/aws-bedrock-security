---
title: "3.2 Testing the JIT Access Workflow"
weight: 2
---

> ⚠️ **Region Reminder:** Use CloudShell in **us-west-2 (Oregon)** for database connections.

**Estimated Time:** 40 minutes

---

> 🔄 **IN THIS SECTION YOU ARE THE USER OF THE AGENTIC APP**
>
> In this section, you will switch between two personas:
> - 🟢 **DBA (Database Administrator), Developer or DevOps:** Requests database access and runs queries
> - 🔴 **Security Admin:** Reviews and approves high-risk access requests
>
> Watch for the colored callout boxes to know which persona you should assume at each step.

---

## Overview

In this section, you'll test the Just-in-Time database access agentic workflow through two scenarios:
1. **Low-risk access** with automatic approval
2. **High-risk access** requiring manual approval

You'll experience how AI agents validate requests, assess risk, provision credentials, automatically revoke access, and generate IoCs when the activity looks risky.

---

## Step 1: Test Low-Risk Access Request (Automatic Approval)

> 🟢 **You are DBA, Developer, DevOps Persona**
>
> You are now **Alice**, a Data Engineer who needs temporary database access to investigate failed payment transactions. You'll request access through the chat interface.

This scenario demonstrates automatic approval for low-risk access requests.

**Scenario:**
- **User:** Alice (Data Engineer)  
- **Task:** Reconcile failed payment transactions  
- **Risk Level:** Low  
- **Expected Outcome:** Automatic approval

---

### 🟢 1.1: Initiate Access Request via Self Service Portal

> 🟢 **DBA Task:** Access the Self Service App Portal and start the DAM (Database Access Management) workflow.

1. Click on your **profile icon** in the top-right corner of the autobotAI header and select **Self Service Portal**.

   ![Access Self Service Portal](../../static/rds-open-self-service-portal.png)

2. On the Self Service Portal page, click on the published **Just In Time RDS Access Control** bot card.

   ![Select Published Bot in Self Service Portal](../../static/rds-self-service-portal-bots.png)

3. The Bot Portal page opens. Click the **Start** button to begin an access request session.

   ![Click Start Button in Bot Portal](../../static/rds-bot-portal-start-button.png)

4. A popup notification banner appears on the right side of the screen. Click **Open Chat** to open the interactive chat interface.

   ![Click Open Chat in Popup Banner](../../static/rds-open-chat-popup.png)

5. The **Val** (validation agent) will greet you in the chat panel. Proceed to complete identity validation.

---

### 🟢 1.2: Complete Identity Validation

> 🟢 **DBA Task:** Provide your identity information for validation.

Val will request the following information:

1. **IP Address:** Enter your current IP address (search "my ip" in browser)

   ![IP Address Request](../../static/ip_validation.png)

   - Expected: `✅ Your IP looks clean! Risk score: 0 out of 100.`

2. **IAM Role:** Enter `WSParticipantRole`

   ![IAM Role Request](../../static/iam_validation.png)

   - Expected: `✅ Found you! The role is active and valid.`

3. **RDS Instance:** Select **cfn-jit-rds-access-writer**

   ![RDS Instance Selection](../../static/instance_selection.png)

4. **Database Schema:** Enter `workshop_db`

   ![Database Schema Request](../../static/schema_selection.png)

5. **Access Justification:** Provide a specific reason

   - Use the access justification given below:

   ```text
   Need to reconcile failed payment transactions from overnight batch jobs. Investigating duplicate payment_id errors. Reference incident: INC-2024-5348.
   ```

   ![Access Justification](../../static/access_reason.png)

6. **Access Duration:** Enter `10 minutes`

   ![Access Duration](../../static/access_duration.png)

> If the chat session does not end automatically:
> 1. Click the **red power button** on the left of the prompt box.
> 2. Click **End Session**.
>
> Now wait for **Eva** (evaluation agent) to evaluate your request and **Grant** (access granting agent) to grant you access to the database.

---

### 🟢 1.3: Automatic Risk Evaluation

> 🟢 **DBA Observation:** Watch as the AI evaluates your request and determines it's low-risk.

**Eva** (evaluation agent) analyzes your request:

<img src="../../static/risk_evaluator.png" alt="Risk Evaluation" width="400"/>

**Risk Factors:**
- IP Reputation: Very safe (2/100)
- IAM Identity: Verified and active
- Access Time: Normal business hours
- Access Reason: Specific and auditable
- Requested Duration: Reasonable (10 minutes)

**Risk Score:** 15/100 → **LOW RISK**  
**Decision:** **AUTOMATIC APPROVAL**

---

### 🟢 1.4: Receive Access Credentials

> 🟢 **DBA Task:** Receive and note your temporary database credentials.

Click on the **sidebar icon** on the left side of the Bot Service Portal page to open the agent drawer and access the next agent — **Grant** (Access Granting Agent) — to view your temporary database credentials.

![Sidebar Icon to Switch Agents](../../static/rds-bot-portal-sidebar-icon.png)

> 💡 **Tip:** You can click this same sidebar icon anytime to switch between and view responses from other agents in the workflow (such as the **Access Revocation Agent** and **User Activity Analysis Agent**).

The **Grant** agent will provide you with temporary access credentials including:

- Temporary database username
- IAM policy for RDS IAM authentication
- VPC and security group details
- MySQL connection command with IAM token generation
- Access valid for: **2 minutes** (Mention 10 minutes if you need more time to configure CLI access)

> **Note:** In case the **Grant** agent's interface does not return the MySQL connection command, please access the command from the **Execution Results** of the **Access Granting Agent** present in the bot workspace.

![Access Credentials](../../static/sql_connect_command.png)

---

### 🟢 1.5: Connect to Database

> 🟢 **DBA Task:** Use AWS CloudShell to connect to the database with your temporary credentials.

1. Open **AWS CloudShell** from the AWS Console
2. Click **+ icon** → **Create VPC Environment**

   <img src="../../static/create_vpc.png" alt="CloudShell Launch" width="500"/>

3. Configure:
   - **Name:** `test-env`
   - **VPC:** Use VPC ID provided by Grant (Access Granting Agent)
   - **Security Group:** Use Security Group ID provided by Grant
   - **Subnet:** Select any available subnet

   ![VPC Environment Config](../../static/vpc_configuration.png)

4. Click **Create**
5. Copy and execute the MySQL connection command provided by Grant

   ![MySQL Connection](../../static/connect_mysql.png)

> **Note:** After successfully connecting to the database in CloudShell, you must return to the bot and end the session with the **Access Granting AI Agent**.
> 1. Click the **red power button** on the left of the prompt box.
> 2. Click **End Session**.

---

### 🟢 1.6: Perform Database Operations

> 🟢 **DBA, DevOps, Developer Task:** Execute your authorized queries to investigate the payment issues.

Execute authorized queries:

> **Important:** Before running any queries, make sure to select the database by running:

```sql
USE workshop_db;
```

```sql
-- Investigate failed transactions
SELECT transaction_id, payment_id, customer_account_id, amount,
       currency, status, error_code, created_at
FROM payment_transactions
WHERE status = 'FAILED'
  AND created_at >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
ORDER BY created_at DESC;

-- Analyze duplicate payment IDs
SELECT payment_id, COUNT(*) as occurrence_count, SUM(amount) as total_amount
FROM payment_transactions
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
GROUP BY payment_id
HAVING COUNT(*) > 1
ORDER BY occurrence_count DESC;
```

> **Tip:** If you still have access time remaining, verify the query results by running a simple `SELECT * FROM payment_transactions;` to review the data structure and confirm the information is accurate.

---

### 🟢 1.7: Automatic Access Revocation

> 🟢 **DBA Observation:** After 10 minutes, your access will be automatically revoked.

After 10 minutes, **Rev** (revocation agent) automatically:

<img src="../../static/revocation_agent.png" alt="Access Revocation" width="400"/>

- Removes the IAM policy
- Deletes the temporary database user
- Archives CloudWatch logs for compliance

**Verification:** Attempting to reconnect will result in:

```text
ERROR 1045 (28000): Access denied
```

---

### 🔴 1.8: Activity Analysis

> 🔴 **SECURITY ADMIN PERSONA**
>
> Switch to your **Security Admin** role. You'll now review the AI-generated activity analysis for Alice's database session.

**Ana** (analysis agent) reviews the session and generates a report:

<img src="../../static/activity_analysing.png" alt="Activity Analysis" width="400"/>

**Analysis Result:**

```text
✅ All activities matched the stated access purpose
✅ No unauthorized actions detected
✅ Read-only operations only
✅ Access revoked successfully
```

You will receive an email with the complete activity report.

---

## Step 2: Test High-Risk Access Request (Manual Approval)

This scenario demonstrates manual approval for high-risk access requests.

**Scenario:**
- **User:** Bob (Database Administrator)  
- **Location:** London (using commercial VPN)  
- **Task:** Update payment gateway timeout configuration  
- **Risk Level:** High  
- **Expected Outcome:** Manual approval required

---

### 🟢 2.1: Initiate High-Risk Request

> 🟢 **DBA PERSONA**
>
> You are now **Bob**, a Database Administrator working remotely from London. Your corporate VPN is down, so you're using a commercial VPN. You need emergency access to fix critical payment gateway issues.

Follow the same validation process with these details:

1. **IP Address:** Use high-risk IP: `80.94.92.171`
   - Expected: `⚠️ IP ADDRESS FLAGGED - Risk Score: 87/100`

2. **Explanation:** Provide context

   Use the explanation given below:
   ```text
   I'm in London for an emergency client escalation. Corporate VPN is down, using a commercial VPN for secure connectivity while resolving critical payment gateway issues.
   ```
   ![High-Risk IP](../../static/high_risk_ip_reason.png)

3. **IAM Role:** `WSParticipantRole`
4. **RDS Instance:** `cfn-jit-rds-access-writer`
5. **Schema:** `workshop_db`
6. **Reason:**
   ```text
   Need to update payment gateway timeout configuration to resolve production transaction failures. 127 transactions timing out per hour. Manager approval: Sarah Chen, VP Engineering. Change request: CHG-2024-8821.
   ```
7. **Duration:** `10 minutes`

---

### 🟢 2.2: Risk Evaluation

> 🟢 **DBA Observation:** Watch as the AI evaluates your request and determines it requires manual approval.

**Eva** calculates:

**Risk Factors:**
- IP Reputation: High-risk commercial VPN (87/100)
- Geographic Location: Unusual (London)
- Database Schema: Production payment system
- Impact Scope: Business-critical

**Risk Score:** 84/100 → **VERY HIGH RISK**  
**Decision:** ⚠️ **REQUIRES MANUAL APPROVAL**

---

### 🔴 2.3: Security Operations Review

> 🔴 **SECURITY ADMIN PERSONA**
>
> Switch to your **Security Admin** role. You've received an approval request for Bob's high-risk database access. Review the request details and make an approval decision.

1. Check your approver email inbox
2. Review the approval request details
3. Verify:
   - User employment status and role
   - Business justification
   - Manager confirmation (Sarah Chen approved CHG-2024-8821)
   - Change request validity
4. Open the approval interface from email or platform

   ![Approval Interface](../../static/manual_approval.png)

5. Click **Take Action**
6. Select the flagged resource
7. Enter approval message and submit

   ![Submit Approval](../../static/user_approved.png)

---

### 🟢 2.4: Receive Conditional Access

> 🟢 **DBA PERSONA**
>
> Switch back to your **DBA** role as Bob. Your access request has been approved by the Security Admin.

After approval, **Grant** provisions access with **enhanced monitoring**:
- All queries receive additional logging
- Real-time anomaly detection enabled
- Payment system changes audited immediately

---

### 🟢 2.5: Perform Authorized Work

> 🟢 **DBA Task:** Connect to the database and perform your authorized configuration changes.

Connect to database and execute authorized changes:

> **Important:** Before running any queries, make sure to select the database by running:

```sql
USE workshop_db;
```

```sql
-- Review current configuration
SELECT gateway_name, timeout_seconds, retry_attempts, 
       last_modified, modified_by
FROM payment_gateway_config
WHERE gateway_name = 'PRIMARY_PROCESSOR';

-- Update timeout configuration
UPDATE payment_gateway_config
SET timeout_seconds = 30,
    retry_attempts = 5,
    last_modified = NOW(),
    modified_by = 'bob_emergency_change_CHG-2024-8821'
WHERE gateway_name = 'PRIMARY_PROCESSOR';

-- Verify changes
SELECT gateway_name, timeout_seconds, retry_attempts, 
       last_modified, modified_by
FROM payment_gateway_config
WHERE gateway_name = 'PRIMARY_PROCESSOR';
```

---

### 🟢 2.6: (Optional) Test Unauthorized Activity Detection

> 🟢 **DBA Task (Optional):** Test the system's ability to detect unauthorized activities by running queries outside your stated purpose.

To demonstrate monitoring capabilities, execute these queries:

```sql
-- Attempt 1: Unauthorized customer account access
SELECT customer_account_id, account_holder_name,
    account_balance, credit_limit
FROM customer_accounts
WHERE account_balance > 1000000
ORDER BY account_balance DESC LIMIT 20;

-- Attempt 2: Unauthorized payment data access
SELECT transaction_id, customer_account_id,
    card_number_last4, amount, merchant_name
FROM payment_transactions
WHERE amount > 50000
AND created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
ORDER BY amount DESC;
```

These queries will execute but be logged as **highly suspicious** and **unauthorized**.

**Advanced Tip:** If you still have access time remaining, explore additional unauthorized activities to test the monitoring system:

> ```sql
> -- Discover all tables in the database
> SHOW TABLES;
>
> -- Attempt unauthorized table modification (will be blocked or logged)
> DROP TABLE payment_transactions;
>
> -- Attempt unauthorized data updates
> UPDATE customer_accounts SET account_balance = 0 WHERE customer_account_id = 1;
> ```

> These actions will be flagged as **critical security violations** and demonstrate the system's ability to detect malicious behavior.

---

### 🔴 2.7: Review Enhanced Activity Analysis

> 🔴 **SECURITY ADMIN PERSONA**
>
> Switch to your **Security Admin** role. Review the AI-generated activity analysis for Bob's session, which includes detection of unauthorized activities.

**Ana** performs detailed analysis:

**Authorized Activities:**
- Configuration review: Authorized
- Timeout adjustment per CHG-2024-8821: Authorized
- Change verification: Authorized

**Unauthorized Activities Detected:**
- **HIGH SEVERITY:** Customer account enumeration (20 accounts, $47.3M exposed)
- **HIGH SEVERITY:** Payment data exfiltration attempt (43 transactions, $4.2M)

**Analysis Result:**
```text
⚠️ CRITICAL SECURITY ALERT

User completed authorized work but attempted unauthorized access patterns.

IMMEDIATE ACTIONS TAKEN:
✅ Access automatically revoked
✅ All unauthorized queries logged
✅ Manager notified
✅ Compliance team alerted

RECOMMENDED FOLLOW-UP:
1. Conduct security interview
2. Review 90-day access history
3. Mandatory security training
4. Consider access suspension pending investigation
```

You will receive a detailed security alert email with complete session timeline and forensics.

---

## Key Takeaways

By completing this module, you have learned:

1. **AI-Driven Access Management**: How AI agents automate the complete lifecycle of database access — from validation to revocation
2. **Risk-Based Decision Making**: How the Evaluation Agent (Eva) assesses risk factors to determine automatic vs. manual approval paths
3. **Zero Standing Privileges**: The principle of granting temporary, time-limited access instead of permanent credentials
4. **Intelligent Monitoring**: How the Analysis Agent (Ana) reviews database activity and detects unauthorized behavior in real time
5. **Insider Threat Detection**: The system's ability to identify data exfiltration attempts even during legitimate access sessions
6. **Automated Compliance**: How complete audit trails are generated automatically for compliance and incident response

---

## Summary

In this module, you experienced a complete Just-in-Time database access workflow powered by AI agents:

**Configuration Phase (🔴 Security Admin):**
- Imported the JIT access bot from the autobotAI library
- Configured five specialized AI agents using Amazon Bedrock
- Set up integrations for IP validation, AWS services, and email notifications

**Testing Phase (🟢 DBA + 🔴 Security Admin):**
- 🟢 Tested automatic approval for low-risk access requests with immediate credential provisioning
- 🟢 Tested manual approval for high-risk requests with enhanced monitoring
- 🔴 Reviewed and approved high-risk access requests
- 🟢 Observed automatic access revocation after time expiration
- 🔴 Reviewed AI-generated activity analysis and security reports

**Key Security Benefits:**

| Benefit | Description |
|---------|-------------|
| **Zero Standing Privileges** | No permanent database credentials exist |
| **Automated Risk Assessment** | Every request evaluated against multiple threat indicators |
| **Real-Time Monitoring** | Unauthorized activities detected and logged immediately |
| **Complete Audit Trail** | Full forensics available for compliance and investigation |
| **Frictionless Security** | Legitimate work proceeds quickly while maintaining strong security controls |
| **Insider Threat Detection** | Data exfiltration attempts identified even during legitimate sessions |

The high-risk scenario with unauthorized activity detection demonstrates how the system protects against insider threats while still enabling legitimate emergency access — providing both security and operational flexibility.

> **Workshop Tip**: The JIT access approach eliminates the need for standing database privileges while maintaining complete visibility into all database activities, making it ideal for organizations with strict compliance requirements.

---

## ✅ Success Criteria

You've completed this section when:

| Task | Persona | Status |
|------|---------|--------|
| Low-risk access request completed with automatic approval | 🟢 DBA | ☐ |
| Successfully connected to database via CloudShell | 🟢 DBA | ☐ |
| Executed sample queries successfully | 🟢 DBA | ☐ |
| Access automatically revoked after 10 minutes | 🟢 DBA | ☐ |
| Received activity analysis email | 🔴 Security Admin | ☐ |
| High-risk access request initiated | 🟢 DBA | ☐ |
| Reviewed and approved high-risk request | 🔴 Security Admin | ☐ |
| Completed authorized work after approval | 🟢 DBA | ☐ |
| Observed unauthorized activity detection in analysis report | 🔴 Security Admin | ☐ |

---

## Troubleshooting

### Issue: CloudShell VPC environment creation fails
**Solution:**
1. Ensure you're using the correct VPC ID from CloudFormation outputs
2. Select a subnet that has internet access (public subnet)
3. Try a different availability zone if the first fails

### Issue: MySQL connection command fails
**Solution:**
1. Verify the database endpoint is correct
2. Ensure the temporary user was created (check Grant agent response)
3. Wait 30 seconds and try again (IAM auth token may need time)

### Issue: Access not revoked after time expires
**Solution:** The revocation happens automatically. Check the chat interface for Rev agent's confirmation message.

### Issue: Approval email not received
**Solution:**
1. Check spam folder
2. Verify SES email identity is verified
3. Check the notification node configuration

---

**Next Steps**: Proceed to Module 4 for Threat Mitigation and Incident Response with GuardDuty and autobotAI.
