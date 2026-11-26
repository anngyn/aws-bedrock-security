---
title: "6.1 Configuring Amazon Inspector for Code Security"
weight: 1
---

> ⚠️ **Region Reminder:** Enable Amazon Inspector Code Security in **us-west-2 (Oregon)**.

**Estimated Time:** 20 minutes

## Configuring Amazon Inspector for Code Security

### Step 1: Fork the Sample Vulnerable App

You need to fork the sample vulnerable application repository to your own GitHub account so you can scan it with Amazon Inspector.

> **Note:** This sample vulnerable application is provided by autobotAI (fusiongate-inc) for workshop demonstration purposes. It contains intentional security vulnerabilities for testing automated remediation workflows. We recommend removing this forked repository from your GitHub account after completing the workshop (see cleanup instructions in the Summary section).

**Repository to Fork:**  
👉 [fusiongate-inc/sample-vulnerable-app](https://github.com/fusiongate-inc/sample-vulnerable-app)

**How to Fork the Repository:**

1. **Navigate to the Repository**
   - Click on the repository link above or visit: `https://github.com/fusiongate-inc/sample-vulnerable-app`
   - You'll be taken to the GitHub repository page

   ![Navigate to Repository](../../static/module6step1.png)

2. **Sign in to GitHub**
   - If you're not already signed in, click **Sign in** in the top right corner
   - Enter your GitHub credentials
   - If you don't have a GitHub account, click **Sign up** to create one first

3. **Fork the Repository**
   - Once signed in, locate the **Fork** button in the top right corner of the repository page
   - Click the **Fork** button

   ![Fork the Repository](../../static/module6step3.png)

   - GitHub will show you a "Create a new fork" page

4. **Configure Your Fork**
   - **Owner:** Your GitHub username (should be pre-selected)
   - **Repository name:** Keep the default `sample-vulnerable-app` or customize if desired
   - **Description:** Optional - you can add a description
   - **Copy the main branch only:** Keep this checked (recommended)
   - Click **Create fork**

   ![Configure Your Fork](../../static/module6step4.png)

5. **Verify Your Fork**
   - After a few seconds, you'll be redirected to your forked repository
   - The URL should now be: `https://github.com/YOUR-USERNAME/sample-vulnerable-app`
   - You should see a note under the repository name indicating it was forked from `fusiongate-inc/sample-vulnerable-app`

   ![Verify Your Fork](../../static/module6step5.png)

---

### Step 2: Enable Code Security in Amazon Inspector
1. Open the **Amazon Inspector Console** in the **us-west-2** region.
2. Go to the **Code Security** section.  
   - If Code Security is not yet enabled, you'll see a popup like this:  
     ![Step 1 – Enable Code Security Popup](../../static/inspector-1.png)
3. Click on **Enable code scanning**.  
4. You'll be redirected to **Account Management**. You should see **Code repository scanning** marked as *Activated*.  
   ![Step 2 – Code Repository Scanning Activated](../../static/inspector-3.png)
5. If it's not activated:  
   - Click **Activate**.  
   - Select **Code repository scanning**, submit, and it will be enabled.  
     ![Step 3 – Activating Code Repository Scanning](../../static/inspector-2.png)

---

### Step 3: Connect Amazon Inspector with the Forked GitHub Repository
1. From the **Code Security** tab in the Amazon Inspector console, click **Connect to**, and select **GitHub**.
2. Keep all settings as default, then click **Create scan configuration**.  
   ![Step 5 – Create Scan Configuration](../../static/inspector-4.png)
3. On the next page, provide an **Integration Name**, then click **Connect**.  
   - **Note:** If the **Connect to GitHub** option doesn't appear, refresh the page.  
     ![Step 6 – Connect to GitHub Integration](../../static/inspector-5.png)
4. When prompted, authorize Amazon Inspector to access your GitHub account:
   - A popup will appear — click **Authorize Amazon Inspector**.  
     ![Step 7 – Authorize Amazon Inspector](../../static/inspector-6.png)
5. Once authorized, you'll be redirected back to the Amazon Inspector console, where you'll see the following popup:
   - Click on **Go to GitHub connection page**.  
     ![Step 8 – Redirect to GitHub Connection Page](../../static/inspector-7.png)
6. Click **Install a new app** — this will redirect you to the GitHub App installation page.  
   ![Step 9 – Install GitHub App](../../static/inspector-8.png)
   - Choose **Only select repositories**.  
   - Search for and select your forked sample repository.  
   - Click **Install & Authorize**.  
     ![Step 10 – Authorize Selected Repository](../../static/inspector-9.png)
7. After installation, go back to **Code Security** in the Amazon Inspector console.
   - Scroll down to **Code Repositories** — your repository should now appear in the list.  

---

### Step 4: Start Your First Scan
1. Once integration is complete, ensure your repository is listed and the configuration status shows as **Configured**.  
2. Select your repository and click on **On-demand scan**.  
   ![Step 12 – Start Your First Scan](../../static/inspector-10.png)
3. Wait a few minutes, then click on the repository name.  
4. Scroll down to the **Findings** section — you should now see the identified vulnerabilities and security issues.  
   ![Step 13 – View Scan Findings](../../static/inspector-11.png)

---

**Next:** Proceed to Module 6.2 to import and configure the workflow.

---

## 📝 Optional: Set Up a GitHub App Integration

> [!NOTE]
> This step is **not mandatory**. The workflow can also run using the standard GitHub integration you created in the earlier modules. However, a GitHub App integration provides more fine-grained repository permissions and is recommended for production use.

---

### Step A: Create a GitHub App on GitHub

1. Click your **profile icon** in the top-right corner of GitHub and select **Settings**.

   ![GitHub Profile Settings Menu](../../static/github-app-profile-settings-menu.png)

2. Scroll to the very bottom of the left sidebar and click **Developer settings**.

   ![Developer Settings Link](../../static/github-app-developer-settings-link.png)

3. Under **GitHub Apps**, click **New GitHub App**.

   ![GitHub Apps Listing](../../static/github-app-github-apps-listing.png)

4. Fill in the **Create GitHub App** form:
   - **GitHub App name:** Give it a unique name (e.g. `PR-Review-Bot`)
   - **Description:** Describe the app (e.g. `Github app to remediate inspector findings and generate PR review`)
   - **Homepage URL:** `https://autobot.live`

   ![Create GitHub App Form](../../static/github-app-create-form.png)

5. Under **Webhook**, **uncheck the Active** checkbox — a webhook is not required for this workflow.

   ![Uncheck Webhook Active](../../static/github-app-webhook-section.png)

6. Under **Permissions → Repository permissions**, expand and set:
   - **Contents:** Read & Write
   - **Pull Requests:** Read & Write

   Then at the bottom of the form under **Where can this GitHub App be installed?**, select **Only on this account**. Click **Create GitHub App**.

   ![Permissions and Install Scope](../../static/github-app-permissions-install.png)

---

### Step B: Get Client ID & Generate a Private Key

1. After the app is created, you will land on the **General** tab of your new GitHub App. Note down the **Client ID** — you will need it for the autobotAI integration.

   > **Note:** Do not use the **App ID** shown here. The actual **Installation App ID** you need is found later in Step D from the browser URL after installing the app.

   ![General Tab — Client ID](../../static/github-app-general-tab-clientid.png)

2. Scroll to the bottom of the **General** tab to the **Private keys** section. Click **Generate a private key**. A `.pem` file will be automatically downloaded to your computer.

   ![Generate Private Key](../../static/github-app-private-key-section.png)

---

### Step C: Install the App on Your Repository

1. In the left sidebar of your GitHub App settings, click **Install App**. Click the **Install** button next to your account.

   ![Install App Tab](../../static/github-app-install-tab.png)

2. On the installation page, select **Only select repositories**, search for and select your `sample-vulnerable-app` fork, then click **Install**.

   ![Select Repository and Install](../../static/github-app-select-repo-install.png)

---

### Step D: Find Your Installation App ID

1. Go to your GitHub **Settings** (profile icon → Settings). In the left sidebar under **Integrations**, click **Applications**. You will see all your installed GitHub Apps listed here.

   ![Integrations > Applications](../../static/github-app-integrations-menu.png)

2. The page lists all your installed apps. Find your app and click **Configure**.

   ![Settings > Applications](../../static/github-app-settings-applications.png)

3. Look at the URL in your browser — it will look something like `https://github.com/settings/installations/12345678`. The **sequence of numbers at the end** is your **Installation App ID**. Note this down.

---

### Step E: Add the Integration in autobotAI

1. In autobotAI, navigate to **Integrations**, search for **Githubapp**, and click **Add Integration**.

   ![autobotAI Search for GitHub App](../../static/github-app-autobotai-search.png)

2. Fill in the **GitHub App Integration Setup** form:
   - **Alias:** A friendly name (e.g. `test-app`)
   - **Github Installation Id:** The installation ID from the browser URL in Step D
   - **Github Private Key:** Open your terminal and run `cat /path/to/your-downloaded-key.pem`, then paste the entire output into this field
   - **Github Client Id:** The Client ID from the General tab of your GitHub App

   Click **Create**.

   ![autobotAI GitHub App Integration Form](../../static/github-app-autobotai-form.png)

---

## ✅ Success Criteria

You've completed this section when:
- [ ] Repository forked to your GitHub account
- [ ] Amazon Inspector Code Security enabled
- [ ] GitHub integration authorized
- [ ] Repository appears in Code Repositories list
- [ ] On-demand scan completed
- [ ] Vulnerability findings visible in Inspector console

---

## Troubleshooting

### Issue: Fork button not visible on GitHub
**Solution:** Ensure you're signed in to GitHub. The Fork button appears in the top-right corner.

### Issue: Code Security not showing in Inspector console
**Solution:**
1. Ensure you're in us-west-2 region
2. Navigate to Inspector → Code Security in the left menu
3. Click "Enable code scanning" if prompted

### Issue: GitHub authorization popup blocked
**Solution:** Allow popups for the AWS console domain in your browser settings.

### Issue: Repository not appearing after authorization
**Solution:**
1. Refresh the Amazon Inspector console page
2. Verify you selected "Only select repositories" and chose your fork
3. Try disconnecting and reconnecting the GitHub integration
