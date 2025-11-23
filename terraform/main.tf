# main.tf

# This block configures Terraform to use the AWS provider.
# The AWS provider is responsible for creating and managing AWS resources.
# We are setting the region to "us-east-1" and allowing for version 3.x of the provider.
provider "aws" {
  region = var.aws_region
}

# This block is used to create a zip file of the Python code.
# We are packaging the bot_lambda.py file into a zip file called "lambda.zip".
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir = "${path.module}/../package"
  output_path = "${path.module}/lambda.zip"
}

# This block creates an IAM role for the Lambda function.
# The role allows the function to be assumed by the Lambda service and to write logs to CloudWatch.
resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# This block attaches the AWSLambdaBasicExecutionRole policy to the IAM role.
# This policy grants the permissions needed to write logs to CloudWatch.
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# This block creates the Lambda function.
# We are specifying the function name, the IAM role, the handler, the runtime, and the source code.
# We are also setting the environment variables for the bot token and chat ID.
resource "aws_lambda_function" "telegram_bot_lambda" {
  function_name = "telegram-bot-poll"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "bot_lambda.lambda_handler"
  runtime       = "python3.14"
  filename      = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      TELEGRAM_BOT_TOKEN = var.telegram_bot_token
      TELEGRAM_CHAT_ID   = var.telegram_chat_id
    }
  }
}

# This block creates an EventBridge rule to trigger the Lambda function on a schedule.
# We are using a cron expression to run the function every Friday at 12:00 UTC.
resource "aws_cloudwatch_event_rule" "schedule" {
  name                = "run-lambda-every-wednesday"
  description         = "Triggers the Telegram bot Lambda function"
  schedule_expression = "cron(45 12 ? * WED *)"
}

# This block creates a target for the EventBridge rule.
# The target is our Lambda function.
resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.schedule.name
  target_id = "trigger-lambda"
  arn       = aws_lambda_function.telegram_bot_lambda.arn
}

# This block grants EventBridge permission to invoke the Lambda function.
resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.telegram_bot_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.schedule.arn
}
