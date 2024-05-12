#!/usr/bin/env python3
import aws_cdk as cdk

from aws_mongodb_sample.aws_mongo_db_create import AwsMongodbAtlasCreateStack
from aws_mongodb_sample.aws_mongodb_sample_stack import AwsMongodbSampleStack
from aws_mongodb_sample.aws_amplify_stack import amplifystack
from global_args import GlobalArgs
import boto3
import json
import base64

def get_secret(secret_name):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name = GlobalArgs.AWS_REGION )

    get_secret_value_response = client.get_secret_value( SecretId=secret_name)

    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
    else:
        secret = base64.b64decode(get_secret_value_response['SecretBinary'])

    return json.loads(secret)

secret_name = GlobalArgs.SECRET_NAME
secrets = get_secret(secret_name)

aws_account_id = secrets["AWSACCOUNTID"]
aws_region = GlobalArgs.AWS_REGION

app = cdk.App()




AtlasClusterStack = AwsMongodbAtlasCreateStack(app, "AwsMongodbAtlasCreateStack",
    env=cdk.Environment(account=aws_account_id, region=aws_region),
)


atlasuri = AtlasClusterStack.Atlas_URI


AwsMongodbSampleStack(app, "AwsMongodbSampleStack",
   env=cdk.Environment(account=aws_account_id, region=aws_region),
   atlas_uri = atlasuri,
    )

# amplifystack(app, "amplifystack",
#    env=cdk.Environment(account=aws_account_id, region=aws_region)
#     )



app.synth()
