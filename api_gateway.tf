# Create an API Gateway HTTP API
resource "aws_apigatewayv2_api" "this" {
    name          = "check_prices"
    description = "API for checking if values on a webpage equal what we expect."
    protocol_type = "HTTP"
    cors_configuration {
        allow_origins = ["*"]
        allow_methods = ["POST", "GET", "OPTIONS"]
        allow_headers = ["content-type"]
        expose_headers = ["*"]
        max_age           = 1
    }
}

# Add the role to api gateway
resource "aws_api_gateway_account" "this" {
    cloudwatch_role_arn = aws_iam_role.this.arn
}

resource "aws_cloudwatch_log_group" "api_gateway" {
  # checkov:skip=CKV_AWS_158: Doesn't require KMS encryption
    name = "check_prices"
    retention_in_days = 7
}
# -----------------------------------------------------------------------------
# Create a /{check_price} resource for checking a price
# -----------------------------------------------------------------------------


# Create a /check_price route from the api to the backend integration
resource "aws_apigatewayv2_route" "check_price" {
    api_id    = aws_apigatewayv2_api.this.id
    route_key = "POST /check_price"
    target    = "integrations/${aws_apigatewayv2_integration.check_price.id}"
}

# Create a GET integration for /animal
resource "aws_apigatewayv2_integration" "check_price" {
    api_id                 = aws_apigatewayv2_api.this.id
    integration_type       = "AWS_PROXY"
    integration_uri        = aws_lambda_function.this.invoke_arn
    integration_method     = "POST"
    payload_format_version = "2.0"
}

# Create the API Gateway deployment
resource "aws_apigatewayv2_stage" "prod" {
    api_id      = aws_apigatewayv2_api.this.id
    name        = "prod"
    auto_deploy = true
    description = "Production deployment"
    access_log_settings {
        destination_arn = aws_cloudwatch_log_group.api_gateway.arn
        format = "{\"requestId\":\"$context.requestId\",\"extendedRequestId\":\"$context.extendedRequestId\",\"ip\":\"$context.identity.sourceIp\",\"caller\":\"$context.identity.caller\",\"user\":\"$context.identity.user\",\"requestTime\":\"$context.requestTime\",\"httpMethod\":\"$context.httpMethod\",\"resourcePath\":\"$context.resourcePath\",\"status\":\"$context.status\",\"protocol\":\"$context.protocol\",\"responseLength\":\"$context.responseLength\"}"
    }
}

