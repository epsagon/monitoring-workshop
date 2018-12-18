"""
handlers for monitoring/debugging workshop
"""
import os
import json
import boto3
import botocore
import requests
from influencer_model import Influencer

S3_RESOURCE = boto3.resource('s3')
TOPICS_LIST_KEY = 'topics_names_list/topics_list.csv'
SQS_CLIENT = boto3.client('sqs')


def add_from_api_gateway(event, _):
    """
    add new topic from api gateway event
    """
    topics_bucket_name = os.getenv('TOPICS_BUCKET_NAME')
    topics_names_obj = S3_RESOURCE.Object(
        topics_bucket_name, TOPICS_LIST_KEY)

    topics_list = _get_topics_list(topics_names_obj)
    topics_list.append(str.encode(event['body']))
    topics_list = b','.join(topics_list)

    msg = f'new topics_list = {topics_list}'
    print(msg)
    put_response = topics_names_obj.put(Body=topics_list)

    return {
        'statusCode': put_response['ResponseMetadata']['HTTPStatusCode'],
        'body': msg,
    }


def scan_all_topics(_event, _):
    """
    scan all topics from S3/Dynamodb
    for each topic s
    """
    topics_bucket_name = os.getenv('TOPICS_BUCKET_NAME')
    topics_names_obj = S3_RESOURCE.Object(
        topics_bucket_name, TOPICS_LIST_KEY)
    topics_list = _get_topics_list(topics_names_obj)
    for topic in topics_list:
        scan_topic(topic.decode('utf-8'))


def scan_topic(topic):
    """
    scan a specific topic
    write top tweet and twitter to dynamodb
    """
    print(f'entering scan_topic with topic = {topic}')
    url = os.getenv('TWITTER_SERVICE_API')
    response = requests.post(url, data=topic)
    try:
        top_tweet = response.json()
    except ValueError:
        top_tweet = None
    if not top_tweet:
        print(f'No tweet was found for topic = {topic}')
        return

    influencer = top_tweet['screen_name']

    if not Influencer.exists(influencer, topic):
        _handle_new_influencer(influencer, topic)


def alert(event, _):
    """
    alert due to new influencing twitter
    """
    print(f'received event = {event}')


def _handle_new_influencer(influencer, hash_tag):
    """
    add the new influencer to dynamodb and send SQS message
    """
    Influencer(influencer, hash_tag).write_to_db()
    response = SQS_CLIENT.send_message(
        QueueUrl=os.getenv('NEW_INFLUENCER_SQS'),
        MessageBody=json.dumps({'influencer': influencer, 'topic': hash_tag}),
    )
    print(f'MessageId = {response["MessageId"]}')


def _get_topics_list(topics_names_obj):
    """ gets the names list from `topics_names_obj` """
    try:
        names_list_response = topics_names_obj.get()
        return names_list_response['Body'].read().split(b',')
    except botocore.errorfactory.ClientError:
        return []


if __name__ == '__main__':
    pass
