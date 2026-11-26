---
title: "4.2 Automated Remediation with Federated Risk Owner Human-in-the-Loop Approval"
weight: 02
---

> ⚠️ **Region Reminder:** Configure GuardDuty node to use **us-west-2 (Oregon)**.

**Estimated Time:** 25 minutes

## Bot Overview

This bot leverages **autobotAI's agentic capabilities** to automate the **analysis, decision-making, and remediation** of **Amazon GuardDuty findings** across **RDS** and **EC2** security incidents.  

By combining AI-driven intelligence with AWS-native tools, it identifies real threats, validates attacker IPs, executes mitigation actions, and performs automated incident response — enabling **end-to-end autonomous protection** for both database and compute layers.

---

## Covered Findings

This combined module includes findings related to **RDS** and **EC2** threats:

### **RDS-Related Findings**
- **IAM Medium** - `Recon:IAMUser/MaliciousIPCaller.Custom`
  - *Description:* An IAM user is making API calls from a known malicious IP address.  
  - *Automated Action:* The AI agent validates the IP using AbuseIPDB and determines appropriate response actions.
- **RDS Medium** - `CredentialAccess:RDS/TorIPCaller.FailedLogin`
  - *Description:* A Tor exit node attempted failed logins to the RDS database.  
  - *Automated Action:* Retrieves RDS security group rules and tightens them if `0.0.0.0/0` access is found.
- **RDS Medium** - `Discovery:RDS/TorIPCaller`
  - *Description:* A Tor exit node is performing reconnaissance against RDS.  
  - *Automated Action:* Identifies and restricts overly permissive RDS security groups.

### **EC2-Related Findings**
- **EC2** - `UnauthorizedAccess:EC2/SSHBruteForce`
  - *Description:* SSH brute force attack detected on EC2.  
  - *Automated Action:* Validates the attacking IP via AbuseIPDB, blocks it, and isolates the instance if required.
- **EC2** - `Backdoor:EC2/C&CActivity.B!DNS` (Tor Client Detection)
  - *Description:* EC2 instance communicating with Tor network.  
  - *Automated Action:* Isolates instance, modifies SGs, captures forensic data.
- **EC2** - `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.OutsideAWS`
  - *Description:* Compromised IAM credentials used from outside AWS.  
  - *Automated Action:* Rotates IAM credentials, isolates EC2 instance, and sends notification.

---

## Importing and Running Workflow

> **Note:** The bot will run for approximately **10-15 minutes**. You can monitor the progress in the execution logs or via the chat interface during the session.

