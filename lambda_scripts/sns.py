# -----------------------------------------------------------------------------
# SNS functions - All about those notifications
# -----------------------------------------------------------------------------

import boto3
import logging
import configuration
configuration.configure_logging()
import helpers

# Create topic.  Need a topic per item.  Returns the ARN of the newly created topic
def create_sns_topic(topic_name,item_name):
    return boto3.resource('sns',region_name=helpers.get_region_from_arn(topic_arn)).create_topic(
        Name=topic_name,
        Tags=[
            {
                'Key': 'Name',
                'Value': topic_name,
            },
            {
                'Key':'Project',
                'Value':'price_checker'
            },
            {
                'Key':'item',
                'Value':item_name
            }
        ]
    )['TopicArn']

# Subscribe an email using an email address and topic arn.
def subscribe_email_to_sns_topic(topic_arn, email):

    try:
        # Subscribe the email to the specified topic
        response = boto3.resource('sns', region_name=helpers.get_region_from_arn(topic_arn)).Topic(topic_arn).subscribe(
            Protocol='email',
            Endpoint=email
        )
        subscription_arn = response['SubscriptionArn']
        logging.info(f"Successfully subscribed email address: {email} to topic: {topic_arn}. Subscription ARN: {subscription_arn}")
        return subscription_arn
    except Exception as e:
        error_message = f"Error subscribing email {email} to topic {topic_arn}: {e}"
        logging.error(error_message)
        raise Exception(error_message)
# Don't need an unsub function as unsub links are sent in any correspondence.

# Send message
def send_notification(topic_arn,item_name,item_url,item_price):
    # Build the required ARN, assuming region = ap-southeast-2
    try:
        # Send the message
        response = boto3.resource('sns', region_name=helpers.get_region_from_arn(topic_arn)).publish(
            TopicArn=topic_arn,
            Message=f'Price of {item_name} has dropped to {item_price}.\n\n{item_url}',
            Subject='Price Drop Alert'
        )
        logging.info(f"Successfully sent message to topic: {topic_arn}. Message ID: {response['MessageId']}")
    except Exception as e:
        error_message = f"Error sending message to topic {topic_arn}: {e}"
        logging.error(error_message)
        raise Exception(error_message)

# Delete a topic.
def subscribe_email_to_sns_topic(topic_arn):
    try:
        # Subscribe the email to the specified topic
        response = boto3.resource('sns', region_name=helpers.get_region_from_arn(topic_arn)).Topic(topic_arn).delete()
        logging.info(f"Successfully deleted topic: {topic_arn}")
        return True
    except Exception as e:
        error_message = f"Error deleting topic {topic_arn}: {e}"
        logging.error(error_message)
        raise Exception(error_message)

def testing:
    print("WRITE THE TESTS")
    
if __name__ == '__main__':
    testing()