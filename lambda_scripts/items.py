# -----------------------------------------------------------------------------
# Item functions
# -----------------------------------------------------------------------------
# All code within revolves around manipulating items in the database.  
# Get, Update, Add, Delete

import boto3
import logging
import configuration
configuration.configure_logging()

# -----------------------------------------------------------------------------
# Database client
# -----------------------------------------------------------------------------
# Split this out to a seperate function to reduce repetition, 
# and centralise db connection errors
def database_connection(table_name):
    try:
        dynamodb = boto3.resource('dynamodb')
        return dynamodb.Table(table_name)
    except Exception as e:
        logging.error(f"An error occurred while connecting to the database: {e}")
        raise SystemExit(f'Error: {e}')

# -----------------------------------------------------------------------------
# Get item functions - Item retrieval
# -----------------------------------------------------------------------------

# Requests all records from the database, returns just the items without
# the table search metadata
def get_all_items(db_resource):
    try:
        response = db_resource.scan()
        logging.debug("----- Debug output -----\n" +
                      "Response returned:\n" +
                      f"{response}\n" +
                      "----- /Debug output -----")
        items = response['Items']
        logging.debug("----- Debug output -----\n" + 
                      "items returned:\n" +
                      f"{items}\n" +
                      "----- /Debug output -----")
        return items
    except Exception as e:
        logging.error(f"An error occurred while retrieving items: {e}")
        raise SystemExit(f'Error: {e}')

# Requests a single record from the database
def get_item(db_resource, item_name):
    try:
        response = db_resource.get_item(Key={'item': item_name})
        if 'Item' in response:
            return response['Item']
        else:
            logging.error(f"Item {item_name} not found in database.")
            raise SystemExit(f'Error: Item {item_name} not found in database.')
    except Exception as e:
        logging.error(f"An error occurred while retrieving item {item_name}: {e}")
        raise SystemExit(f'An error occurred while retrieving item {item_name}: {e}')


# -----------------------------------------------------------------------------
# Add item functions - Item creation
# -----------------------------------------------------------------------------

# NOTE: Should probably do testing for correct item structure & 
# minimum information required.
# NOTE: Will fail if the item already exists. Might be worth a force option?
def add_item(db_resource, new_item):
    try:
        return db_resource.put_item(
            Item=new_item,
            ConditionExpression="attribute_not_exists(#itemAttr)",
            ExpressionAttributeNames={"#itemAttr": "item"}
        )
    except db_resource.meta.client.exceptions.ConditionalCheckFailedException:
        logging.error(f'Error: Item {new_item["item"]} already exists.')
        raise SystemExit(f'Error: Item {new_item["item"]} already exists.')
    except Exception as e:
        raise SystemExit(f'Error adding/updating item: {e}')


# -----------------------------------------------------------------------------
# Delete item function - Item creation
# -----------------------------------------------------------------------------
def delete_item(db_resource, item_name):
    try:
        return db_resource.delete_item(Key={'item': item_name})
    except Exception as e:
        raise SystemExit(f'Error deleting item: {e}')

# -----------------------------------------------------------------------------
# Update item function - Change an existing item
# -----------------------------------------------------------------------------
# Example use:
# updated_values = {
#     'current_price': '2.0',
#     'selector': 'new_search_parameters'
# }
# update_item(db_resource, 'Test_Item1234567890', updated_values)
def update_item(db_resource, item_name, updated_attributes):
    try:
        update_expression_parts = []
        expression_attribute_values = {}
        
        for key, value in updated_attributes.items():
            update_expression_parts.append(f"{key} = :{key}")
            expression_attribute_values[f":{key}"] = value

        update_expression = "SET " + ", ".join(update_expression_parts)
        
        db_resource.update_item(
            Key={'item': item_name},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
    except Exception as e:
        logging.error(f"Error updating item {item_name}: {e}")
        raise SystemExit(f'Error updating item: {e}')

# Identical to add_item(), except it's able to overwrite existing items
def replace_item(db_resource, item):
    try:
        return db_resource.put_item(Item=item)
    except Exception as e:
        raise SystemExit(f'Error adding/updating item: {e}')
# -----------------------------------------------------------------------------
# Tests - Make sure it works
# -----------------------------------------------------------------------------
def testing(table_name):
    new_item = {
        'item':'Test_Item1234567890',
        'current_price':'1.0',
        'sellers':[
            {
                'name':'Test_Seller',
                'url':'https://www.test_seller.com',
                'selector':'search_parameters',
                'min_price':'1.0',
                'current_price':'1.0'
            }
        ]
    }
    add_item(table_name,new_item)
    get_item(table_name,new_item['item'])
    replace_item(table_name,new_item)
    delete_item(table_name,new_item['item'])

# -----------------------------------------------------------------------------
# Main - When the file's called direct, do testing
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    testing(database_connection("check_prices"))
