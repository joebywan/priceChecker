# TODO

## Data schema
{
    'item':{'S':'Dell S3423CDW Monitor'},
    'current_value':{'S':'$697.40'},
    'sellers':[
        {
            'name':{'S':'Dell'},
            'url':{'S':'https://www.dell.com/en-au/shop/dell-34-curved-usb-c-monitor-s3423dwc/apd/210-beic/monitors-monitor-accessories'},
            'selector':{'S':'div.smart-popover-btn'}
            'minimum_price':{'S':'$697.40'},
            'current_price':{'S':'1.0'}
        }
}

## Functions
### Database
* Get all items **Implemented**
    * Grab all items from DynamoDB and return the list of dict
* Get all item names /get_item_names  **Implemented**
    * Grab all item names from DynamoDB and return the list of dict.  Don't want to expose the Get all items function above externally to avoid unneeded data download.
* Get 1 item /get_item/{item}  **Implemented**
    * Uses Boto3 to pull only the item
* Add item /add_item   **Implemented**
    * Supplied with the info from the schema, adds an item to the DynamoDB database
* Update item /update_item   **Implemented**
    * Supplied with the item or some filter, update an item
* Delete item /delete_item/{item}   **Implemented**
    * Supplied with the item or some filter, delete an item

### Web scraping/prices
* Get 1 price /check_price/{item}  **Implemented**
    * Supplied with url, current_value, selector.  Gets the url, parses it with beautifulsoup and returns the current price
* check_all_prices /check_prices/  **Implemented**
    * Use 'Get all items' and using a loop invokes the 'Get 1 price' function for each item

### Lambda
* Lambda_handler
    * Lambda_handler function to be invoked by lambda.  Will decide on which function to use based on the route_key.  Still need to decide on names for each.
* Create response back to the user
    * Mainly used to standardise the responnses back through API Gateway.  Adding requisite headers and status codes etc.
* Add error handling?  Have them raised up to here?


### SNS
* Create SNS Topic **Implemented**
    * Will need this for when a new item is added, so will have to call it from/along with the add_item function.  Now that I'm at this point, it's definitely going to differentiate the add_item from replace_item, as replace_item won't require the SNS modifications.  I read that SNS has a limit of 100,000 SNS topics per account, so I should monitor how many are in the account after each one's created, and if it's 50,000 or more, I should look at coding up SES or an alternative, if I can do it cheaper than SES
* Delete SNS Topic **Implemented**
    * When deleting an item, the associated topic will need to be deleted.  
* Send SNS Message **Implemented**
    * Will need to send an SNS message to the topic when an item shows a lower price than the last detected current_price.
* Subscribe to Topic  **Implemented**
    * Don't need an unsubscribe function, or atleast see if SNS communications have an unsubscribe link in if it's via email.

### Logic
This is where the tying things together will occur.
E.g. Create an item, and a requisite SNS topic.
Wrap around the database functions to connect to the DB first before any DB calls are made & then reusing that connection.
Will have to figure this out as I flesh out the rest.

### Eventbridge
I was suggested to have a seperate Eventbridge function, it'll be using the existing functions, but just setup for Eventbridge to call it incase there's any unique logic required there.

## Endpoints for API  **Needs testing, TF code written**
/add_item - Supply an item, creates a sns topic, then the item in dynamodb
/delete_item - Deletes the SNS topic and the item
/update_item - Modifies an item
/replace_item - Replaces an item with a full item object
/check_price - Initiate a price check, return the current price
/subscribe_to_item - Supply an item name and an email, it'll lookup the sns, and subscribe.  Still requires email verification.

# Remaining
Get 'er done?!?!
Ignore people requesting a frontend, or see how amenable ChatGPT is to spitting it out.