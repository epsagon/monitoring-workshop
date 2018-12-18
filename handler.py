"""
handlers for monitoring/debugging workshop
"""
import os
import boto3
import botocore

S3_RESOURCE = boto3.resource('s3')
TOPICS_LIST_KEY = 'topics_names_list/topics_list.csv'


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


def _get_topics_list(topics_names_obj):
    """ gets the names list from `topics_names_obj` """
    try:
        names_list_response = topics_names_obj.get()
        return names_list_response['Body'].read().split(b',')
    except botocore.errorfactory.ClientError:
        return []


if __name__ == '__main__':
    pass
