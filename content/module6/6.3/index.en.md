---
title: "6.3 Running the Workflow and Managing Escalations"
weight: 3
---

> ⚠️ **Region Reminder:** Amazon Inspector findings and SES notifications are in **us-west-2 (Oregon)**.

**Estimated Time:** 15 minutes

## Prerequisite Check

Before triggering the workflow, ensure your platform integrations (GitHub App and Amazon SES) are fully configured, as the Resolver bot relies on them to create PRs and send email notifications.

## The Automated Remediation Lifecycle

Now we will run the workflow and observe how the agentic bots collaborate to solve the problem of abandoned PRs and automatically deploy WAF shielding rules.

### Step 1: Monitoring the Scanner

Since Optimus automatically triggered the Scanner bot for you at the end of the previous module, you do not need to run it manually. Your job is just to monitor its progress.

1. If you didn't click the **View Execution** button directly from the Optimus chat, navigate to the **Bot Execution** menu from the main navigation.

   ![Bot Execution Page](../../static/bot-execution-page-nav.png)

2. Locate the running `AppSec Inspector Scanner` session. When the green popup appears in the bottom right corner, click **Open** to access the DeepAgent chat thread.

   ![Open Scanner Chat](../../static/scanner-open-chat-popup.png)

3. The scanner queries Amazon Inspector for code vulnerabilities (like SQL injection or IAM wildcard policies).

   ![Inspector Findings](../../static/inspector-findings-before-remediation.png)

4. In the scanner's execution log, you'll see it recording each finding as an individual task in the register and then firing the `inspector-resolver-trigger` event.

   ![Scanner Execution Log](../../static/scanner-bot-task-execution.png)
   ![Scanner Registering Task](../../static/scanner-task-registered.png)

### Step 2: The Resolver Takes Over

The listener event automatically wakes up the `AppSec Inspector Resolver` bot in the background.

1. You can track its progress by going back to the **Bot Execution** page and opening the Resolver bot's chat thread.

   ![Resolver Execution List](../../static/resolver-execution-page.png)
   ![Open Resolver Chat](../../static/resolver-open-chat-popup.png)

2. The Resolver processes the batched findings, clones the vulnerable repository, applies fixes to the code, and pushes a single new branch.

   ![Vulnerable Repo on GitHub](../../static/github-vulnerable-repo.png)
   ![Resolver Tasks](../../static/resolver-bot-tasks.png)

3. It then opens a Pull Request addressing all the identified vulnerabilities.

   ![Open PR on GitHub](../../static/github-open-pr.png)

4. **Inline Annotations:** To help the human reviewer understand the changes, the bot leverages the GitHub App integration to post inline annotations directly on the code diff, explaining which CWE/CVE was fixed and why.

   ![Inline Annotations](../../static/github-pr-inline-annotations.png)

### Step 3: SLA Enforcement and Escalation

Once the PR is open, the Resolver bot sends an initial email notification to the reviewer.

![PR Review Email](../../static/email-pr-review-notification.png)

Instead of terminating, the bot enters a **Wait Loop**, pausing its execution to enforce the review Service Level Agreement (SLA).

![Waiting for Merge SLA](../../static/resolver-waiting-merge-sla.png)

If the reviewer ignores the PR and the SLA window expires, the bot will escalate the issue. It looks up the reviewer's manager and sends a formal escalation email via Amazon SES.

![Manager Escalation Email](../../static/email-manager-escalation.png)
![Final Manager Escalation](../../static/email-final-manager-escalation.png)

If the hard deadline is reached without a merge, the bot automatically deploys protective WAF shielding rules to safeguard the application, sends a final deadline notice, and concludes the session.

![Final Deadline Email to Reviewer](../../static/email-final-reviewer-escalation.png)

> 💡 **Note (Demonstration Purpose):** Since the sample application is not actually live, these WAF rules are created for demonstration purposes to show how autobotAI can automatically deploy a shield at the edge when a user ignores or postpones a critical code remediation.

The bot will then conclude its session, summarizing the WAF rule details and final status in the Goal Evaluation section.

![Goal Evaluation Summary](../../static/resolver-final-goals-summary.png)

### Step 4: Tracking Tasks and the Risk Register

Throughout this process, the bot maintains a strict audit trail.

1. Navigate to the **Tasks** dashboard to view the status of all vulnerability remediations.

   ![Navigate to Tasks](../../static/nav-to-tasks.png)
   ![Tasks List in Register](../../static/task-register-list.png)

2. If a reviewer decides to postpone or reject a fix due to a valid business reason (e.g. by commenting that remediation will be done later), the Resolver bot automatically deploys WAF shielding rules to protect the application, registers this decision, and logs it in the **Risk Register**. Navigate to the **Risk Register** to see active exceptions.

   ![Navigate to Risk Register](../../static/nav-to-risk-register.png)
   ![Risks List in Register](../../static/risk-register-list.png)

3. You can also verify the findings on the Inspector console after some time to check if the remediations you merged have successfully resolved the vulnerabilities.

   ![Resolved Findings](../../static/inspector-findings-after-remediation.png)

4. **Verifying Applied WAF Rules:** To inspect the shielding rules automatically deployed for the deferred or unmerged findings, navigate to the **AWS WAF & Shield Console** in the **us-west-2** region and view your Web ACL or Rule groups.

The next time the Scanner runs, the Resolver bot will check the Risk Register and automatically skip any vulnerabilities covered by an active exception.

---

## Conclusion

You have successfully built and executed an intelligent, agent-driven AppSec remediation workflow! By leveraging Optimus, listener events, and wait loops, you transformed a standard "fire-and-forget" alert system into a rigorous, SLA-enforced governance process that ensures vulnerabilities are actually fixed, not just reported.

---

## ✅ Success Criteria

You've completed this section when:
- [ ] Scanner bot successfully identifies vulnerabilities from Amazon Inspector
- [ ] Resolver bot clones the repo and pushes a code fix branch
- [ ] Pull Request is created with inline annotations on the code diff
- [ ] Escalation email is sent to the reviewer's manager upon SLA breach
- [ ] Automated WAF shielding rules are created for postponed or hard-deadline unmerged findings
- [ ] Tasks are properly logged and exceptions tracked in the Risk Register

---

## Troubleshooting

### Issue: The Resolver bot didn't create a Pull Request
**Solution:** Check the Bot Execution logs for the Resolver. Ensure that your GitHub App integration has the required repository permissions (Contents: Write, Pull Requests: Write).

### Issue: Escalation emails are not sending
**Solution:** Verify that the email addresses configured in your prompt variables (for reviewer and manager) are verified in your Amazon SES sandbox account.
