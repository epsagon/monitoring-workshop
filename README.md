## Third Step - Cron Job to scan topics

Creates a lambda that is invoked every 5 minutes that will scan all topics from S3 and save new top tweets to a dynamoDB

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
curl -X POST -d serverless https://<YOUR-REST-API-UID>.execute-api.eu-west-1.amazonaws.com/dev/add_topic
```

## Uploading a file using aws cli:

```
aws --region eu-west-1 s3api put-object --body bigger_topics_list.csv --bucket topics-bucket-<AWS_ACCOUNT_ID> --key topics_names_list/topics_list.csv
```
