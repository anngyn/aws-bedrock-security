---
title: "6.2 Amazon Inspector → Fix Code / Patch → Dev Feedback → Raise PR → Mitigate with WAF → Risk Register"
weight: 2
---

**Objective:** Use an Optimus template to build remediation for first-party code findings (SAST, IaC) and third-party code findings (SCA) with a process that doesn't stop at recommendation but manages risk through federated risk owner approval. You will configure the autonomous orchestrator (Optimus) to define the remediation operation flow, launch the template (which configures automated WAF shielding for deferred or unmerged findings), approve tool governance, and monitor the automated creation of the Scanner and Resolver bots.

> ⚠️ **Region Reminder:** Configure all AWS resources in **us-west-2 (Oregon)**.

**Estimated Time:** 10 minutes

---

## Building with Optimus

### Step 1: Navigate to Optimus

1. From the autobotAI top navigation, click the **OPTIMUS** button to open the Optimus panel.

   ![Open Optimus](../../static/optimus-nav-button.png)

---

### Step 2: Launch the AppSec Inspector Template

Instead of building everything manually, we use a pre-created template that instructs Optimus on how to build the entire 2-bot architecture.

1. In the Optimus chat window, click the **Browse All Templates** button visible in the chat window.

   ![Browse All Templates](../../static/optimus-inspector-home-browse-templates.png)

2. In the Template Library, find and select **Inspector Code Security Findings Remediation with Escalation Management**.

   ![Template Library](../../static/optimus-inspector-template-library.png)

3. Click the **settings (⚙️)** icon visible above the prompt box to open the configuration panel.

4. Under **AI Model → Provider & Integration**, configure the following:
   - **AI Provider:** `aws bedrock`
   - **Integration Account:** your Bedrock integration (e.g. `test-aws-bedrock-us-west-2`)
   - **Model:** `global.anthropic.claude-opus-4-6-v1`

   ![AI Model Configuration](../../static/optimus-inspector-ai-model-config.png)

5. In the same config tab, verify the **Model Parameters** are set correctly:
   - **Temperature:** `0.70`
   - **Max Iterations:** toggled on to **No limit**

   ![Model Parameters](../../static/optimus-inspector-model-parameters.png)

6. **Enable GitHub MCP Tools:** Go to the **Tools** tab, search for **Github App**, navigate to the **MCP Server** section, and select both `Github All` and `Github Pull Requests`.

   > ⚠️ **Important:** Enable the `Github All` and `Github Pull Requests` MCP servers for every GitHub integration you have configured:
   > - **If you created a GitHub App integration:** Enable both MCP servers for **both** your **GitHub App integration** and your standard **GitHub integration**.
   > - **If you did not create a GitHub App integration:** Enable both MCP servers for your standard **GitHub integration**.
   >
   > The screenshot below shows the settings for a GitHub App integration. Enabling the MCP servers for the standard GitHub integration as well gives you a seamless fallback during automated PR creation and review.

   ![Enable GitHub MCP](../../static/optimus-github-mcp-tools.png)

7. Go to the **Knowledge** tab and verify which skills have been added to Optimus. You should see the `appsec-inspector-workflow` skill along with supporting skills like `AppSec Harness Guide`, `Bot Creation Guide`, `Bot Builder Guide`, and the code review skills.

   ![Knowledge Skills](../../static/optimus-inspector-knowledge-skills.png)

8. Before sending, review the **user prompt** that has been automatically loaded into the prompt box by the template. Update the following values to match your environment and preferences:
   - **AWS Integration name** — the name of your AWS integration in autobotAI (e.g. `test-aws`)
   - **SES Integration name** — your AWS SES integration name (e.g. `test-aws-ses-us-west-2`)
   - **GitHub repository name** — your target repo (e.g. `your-org/your-repo`) and base branch
   - **REVIEW_SLA_MINUTES** — how many minutes the reviewer has to review the PR before escalation
   - **MERGE_SLA_MINUTES** — how many additional minutes after review SLA before a merge escalation is triggered
   - **HARD_DEADLINE_SLA** — the total hard deadline in minutes, after which the bot ends the session

9. Once all values are confirmed and updated, press **Enter** or click **Send** to begin the workflow.

---

### Step 3: Monitor Autonomous Bot Creation

Once you send the prompt, Optimus takes over and does everything for you. Your only job is to monitor its progress.

1. **Workflow Generation:** Optimus will parse the template, determine the skills needed, and create all the required resources (Scanner bot, Resolver bot, and Listeners).

   ![Optimus Workflow Generation](../../static/optimus-workflow-creation-tasks.png)

2. **Tool Governance:** If Optimus pauses for authorization during skill or tool creation, follow the prompts to navigate to the **Tools** menu, enable the generated actions, and reply in the chat to confirm.

---

### Step 4: Verifying Bot Creation (Optional)

1. Once Optimus finishes the build process, it will automatically enable both bots and trigger the Scanner bot for you!
2. If you want to manually confirm the bots are created, you can navigate to **Bots** from the main menu.
3. You will see both bots fully configured and enabled.

![Bot List](../../static/optimus-bots-created-list.png)

> 💡 **Tip:** After Optimus completes the workflow creation and automatically triggers the Scanner bot, a **View Execution** button will appear directly in the Optimus chat. You can click this button to jump straight to the Scanner's execution page, or you can navigate there manually via the **Bot Execution** menu in the next section.

---

**Next:** Proceed to Module 6.3 to run the workflow and observe the intelligent escalation lifecycle.

---

## ✅ Success Criteria

You've completed this section when:
- [ ] Optimus default settings are configured
- [ ] AppSec Inspector template is launched with correct variables
- [ ] GitHub MCP integrations are enabled in the Tools menu
- [ ] Scanner and Resolver bots are successfully created and enabled

---

## Troubleshooting

### Issue: Optimus pauses and asks for authorization
**Solution:** This is expected tool governance. Follow Optimus's prompt to navigate to the Tools menu, authorize the skill/tool, and reply to Optimus to resume.

### Issue: GitHub MCP tools are not showing up
**Solution:** Ensure you successfully installed the GitHub App in your GitHub account during the earlier prerequisites module. Refresh the Tools > MCP Server page.
