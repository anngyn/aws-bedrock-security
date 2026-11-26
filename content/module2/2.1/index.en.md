---
title: "2.1 Configuring Optimus & Running WAF Log Analysis"
weight: 1
---

> ⚠️ **Region Reminder:** WAF log analysis and Athena queries use resources in **us-west-2 (Oregon)**.

**Estimated Time:** 20 minutes

**Objective:** Open Optimus, set the default AI model to **Claude Opus 4.6**, launch the **WAF Log Threat Analysis** template, and review the threat report Optimus produces from the WAF logs pre-loaded in your workshop account.

---

## Step 1: Open Optimus

1. From the autobotAI top navigation, click the **OPTIMUS** button to open the Optimus panel.
2. A new Optimus panel opens. The toolbar at the top lets you start a **new chat** (the **+** button), switch on **Fast Mode**, and open **Optimus settings** (the sliders icon).

![Open Optimus](../../static/optimus-header.png)

> **Tip:** If a **Community Edition Features** or subscription pop-up appears the first time, you can dismiss it — the workshop account already has the required plan.

---

## Step 2: Set the Default AI Model to Claude Opus 4.6

The default configuration applies to every new Optimus thread (you can still override it per-chat). We'll point Optimus at the most capable model for this analysis.

1. In the Optimus panel, click the **settings (sliders)** icon to open **Configure Optimus**.
2. Select the **AI Model** tab on the left.
3. Under **Provider & Integration → AI Provider**, choose **Anthropic**, then select **Claude Opus 4.6** as the model.

![Set the default AI model](../../static/mod2-provider-image.png)

4. Under **Model Parameters**, set the values for analysis:
   - **Temperature:** `0.7`
   - **Max Tokens:** `8192`
   - **Max Iterations:** toggle on **No limit**.

> **Important:** Turn **Max Iterations** to **No limit**. WAF log analysis is deeply iterative — Optimus runs many Athena queries and tool calls in a single run, and a capped iteration limit can cut the analysis short before it finishes classifying every campaign.

![Set the model parameters and enable No limit for Max Iterations](../../static/mod2-parameter-image.png)

5. (Optional) Open the **Knowledge** tab to confirm the supporting skills are attached (e.g. *Action Generation*, *Bot Creation Guide*). These help Optimus reason about the WAF tools.

![Optimus knowledge & skills](../../static/mod2-knowledge-image.png)

> **Note:** These settings are applied automatically to all new Optimus threads. The banner at the top of the settings reminds you that you can still override them per chat after starting.

---

## Step 3: Launch the WAF Log Threat Analysis Template

The new Optimus page shows a set of ready-made template boxes. The first box is **WAF Log Threat Analysis & Remediation** — it comes pre-loaded with the right system prompt, guardrails, and the full WAF + Athena toolkit, so you don't have to attach anything manually.

1. Start a **new Optimus chat** (the **+** button).
2. On the empty-state page, select the **WAF Log Threat Analysis & Remediation** box (the first box).

![Select the WAF Log Threat Analysis template](../../static/optimus-waf-template-box.png)

3. Selecting the box pre-fills the starter prompt. Provide the target details for the workshop Web ACL when asked:
   - **Web ACL name:** *(provided in your workshop environment)*
   - **Web ACL ID:** *(provided in your workshop environment)*
   - **Scope:** `REGIONAL`
   - **AWS Region:** `us-west-2`
   - **Time window to analyze:** *(e.g. the last 24 hours, or the window provided)*

> **Note:** Your workshop AWS account is **pre-provisioned** with AWS WAF v2 logs in S3 — a legitimate **benign baseline** mixed with several live **attack campaigns**. You do not need to generate any traffic; Optimus will find what's already there.

4. Send the message. Optimus begins working autonomously.

---

## Step 4: Watch Optimus Analyze the Logs

Optimus now runs its operating procedure end-to-end. You'll see it think and call tools in sequence:

1. **Orient** — lists the Web ACLs and reads the target Web ACL's config and rules (what's already in COUNT vs BLOCK).
2. **Locate logs** — reads the Web ACL's logging configuration to find the S3 destination, then creates/locates the Athena table over those logs and inspects the schema.
3. **Analyze** — runs a sweep of Athena SQL queries across the log window, pivoting across the detection lenses (labels, fingerprints, subnets, payloads, cardinality, rate).
4. **Classify** — groups findings into distinct threat campaigns with supporting evidence.

![Optimus running the WAF log analysis](../../static/optimus-waf-analysis.png)

> **Tip:** Optimus shows the **SQL it runs** for each finding so the results are reproducible. Expand the tool calls to follow exactly how each campaign was detected.

---

## Step 5: Review the Threat Report

When the analysis completes, Optimus returns a structured report:

- A one-paragraph **executive summary** (how many distinct campaigns, overall risk).
- One **section per campaign**, each with: threat class, severity, source IP(s)/country spread/`/24`, target endpoint + method, volume, the managed-rule label(s) or analytical pivot that detected it, an **evasion note**, sample payloads, the **current WAF action** (ALLOW/COUNT/BLOCK), and a **recommended remediation**.
- A clearly separated **benign baseline** so legitimate traffic is excluded from enforcement.
- A **prioritized remediation plan** — the ordered set of WAF changes (with the tool for each) — ending with a request for your authorization before any change is applied. Note that **no changes are applied** at this stage.

![Optimus WAF threat report and prioritized remediation plan](../../static/optimus-waf-report.png)

Typical campaigns Optimus surfaces in the workshop dataset include:

- **SQL injection** from a single source IP
- **Path traversal** (multi-encoded) from a single IP
- **Scanner / tool fingerprinting** hitting many distinct URIs
- **Account-creation fraud** from a proxy `/24` subnet
- **Checkout rate abuse** on `POST /api/v1/checkout`
- **Distributed scraping botnet** sharing a headless-browser fingerprint across many IPs
- **Credential stuffing** against `/login`
- plus the **benign baseline** of normal users

Read the report carefully and confirm the campaigns and the benign baseline make sense before moving on.

---

**Next:** Proceed to [Module 2.2: Building WAF Rules from the Threat Findings](../2.2/) to remediate each campaign.
