---
title: "Module 2: WAF Log Analysis & Rule Building with Autonomous Orchestrator (Optimus)"
weight: 03
---

**Objective:** Use **Optimus**, autobotAI's agentic security orchestrator, to analyze AWS WAF logs, detect and classify live web attacks that are slipping through current configuration, and then build the WAF rules that remediate them, all from a single chat-driven ad-hoc workflow powered by Amazon Bedrock. Finally, deploy a bot that does the same at a defined interval — daily or hourly.

## Module Overview

This module starts the workshop's hands-on agentic security workflow by focusing on the **web application layer**: your AWS WAF. Later modules extend the same pattern to GuardDuty, Security Hub, and Amazon Inspector.

WAF logs are high-volume and noisy. Attackers deliberately spread activity across many IPs, encode payloads multiple times, and ride just under per-IP rate thresholds — so a human eyeballing the logs, or a single per-IP query, will miss coordinated campaigns. **Optimus** queries the logs through Amazon Athena across multiple analytical lenses (labels, fingerprints, subnets, payloads, cardinality, rate), groups what it finds into distinct threat campaigns, and then proposes and applies the exact WAF rule changes to stop them.

---

## The Agentic SecOps Transformation

Before Agentic SecOps, WAF log analysis required security engineers to manually write complex Athena queries over millions of high-volume logs, manually group attack IP patterns, and hand-craft JSON rule definitions. With **autobotAI Agentic SecOps**, Optimus autonomously queries WAF logs across multi-dimensional lenses, categorizes attack campaigns, generates evidence-backed threat reports, and translates findings into applied WAF rule remediations.

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
        <p><strong>No WAF Rules & Unnoticed Attacks</strong></p>
        <p>Before Agentic SecOps, there are no active WAF rules enforcing block mode. Multiple web attack campaigns (SQLi, XSS, bot scrapers) go completely unnoticed across unmonitored endpoints.</p>
        <img src="../static/mod2-before-secops.png" alt="Before Agentic SecOps - No WAF Rules & Unnoticed Attacks" style="width:100%; border-radius: 6px; margin-top: 10px;" />
      </td>
      <td style="padding: 15px; vertical-align: top; border: 1px solid #e9ecef; background-color: #f5fff5;">
        <p><strong>1) Created New WAF Rules & Prevented Attacks</strong></p>
        <p>Optimus automatically detects attack patterns, creates new WAF rules based on detected threats, and prevents multiple web attacks with 100% mitigation efficiency.</p>
        <img src="../static/mod2-after-secops.png" alt="After Agentic SecOps - Created New Rules Based on Detected Threats and Prevented Multiple Attacks" style="width:100%; border-radius: 6px; margin-top: 10px;" />
      </td>
    </tr>
  </tbody>
</table>

---

In this module, you will:

1. **Open Optimus** and set the default AI model to **Claude Opus 4.6**
2. **Launch the WAF Log Threat Analysis** template and let Optimus analyze the pre-loaded WAF logs in your workshop account
3. **Review the threat report** — distinct campaigns, evidence, and the benign baseline
4. **Build and apply the WAF rules** that remediate each confirmed attack, with you approving every mutation

By the end, you'll have hands-on experience driving an autonomous security analyst that turns raw WAF logs into an evidence-backed threat report **and** a concrete, applied remediation plan.

---

## What Optimus Does

**Optimus** is the conversational, agentic front-end of autobotAI. Unlike a fixed workflow bot, Optimus reasons about your request, picks the right tools from its toolkit, and runs them iteratively until the goal is met — asking for your approval before it changes anything.

For this module, Optimus is equipped with a **WAF Log Threat Analysis & Remediation** toolkit:

- **Log analytics (Athena):** create an external table over the WAF logs in S3, inspect the schema, and run SQL across the log window.
- **Discovery & inspection (read-only):** list Web ACLs, read a Web ACL's full config and rules, read logging configuration, sampled requests, CloudWatch metrics, and existing IP sets.
- **Response (mutations — only after your approval):** create/update IP sets, block IPs, and update the Web ACL to add rules or flip managed rules from COUNT to BLOCK.
- **Threat intelligence:** validate suspicious source IPs against AbuseIPDB.

---

## Detection Techniques Optimus Uses

A single signal is easy to evade, so Optimus pivots across many lenses:

- **Label-driven:** filter the managed-rule labels (`awswaf:managed:aws:*`) that fired — even when the rule was only in COUNT mode.
- **Fingerprint clustering:** group by User-Agent / header shape across many IPs to expose one distributed campaign.
- **Aggregate / session-volumetric:** count distinct source IPs hitting `/login` or `/signup` — the signature of credential stuffing and account-creation fraud.
- **Subnet clustering:** collapse IPs to their `/24` to catch proxy-subnet abuse.
- **Payload inspection:** decode `args`/`uri` (twice) to catch SQLi, XSS, and multi-encoded path traversal.
- **Cardinality scan:** one IP requesting many distinct URIs = scanner / web-shell discovery.
- **Rate-based:** inspect rate-based rule hits on money endpoints (checkout).
- **Signal vs noise:** profile the legitimate ALLOW baseline so safe traffic is never blocked.

---

## Prerequisites

Before starting this module, ensure you have:

- ✅ Completed **Module 1** — your **AWS**, **Amazon Bedrock**, and **Amazon Athena** integrations are **Active**
- ✅ (Optional) **AbuseIPDB** integration configured (Module 1.3) for IP reputation checks
- ✅ The workshop AWS account, which is **pre-loaded with AWS WAF v2 logs** (benign baseline traffic plus several live attack campaigns) in `us-west-2`

---

## Module Sections

### 2.1 Configuring Optimus & Running WAF Log Analysis
Open Optimus, set the default model to Claude Opus 4.6, launch the WAF Log Threat Analysis template, and review the threat report Optimus produces from the pre-loaded logs.

### 2.2 Building WAF Rules from the Threat Findings
Hand Optimus the remediation prompt and watch it translate each confirmed campaign into concrete WAF rule changes — flipping COUNT rules to BLOCK, building IP-set block rules, adding rate-based and bot-control rules — while you approve every change.

---

**Ready?** Start with [Module 2.1: Configuring Optimus & Running WAF Log Analysis](2.1/)