### Step 1: Import the Bot from Library
1. Visit the [autobotAI Library](https://autobot.live/app#/library).  
2. Search for **"agentic"**.  
3. Select the bot **"Agentic Remediation for GuardDuty Findings"** and click **Import**.  

---

### Step 2: Configure "Agent" Node
1. Under **Integration**, choose:
   - **Integration Type:** `Amazon Bedrock`
   - **Integration Account:** Amazon Bedrock integration added earlier.

![Configure AI Agent Integration](../../static/module4/gd-w-2.png)

2. Under **AI**, select **global.anthropic.claude-sonnet-4-6**.  

---

### Step 3: Configure "AI Notification" Node
> **Note:** You must have configured Amazon SES notifications as per Module 1.3.

1. **Recipients:** Select **Events** from the top-right corner of the field, then manually enter the personal email address you verified in SES and press **Enter**.
2. **Service:** `AWS SES`  
3. **Connection:** Your Amazon SES integration.

![Configure AI Notification Node](../../static/module4/ins-w-4.png)

---

### Step 4: Save and Run the Bot
1. Click **Save** to apply configuration changes.  
2. Click **Run** to execute the combined RDS + EC2 response bot.

---

### Step 5: Review Execution Results
1. Once complete, you will receive a notification via **Slack** or **Amazon SES** summarizing the actions taken:
   - RDS remediation details  
   - EC2 isolation and incident response summary  

![AI Notification for GuardDuty Findings](../../static/module4/gd-notify.png)

![Remediation Details](../../static/module4/gd-rem-2.png)

![Agent View](../../static/mod4-agent-view.png)

---

## How the AI Agent Works

### Intelligent Decision-Making Process

The autobotAI agent follows a sophisticated decision-making workflow:

1. **Finding Analysis**
   - Receives GuardDuty findings from the List GuardDuty Findings node
   - Parses finding type, severity, and affected resources
   - Extracts key indicators (IP addresses, instance IDs, IAM roles)

2. **Threat Validation**
   - Uses AbuseIPDB integration to validate suspicious IP addresses
   - Checks IP reputation scores and abuse confidence levels
   - Determines if the threat is legitimate or a false positive

3. **Context Assessment**
   - Analyzes the affected resource configuration
   - Reviews security group rules and network access patterns
   - Evaluates IAM permissions and credential usage

4. **Response Decision**
   - Determines appropriate mitigation actions based on:
     - Finding severity level
     - Threat validation results
     - Resource criticality
     - Organizational policies
   - Selects graduated response (block, isolate, rotate credentials)

5. **Action Execution**
   - Executes remediation actions through AWS APIs
   - Modifies security groups to block malicious IPs
   - Isolates compromised instances
   - Rotates compromised credentials
   - Captures forensic evidence

6. **Notification and Reporting**
   - Generates detailed incident summary
   - Sends notifications via Amazon SES or Slack
   - Provides actionable insights and recommendations
   - Maintains audit trail of all actions

---

## Remediation Actions by Finding Type

### RDS-Related Findings

#### IAM Reconnaissance from Malicious IP
**Finding:** `Recon:IAMUser/MaliciousIPCaller.Custom`

**AI Agent Actions:**
1. Validates IP address using AbuseIPDB
2. If confirmed malicious (abuse confidence > 75%):
   - Implements IAM scope reduction for affected user/role
   - Blocks IP at network level if possible
   - Generates detailed threat intelligence report
3. Sends notification with validation results and actions taken

#### RDS Tor Access Attempts
**Finding:** `CredentialAccess:RDS/TorIPCaller.FailedLogin` or `Discovery:RDS/TorIPCaller`

**AI Agent Actions:**
1. Retrieves RDS instance security group configuration
2. Identifies overly permissive rules (0.0.0.0/0 access)
3. If found:
   - Modifies security group to restrict access to known good IPs
   - Implements least-privilege network access
   - Documents changes in audit log
4. Sends notification with security group modifications

### EC2-Related Findings

#### SSH Brute Force Attack
**Finding:** `UnauthorizedAccess:EC2/SSHBruteForce`

**AI Agent Actions:**
1. Validates attacking IP using AbuseIPDB
2. If confirmed malicious:
   - Creates or updates security group rule to block attacking IP
   - Applies blocking rule to affected instance
   - Captures VPC Flow Logs for forensic analysis
3. If attack persists from multiple IPs:
   - Considers instance isolation
   - Recommends additional hardening measures
4. Sends notification with attack details and mitigation status

#### Tor Client Detection
**Finding:** `Backdoor:EC2/C&CActivity.B!DNS` or `UnauthorizedAccess:EC2/TorClient`

**AI Agent Actions:**
1. Immediately isolates affected instance:
   - Modifies security groups to block all outbound traffic except to AWS services
   - Preserves instance state for forensic analysis
2. Captures forensic evidence:
   - Takes EBS snapshot of instance volumes
   - Collects VPC Flow Logs
   - Documents network connections
3. Sends high-priority notification with:
   - Tor connection details
   - Isolation status
   - Forensic evidence locations
   - Recommended next steps

#### Instance Credential Exfiltration
**Finding:** `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.OutsideAWS`

**AI Agent Actions:**
1. **Immediate Credential Rotation:**
   - Identifies compromised IAM role
   - Initiates credential rotation process
   - Invalidates existing temporary credentials
2. **Instance Isolation:**
   - Modifies security groups to prevent further external access
   - Blocks outbound connections to suspicious IPs
3. **Forensic Collection:**
   - Captures instance metadata access logs
   - Documents API calls made with stolen credentials
   - Identifies potentially accessed resources
4. **Comprehensive Notification:**
   - Details credential theft timeline
   - Lists actions taken with stolen credentials
   - Provides remediation status
   - Recommends security improvements

---

## Benefits of Agentic Automation

### Speed and Efficiency
- **Response Time:** Reduces incident response from hours to minutes
- **24/7 Coverage:** Continuous monitoring and response without human intervention
- **Consistency:** Applies security policies uniformly across all findings

### Intelligence and Accuracy
- **Threat Validation:** Reduces false positives through external intelligence
- **Context-Aware:** Makes decisions based on full threat context
- **Adaptive:** Learns from patterns and adjusts responses accordingly

### Comprehensive Protection
- **Multi-Layer Defense:** Addresses threats across RDS, EC2, and IAM
- **Graduated Response:** Applies appropriate level of mitigation based on severity
- **Evidence Preservation:** Maintains forensic data for investigation

### Operational Excellence
- **Audit Trail:** Complete documentation of all actions
- **Compliance:** Ensures consistent application of security policies
- **Team Enablement:** Frees security teams to focus on strategic initiatives

---

## Monitoring and Validation

### Verifying Remediation Success

After the bot executes, verify the remediation actions:

1. **Check GuardDuty Findings:**
   - Navigate to GuardDuty console
   - Verify that similar findings have stopped appearing
   - Review finding status (archived or resolved)

2. **Review Security Group Changes:**
   - Navigate to EC2 > Security Groups
   - Verify that blocking rules have been applied
   - Confirm that malicious IPs are blocked

3. **Validate IAM Changes:**
   - Navigate to IAM console
   - Verify credential rotation for affected roles
   - Confirm scope reduction policies are in place

4. **Review Notifications:**
   - Check email or Slack for detailed incident reports
   - Review AI agent's decision-making process
   - Verify all actions were completed successfully

### Continuous Improvement

Use the bot's execution history to improve security posture:

1. **Analyze Patterns:**
   - Identify frequently targeted resources
   - Recognize common attack vectors
   - Detect security configuration weaknesses

2. **Refine Policies:**
   - Adjust security group rules based on findings
   - Update IAM policies to follow least privilege
   - Implement additional preventive controls

3. **Optimize Response:**
   - Fine-tune AI agent decision thresholds
   - Adjust notification preferences
   - Customize remediation actions for specific scenarios

---

## Best Practices

### Configuration
1. **Test in Non-Production:** Validate bot behavior in test environment first
2. **Start Conservative:** Begin with less aggressive remediation actions
3. **Monitor Closely:** Review bot actions regularly during initial deployment
4. **Document Policies:** Clearly define organizational security policies

### Operations
1. **Regular Reviews:** Periodically review bot execution logs
2. **Update Integrations:** Keep AWS and AbuseIPDB integrations current
3. **Refine Rules:** Adjust remediation logic based on operational experience
4. **Team Training:** Ensure security team understands bot capabilities

### Security
1. **Least Privilege:** Grant bot only necessary AWS permissions
2. **Audit Logging:** Enable comprehensive logging of all bot actions
3. **Access Control:** Restrict who can modify bot configuration
4. **Backup Plans:** Maintain manual response procedures as backup

---

## Summary

In this section, you learned:

- ✅ How to import and configure the autobotAI agentic remediation bot
- ✅ The intelligent decision-making process used by the AI agent
- ✅ Specific remediation actions for each finding type
- ✅ How to verify and monitor automated remediation
- ✅ Best practices for operating agentic security automation

The combination of GuardDuty's threat detection and autobotAI's intelligent automation provides comprehensive, autonomous protection for your AWS infrastructure across RDS, EC2, and IAM layers.

---

## Next Steps

Now that you've completed Module 4, you have:
- Comprehensive understanding of GuardDuty threat detection across multiple AWS services
- Hands-on experience with AI-driven automated remediation
- Knowledge of best practices for securing RDS, EC2, and IAM resources

Continue to [Module 5: Agentic Remediation for Security Hub & Escalation](../../module5/) to explore additional security capabilities and advanced threat response scenarios.

---

## Additional Resources

- [autobotAI Documentation](https://autobot.live/docs)
- [Amazon GuardDuty Best Practices](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_best-practices.html)
- [AbuseIPDB API Documentation](https://docs.abuseipdb.com/)
- [AWS Security Best Practices](https://aws.amazon.com/architecture/security-identity-compliance/)

---

## ✅ Success Criteria

You've completed this section when:
- [ ] Bot imported from library successfully
- [ ] GuardDuty findings node configured with us-west-2
- [ ] AI Agent configured with Amazon Bedrock
- [ ] Agent tools configured with AWS and AbuseIPDB integrations
- [ ] Notification node configured with SES
- [ ] Bot executed successfully
- [ ] Received remediation notification email
- [ ] Verified security group changes in AWS console

---

## Troubleshooting

### Issue: Bot not finding GuardDuty findings
**Solution:**
1. Verify region is set to us-west-2
2. Check that GuardDuty has active findings
3. Ensure AWS integration has proper permissions

### Issue: Remediation actions not executing
**Solution:**
1. Check AI Agent node configuration
2. Verify AWS integration has necessary IAM permissions
3. Review execution logs for specific errors

### Issue: Notification not received
**Solution:**
1. Check SES email identity verification
2. Verify notification node configuration
3. Check spam folder
