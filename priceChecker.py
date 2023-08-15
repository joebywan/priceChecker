# Original script, deprecated in favour of serverless structure.  Will work on it's own, but not with the api/lambda/dynamodb structure

import requests
from bs4 import BeautifulSoup
import os

# Future notes
# Could use in lambda with API gateway & eventbridge with SNS.
# Output current price to console which would show up in logs, but if a new price is detected, send an email via SNS
# Use API Gateway to expose the ability to add new dynamodb items containing url:<url>,CURRENT_VALUE: <CURRENT_VALUE>,selector: <selector>
# Then loop through all dynamodb items.  This'd likely need more fields like a name/description to use when sending emails, but then
# it'd be usable for checking multiple sites and emailing if any of them change.
# Can also check the price, and track the max price, but email if the price goes low.


# Beautifulsoup documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/ Need this for the SELECTOR syntax

# Dell S3423CDW
SEARCH_ITEMS = [
    {
        'URL' : 'https://www.dell.com/en-au/shop/dell-34-curved-usb-c-monitor-s3423dwc/apd/210-beic/monitors-monitor-accessories',
        'CURRENT_VALUE' : '$697.40',
        'SELECTOR' : 'div.smart-popover-btn'
    },
    {
        'URL' : 'https://www.umart.com.au/product/aoc-34in-wqhd-va-144hz-freesync-curved-gaming-monitor-cu34g2x-54626',
        'CURRENT_VALUE' : '529.0',
        'SELECTOR' : 'span[itemprop="price"].goods-price'
    }
]

# retrieve all dynamodb items, and put them into a dictionary usable to check each of them


# Umart test for different website
def check_all_items():
    for item in SEARCH_ITEMS:
        check_price_change(item['URL'],item['CURRENT_VALUE'],item['SELECTOR'])



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

def lambda_handler(event, context):
    db = os.environ['table_name']   # Pull the DynamoDB name from the environment variable "table_name"
    print("----- EVENT FROM LAMBDA -----")
    print(event)
    price_check = check_price_change()
    print("----- PRICE_CHECK RESULT -----")
    print(price_check)
    return create_response(price_check, 200)

if __name__ == '__main__':
    db = "check_prices"
    check_all_items()
    get_all_items()