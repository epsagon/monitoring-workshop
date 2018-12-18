"""
Model for the dynamodb influencers table
"""
import os
import boto3

TABLE_NAME = os.getenv('INFLUENCERS_TABLE_NAME')
if TABLE_NAME:
    DYNAMODB_CLIENT = boto3.resource(
        'dynamodb', region_name=os.getenv('AWS_REGION'))
    INFLUENCERS_TABLE = DYNAMODB_CLIENT.Table(TABLE_NAME)


class Influencer:
    """
    Represents and influencer
    """
    def __init__(self, name, topic):
        self.name = name
        self.topic = topic

    def write_to_db(self):
        """ write influencer to dynamodb """
        INFLUENCERS_TABLE.put_item(
            Item={
                'influencer_name': self.name,
                'topic': self.topic,
            }
        )

    @staticmethod
    def exists(name, topic):
        """ return True if  """
        return 'Item' in INFLUENCERS_TABLE.get_item(
            Key={
                'influencer_name': name,
                'topic': topic,
            }
        )
