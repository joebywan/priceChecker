'''-------------------------------------------------------------------------------
Helper functions - Those that don't fit anywhere in particular, but are
useful nonetheless
-------------------------------------------------------------------------------

'''
import logging
import boto3
import configuration
configuration.configure_logging()

# Parse ARN, splits it into it's requisite parts, then returns the list.  I know
# it's nothing special, just making things more readable
def parse_arn(arn):
    return arn.split(":")

# Query EC2 for all regions, returns as a list
def get_all_regions(default_region=configuration.default_region):
    try:
        session = boto3.Session(region_name=default_region)
        ec2 = session.client('ec2')
        return [region['RegionName'] for region in ec2.describe_regions()['Regions']]
    except Exception as e:
        error = f"get_all_regions: Error retrieving regions: {str(e)}"
        logging.error(error)
        raise SystemExit(error)

# Get the region from the split arn by comparing each element to the list of regions
def get_region_from_arn(arn):
    all_regions = get_all_regions()
    for element in parse_arn(arn):
        if element in all_regions:
            return element
    raise SystemExit(f"get_region_from_arn: Couldn't retrieve region from {arn}")

# Get the account id from the split arn by checking for integers & length
def get_account_id_from_arn(arn):
    for element in parse_arn(arn):
        if isinstance(element, int):
            if len(element) == 12:
                return element
    raise SystemExit(f"get_account_id_from_arn: Couldn't retrieve account id from {arn}")
