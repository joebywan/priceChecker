resource "aws_dynamodb_table" "this" {
    # checkov:skip=CKV_AWS_28: ADD REASON
    # checkov:skip=CKV_AWS_119: ADD REASON
    name         = "check_prices"
    billing_mode = "PAY_PER_REQUEST"
    hash_key     = "item"

    attribute {
        name = "item"
        type = "S"
    }

    tags = {
        Name = "check_prices_items_table" 
    }
}

resource "aws_dynamodb_table_item" "cat_test" {
    table_name = aws_dynamodb_table.this.name
    hash_key   = aws_dynamodb_table.this.hash_key
    item       = <<ITEM
    {
        "item":{"S":"AOC 34in WQHD VA 144Hz FreeSync Curved Gaming Monitor (CU34G2X)"},
        "current_value":{"S":"579.0"},
        "url":{"S":"https://www.umart.com.au/product/aoc-34in-wqhd-va-144hz-freesync-curved-gaming-monitor-cu34g2x-54626"},
        "selector":{"S":"span[itemprop=\"price\"].goods-price"},
        "previous_price":{"S":"579.0"}
    }
    ITEM
}

resource "aws_dynamodb_table_item" "dog_test" {
    table_name = aws_dynamodb_table.this.name
    hash_key   = aws_dynamodb_table.this.hash_key
    item       = <<ITEM
    {
        "item":{"S":"Dell S3423CDW Monitor"},
        "current_value":{"S":"$697.40"},
        "url":{"S":"https://www.dell.com/en-au/shop/dell-34-curved-usb-c-monitor-s3423dwc/apd/210-beic/monitors-monitor-accessories"},
        "selector":{"S":"div.smart-popover-btn"},
        "previous_price":{"S":"697.40"}
    }
    ITEM
}