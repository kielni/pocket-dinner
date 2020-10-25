# Dinner generator from Pocket items

Randomly choose 10 Pocket items tagged with `recipe` and display as a list.

Uses the [pocket python wrapper](https://github.com/tapanpandita/pocket) to get data from
the [Pocket API](https://getpocket.com/developer/docs/overview).

Deploy as an AWS Lambda function with [serverless](https://www.serverless.com/framework/docs/getting-started/).

## setup

```
pip install -r dev-requirements.txt
pip install -r requirements.txt
```

Get Pocket keys:

  - create an app to get a consumer key: https://getpocket.com/developer/apps/new
  - get access token for app: https://reader.fxneumann.de/plugins/oneclickpocket/auth.php

Add parameters to [AWS Parameter Store](https://us-east-1.console.aws.amazon.com/systems-manager/parameters/):

  - POCKET_CONSUMER_KEY
  - POCKET_ACCESS_TOKEN

Add parameters to environment:

```
export POCKET_CONSUMER_KEY="123abc..."
export POCKET_ACCESS_TOKEN="123abc..."
export PARAMS_ARN="arn:aws:ssm:us-west-1:*accountId*:parameter/*"
```

## deploy

```
black .
flake8 .
mypy .
serverless deploy
serverless invoke -f pocket_dinner
```

Add an [API Gateway trigger](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html)
to access via HTTP.
