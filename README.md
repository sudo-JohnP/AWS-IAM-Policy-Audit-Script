# AWS IAM Policy Audit Script

Built using Python and Boto3, this tool helps enforce the principle of least privilege by flagging over-permissive IAM policies.
The script scans your AWS account for customer-managed IAM policies and identifies risky permissions such as:

- ✅ Wildcard actions (`"Action": "*"` or `"s3:*"`)
- ✅ Wildcard resources (`"Resource": "*"` or global access)
- ✅ High-risk actions (`iam:PassRole`, `iam:PutUserPolicy`)

---

## Why These Permissions Are Risky:

### 'iam:PassRole' -- Allows user to assign roles to resources in AWS (including higher priveleged roles!)
**Why's that risky?** -- Risks privelege escalation by an attacker as they could assign higher priveleged roles to a service to gain broader access.

### 'iam:CreatePolicy', 'iam:PutUserPolicy', 'iam:AttachRolePolicy' -- Allows users to create/attach policies to users/roles
**Why's that risky?** -- Possible security bypass through the attachment of admin-level priveleges.

### Wildcard Actions ('s3:*', 'ec2:*', '"Action": "*"') -- Grants access to all actions on a service/across all services
**Why's that risky?** -- Goes against the principle of least privelege. Also increases the possible impacts of leaked/stolen credentials.

### Wildcard Resources ('"Resource": "*"') -- Grants permissions for all resources in an account
**Why's that risky?** -- Even the smallest scoped actions can become dangerous when they're applied to **ALL** resources. 

---

## ⚙️ Features

- 🔍 Scans all customer-managed IAM policies in your AWS account
- 🚨 Detects wildcard permissions and high-risk actions
- 📋 Outputs easily readable findings to the terminal
- 🧪 Tested with intentionally risky IAM policies for validation

---

## 🖥️ How to Use

### 1. Configure AWS CLI credentials

In Command Prompt:
  aws configure

### 2. Install Python Dependencies

In IED:
  pip install boto3

### 3. Run the script from this Repo

---

## Sample Output

Auditing customer-managed IAM policies...

Policy: TestAuditPolicy (arn:aws:iam::123456789012:policy/TestAuditPolicy)
 - Wildcard Resource: '*' found
 - High-Risk Action: iam:PassRole
 - High-Risk Action: s3:*
 - High-Risk Action: ec2:*

---

## 🚀 Project Steps

Below are the steps I took to build and validate the IAM audit script, with screenshots included.

### 1. Created a Risky Test Policy in AWS Console
I intentionally included high-risk actions like `s3:*`, `iam:PassRole`, and a wildcard resource `"*"`.

<img width="677" height="360" alt="image" src="https://github.com/user-attachments/assets/9b043a87-33bf-4936-8b17-91d380338164" />


---

### 2. Ran the Python Audit Script
After configuring AWS CLI and running `iam_audit.py`, the script flagged the risky policy as expected.

<img width="1088" height="530" alt="image" src="https://github.com/user-attachments/assets/6411025a-641a-4789-925a-c4896468b709" />


---

### 3. Script Running in VS Code
The script was developed and tested in VS Code using Python and Boto3.

See [iam_audit.py](https://github.com/sudo-JohnP/AWS-IAM-Policy-Audit-Script/blob/main/iam_audit.py) for the script!
