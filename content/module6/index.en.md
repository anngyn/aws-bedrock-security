---
title: "Module 6: AppSec Workflow for SCA, IaC and SAST Remediation → Developer Feedback → Follow-up with Escalation → Risk Register"
weight: 07
---

> ⚠️ **Region Reminder:** Amazon Inspector Code Security should be enabled in **us-west-2 (Oregon)**.

**Estimated Time:** 45 minutes

## Overview: The Limbo of Automated PRs & WAF Shielding

In today's world, there are lots of agents that can fetch security findings, apply remediations, and send them for review by generating Pull Requests (PRs). But what happens if the reviewer doesn't actually review it?

Often, there's no one to follow up on the workflows. The bot just remediates and generates a PR, which then exists in limbo—neither fixed in production nor reviewed by a human. The vulnerability remains active.

Moreover, during the time the PR is open (or if a developer decides to postpone the remediation for later), the application remains exposed to attacks. 

**autobotAI Agentic SecOps** solves this by enforcing review SLAs and **automatically deploying WAF shielding rules** to protect the application while it's in review or if the remediation is deferred.

---

## The Agentic SecOps Transformation

Before Agentic SecOps, automated code scanning tools generated Pull Requests (PRs) that lingered in review limbo indefinitely without developer follow-up or manager visibility. With **autobotAI Agentic SecOps**, code vulnerabilities detected by Amazon Inspector trigger scheduled Scanner bots and long-running Resolver bots that generate inline PR security annotations, enforce review SLAs, and automatically log unaddressed items into a Risk Register.

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
        <p><strong>Cluttered Code Vulnerability Findings</strong></p>
        <p>Unresolved code security findings sitting idle without automated reviewer tracking or escalation.</p>
        <img src="../static/inspector-findings-before-remediation.png" alt="Before Agentic SecOps - Cluttered Inspector Findings" style="width:100%; border-radius: 6px; margin-top: 10px;" />
      </td>
      <td style="padding: 15px; vertical-align: top; border: 1px solid #e9ecef; background-color: #f5fff5;">
        <p><strong>1) Remediated Finding Status</strong></p>
        <img src="../static/inspector-findings-after-remediation.png" alt="After Agentic SecOps - Remediated Inspector Finding" style="width:100%; border-radius: 6px; margin-bottom: 15px;" />
        <p><strong>2) DeepAgent Autonomous Execution Thread</strong></p>
        <img src="../static/mod6-deepagent-execution.png" alt="After Agentic SecOps - DeepAgent Execution Thread" style="width:100%; border-radius: 6px;" />
      </td>
    </tr>
  </tbody>
</table>

---

This module will show you how to build a complete **AppSec Inspector Review Workflow** using autobotAI that solves this problem. You will learn:
- How **escalation** is created to ensure action.
- How the bot makes the reviewer follow up by escalating things, even for old pending PRs.
- How the bot **watches the PR** for review during the open window time.
- How the bot **registers tasks with ownership** to track accountability.
- How the bot handles risk acceptance by registering exceptions into a **Risk Register**.

## What You'll Build

You will create a robust 2-bot architecture:
1. **Scanner Bot (Scheduled):** Fetches new code vulnerabilities from Amazon Inspector, records them as tracked tasks, and fires a batch event.
2. **Resolver Bot (Listener):** A long-running agent that processes the batch, generates ONE PR for all findings, posts inline security annotations, enters an intelligent wait loop to enforce SLAs, and automatically deploys WAF shielding rules if a finding is postponed or remains unmerged at the SLA deadline.

---

## Module Sections

### 6.1 Configuring Amazon Inspector for Code Security
Set up Amazon Inspector Code Security and connect it to your GitHub repository:
- Fork the sample vulnerable application
- Enable Code Security in Amazon Inspector
- Connect Amazon Inspector with your GitHub repository

### 6.2 Building the AppSec Inspector Bots
Build the Inspector workflow using Optimus:
- Create the Scanner and Resolver skills
- Configure the Scanner bot with Inspector filters
- Configure the Resolver bot for PR creation and escalation tracking

### 6.3 Running the Workflow and Managing Escalations
Execute the workflow and explore the lifecycle:
- Trigger the Scanner and watch the Resolver generate a PR
- Review inline annotations and automated emails
- Observe the wait loop and SLA escalation
- Track tasks in the dashboard and manage exceptions in the Risk Register

### 6.4 (Bonus) Importing from Library: Pre-built Inspector Workflow
As an alternative to building the bots with Optimus, you can import the pre-built workflow manually:
- Import the AppSec Inspector bot from the public library
- Configure AWS and Amazon Bedrock integrations
- Set up AI agent parameters and notifications
- Run the bot and review AI-generated pull requests

---

**Ready to begin?** Start with [Module 6.1: Configuring Amazon Inspector for Code Security](6.1/)

---

## ✅ Module Success Criteria

By the end of this module, you should have:
- [ ] Connected your GitHub repository to Amazon Inspector
- [ ] Built the Scanner and Resolver bots
- [ ] Received an automated PR with inline security annotations
- [ ] Experienced the automated email escalations for pending PRs
- [ ] Observed the automated creation of WAF shielding rules
- [ ] Viewed tracked tasks and risk exceptions in the dashboard
