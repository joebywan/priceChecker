# -----------------------------------------------------------------------------
# SNS functions - All about those notifications
# -----------------------------------------------------------------------------

import boto3
import logging
from logging_configuration import configure_logging
configure_logging()

# Subscribe an email using an email address and topic arn.
def subscribe_email_to_sns_topic(topic_name, email, region='ap-southeast-2'):
    
    # Build the required ARN, assuming region = ap-southeast-2
    topic_arn = f'arn:aws:sns:{region}:123456789012:{topic_name}'
    
    try:
        # Subscribe the email to the specified topic
        response = boto3.client('sns', region_name=region).sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=email
        )
        subscription_arn = response['SubscriptionArn']
        logging.info(f"Successfully subscribed email address: {email} to topic: {topic_name}. Subscription ARN: {subscription_arn}")
        return subscription_arn
    except Exception as e:
        error_message = f"Error subscribing email {email} to topic {topic_name}: {e}"
        logging.error(error_message)
        raise Exception(error_message)
