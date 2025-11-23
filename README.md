# Scheduled Telegram Poll Bot

This project contains a simple, serverless Telegram bot that automatically sends a poll to a specified chat on a recurring schedule.

It uses AWS Lambda to run the Python script and Amazon EventBridge to trigger it. The entire infrastructure is defined using Terraform and deployed automatically via a GitHub Actions CI/CD pipeline.

## Technology Stack

-   **Backend:** Python 3.9
-   **Telegram Library:** `python-telegram-bot`
-   **Cloud Provider:** Amazon Web Services (AWS)
    -   **Compute:** AWS Lambda
    -   **Scheduling:** Amazon EventBridge
-   **Infrastructure as Code:** Terraform
-   **CI/CD:** GitHub Actions

## Project Structure

```
.
├── .github/workflows/deploy.yml   # GitHub Actions workflow for CI/CD
├── terraform/                     # Terraform files for defining AWS infrastructure
│   ├── main.tf                    # Main infrastructure definition (Lambda, IAM Role, etc.)
│   ├── variables.tf               # Input variables for Terraform
│   └── outputs.tf                 # Outputs from the Terraform deployment
├── bot_lambda.py                  # The Python script for the Lambda function
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Deployment Instructions

The project is deployed automatically when you push changes to the `main` branch. Before you do that, you must complete the following one-time setup.

### Step 1: Create an IAM User in AWS

The GitHub Actions workflow needs AWS credentials to deploy resources on your behalf. You must create a dedicated user for this.

1.  Navigate to the **IAM** service in your AWS Console.
2.  Create a new **User** (e.g., `github-actions-deployer`).
3.  On the "Set permissions" step, select **Attach policies directly** and attach the `AdministratorAccess` policy.
    > **Note:** For production, it is highly recommended to create a custom, more restrictive policy instead of using `AdministratorAccess`.
4.  After creating the user, navigate to the **Security credentials** tab for that user.
5.  Click **Create access key**, select **Command Line Interface (CLI)** as the use case, and create the key.
6.  You will be shown an **Access key ID** and a **Secret access key**. Copy both of these immediately. **You will not be able to see the secret key again.**

### Step 2: Configure GitHub Secrets

You need to store the AWS credentials and Telegram bot details as encrypted secrets in your GitHub repository.

1.  In your GitHub repository, go to **Settings** > **Secrets and variables** > **Actions**.
2.  Click **New repository secret** and add the following four secrets:

| Secret Name            | Value                                        | Description                                     |
| ---------------------- | -------------------------------------------- | ----------------------------------------------- |
| `AWS_ACCESS_KEY_ID`    | The Access Key ID you copied in Step 1.      | The access key for your AWS IAM user.           |
| `AWS_SECRET_ACCESS_KEY`| The Secret Access Key you copied in Step 1.  | The secret key for your AWS IAM user.           |
| `TELEGRAM_BOT_TOKEN`   | Your Telegram bot's token.                   | You get this from the BotFather on Telegram.    |
| `TELEGRAM_CHAT_ID`     | The ID of the chat for the bot to post in.   | Can be a personal chat, group, or channel ID. |

### Step 3: Push to Deploy

Once the four secrets are configured in your GitHub repository, you are ready to deploy.

Commit all the files we have created (`terraform/`, `.github/workflows/`, `bot_lambda.py`, etc.) and push them to the `main` branch.

```sh
git add .
git commit -m "Initial setup for Telegram bot and deployment workflow"
git push origin main
```

The push will automatically trigger the `Deploy Lambda Function` workflow in the "Actions" tab of your repository. The workflow will use Terraform to create the necessary AWS resources and deploy the bot.

## Customization

### Changing the Poll Content

To change the poll question and options, edit the `question` and `options` variables at the top of the `bot_lambda.py` file.

### Changing the Schedule

The bot is configured to run every Friday at 12:00 UTC. You can change this by modifying the `schedule_expression` in the `terraform/main.tf` file. The expression uses a standard cron format.

```terraform
# terraform/main.tf

resource "aws_cloudwatch_event_rule" "schedule" {
  name                = "run-lambda-every-friday"
  description         = "Triggers the Telegram bot Lambda function"
  schedule_expression = "cron(0 12 ? * FRI *)" # <-- Change this line
}
```
