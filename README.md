## Fourth Step - Async Message Sending

Split bottleneck load to multiple functions

## Deploy:
```
sls deploy
```

## Using the API:
When deploying with sls you will see the rest api uid, which you have to use here:

```
curl -X POST -d serverless https://<YOUR-REST-API-UID>.execute-api.eu-west-1.amazonaws.com/dev/add_topic
```
