# AWS IAM Policy Audit Script

This Python script scans your AWS account for customer-managed IAM policies and identifies risky permissions such as:

- ✅ Wildcard actions (`"Action": "*"` or `"s3:*"`)
- ✅ Wildcard resources (`"Resource": "*"` or global access)
- ✅ High-risk actions (`iam:PassRole`, `iam:PutUserPolicy`)

Built using Python and Boto3, this tool helps enforce the principle of least privilege by flagging over-permissive IAM policies.

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
