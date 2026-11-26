---
title: "Module 0: Environment Setup & Service Introduction"
weight: 01
---

> ⚠️ **Region Reminder:** All workshop activities should be performed in the **us-west-2 (Oregon)** region.

**Estimated Time:** 15 minutes

Welcome to the Security Issues Detection & Mitigation with autobotAI Workshop! In this module, you'll learn about the AWS security services that form the foundation of our intelligent security automation system.

## What is a Cybersecurity Agent Factory?

Most security teams automate the same way: one script, one Lambda, one runbook at a time. Each one is written by hand, tied to a single cloud, and maintained by whoever wrote it. That approach works for the first ten automations and breaks down well before the hundredth.

A **Cybersecurity Agent Factory** flips the model. Instead of building individual automations, you build a *production line* for them. The factory supplies the reusable pieces every security agent needs:

- **Pre-built integrations** - Authenticated connections to cloud providers, security tools, ticketing systems, and identity platforms
- **Reusable action libraries** - Vetted, parameterized tasks (isolate an instance, revoke a key, open a ticket) instead of bespoke API code
- **A common agent runtime** - Shared execution, scheduling, approval, and audit logic that every agent inherits
- **Governance by default** - Every agent run is logged, permission-scoped, and reversible

The result: building a new security agent becomes a configuration exercise measured in minutes, not a development project measured in sprints.

### What Teams Build With It

The same factory pattern covers detection triage, vulnerability response, compliance drift, identity hygiene, and incident enrichment. A few representative use cases:

![Cybersecurity Agent Factory Use Cases](../static/Cybersecurity-agent-factory-use-cases.gif)

> **Why this matters for this workshop:** Every agent you build in the modules ahead uses this factory model. You won't be writing integration plumbing — you'll be composing agents from components that already exist.

### Scaling to Thousands of Agents Across Multi-Cloud and On-Premises

A single agent solves one problem. Enterprise security posture requires thousands of them, running continuously across every environment you own. The factory model is what makes that tractable.

![How the Cybersecurity Agent Factory Works](../static/how-it-works.gif)

Three properties make scale possible:

| **Property** | **What It Means** | **Why It Scales** |
|----------|---------------|---------------|
| **Environment-agnostic agents** | Agent logic is written once, independent of where it runs | The same compliance agent targets AWS, Azure, GCP, Kubernetes, or on-prem |
| **Multi-account fan-out** | One agent definition executes across hundreds of accounts, subscriptions, or projects | Adding an account inherits your entire agent library, no rebuild |
| **Composable actions** | Agents are assembled from shared, tested building blocks | Fixing or improving one action improves every agent using it |

This is what separates "we automated a few things" from "our security operations are automated." Ten hand-built scripts across three accounts is a weekend of work. Ten *thousand* agent executions across three hundred accounts and four clouds is only possible when the integrations, runtime, and governance are supplied by the platform rather than rebuilt each time.

autobotAI is the Cybersecurity Agent Factory you'll use throughout this workshop — and the rest of Module 0 covers how it's deployed and secured before you start building.

---

## autobotAI Deployment Architecture & Security

autobotAI is designed with a **zero trust based self-hosted architecture**. In a standard production environment, the platform is self-deployed within the customer's own AWS VPC.

### Key Security Principles
- **Zero Data Outbound:** No data or permissions leave your AWS account. All processing and agentic operations happen within your security perimeter.
- **Local Control:** You maintain full control over the AI agents, integrations, and data storage.
- **AWS Native Security:** Leverages AWS IAM, KMS, and CloudWatch for secure operation.

