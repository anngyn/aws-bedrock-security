---
title: "Module 3: Agentic Database Access Management (DAM) with Just-in-time Access"
weight: 04
---

> ⚠️ **Region Reminder:** All AWS resources for this module are pre-deployed in **us-west-2 (Oregon)**.

**Estimated Time:** 60 minutes

## Overview

This module demonstrates how to implement Just-in-Time (JIT) database access management using agentic AI capabilities powered by **Amazon Bedrock**. You'll experience how AI agents can automate the entire lifecycle of temporary database access — from request validation to credential provisioning to automatic revocation — eliminating the security risks of standing database privileges.

---

## The Agentic SecOps Transformation

Before Agentic SecOps, managing database access required static credentials, shared passwords, or manual ticket approval workflows that created standing privileges and insider risk. With **autobotAI Agentic SecOps**, five specialized AI agents dynamically validate requests, evaluate risk scores, provision temporary credentials, monitor real-time queries, and automatically revoke access when sessions end.

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
        <p><strong>Standing Privileges & Static Keys</strong></p>
        <p>Engineers hold permanent database credentials with unmonitored access and delayed revocation.</p>
        <ul>
          <li>High risk of credential leaks & insider misuse</li>
          <li>Manual ticket bottlenecks for temporary access</li>
          <li>Lack of query-level audit visibility</li>
        </ul>
      </td>
      <td style="padding: 15px; vertical-align: top; border: 1px solid #e9ecef; background-color: #f5fff5;">
        <p><strong>1) Zero Standing Privileges (JIT Access)</strong></p>
        <p>Temporary database credentials created dynamically for valid windows and revoked automatically upon expiration.</p>
        <br />
        <p><strong>2) 5-Agent Autonomous Orchestration Thread</strong></p>
        <p>AI agents validate identity, assess risk scores, route high-risk approvals, and audit query execution in real time.</p>
      </td>
    </tr>
  </tbody>
</table>

---

## Personas in This Module

In this module, you will play **two different roles** to experience the complete JIT database access workflow from both perspectives. As a single participant, you'll switch between these personas at different stages of the module.

<table style="width:100%; border-collapse: collapse; margin: 20px 0;">
<tr>
<td style="width:50%; padding: 20px; vertical-align: top; border: 3px solid #dc3545; border-radius: 8px; background-color: #fff5f5;">

<h3>🔴 Security Admin</h3>

**Role:** Platform Security Administrator

**Responsibilities:**
- Import and configure the JIT access bot
- Set up AI models and integrations
- Configure notification workflows
- Review and approve high-risk access requests
- Monitor security alerts and compliance reports

**You'll see this callout:**

> 🔴 **SECURITY ADMIN PERSONA**
>
> *You are now acting as the Security Administrator...*

</td>
<td style="width:50%; padding: 20px; vertical-align: top; border: 3px solid #28a745; border-radius: 8px; background-color: #f5fff5;">

<h3>🟢 Database Administrator (DBA)</h3>

**Role:** Database Administrator / Data Engineer

**Responsibilities:**
- Request temporary database access
- Provide identity validation information
- Connect to databases and execute queries
- Perform authorized database operations
- Complete assigned tasks within access window

**You'll see this callout:**

> 🟢 **DBA PERSONA**
>
> *You are now acting as the Database Administrator...*

</td>
</tr>
</table>

### Understanding Persona Callouts

Throughout this module, colored callout boxes indicate which persona you should assume:

| Indicator | Persona | Action |
|-----------|---------|--------|
| 🔴 **Red callouts** | Security Admin | Configure systems, approve requests, review security alerts |
| 🟢 **Green callouts** | DBA | Request access, connect to databases, run queries |

> 💡 **Tip:** Think of this as a role-playing exercise. When you switch personas, imagine you're a different person with different access levels and responsibilities. This helps you understand how the JIT access system works from multiple perspectives in a real organization.

---

## What You'll Learn

By the end of this module, you will be able to:

- Understand the security risks of traditional database access management
- Experience AI-driven access request validation and risk assessment
- Test automated credential provisioning with time-limited access
- Observe automatic access revocation after the designated time period
- Review AI-generated activity analysis and compliance reports

## Use Cases and AI Agents Architecture

### The Problem

