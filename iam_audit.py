# Main Audit Script


import boto3
iam = boto3.client('iam')

# Risky IAM actions that will be flagged by this script
HIGH_RISK_ACTIONS = [
    "iam:PassRole",
    "iam:CreatePolicy",
    "iam:AttachRolePolicy",
    "iam:PutUserPolicy",
    "s3:*",
    "ec2:*"
]

# This function will check policies for risks based on HIGH_RISK_ACTIONS
def check_policy_risks(policy_doc):
    findings = []
    statements = policy_doc.get('Statement', [])
    if not isinstance(statements, list):
        statements = [statements]

    for stmt in statements: # Loops through each statement in the policy
        actions = stmt.get('Action', [])
        resources = stmt.get('Resource', [])
        
        # Normalize single values to lists
        if isinstance(actions, str): actions = [actions]
        if isinstance(resources, str): resources = [resources]

        # Check for wildcard actions
        if '*' in actions or any(action.strip() == '*' for action in actions):
            findings.append("Wildcard Action: '*' found")

        # Check for wildcard resources
        if '*' in resources or any(res.strip() == '*' for res in resources):
            findings.append("Wildcard Resource: '*' found")

        # Check for high-risk actions
        for risky_action in HIGH_RISK_ACTIONS:
            if any(risky_action.lower() in a.lower() for a in actions):
                findings.append(f"High-Risk Action: {risky_action}")

    return findings

# Fucntion that scans all managed IAM policies
def audit_managed_policies():
    findings = []

    paginator = iam.get_paginator('list_policies') # Using Paginator in case there are lots of policies
    for page in paginator.paginate(Scope='Local'): # Local Scope to scan customer managed policies (not AWS managed)
        for policy in page['Policies']:
            policy_name = policy['PolicyName']
            policy_arn = policy['Arn']
            default_version = policy['DefaultVersionId']

            version = iam.get_policy_version(
                PolicyArn=policy_arn,
                VersionId=default_version
            )
            doc = version['PolicyVersion']['Document']
            risks = check_policy_risks(doc) # Runs risk check

            if risks: # Adds results to findings
                findings.append({
                    'PolicyName': policy_name,
                    'PolicyArn': policy_arn,
                    'Findings': risks
                })

    return findings

if __name__ == "__main__":
    print("Auditing customer-managed IAM policies...\n")
    results = audit_managed_policies()

    if not results:
        print("✅ No risky policies found.")
    else:
        for result in results:
            print(f"\n🔎 Policy: {result['PolicyName']} ({result['PolicyArn']})")
            for f in result['Findings']:
                print(f" - {f}")
