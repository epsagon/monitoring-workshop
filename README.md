## First Step - Twitter API lambda

This will create a simple lambda behind an API Gateway that will look for a top tweet with a specific hashtag and return it with the screen name of the author

## Install Dependencies:

```
npm install serverless serverless-python-requirements serverless-dotenv-plugin
```

## Deploy:
```
sls deploy
```

## Using the API:
When deploying with sls you will see the rest api uid, which you have to use here:

```
curl -X POST -d serverless https://<YOUR-REST-API-UID>.execute-api.eu-west-1.amazonaws.com/dev/top_tweet
```
