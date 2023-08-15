# Zip up the lambda function for use in the lambda function resource
data "archive_file" "this" {
  type        = "zip"
  # source_file = "./priceChecker.py"
  source_dir = "./lambda_package"
  output_path = "./lambda_function.zip"
}

# Lambda function for price checker, we'll see whether I split it into multiple.  
# Investigating use of the url path to decide what's done by the function.
resource "aws_lambda_function" "this" {
  # checkov:skip=CKV_AWS_50: ADD REASON
  # checkov:skip=CKV_AWS_115: ADD REASON
  # checkov:skip=CKV_AWS_116: ADD REASON
  # checkov:skip=CKV_AWS_117: ADD REASON
  # checkov:skip=CKV_AWS_173: ADD REASON
  function_name    = "check_prices"
  filename         = "lambda_function.zip"
  role             = aws_iam_role.lambda.arn
  handler          = "priceChecker.lambda_handler"
  runtime          = "python3.8"
  source_code_hash = data.archive_file.this.output_base64sha256
  timeout = 30
  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.this.name
    }
  }
}

# Gotta allow API Gateway to use the Lambda function
resource "aws_lambda_permission" "this" {
  statement_id  = "Allow_APIGW_to_invoke_my_function"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.this.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.this.execution_arn}/*"
}

# Create a CloudWatch logging group to store execution logs
resource "aws_cloudwatch_log_group" "lambda" {
  # checkov:skip=CKV_AWS_158: ADD REASON
  name              = "/aws/lambda/${aws_lambda_function.this.function_name}"
  retention_in_days = 7
}