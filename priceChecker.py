import requests
from bs4 import BeautifulSoup

# Dell S3423CDW
SEARCH_ITEMS = [
    {
        'URL': 'https://www.dell.com/en-au/shop/dell-34-curved-usb-c-monitor-s3423dwc/apd/210-beic/monitors-monitor-accessories',
        'CURRENT_VALUE': '$697.40',
        'SELECTOR': 'div.smart-popover-btn'
    },
    {
        'URL': 'https://www.umart.com.au/product/aoc-34in-wqhd-va-144hz-freesync-curved-gaming-monitor-cu34g2x-54626',
        'CURRENT_VALUE': '529.0',
        'SELECTOR': 'span[itemprop="price"].goods-price'
    }
]

def check_all_items():
    for item in SEARCH_ITEMS:
        check_price_change(item['URL'], item['CURRENT_VALUE'], item['SELECTOR'])

def check_price_change(url, current_value, selector):
    try:
        response = requests.get(url)
        response.raise_for_status()  # will raise an HTTPError if the HTTP request returned an unsuccessful status code
        soup = BeautifulSoup(response.text, 'html.parser')
        value_element = soup.select_one(selector)
        if value_element:
            new_value = value_element.text.strip()
            if new_value != current_value:
                print(f"Price Change Alert for {url}")
                print(f"The price has changed from {current_value} to {new_value}.")
            else:
                print(f"No change in price for {url}.")
        else:
            print(f"Could not find the price element for {url} using the selector: {selector}.")
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred for {url}: {http_err}")
    except Exception as err:
        print(f"Error occurred for {url}: {err}")

if __name__ == '__main__':
    check_all_items()
