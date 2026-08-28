# AWS Billing Skills for GitHub Copilot

GitHub Copilot skill for generating AWS billing reports using Cost Explorer API.

## Skills Included

### `aws-billing`
Generates monthly cost reports from AWS Cost Explorer with breakdown by service. Supports current month, previous month, or specific month queries.

**Features:**
- 📊 Detailed cost breakdown by AWS service
- 🔒 Secure authentication via AWS profiles
- 📅 Flexible date range queries
- 📝 Markdown-formatted output

## Installation

Using GitHub CLI:

```bash
# Install for GitHub Copilot
gh skill install rsevalueserve/copilot-skill-aws-billing aws-billing

# Install for other agents (e.g., Claude Code)
gh skill install rsevalueserve/copilot-skill-aws-billing aws-billing --agent claude-code

# Install at user scope (available everywhere)
gh skill install rsevalueserve/copilot-skill-aws-billing aws-billing --scope user
```

## Prerequisites

1. **Python dependencies:**
   ```bash
   pip install boto3
   ```

2. **AWS Configuration:**
   Configure an AWS profile with Cost Explorer read permissions:
   ```bash
   aws configure --profile your-profile-name
   ```

3. **IAM Permissions:**
   The AWS profile needs the following permission:
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": "ce:GetCostAndUsage",
               "Resource": "*"
           }
       ]
   }
   ```

## Usage

Once installed, GitHub Copilot can use the skill automatically. You can also run it manually:

```bash
# Current month report
~/.agents/skills/aws-billing/scripts/get_billing_report.py --profile your-profile --month current

# Previous month report
~/.agents/skills/aws-billing/scripts/get_billing_report.py --profile your-profile --month previous

# Specific month (YYYY-MM)
~/.agents/skills/aws-billing/scripts/get_billing_report.py --profile your-profile --month 2026-07
```

## Security

✅ **No hardcoded credentials** - Uses AWS profile-based authentication  
✅ **Principle of least privilege** - Only requires Cost Explorer read access  
✅ **Safe for version control** - No secrets stored in code

## Updating

```bash
gh skill update aws-billing
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Issues and pull requests are welcome!
