# -----------------------------------------------------------------------------
# Price functions
# -----------------------------------------------------------------------------
# All code within revolves around pulling sites, searching for the price and 
# the logic for what to do next

import requests
from bs4 import BeautifulSoup
import logging  # FUCKING USE ME
from logging_configuration import configure_logging
configure_logging()

# Check the URL, search using BS & return the value.
def get_current_price(web_address,search_term):
    try:
        response = requests.get(web_address)
        response.raise_for_status()  # Raise an exception for HTTP errors.

        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.select_one(search_term)
        if price_element:
            return price_element.text.strip()
        else:
            return None
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

# Checks the price, updates the seller current & minimum prices, and the 
# item's current price.  Returns the modified item for reinsertion into the db
def check_item(item):
    for seller in item['sellers']:
        seller['current_price'] = get_current_price(seller['url'],seller['selector'])
        if seller['min_price'] > seller['current_price']:
            seller['min_price'] = seller['current_price']
    seller_prices = []
    for seller in item['sellers']:
        seller_prices.append(seller['current_price'])
    item['current_price'] = seller_prices.min()
    return item

# Essentially just function for a loop.  Iterates all items, and checks each one
# Returns a list of items with updated prices
def check_items(items):
    return_items = []
    for item in items:
        return_items.append(check_item(item))
    return return_items
# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------

# The values returned by the website isn't necessarily an integer.  This 
# function is for stripping them down to the integer.
def convert_to_int(value):
    # If the value is already an integer or float, simply convert to int
    if isinstance(value, (int, float)):
        return int(value)

    # If it's a string, remove commas, strip non-integer characters from the 
    # front, and convert to int
    if isinstance(value, str):
        # Removing commas
        value = value.replace(',', '')
        # Using lstrip to remove non-integer characters from the beginning
        stripped_value = value.lstrip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ$ ')
        return int(float(stripped_value))

    # If none of the above, raise a ValueError
    raise SystemExit(f"Invalid type for conversion: {type(value)}")



# -----------------------------------------------------------------------------
# Tests - Make sure it works TBC
# -----------------------------------------------------------------------------
def test_prices():
    web_address="COMPLETE ME"
    search_term="COMPLETE ME"
    get_current_price(web_address,search_term)

# -----------------------------------------------------------------------------
# Main - When the file's called direct, do testing
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    test_prices()
