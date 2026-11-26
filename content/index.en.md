---
title: "Agentic Security Operations Workflow with Amazon Bedrock"
weight: 0
---

## Intelligent Security Workshop with AWS Security Services & Agentic Automation

Welcome to this hands-on workshop where you'll learn to build an intelligent security ecosystem that automatically detects, analyzes, and mitigates security threats using AWS native security services combined with Agentic Bot automation (autobotAI), powered by AI capabilities through Amazon Bedrock.

---

## Workshop Quick Reference

| Item | Details |
|------|---------|
| **Duration** | ~4h 45m |
| **Region** | us-west-2 (Oregon) |
| **Coupon Code** | `AWSAISECWS` |
| **Difficulty** | Intermediate |

---

## Prerequisites

Before starting this workshop, ensure you have:

**Required:**
- ✅ Valid email address for account registration
- ✅ Mobile phone for SMS verification
- ✅ Authenticator app installed (Zoho OneAuth, Authy, or Google Authenticator)

**For Code Security Module:**
- ✅ GitHub account (free tier is sufficient)
- ✅ Ability to fork repositories

**Workshop Environment:**
- ✅ Modern web browser (Chrome, Firefox, Safari, or Edge)
- ✅ Stable internet connection
- ✅ Access to email during workshop

> ⚠️ **Important:** This workshop uses AWS Event accounts provided via Workshop Studio. All resources are pre-configured in the **us-west-2 (Oregon)** region.

---

## Workshop Theme

In today's rapidly evolving threat landscape, manual security operations are no longer sufficient. This workshop introduces you to the future of security operations - **Intelligent Security Automation** - where AI-powered agents work alongside AWS security services to provide real-time threat detection, intelligent analysis, and automated response capabilities.

You'll experience how **autobotAI**, an advanced Agentic security automation system powered by Amazon Bedrock, integrates with AWS Security Hub, Amazon GuardDuty, and Amazon Inspector to create a comprehensive security defense mechanism that learns, adapts, and responds to threats autonomously.

## What You'll Learn

By the end of this workshop, you will have hands-on experience with:

### 🔍 **Intelligent Threat Detection**
- **AWS Security Hub**: Centralized security findings aggregation and compliance monitoring
- **Amazon GuardDuty**: AI-powered threat detection for malicious activity and unauthorized behavior
- **Amazon Inspector**: Automated vulnerability assessments for applications and infrastructure
- **Amazon Bedrock**: Foundation models powering intelligent decision-making and automated responses

### 🤖 **Agentic Security Automation (autobotAI)**
- **Automated Incident Response**: How autobotAI processes security findings and triggers appropriate responses
- **Intelligent Decision Making**: Machine learning-driven threat prioritization and response selection
- **Cross-Service Orchestration**: Seamless integration between detection services and response mechanisms
- **Adaptive Learning**: How the system improves its responses based on historical data and outcomes

### 🛡️ **Real-World Security Scenarios**
- IAM vulnerability management and access control
- RDS database security threats and automated protection
- EC2 instance security incidents and intelligent response
- Vulnerability management and automated patching workflows
- Compliance violation detection and remediation

## Workshop Architecture

This workshop demonstrates a modern security operations architecture where multiple AWS security services feed intelligence into a centralized autobotAI system powered by Amazon Bedrock. The foundation models in Bedrock enable intelligent decision-making, contextual analysis, and automated responses based on security findings.

**Key Components:**
- **Detection Layer**: Security Hub, GuardDuty, and Amazon Inspector continuously monitor for threats and vulnerabilities
- **Intelligence Layer**: Amazon Bedrock provides AI-powered analysis and decision-making capabilities
- **Automation Layer**: autobotAI orchestrates remediation workflows and executes responses
- **Notification Layer**: Stakeholders receive real-time alerts and detailed incident reports

![Workshop Architecture](static/ServiceIntegrationPage0.png)

## Workshop Modules

