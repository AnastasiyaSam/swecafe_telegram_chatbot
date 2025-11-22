# outputs.tf

# This block defines an output for the Lambda function's name.
output "lambda_function_name" {
  description = "The name of the created Lambda function."
  value       = aws_lambda_function.telegram_bot_lambda.function_name
}

# This block defines an output for the Lambda function's ARN.
output "lambda_function_arn" {
  description = "The ARN of the created Lambda function."
  value       = aws_lambda_function.telegram_bot_lambda.arn
}
