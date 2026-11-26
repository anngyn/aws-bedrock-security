---
title: "2.2 Building WAF Rules from the Threat Findings"
weight: 2
---

> ⚠️ **Region Reminder:** WAF Web ACL rule modifications apply to resources in **us-west-2 (Oregon)**.

**Estimated Time:** 25 minutes

**Objective:** Turn the threat report from Module 2.1 into concrete, applied WAF rule changes. Optimus will propose the exact rule JSON for each campaign and — only after you approve — update the Web ACL and IP sets to remediate every confirmed attack.

---

## Step 1: Ask Optimus to Build the Remediation Rules

In the **same Optimus chat** (so it keeps the full threat report as context), send the following prompt. This instructs Optimus to remediate each confirmed campaign with the right enforcement, while protecting the benign baseline.

```text
Based on the threat findings, implement the WAF rule changes to remediate each
campaign. For every confirmed attack, choose the right enforcement and apply it with
the WAF tools:

- Where a managed-rule label fired but the rule is only in COUNT, use Update WAF Web
  ACL to flip that rule (or rule group) to BLOCK — e.g. SQLi, XSS-body, ATP, ACFP,
  known-bad-inputs/path-traversal, and bot-control scanner labels.
- For single-source attackers (the SQLi IP, the path-traversal IP, the scanner IP),
  create or update an IP set with Create WAF IP Set / Block IP in WAF, and add an
  IP-set-reference BLOCK rule to the Web ACL.
- For the proxy /24 doing account-creation fraud, add the whole subnet CIDR to the
  block IP set.
- For the checkout rate abuse, add (or tighten) a rate-based rule scoped to
  POST /api/v1/checkout via Update WAF Web ACL.
- For the distributed scraping botnet, enable the bot-control automated-browser
  signal as BLOCK rather than relying on per-IP limits.

Rules:
- Read the Web ACL first to get its current rules and lock token, assign non-colliding
  priorities, and preserve all existing rules and the default action when you update.
- Do NOT touch anything matching the benign baseline.
- Show me the exact rule JSON / parameters for each change and the resulting rule list,
  and report the new lock token after each Update WAF Web ACL call.
```

> **Tip:** You can copy this prompt verbatim. It maps each campaign Optimus found in 2.1 to a specific enforcement action and sets the safety rules (read first, preserve existing rules, never block the baseline).

---

## Step 2: How Optimus Applies the Changes

Optimus works through the plan methodically. For each campaign it:

1. **Reads the Web ACL first** — `Get WAF WebACL` / `Get WAF Web ACL Rules` to capture the current rules, default action, and the **lock token** required for a safe update.
2. **Chooses the enforcement** that matches the campaign:

   | Campaign | Enforcement Optimus applies |
   |---|---|
   | Managed-rule label fired but only in COUNT (SQLi, XSS-body, ATP, ACFP, known-bad-inputs / path-traversal, bot-control scanner) | `Update WAF Web ACL` — flip that rule / rule group from **COUNT → BLOCK** |
   | Single-source attackers (SQLi IP, path-traversal IP, scanner IP) | `Create WAF IP Set` / `Block IP in WAF` + an **IP-set-reference BLOCK rule** |
   | Proxy `/24` account-creation fraud | Add the whole **subnet CIDR** to the block IP set |
   | Checkout rate abuse on `POST /api/v1/checkout` | Add / tighten a **rate-based rule** scoped to that endpoint |
   | Distributed scraping botnet | Enable the **bot-control automated-browser signal** as **BLOCK** |

3. **Assigns non-colliding priorities** and **preserves all existing rules and the default action** in the updated Web ACL.
4. **Presents the change for approval** — Optimus shows you the exact **rule JSON / parameters** before it calls `Update WAF Web ACL`. Approve it to apply, or reject to adjust.
5. **Reports the new lock token** after each successful `Update WAF Web ACL` call (the token rotates on every update, so it's needed for the next change).

---

## Step 3: Approve (Optional)

The Optimus skill is configured to **investigate read-only first and never apply a risky change without approval**.

If Optimus asks for approval:

- Review the rule JSON and the resulting rule list Optimus shows you.
- Confirm it **does not touch the benign baseline**.
- **Approve** to apply the change, or reply with adjustments.

After each `Update WAF Web ACL`, note the **new lock token** Optimus reports — it confirms the change landed and is carried into the next update.

---

## Step 4: Verify the Result

Once Optimus has worked through the plan, verify the remediation:

1. Ask Optimus (or use `Get WAF Web ACL Rules`) to show the **final rule list**, confirming:
   - The previously-COUNT managed rules are now **BLOCK**.
   - A new **IP-set-reference BLOCK rule** references the block IP set (single IPs + the proxy `/24` CIDR).
   - A **rate-based rule** is scoped to `POST /api/v1/checkout`.
   - The **bot-control automated-browser** signal is set to **BLOCK**.
   - All **pre-existing rules and the default action are preserved**.
2. (Optional) In the AWS console, open **WAF & Shield → Web ACLs** in `us-west-2` and confirm the rules match what Optimus reported.
3. (Optional) Re-run a quick Athena query (or `Get WAF Sampled Requests` / `Get WAF CloudWatch Metrics`) to confirm the attack traffic is now being **Blocked** while baseline traffic is still **Allowed**.

---

## What You've Accomplished

In this module you used **Optimus** to:

- Analyze raw AWS WAF v2 logs across multiple detection lenses and classify them into distinct threat campaigns.
- Distinguish coordinated attacks from the benign baseline with reproducible evidence.
- Translate each confirmed campaign into the correct WAF enforcement — COUNT→BLOCK flips, IP-set block rules, subnet CIDR blocks, rate-based rules, and bot-control signals.
- Apply every change safely — reading the Web ACL and lock token first, preserving existing rules, and approving each mutation — without ever blocking legitimate users.

This is the agentic security operations loop end-to-end: **detect → classify → recommend → remediate**, driven by natural language and powered by Amazon Bedrock / Claude.

---

**Congratulations!** You've completed the WAF Log Threat Analysis & Rule Building module. Continue to **Module 3** to explore AI-powered Just-in-Time database access.