### Workshop Environment
For the purpose of this workshop, we are using the **autobotAI SaaS (https://autobot.live)** to simplify the setup process. However, the agentic logic and AWS interactions demonstrated here are identical to the self-deployed version.

### autobotAI Architecture
![autobotAI Architecture](../static/autobotAI-data-and-permissions.drawio.png)

---

## Core AWS Security Services Overview

Understanding these three foundational services is crucial for building effective autobotAI agents. Each service provides unique capabilities that, when combined, create a comprehensive security automation platform.

Before diving into the hands-on activities, let's explore the three pillars of our autobotAI intelligent security system:

![Service Integration Architecture](../static/ServiceIntegration.png)

---

# Amazon GuardDuty
## Intelligent Threat Detection Service

**Service Type:** Threat Detection & Monitoring  
**Key Benefit:** Zero-infrastructure threat monitoring with ML-driven insights

### What is Amazon GuardDuty?

Amazon GuardDuty is a threat detection service that continuously monitors your AWS environment for malicious activity and unauthorized behavior. It uses machine learning, anomaly detection, and integrated threat intelligence to identify threats such as compromised instances, cryptocurrency mining, reconnaissance, and data exfiltration.

#### Key Capabilities
- **Machine Learning Detection** - Identifies unknown threats using behavioral analysis
- **Threat Intelligence Integration** - Leverages feeds from AWS Security, CrowdStrike, and Proofpoint  
- **Real-time Monitoring** - Continuous analysis with sub-5-minute alert generation
- **Zero Configuration** - Starts protecting immediately upon activation
- **Multi-source Analysis** - Correlates data across CloudTrail, VPC Flow Logs, and DNS logs

### How GuardDuty Works

GuardDuty combines supervised and unsupervised machine learning models with threat intelligence feeds from AWS Security, CrowdStrike, and Proofpoint to identify known malicious IPs, domains, and URLs. The service establishes baselines for normal activity patterns and detects deviations that may indicate threats.

#### Data Source Analysis

| **Core Data Sources** | **Optional Protection Plans** |
|-------------------|---------------------------|
| **CloudTrail Events** - Management API calls | **EKS Audit Logs** - Kubernetes API activity |
| **VPC Flow Logs** - Network traffic patterns | **S3 Data Events** - Object-level operations |
| **DNS Query Logs** - Route 53 resolver activity | **RDS Login Activity** - Database access patterns |
| | **Lambda Network Logs** - Serverless communications |
| | **EBS Volume Scanning** - Malware detection |
| | **Runtime Monitoring** - EC2/Container behavior |

> **Note:** Enable optional protection plans for comprehensive coverage, especially in production environments with sensitive workloads.

### Understanding Findings

GuardDuty uses a sophisticated scoring system to help you prioritize security responses effectively.

#### Severity Levels

| **Severity** | **Score Range** | **Description** | **Response Time** |
|----------|-------------|-------------|---------------|
| **CRITICAL** | 9.0-10.0 | Attack sequences in progress | **Immediate** |
| **HIGH** | 7.0-8.9 | Compromised resources detected | **< 1 hour** |
| **MEDIUM** | 4.0-6.9 | Suspicious activities requiring investigation | **< 24 hours** |
| **LOW** | 1.0-3.9 | Attempted suspicious activity (blocked) | **< 72 hours** |

#### Common Threat Categories
- **Backdoor Communications** - Detection of command and control server communications indicating potential system compromise
- **Unusual Behavior Patterns** - Deviations from established baselines that may indicate insider threats or compromised accounts
- **Cryptocurrency Mining** - Unauthorized cryptocurrency mining activities consuming your compute resources
- **Malware Detection** - Known malicious software signatures and behavioral patterns
- **Reconnaissance Activities** - Port scanning, network enumeration, and other information-gathering attempts
- **Multi-Stage Attack Sequences** - Sophisticated attacks correlating multiple events across different data sources to identify coordinated threats

### Integration and Automation

GuardDuty is designed for seamless integration with your existing security infrastructure and automated response systems.

#### Real-time Integration Flow

![GuardDuty to autobotAI Response Flow](../static/generated-diagrams/guardduty-autobotai-flow.png)

#### Integration Endpoints
- **Security Hub** - Centralized finding aggregation (ASFF format)
- **EventBridge** - Real-time event streaming for automation
- **SNS/SQS** - Custom notification and queuing systems
- **Third-party SIEM** - Enterprise security platform integration

### Agentic Security Operations

Learn how to transform GuardDuty from a detection tool into an intelligent, self-improving security system.

#### Intelligent Agent Capabilities
- **Threat Intelligence Enrichment** - Automatic OSINT correlation with external threat feeds, geolocation analysis of suspicious IP addresses, reputation scoring using multiple intelligence sources, and attack pattern recognition across historical data
- **Cross-Account Threat Correlation** - Multi-account attack sequence detection, lateral movement pattern identification, coordinated threat campaign analysis, and organization-wide threat hunting automation
- **Automated Response Actions** - Instance isolation and quarantine procedures, network access control and IP blocking, credential revocation and rotation workflows, and evidence collection and forensic preparation
- **Continuous Learning & Improvement** - Response effectiveness analysis and optimization, false positive reduction through machine learning, adaptive decision-making based on environmental context, and threat landscape evolution tracking and adaptation

---

# AWS Security Hub
## Centralized Security Command Center

**Service Type:** Cloud Security Posture Management (CSPM)  
**Key Benefit:** Unified security operations center with intelligent correlation

### What is AWS Security Hub?

AWS Security Hub is a centralized security command center that transforms fragmented security data into actionable intelligence. It serves as mission control for your cloud security operations, where all security findings converge for intelligent analysis and coordinated response.

#### Core Capabilities
- **Unified Dashboard** - Single pane of glass for all security findings
- **Multi-source Aggregation** - 100+ AWS and partner integrations
- **Compliance Management** - Automated assessment against security standards
- **Finding Standardization** - AWS Security Finding Format (ASFF) normalization
- **Intelligent Prioritization** - ML-powered risk scoring and correlation

### How Security Hub Works

Security Hub automatically collects findings from integrated AWS services including GuardDuty, Inspector, Macie, Config, Firewall Manager, and IAM Access Analyzer. It also supports over 100 third-party security tools through AWS Partner integrations, creating a unified security operations center.

#### Integration Ecosystem

| **AWS Native Services** | **Third-Party Partners** | **Custom Integrations** |
|---------------------|----------------------|---------------------|
| **GuardDuty** | **Splunk** | **REST APIs** |
| **Amazon Inspector** | **Qualys** | **EventBridge** |
| **Config** | **Rapid7** | **Custom Findings** |
| **Macie** | **Trend Micro** | **autobotAI Agents** |
| **Firewall Manager** | **Tenable** | **SIEM Integration** |

#### Security Standards Assessment

Security Hub automatically evaluates your environment against industry-standard frameworks 24/7.

| **Standard** | **Controls** | **Focus Areas** |
|----------|----------|-------------|
| **AWS Foundational** | 200+ | Comprehensive AWS best practices |
| **CIS Benchmark** | 100+ | Industry-hardened configurations |
| **PCI DSS** | 50+ | Payment card industry compliance |
| **NIST CSF** | 150+ | Cybersecurity framework alignment |

### Understanding Security Standards and Controls

The AWS Foundational Security Standard includes over 200 controls covering areas like access management, logging and monitoring, network security, and data protection. Each control has a defined remediation procedure and maps to specific AWS Config rules or custom logic.

#### Control Categories

| **Category** | **Examples** |
|----------|----------|
| **Access Management** | IAM policies, MFA enforcement |
| **Logging & Monitoring** | CloudTrail, VPC Flow Logs |
| **Network Security** | Security groups, NACLs |
| **Data Protection** | Encryption, backup policies |

#### Finding Status & Severity

Security Hub uses contextual risk scoring to help you focus on the most critical issues first.

| **Status** | **Severity** | **Description** |
|--------|----------|-------------|
| **FAILED** | Critical | Immediate security risk |
| **WARNING** | Medium | Configuration drift detected |
| **PASSED** | Low | Compliant with standard |
| **NOT_AVAILABLE** | Info | Assessment not applicable |

### Centralized Security Management

Security Hub's central dashboard provides real-time visibility into your security posture through customizable insights and summary statistics. You can filter and group findings by various attributes including severity, compliance status, resource type, and finding source.

#### Advanced Filtering & Analytics

| **Filter Type** | **Options** | **Use Case** |
|-------------|---------|----------|
| **Severity** | Critical, High, Medium, Low | Priority-based triage |
| **Compliance** | PASSED, FAILED, WARNING | Regulatory reporting |
| **Resource Type** | EC2, S3, IAM, Lambda | Service-specific analysis |
| **Finding Source** | GuardDuty, Amazon Inspector, Config | Source-based investigation |

#### Multi-Account Architecture

Security Hub supports cross-account finding aggregation through AWS Organizations for unified security governance.

![Security Hub Multi-Account Architecture](../static/securityhubmultiaccount.drawio.png)

### Integration and Automation

Security Hub's EventBridge integration enables real-time, automated security orchestration at enterprise scale.

#### Automation Workflows

| **Integration** | **Trigger** | **Action** | **Benefit** |
|-------------|---------|--------|---------|
| **EventBridge** | New finding | Lambda execution | Real-time response |
| **SNS** | Critical severity | Team notification | Immediate alerting |
| **Third-party SIEM** | All findings | SIEM ingestion | Centralized logging |
| **autobotAI Agents** | Pattern detection | Intelligent remediation | Proactive security |

#### API-Driven Operations
- **Programmatic Access** - REST APIs for custom integrations
- **Bulk Operations** - Batch finding management and updates
- **Custom Reporting** - Automated compliance and security reports
- **Finding Enrichment** - Context addition and threat intelligence correlation

### Agentic Security Operations

Transform Security Hub from a passive dashboard into an intelligent, self-managing security operations center.

#### Intelligent Agent Capabilities
- **Centralized Intelligence Hub** - Multi-source correlation across all integrated security services, pattern recognition for identifying coordinated attacks, risk prioritization using business context and threat intelligence, and automated triage and finding classification workflows
- **Predictive Security Analytics** - Historical pattern analysis for proactive threat hunting, anomaly detection in security finding trends, risk forecasting based on environmental changes, and compliance drift prediction and prevention
- **Orchestrated Response Workflows** - Cross-service remediation coordination and execution, escalation management with intelligent routing, evidence collection and forensic data preservation, and stakeholder notification with contextual information

---

# Amazon Inspector
## Automated Vulnerability Management

**Service Type:** Automated Vulnerability Management  
**Key Benefit:** Continuous security assessment with intelligent risk prioritization

### What is Amazon Inspector?

Amazon Inspector is an automated vulnerability management system that continuously guards your AWS workloads against security weaknesses. It constantly scans your infrastructure and applications for vulnerabilities while providing intelligent remediation guidance.

#### Core Capabilities
- **Continuous Assessment** - Automated scanning without agents or manual configuration
- **Multi-Workload Support** - EC2 instances, ECR containers, and Lambda functions
- **Risk-Based Prioritization** - Inspector Risk Score with network reachability analysis
- **Real-time Updates** - Latest CVE database with vendor security advisories
- **Intelligent Remediation** - Actionable guidance with automated patching integration

### How Amazon Inspector Works

Amazon Inspector automatically discovers eligible resources across your AWS accounts and begins continuous assessment without requiring agents or manual configuration for most resource types. The service seamlessly integrates with your existing AWS infrastructure.

#### Workload Assessment Matrix

| **Workload Type** | **Assessment Method** | **Scan Triggers** | **Coverage** |
|---------------|-------------------|---------------|----------|
| **EC2 Instances** | SSM Agent integration | Continuous + on-demand | OS packages & dependencies |
| **ECR Images** | Layer-by-layer analysis | Push + continuous discovery | All container layers |
| **Lambda Functions** | Runtime dependency scan | Deployment + periodic | Application dependencies |

#### Intelligence Database

Amazon Inspector maintains real-time vulnerability intelligence from multiple authoritative sources.

| **Source** | **Content** | **Update Frequency** |
|--------|---------|------------------|
| **CVE Database** | Common vulnerabilities & exposures | Real-time |
| **Vendor Advisories** | Security bulletins & patches | Daily |
| **AWS Security Research** | Cloud-specific threat intelligence | Continuous |
| **NIST NVD** | National vulnerability database | Real-time sync |

### Understanding Vulnerability Assessments

The Amazon Inspector Risk Score goes beyond CVSS to include network exposure, exploit availability, and business context for intelligent prioritization.

#### Risk Scoring Framework

| **Factor** | **Weight** | **Description** | **Impact** |
|--------|--------|-------------|--------|
| **Network Reachability** | High | Internet accessibility analysis | Critical exposure |
| **Exploit Availability** | High | Known exploits in the wild | Active threat |
| **CVSS Base Score** | Medium | Industry-standard severity | Inherent risk |
| **Business Context** | Medium | Asset criticality & environment | Operational priority |

#### Assessment Coverage by Workload

**EC2 Instance Assessment:**
- **Operating system packages** - Comprehensive OS-level vulnerability scanning
- **Application dependencies** - Runtime library and framework analysis  
- **Configuration analysis** - Security best practice compliance
- **Network exposure mapping** - Reachability and attack surface analysis

**Container Image Assessment:**
- **Multi-layer analysis** - Scanning all container image layers
- **Base image vulnerabilities** - Foundation security assessment
- **Package dependency mapping** - Application stack vulnerability analysis
- **Remediation recommendations** - Specific update and patch guidance

**Lambda Function Assessment:**
- **Runtime dependency analysis** - Language-specific package scanning
- **Application library assessment** - Third-party component evaluation
- **Configuration security review** - Function permission and access analysis
- **Performance impact evaluation** - Security vs. performance optimization

### Network Reachability Analysis

A vulnerability in an internet-accessible resource poses significantly higher risk than the same vulnerability in an isolated system.

Amazon Inspector performs intelligent network reachability analysis to determine if vulnerable resources are accessible from the internet or other networks. This analysis goes beyond simple port scanning to understand actual attack paths.

#### Network Security Assessment

| **Network Component** | **Analysis Scope** | **Risk Impact** |
|-------------------|----------------|-------------|
| **Security Groups** | Inbound/outbound rules | Direct access control |
| **Network ACLs** | Subnet-level filtering | Network segmentation |
| **Route Tables** | Traffic routing paths | Network topology |
| **Internet Gateways** | Public internet exposure | External attack surface |
| **NAT Gateways** | Outbound connectivity | Data exfiltration risk |

#### Enhanced Risk Prioritization Matrix

<div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 20px; border-radius: 10px; margin: 20px 0;">

| **Risk Level** | **Network Exposure** | **CVSS Score** | **Exploit Status** | **Response Priority** | **Action Required** |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **🔴 CRITICAL** | Internet-facing | 9.0-10.0 | Active exploits | **Immediate** | Emergency patching |
| **🟠 HIGH** | VPC-accessible | 7.0-8.9 | Known exploits | **< 4 hours** | Priority remediation |
| **🟡 MEDIUM** | Private subnet | 4.0-6.9 | Proof of concept | **< 24 hours** | Scheduled patching |
| **🟢 LOW** | Isolated | 1.0-3.9 | Theoretical | **< 7 days** | Maintenance window |
| **⚪ INFO** | No exposure | 0.1-0.9 | No known exploits | **Next cycle** | Documentation only |

</div>

#### Attack Path Visualization
- **Source Analysis** - Potential attacker entry points
- **Path Mapping** - Network routes to vulnerable resources  
- **Target Assessment** - Resource exposure and accessibility
- **Impact Evaluation** - Potential compromise scenarios

### Integration and Remediation

Amazon Inspector integrates natively with AWS services and third-party tools for comprehensive vulnerability lifecycle management.

#### Automated Integration Workflows

| **Integration Point** | **Capability** | **Automation Benefit** |
|-------------------|------------|-------------------|
| **Security Hub** | Centralized finding aggregation | Unified security operations |
| **Systems Manager** | Automated patch management | Zero-touch remediation |
| **EventBridge** | Real-time finding notifications | Instant response triggers |
| **ECR/ECS** | Container deployment blocking | Secure-by-default pipelines |
| **CI/CD Pipelines** | Build-time vulnerability gates | Shift-left security |

#### Remediation Automation

**Automated Patching Workflows:**
- **Patch Manager integration** for OS-level vulnerability remediation
- **Maintenance window coordination** with business requirements
- **Rollback capabilities** for failed patch deployments
- **Compliance tracking** and audit trail maintenance

**Container Security Automation:**
- **Admission controller integration** for Kubernetes environments
- **CI/CD pipeline gates** preventing vulnerable image deployments
- **Base image update recommendations** with automated testing
- **Registry scanning** with policy-based access control

### Agentic Security Operations

Transform Amazon Inspector from a scanning tool into an intelligent, self-managing vulnerability remediation system.

#### Intelligent Agent Capabilities
- **Vulnerability Intelligence Engine** - Continuous monitoring of vulnerability findings across all workloads, risk assessment based on network exposure and business context, threat correlation with external intelligence feeds, and exploit prediction using machine learning and historical data
- **Automated Remediation Workflows** - Intelligent patching schedules based on risk priority and business impact, maintenance window coordination with operational requirements, remediation progress tracking across large-scale environments, and success rate optimization through continuous learning
- **Proactive Defense Measures** - Active exploit correlation with real-world threat intelligence, zero-day vulnerability preparation through predictive analysis, attack surface reduction through automated configuration hardening, and compliance drift prevention with continuous monitoring
- **Advanced Analytics & Reporting** - Vulnerability trend analysis for strategic security planning, risk forecasting based on environmental changes, remediation effectiveness metrics and optimization recommendations, and executive dashboards with business-relevant security insights

---

## Next Steps

With your solid understanding of the core AWS security services, you're ready to begin building your intelligent security system. In Module 1, we'll configure autobotAI as your central command center to start aggregating and intelligently responding to security findings from multiple sources.
