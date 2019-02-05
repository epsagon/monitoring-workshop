## First Step - Twitter API Lambda

This will create a simple Lambda function behind an API Gateway that will look for a top tweet with a specific hashtag and return it with the screen name of the author

## Install Dependencies:

```
npm install serverless serverless-python-requirements serverless-dotenv-plugin
pip install -r requirements.txt
```

## Deploy:
```
sls deploy
```

## Using the API:
When deploying with `sls` you will see the REST API UID, which you have to use here:

```
curl -X POST -d serverless https://<YOUR-REST-API-UID>.execute-api.eu-west-1.amazonaws.com/dev/top_tweet
```

## Query CloudWatch Logs:

Last logs:
```
sls logs -f get-top-tweet
```

Tail logs:
```
sls logs -f get-top-tweet -t
```

## Running it locally:

```
sls invoke local -f get-top-tweet -p data.json
```


