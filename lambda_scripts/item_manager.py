'''
-------------------------------------------------------------------------------
Item functions
-------------------------------------------------------------------------------
All code within revolves around manipulating items in the database.
Get, Update, Add, Delete

'''
# Lint exceptions
# ruff: noqa: E501

import boto3
import logging
from moto import mock_dynamodb2
import configuration
configuration.configure_logging()

class ItemManager:
    '''
    Made into a class to use the __init__ to centrally create the db access and
    pass to the rest of the functions
    '''
# -----------------------------------------------------------------------------
# Database client
# -----------------------------------------------------------------------------
# Split this out to a seperate function to reduce repetition,
# and centralise db connection errors
    def __init__(self, table_name):
        try:
            dynamodb = boto3.resource('dynamodb')
            self.db = dynamodb.Table(table_name)
        except Exception as e:
            logging.error(f"An error occurred while connecting to the database: {e}")
            raise SystemExit(f'Error: {e}')

# -----------------------------------------------------------------------------
# Get item functions - Item retrieval
# -----------------------------------------------------------------------------

# Requests all records from the database, returns just the items without
# the table search metadata
    def get_all_items(self):
        '''Returns all items in the database'''
        try:
            response = self.db.scan()
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

    def get_all_item_names(self):
        '''Returns all names of items in the database.  Used to:
        get all names
        then use a lookup to get the item you're after
        
        This is meant to save data by not returning all full items'''
        try:
            items = self.get_all_items()
            item_names = [item['item'] for item in items]
            logging.debug("----- Debug output -----\n" +
                          "Item names returned:\n" +
                          f"{item_names}\n" +
                          "----- /Debug output -----")
            return item_names
        except Exception as e:
            logging.error(f"An error occurred while retrieving item names: {e}")
            raise SystemExit(f'Error: {e}')

# Requests a single record from the database
    def get_item(self, item_name):
        '''Returns a single item having supplied the itemname.'''
        try:
            response = self.db.get_item(Key={'item': item_name})
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
    def add_item(self, new_item):
        '''Adds a new item to the database'''
        try:
            return self.db.put_item(
                Item=new_item,
                ConditionExpression="attribute_not_exists(#itemAttr)",
                ExpressionAttributeNames={"#itemAttr": "item"}
            )
        except self.meta.client.exceptions.ConditionalCheckFailedException:
            logging.error(f'Error: Item {new_item["item"]} already exists.')
            raise SystemExit(f'Error: Item {new_item["item"]} already exists.')
        except Exception as e:
            raise SystemExit(f'Error adding/updating item: {e}')


# -----------------------------------------------------------------------------
# Delete item function - Item creation
# -----------------------------------------------------------------------------
    def delete_item(self, item_name):
        '''Deletes an item from the database'''
        try:
            return self.db.delete_item(Key={'item': item_name})
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
# update_item(self, 'Test_Item1234567890', updated_values)
    def update_item(self, item_name, updated_attributes):
        '''Updates an item in place, only transfers and modifies the requisite fields'''
        try:
            update_expression_parts = []
            expression_attribute_values = {}

            for key, value in updated_attributes.items():
                update_expression_parts.append(f"{key} = :{key}")
                expression_attribute_values[f":{key}"] = value

            update_expression = "SET " + ", ".join(update_expression_parts)

            self.db.update_item(
                Key={'item': item_name},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values
            )
        except Exception as e:
            logging.error(f"Error updating item {item_name}: {e}")
            raise SystemExit(f'Error updating item: {e}')

# Identical to add_item(), except it's able to overwrite existing items
    def replace_item(self, item):
        '''Overwrites an existing item with a full item schema'''
        try:
            return self.db.put_item(Item=item)
        except Exception as e:
            raise SystemExit(f'Error adding/updating item: {e}')
# -----------------------------------------------------------------------------
# Tests - Make sure it works
# -----------------------------------------------------------------------------
    def testing(self):
        table_name = 'check_prices'

        # Start the DynamoDB mock
        with mock_dynamodb2():
            dynamodb = boto3.resource('dynamodb')

            # Create the table
            dynamodb.create_table(
                TableName=table_name,
                KeySchema=[{'AttributeName': 'item', 'KeyType': 'HASH'}],
                AttributeDefinitions=[{'AttributeName': 'item', 'AttributeType': 'S'}],
                ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
            )

            new_item = {
                'item': 'Test_Item1234567890',
                'current_price': '1.0',
                'sellers': [
                    {
                        'name': 'Test_Seller',
                        'url': 'https://www.test_seller.com',
                        'selector': 'search_parameters',
                        'min_price': '1.0',
                        'current_price': '1.0'
                    }
                ],
                'snsarn': '0000000000000000000000000000000000:test_topic'
            }

            item_manager_instance = ItemManager(table_name)
            item_manager_instance.add_item(new_item)
            item_manager_instance.get_item(new_item['item'])
            item_manager_instance.replace_item(new_item)
            item_manager_instance.delete_item(new_item['item'])

# -----------------------------------------------------------------------------
# Main - When the file's called direct, do testing
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    item_manager_instance = ItemManager("check_prices")  # Creating an instance of the class
    item_manager_instance.testing()  # Run the tests
