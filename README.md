# sql-lambda
Register backends with AWS Dynamodb and execute sql queries with API Gateway,
which talks to Lambda.

## Usage

Once you've obtained an API_KEY from your administrator or deploying the api, I recommend using [httpie](httpie.org) or [requests](http://docs.python-requests.org/en/master/) in [jupyter notebook](https://github.com/jupyter/notebook) to call the endpoints.

#### http commands in the terminal
```bash
# To list all routes this service contains
http https://xxxxxx.execute-api.us-east-1.amazonaws.com/dev/sql x-api-key:$API_KEY
```

#### requests library in python

```python
from os import environ as env

import requests

url = 'https://xxxxxx.execute-api.us-east-1.amazonaws.com/dev/sql'
headers = {'x-api-key': env['API_KEY']}
response = requests.get(url, headers=headers) 
print(response.json)

```

## Prerequisites for deployment

* AWS profile name in ~/.aws/credentials and valid credentials for deploying to Zappa.
* Update zappa_settings-example.json for your environments
* You will need an API Gateway key for encryption/decryption. 
* You will need a service account or user credentials in order to connect.
* Obviously do not share your api key with anyone as they can access whatever you can access with it.

I **STRONGLY** advise you to use `api_key_required: true` as well as [IP restriction in IAM](http://benfoster.io/blog/aws-api-gateway-ip-restrictions) to limit usage of this API to within your VPN.

## Deploying the api
Assuming you're already familiar with zappa deployments here.

You will need to build and run these commands in the provided Dockerfile outside of Linux.

Docker based install instructions [here](https://github.com/danielwhatmuff/zappa#using-exported-aws_default_region-aws_secret_access_key-and-aws_access_key_id-env-vars)

Linux 
```
cd ./sql/api
virtualenv venv
. ./venv/bin/activate
pip install -r requirements.txt
zappa deploy dev
```

## Deploying the registration app


Please note to use a separate virtualenv for the api.
```bash
deactivate # We are using a separate virtualenv as these reqs/dockerfile are heavier.
cd ./sql/app
# same as above in a separate virtualenv
```


## First Step for DBA: Register your backend(s)

1. Go to your deployed app URL that zappa provides
2. Click Register backend
3. Follow the instructions and use the api key you got from zappa when deploying the api.

You should see a new table in DynamoDB with your encrypted credentials.

## Test your connection

```bash
http <your-api>/<your-env>/sql/view/<your-registered-backend-name> x-api-key:$API_KEY \
sql=="select 1"
```
