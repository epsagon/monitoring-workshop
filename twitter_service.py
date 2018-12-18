"""
Mimicks another service that is used, this time it just calls twitter,
this will allow us to use this other 'service' to inject problems to
our little serverless system.
"""
import os
import json
from datetime import datetime, timedelta
import twitter


def get_top_tweet(event, _context):
    """
    returns the most popular tweet from the last day with
    #{topic}
    """
    topic = event['body']

    # to allow both local and api-gateway invocation
    # api-gateway will send input in bytes
    if hasattr(topic, 'decode'):
        topic = topic.decode('utf-8')

    twitter_api = twitter.Api(
        consumer_key=os.getenv('CONSUMER_KEY'),
        consumer_secret=os.getenv('CONSUMER_SECRET'),
        access_token_key=os.getenv('ACCESS_TOKEN_KEY'),
        access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'),
        sleep_on_rate_limit=True,
    )
    since_time = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    top_tweet = twitter_api.GetSearch(
        term=('#' + str(topic)),
        count=1,
        result_type='mixed',
        since=since_time,
    )
    body = json.dumps({
        'screen_name': top_tweet[0].user.screen_name,
        'tweet': top_tweet[0].text,
        })
    return {
        'statusCode': 200,
        'body': body,
    }


if __name__ == '__name__':
    pass
