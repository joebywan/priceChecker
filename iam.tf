# IAM Role and policy for API Gateway to send logs to CloudWatch
resource "aws_iam_role" "this" {
    name = "API-Gateway_cloudwatch_role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17",
        Statement = [
        {
            Action = "sts:AssumeRole",
            Effect = "Allow",
            Principal = {
            Service = "apigateway.amazonaws.com"
            }
        }
        ]
    })
}

resource "aws_iam_role_policy_attachment" "this" {
    role       = aws_iam_role.this.name
    policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs"
}

# Lambda IAM Role and policies for required access
data "aws_iam_policy" "cloudwatch" {
  # returns the arn for the aws cloudwatch logging policy
  name = "AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role" "lambda" {
  name = "lambda_role"

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

resource "aws_iam_policy" "lambda" {
  name = "lambda_policy"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Action" : [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:Scan"
        ],
        "Effect" : "Allow",
        "Resource" : [
          "${aws_dynamodb_table.this.arn}"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_to_cloudwatch" {
  policy_arn = data.aws_iam_policy.cloudwatch.arn
  role       = aws_iam_role.lambda.name
}

resource "aws_iam_role_policy_attachment" "lambda" {
  policy_arn = aws_iam_policy.lambda.arn
  role       = aws_iam_role.lambda.name
}