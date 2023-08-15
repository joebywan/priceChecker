# Used to check the size of an item, if item sizes blow out from too many 
# sellers or emails, it might be more economical to use update_item 
# instead of replace_item.

import json

new_item = {
    'item':'Test_Item1234567890',
    'current_value':'1.0',
    'sellers':[
        {
            'name':'Test_Seller',
            'url':'https://www.test_seller.com',
            'selector':'search_parameters',
            'min_price':'1.0',
        }
    ],
    'subscribers':[
        'email1@test.com',
        'email2@test.ccom',
    ]
}

size_bytes = len(json.dumps(new_item))
print(f"Size of the item: {size_bytes} bytes")