Manual database access management creates security risks:
- **Forgotten credentials** — Access granted for temporary tasks remains active indefinitely
- **Over-privileged access** — Users retain permissions long after tasks complete
- **Delayed threat detection** — Unauthorized activity discovered only during audits
- **Manual log analysis** — Security teams spend weeks reviewing CloudWatch logs
- **Insider threats** — Malicious activity goes undetected during legitimate sessions

### AI Agents Architecture

The bot uses five specialized AI agents:

1. **Validation Agent (Val)** — Verifies user identity, IP reputation, and access requirements
2. **Evaluation Agent (Eva)** — Assesses risk and determines approval path (automatic vs. manual)
3. **Grant Agent** — Provisions temporary credentials with precise permissions
4. **Revocation Agent (Rev)** — Automatically removes access after the designated time period
5. **Analysis Agent (Ana)** — Reviews user activity and generates compliance reports

## Module Structure

This module is divided into the following sections:

### 3.1 Importing and Configuring the Workflow

🔴 **Persona: Security Admin**

Import and configure the JIT access bot:

- Import the bot from the autobotAI library
- Configure AI models for all agent nodes
- Set up third-party integrations (AbuseIPDB, AWS)
- Configure email notifications for approvals

### 3.2 Testing the JIT Access Workflow

🔴🟢 **Personas: Both (you'll switch between roles)**

Experience the JIT access workflow through two scenarios:

| Step | Persona | Activity |
|------|---------|----------|
| Low-risk request | 🟢 DBA | Request access, validate identity, receive auto-approval |
| Database work | 🟢 DBA | Connect to database, execute queries |
| High-risk request | 🟢 DBA | Request access with flagged IP, await approval |
| Approval review | 🔴 Security Admin | Review request, approve access |
| Complete work | 🟢 DBA | Connect, perform authorized work, test detection |
| Review analysis | 🔴 Security Admin | Review AI-generated security reports |

## Architecture Overview

The JIT database access architecture includes:

1. **Request Layer**:
   - Chat interface for access requests
   - Natural language processing to understand user needs
   - Initial parameter collection (database, duration, reason)

2. **AI Analysis Layer (Powered by Amazon Bedrock)**:
   - Validation Agent verifies user identity and checks IP reputation via AbuseIPDB
   - Evaluation Agent assesses risk level using Bedrock's foundation models
   - Intelligent decision-making on approval path (automatic vs. manual)

3. **Provisioning Layer**:
   - Grant Agent creates temporary database credentials
   - Time-limited IAM policies with precise permissions
   - Secure credential delivery through chat interface

4. **Revocation Layer**:
   - Revocation Agent monitors access duration
   - Automatic credential removal after time period expires
   - Security group updates to remove network access

5. **Analysis Layer**:
   - Analysis Agent reviews CloudWatch logs for database activity
   - AI-generated reports on user actions during access window
   - Compliance summaries for audit purposes

6. **Audit Layer**:
   - Complete audit trail of all access requests
   - CloudWatch Logs for detailed activity monitoring
   - Integration with security team notifications

## Workflow Diagram

The following diagram illustrates the complete JIT database access request flow:

![Agentic Database Access Workflow](../static/jit-access-workflow.png)

## Key Benefits

- **Zero Standing Privileges**: No permanent database credentials exist
- **Automated Lifecycle**: Request → Validate → Provision → Revoke → Analyze
- **Risk-Based Approval**: AI determines appropriate approval workflow
- **Complete Visibility**: Every action is logged and analyzed
- **Compliance Ready**: Automated reports for audit requirements

---

## ✅ Module Success Criteria

By the end of this module, you should have:

| Task | Persona | Status |
|------|---------|--------|
| JIT access bot imported and configured | 🔴 Security Admin | ☐ |
| Successfully tested low-risk automatic approval workflow | 🟢 DBA | ☐ |
| Successfully tested high-risk manual approval workflow | 🟢 DBA | ☐ |
| Reviewed and approved high-risk access request | 🔴 Security Admin | ☐ |
| Received email notifications for access events | Both | ☐ |
| Observed automatic access revocation after time expiration | 🟢 DBA | ☐ |
| Reviewed AI-generated activity analysis report | 🔴 Security Admin | ☐ |
