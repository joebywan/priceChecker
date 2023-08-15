# In progress

def lambda_handler(event, context):
    db = os.environ['table_name']   # Pull the DynamoDB name from the environment variable "table_name"
    print("----- EVENT FROM LAMBDA -----")
    print(event)
    price_check = check_price_change()
    print("----- PRICE_CHECK RESULT -----")
    print(price_check)
    return create_response(price_check, 200)

def create_response(body, status_code):
    print("---- This is the body of the response ----")
    print(body)
    print("---- body end ----")
    return {
        'statusCode': status_code,
        'body': json.dumps(body) if not isinstance(body, str) else body,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        }
    }