import item_manager
import price
import sns

def check_price(item_name):
    return price.get_current_price(item_manager.get_item(item_name))

def check_all_prices():
    items = item_manager.get_all_item_names()
    checked_items = []

    for item in items:
        checked_items.extend(check_price(item))

    return checked_items

def create_item(item):
    item['snsarn'] = sns.create_sns_topic(item['item'])
    item_manager.add_item(item)
    return True
