# Create a /check_price route from the api to the backend integration
resource "aws_apigatewayv2_route" "check_price" {
    api_id    = var.apigw_id
    route_key = var.route_key
    target    = "integrations/${aws_apigatewayv2_integration.check_price.id}"
}

# Create a GET integration for /animal
resource "aws_apigatewayv2_integration" "check_price" {
    api_id                 = var.apigw_id
    integration_type       = "AWS_PROXY"
    integration_uri        = var.integration_uri
    integration_method     = "POST"
    payload_format_version = "2.0"
}

variable "route_key" {
    type = string
}

variable "apigw_id" {
    type = string
}

variable "integration_uri" {
    type = string
}