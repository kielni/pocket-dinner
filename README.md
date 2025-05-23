# Warning: for archival interest only

Pocket shut down as of 7/8/25; see https://support.mozilla.org/en-US/kb/future-of-pocket

They have a page describing how to export data, but it includes only URLs:

> Your export file will include links (URLs) of your saved items. The export does not extract the text of saved links. Additionally, the export does contain tags or highlights.

Run [download.py](download.py) to export title, url, excerpt, and tags while the API is still available.

Sample:

```
  {
    "title": "How much to water a fruit tree in Southern California, roughly",
    "url": "https://gregalder.com/yardposts/how-much-to-water-a-fruit-tree-in-southern-california-roughly/",
    "excerpt": "These are the rules of thumb that I try to keep in mind for watering fruit trees during late spring, summer, and early fall (think May or June into October): If the fruit tree is two feet wide (about as wide as your body), then give it two gallons each week.",
    "tags": [
      "garden"
    ]
  },
```

# Dinner generator from Pocket items

Randomly choose 10 Pocket items tagged with `dinner` and display as a list.

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
