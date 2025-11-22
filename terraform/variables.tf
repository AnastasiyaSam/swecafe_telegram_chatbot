# variables.tf

# This block defines the AWS region variable.
# We are setting the default value to "us-east-1".
variable "aws_region" {
  description = "The AWS region to deploy resources in."
  type        = string
  default     = "us-east-1"
}

# This block defines the Telegram bot token variable.
# We are marking it as sensitive to prevent it from being displayed in logs.
variable "telegram_bot_token" {
  description = "The token for the Telegram bot."
  type        = string
  sensitive   = true
}

# This block defines the Telegram chat ID variable.
variable "telegram_chat_id" {
  description = "The ID of the Telegram chat to send messages to."
  type        = string
}
