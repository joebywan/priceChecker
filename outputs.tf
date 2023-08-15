# Outputs the dns endpoint of the api gateway
output "api_gateway_endpoint" {
  value = aws_apigatewayv2_stage.prod.invoke_url
}