| Module | Topic | Duration |
|--------|-------|----------|
| **Module 0** | Environment Setup & Service Introduction | 15 min |
| **Module 0.1** | Preparation & AWS Console Access | 10 min |
| **Module 1** | autobotAI Platform Setup & Integration | 45 min |
| **Module 2** | WAF Log Threat Analysis & Rule Building with Optimus | 45 min |
| **Module 3** | AI-Powered Just-in-Time Database Access | 60 min |
| **Module 4** | Threat Mitigation with GuardDuty & autobotAI | 45 min |
| **Module 5** | Agentic Remediation for Security Hub & Escalation | 45 min |
| **Module 6** | Building AppSec Inspector Workflow with Escalation | 45 min |

**Total Estimated Time:** ~4h 45m

### **Module 0: Environment Setup & Introduction** (15 min)
- Workshop environment provisioning
- Understanding the autobotAI architecture
- Initial security baseline establishment

### **Module 1: autobotAI Platform Setup & Integration** (45 min)
- Create your account, set up multi-factor authentication, and activate your subscription using the provided coupon code.
- Set up AWS integrations for infrastructure, AI, and notifications.
- Connect your GitHub repositories for AI-driven code analysis and set up threat intelligence integration.

### **Module 2: WAF Log Threat Analysis & Rule Building with Optimus** (45 min)
- Deploy a WAFv2 WebACL on an Application Load Balancer with AWS managed rule groups in count mode
- Direct S3 log delivery with sensitive headers redacted
- Use **Optimus**, autobotAI's chat-driven agentic assistant, to analyze sophisticated attack patterns through Amazon Athena: distributed bot orchestration, blind boolean SQLi, mutation XSS, credential stuffing, ACFP signup fraud, double-encoded traversal, scanner activity, rate-based abuse
- Drive surgical rule promotions and IPSet additions through natural-language WAF tool calls — every mutation approved before it lands

### **Module 3: Just-In-Time RDS Access Control with AI Agents** (60 min)
- Deploy secure Aurora MySQL Serverless v2 infrastructure
- Implement AI-powered just-in-time access control for databases
- Configure automated risk assessment and temporary credential provisioning
- Enable real-time activity monitoring and insider threat detection
- Experience both low-risk automated and high-risk manual approval workflows

### **Module 4: Threat Mitigation and Incident Response with GuardDuty and autobotAI** (45 min)
- Detecting RDS, EC2, and IAM security threats using GuardDuty
- Implementing AI-driven automated remediation with autobotAI
- Intelligent threat analysis and response workflows powered by Amazon Bedrock

### **Module 5: Agentic Remediation for Security Hub & Escalation** (45 min)
- Differentiate between static CSPM checks and dynamic Security Hub v2 findings.
- Dynamically build and schedule an escalation-aware DeepAgent bot via Optimus.
- Exercise tool governance by explicitly authorizing custom security remediation actions.
- Approve high-risk changes using interactive chat approval cards in the bot thread.
- Or, import a static remediation bot from the Library and run manual canvas configurations.

### **Module 6: Building AppSec Inspector Workflow with Escalation** (45 min)
- Enable Amazon Inspector Code Security connected to GitHub repositories
- Build Scanner and Resolver bots with Optimus for automated vulnerability remediation
- Generate automated pull requests with inline security annotations
- Enforce review SLAs with automated manager email escalations and track risk exceptions

## Target Audience

This workshop is designed for:
- **Security Practitioners** implementing security automation in AWS environments
- **SOC Analysts** responsible for threat detection and incident response
- **Security Engineers** building and maintaining security infrastructure
- **Cloud Security Professionals** managing compliance and security posture
- **DevSecOps Engineers** integrating security into CI/CD pipelines

## Workshop Region
**Primary Region**: us-west-2 (Oregon)  
**Additional Region**: us-east-1 (N. Virginia)

## Learning Outcomes

Upon completion of this workshop, you will:

1. **Understand Modern Security Operations**: Grasp how AI and automation are transforming security operations
2. **Master AWS Security Services**: Gain hands-on expertise with Security Hub, GuardDuty, and Amazon Inspector
3. **Build Intelligent Automation**: Create and deploy agentic security systems that learn and adapt
4. **Implement Real-World Solutions**: Apply learned concepts to actual security scenarios in your organization
5. **Design Scalable Security Architecture**: Architect security systems that grow with your infrastructure

---

**Ready to begin your journey into intelligent security automation?** Let's start by setting up your workshop environment and understanding the foundational concepts that make autobotAI possible.
