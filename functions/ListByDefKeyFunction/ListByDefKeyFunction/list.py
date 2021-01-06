import os
import json
import boto3
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb')
from .decimalencoder import DecimalEncoder

def list(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    data = json.loads(event['body'])
    def_key = data.get('defKey')

    result = table.query(
        KeyConditionExpression= Key('def_key').eq(def_key)
    )
    print(result)
    if len(result['Items']) > 0:
        body = {"results": result['Items']}
        # body = {"results": []}
        # for ele in result['Items']:
        #     item = json.dumps(ele, cls=DecimalEncoder)
        #     body["results"].append(item)
    else:
        body = {"results":"not found"}
    print(body)
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(body, cls=DecimalEncoder)
    }

    return response
