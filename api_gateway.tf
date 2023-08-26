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

# List of the route keys
locals {
    route_keys = ["check_price","add_item","delete_item","update_item","replace_item","subscribe_to_item"]
}

# Make a path/route/endpoint for each route key provided above.  It's all 
# pointing to the same lambda anyway, so just needs to change the key
module "apigw_route_check_price" {
    source = "./apigw_route_integration"
    for_each = toset(local.route_keys)
    apigw_id = aws_apigatewayv2_api.this.id
    integration_uri = aws_lambda_function.this.invoke_arn
    route_key = "POST /${each.value}"
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

